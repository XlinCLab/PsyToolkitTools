import pandas as pd
from statistics import mean

# PsyToolkit Experiment Documentation: https://www.psytoolkit.org/experiment-library/nback2.html

def main(results_file):
    results = pd.read_csv(results_file, sep=" ", header=None, names=[
        "block_number", 
        "trial_number",
        "trial_type",
        "score", # the column we want to extract
        "match",
        "miss",
        "false_alarm",
        "reaction_time",
        "memory",
        "current_letter",
        "nback1",
        "nback2",
    ])
    # Extract mean of score column (1 if correct, 0 if incorrect)
    mean_score = mean(results["score"])
    return mean_score
