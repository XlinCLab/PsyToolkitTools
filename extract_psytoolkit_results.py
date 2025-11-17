import argparse
import logging
import os
import zipfile
from collections import defaultdict
from typing import Callable

import pandas as pd

from process_digitspan import main as process_digitspan
from process_flanker import main as process_flanker
from process_nback import main as process_nback

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_PARTICIPANT_ID_LABEL = "versuchspersonenkennung"

EXPERIMENT_PROCESSING_MAP = {
    "flanker_arrows": process_flanker,
    "digitspan": process_digitspan,
    "nback": process_nback,
}


def get_results_processing_function(experiment_name) -> Callable:
    for experiment_label, processing_func in EXPERIMENT_PROCESSING_MAP.items():
        if experiment_name.startswith(experiment_label):
            return processing_func
    # Raise error if no matching function found
    raise ValueError(f"No processing function found matching experiment name <{experiment_name}>")


def unzip(zip_filepath: str, unzip_to: str = None) -> str:
    """Unzip a zip file."""
    if not zip_filepath.endswith(".zip"):
        raise ValueError(f"{zip_filepath} is not a zip file!")
    if unzip_to is None:
        unzip_to = zip_filepath.replace(".zip", "")
    with zipfile.ZipFile(zip_filepath, 'r') as zipf:
        zipf.extractall(unzip_to)
    logger.info(f"Extracted {zip_filepath} to {unzip_to}")
    return unzip_to


def get_experiment_names(unzipped_directory_path: str) -> set[str]:
    """Extract names of experiments from within an unzipped PsyToolkit results directory."""
    exp_data_dir = os.path.join(unzipped_directory_path, "experiment_data")
    exp_files = os.listdir(exp_data_dir)
    exp_names = set(exp_file.split(".")[0] for exp_file in exp_files)
    return exp_names


def rename_duplicate_ids(df: pd.DataFrame, participant_id_column: str) -> pd.DataFrame:
    """Check for duplicate participant IDs, and if found, rename them such that they are unique."""
    # Identify duplicates
    participant_ids = df[participant_id_column].to_list()
    if len(participant_ids) == len(df[participant_id_column].unique()):
        return df  # return df without changes in case there are no duplicates found
    duplicate_ids = sorted(list(set(participant_id for participant_id in participant_ids if participant_ids.count(participant_id) > 1)))
    duplicate_id_str = ", ".join([str(dup) for dup in duplicate_ids])
    first_duplicate = duplicate_ids[0]
    logger.warning(f"Participant IDs <{duplicate_id_str}> are not unique! These will be automatically renamed as, e.g. <{first_duplicate}_1, {first_duplicate}_2, ...>")

    # Rename duplicates
    for duplicate_id in duplicate_ids:
        row_indices = df.index[df[participant_id_column] == duplicate_id].tolist()
        count = 1
        for row_idx in row_indices:
            df.loc[row_idx, participant_id_column] = str(duplicate_id) + f"_{count}"
            count += 1
    
    # Add final recursive pass to ensure that the renamed IDs are also unique
    return rename_duplicate_ids(df, participant_id_column)


def get_participant_data_files(data_zipfile: str,
                               participant_id_variable_name: str = DEFAULT_PARTICIPANT_ID_LABEL,
                               ) -> defaultdict:
    """Extract a zip file containing PsyToolkit results and create a dictionary with paths to experimental results per participant."""
    # Unzip the zip file
    if data_zipfile.endswith(".zip"):
        logger.info(f"Unzipping {data_zipfile}")
        unzipped_directory = unzip(data_zipfile)
    elif os.path.isdir(data_zipfile):
        logger.info(f"Found already unzipped directory {data_zipfile}")
        unzipped_directory = data_zipfile

    # Extract names of component experiments
    experiment_names = get_experiment_names(unzipped_directory)
    
    # Load data summary file
    data_summary_file = os.path.join(unzipped_directory, "data.csv")
    participant_id_column = participant_id_variable_name + "_1"
    data_summary_df = pd.read_csv(data_summary_file)
    data_summary_df[participant_id_column] = data_summary_df[participant_id_column].astype(str)
    # Drop and warn about any NA entries
    n_entries = len(data_summary_df)
    data_summary_df = data_summary_df.dropna()
    n_valid_entries = len(data_summary_df)
    n_empty_entries = n_entries - n_valid_entries
    if n_empty_entries > 0:
        logger.warning(f"Dropped {n_empty_entries}/{n_entries} entries with NA values")
    logger.info(f"Found data for {n_valid_entries} participants")

    # Validate/ensure that participant IDs are unique
    if n_valid_entries != len(data_summary_df[participant_id_column].unique()):
        data_summary_df = rename_duplicate_ids(data_summary_df, participant_id_column)

    # Get participant data files
    participant_data = defaultdict(lambda: {})
    for _, row in data_summary_df.iterrows():
        participant_id = str(row[participant_id_column])
        for experiment_name in experiment_names:
            exp_column_name = experiment_name + "_1"
            participant_exp_file = row[exp_column_name]
            participant_data[participant_id][experiment_name] = os.path.join(unzipped_directory, "experiment_data", participant_exp_file)
    return participant_data


def process_participant_results(experiment_files_dict: dict) -> dict:
    processed_results = {}
    for experiment, results_file in experiment_files_dict.items():
        processing_func = get_results_processing_function(experiment)
        processed_results[experiment] = processing_func(results_file)
    return processed_results


def assemble_results_df(participant_results_dict: dict) -> pd.DataFrame:
    """Assemble a dictionary of participant results into a pandas DataFrame."""
    results = pd.DataFrame(participant_results_dict)
    # Move the index (outer dict keys) into a column
    results.reset_index(inplace=True)
    # Rename the new column to 'participant_id'
    results.rename(columns={'index': 'participant_id'}, inplace=True)
    return results


def main(data_zipfile: str,
         outdir: str,
         participant_id_variable_name: str = DEFAULT_PARTICIPANT_ID_LABEL,
         ):
    data_zipfile = os.path.abspath(data_zipfile)
    experiments = get_experiment_names(data_zipfile)
    participant_datafiles = get_participant_data_files(data_zipfile, participant_id_variable_name)
    participant_results = {
        participant_id: process_participant_results(experiment_files_dict)
        for participant_id, experiment_files_dict in participant_datafiles.items()
    }

    # Invert results such that they are indexed by experiment, experiment result fields, then participant ID
    experiment_results = defaultdict(lambda: defaultdict(lambda: {}))
    for experiment in experiments:
        for participant in participant_results:
            exp_participant_results = participant_results[participant][experiment]
            for field, value in exp_participant_results.items():
                experiment_results[experiment][field][participant] = value

    # Create separate summary file with all participants' results for each experiment in specified outdir
    os.makedirs(outdir, exist_ok=True)
    for experiment, exp_results in experiment_results.items():
        outfile = os.path.join(outdir, experiment + ".csv")

        # Assemble DataFrame with processed results
        results = assemble_results_df(exp_results)
        # Write results DataFrame to output file
        results.to_csv(outfile, index=False)
        logger.info(f"Extracted experiment <{experiment}> results to {outfile}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Extract PsyToolkit experiment results from zip file.")
    parser.add_argument('--data', required=True, help='Path to data zip file')
    parser.add_argument('--outdir', required=True, help='Path to output directory')
    parser.add_argument('--participant_id_label', default=DEFAULT_PARTICIPANT_ID_LABEL, help='Participant ID variable label')
    args = parser.parse_args()
    main(
        data_zipfile=args.data,
        outdir=args.outdir,
        participant_id_variable_name=args.participant_id_label,
    )