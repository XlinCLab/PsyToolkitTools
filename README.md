# PsyToolkitTools

## Introduction
These scripts serve to process experiment/survey results conducted using the online platform [PsyToolkit](https://www.psytoolkit.org/).

## Process survey results
Survey results downloaded from PsyToolkit will be in `.zip` file format. 

The script `extract_psytoolkit_results.py` will extract such a zip file and further extract the relevant measures per experiment per participant to a single CSV file. Required inputs to this script are:
- File path to the zip file downloaded from PsyToolkit
- File path to a desired output CSV file

Optional input:
- Label used in the results files to indicate participant IDs. If not provided, this is by default the string `versuchspersonenkennung` ("test subject identifier" in German).

Example command syntax:
```
python extract_psytoolkit_results.py --data /path/to/your/psytoolkit/results/zip/file.zip --outfile /path/to/your/desired/results/file.csv 
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
