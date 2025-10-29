import pandas as pd
from statistics import mean

# PsyToolkit Experiment Documentation: https://www.psytoolkit.org/experiment-library/flanker_arrows.html

def main(results_file):
    results = pd.read_csv(results_file, sep=" ", header=None, names=["stimulus", "condition", "status", "time"])
    # Extract mean of 4th column (reaction times)
    mean_reaction_time = mean(results["time"])
    return mean_reaction_time
