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


def get_experiment_names(unzipped_directory_path: str) -> list[str]:
    """Extract names of experiments from within an unzipped PsyToolkit results directory."""
    exp_data_dir = os.path.join(unzipped_directory_path, "experiment_data")
    exp_files = os.listdir(exp_data_dir)
    exp_names = set(exp_file.split(".")[0] for exp_file in exp_files)
    return exp_names


def get_participant_data_files(data_zipfile: str,
                               participant_id_variable_name: str = DEFAULT_PARTICIPANT_ID_LABEL,
                               ) -> defaultdict:
    """Extract a zip file containing PsyToolkit results and create a dictionary with paths to experimental results per participant."""
    unzipped_directory = unzip(data_zipfile)
    experiment_names = get_experiment_names(unzipped_directory)
    data_summary_file = os.path.join(unzipped_directory, "data.csv")
    data_summary_df = pd.read_csv(data_summary_file)
    participant_data = defaultdict(lambda: {})
    participant_id_column = participant_id_variable_name + "_1"
    for _, row in data_summary_df.iterrows():
        participant_id = row[participant_id_column]
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
    results = results.transpose()
    # Move the index (outer dict keys) into a column
    results.reset_index(inplace=True)
    # Rename the new column to 'participant_id'
    results.rename(columns={'index': 'participant_id'}, inplace=True)
    return results


def main(data_zipfile: str,
         output_file: str,
         participant_id_variable_name: str = DEFAULT_PARTICIPANT_ID_LABEL,
         ):
    data_zipfile = os.path.abspath(data_zipfile)
    participant_datafiles = get_participant_data_files(data_zipfile, participant_id_variable_name)
    participant_results = {
        participant_id: process_participant_results(experiment_files_dict)
        for participant_id, experiment_files_dict in participant_datafiles.items()
    }
    # Assemble DataFrame with processed results
    results = assemble_results_df(participant_results)
    # Write results DataFrame to output file
    outdir = os.path.dirname(os.path.abspath(output_file))
    os.makedirs(outdir, exist_ok=True)
    results.to_csv(output_file, index=False)
    logger.info(f"Extracted experiment results to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Extract PsyToolkit experiment results from zip file.")
    parser.add_argument('--data', required=True, help='Path to data zip file')
    parser.add_argument('--outfile', required=True, help='Path to output data file')
    parser.add_argument('--participant_id_label', default=DEFAULT_PARTICIPANT_ID_LABEL, help='Participant ID variable label')
    args = parser.parse_args()
    main(
        data_zipfile=args.data,
        output_file=args.outfile,
        participant_id_variable_name=args.participant_id_label,
    )