import pandas as pd
from statistics import mean

# PsyToolkit Experiment Documentation: https://www.psytoolkit.org/experiment-library/nback2.html

def main(results_file):
    results = pd.read_csv(results_file, sep=" ", header=None, names=[
        "block_number", 
        "trial_number",
        "trial_type",
        "score",
        "match",
        "miss",
        "false_alarm",
        "reaction_time",
        "memory",
        "current_letter",
        "nback1",
        "nback2",
    ])
    # Extract mean of score column (1 if correct, 0 if incorrect) = mean accuracy
    overall_accuracy = mean(results["score"])

    # Extract accuracy per condition (matching vs. non-matching)
    matching_condition_results = results[results["trial_type"] == 1]
    accuracy_matching = mean(matching_condition_results["score"])
    n_correct_matching = sum(matching_condition_results["score"])
    n_incorrect_matching = len(matching_condition_results[matching_condition_results["score"] == 0])
    nonmatching_condition_results = results[results["trial_type"] == 0]
    accuracy_nonmatching = mean(nonmatching_condition_results["score"])
    n_correct_nonmatching = sum(nonmatching_condition_results["score"])
    n_incorrect_nonmatching = len(nonmatching_condition_results[nonmatching_condition_results["score"] == 0])

    processed_results = {
        "overall_accuracy": overall_accuracy,
        "accuracy_matching": accuracy_matching,
        "accuracy_nonmatching": accuracy_nonmatching,
        "n_correct_matching": n_correct_matching,
        "n_incorrect_matching": n_incorrect_matching,
        "n_correct_nonmatching": n_correct_nonmatching,
        "n_incorrect_nonmatching": n_incorrect_nonmatching,
    }
    return processed_results
