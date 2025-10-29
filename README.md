# PsyToolkitTools

## Introduction
These scripts serve to process experiment/survey results conducted using the online platform [PsyToolkit](https://www.psytoolkit.org/).

## Setup
These scripts require [Python 3](https://www.python.org/downloads/) to run. Please ensure you have installed Python before proceeding with setup instructions.

To install Python dependencies for these tools, please run the following command:
```
./setup_venv.sh && source .venv/bin/activate
```

The above needs to be run only the first time for initial setup. Subsequently, it is only necessary to activate the Python virtual environment using this command:
```
source .venv/bin/activate
```

## Process survey results
Survey results downloaded from PsyToolkit will be in `.zip` file format. 

The script `extract_psytoolkit_results.py` will extract such a zip file and further extract the relevant measures per experiment per participant to a single CSV file. Required inputs to this script are:
- File path to the zip file downloaded from PsyToolkit
- File path to a desired output CSV file

Optional input:
- Label used in the results files to indicate participant IDs. If not provided, this is by default the string `versuchspersonenkennung` ("test subject identifier" in German).

Example command syntax:
```
python3 extract_psytoolkit_results.py --data /path/to/your/psytoolkit/results/zip/file.zip --outfile /path/to/your/desired/results/file.csv 
```

The results CSV file will list test subject IDs and experiments as columns, with one line per test subject with that test subject's extracted measures per experiment.

## Currently supported experiments
We presently support the following PsyToolkit psychometric experiments:

- [digitspan](https://www.psytoolkit.org/experiment-library/digitspan.html)

    -> Extracted measure: Length of longest digit sequence successfully recalled twice.

- [flanker-arrows](https://www.psytoolkit.org/experiment-library/flanker_arrows.html)

    -> Extracted measure: Average reaction time.

- [nback-2](https://www.psytoolkit.org/experiment-library/nback2.html)

    -> Extracted measure: Average success rate.
