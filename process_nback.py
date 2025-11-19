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

    # Extract reaction time per condition (matching/non-matching) and status (correct/incorrect)
    rt_matching_overall = mean(matching_condition_results["reaction_time"])
    rt_nonmatching_overall = mean(nonmatching_condition_results["reaction_time"])
    matching_correct = matching_condition_results[matching_condition_results["score"] == 1]
    matching_incorrect = matching_condition_results[matching_condition_results["score"] == 0]
    rt_matching_correct = mean(matching_correct["reaction_time"]) if len(matching_correct) > 0 else pd.NA
    rt_matching_incorrect = mean(matching_incorrect["reaction_time"]) if len(matching_incorrect) > 0 else pd.NA
    nonmatching_correct = nonmatching_condition_results[nonmatching_condition_results["score"] == 1]
    nonmatching_incorrect = nonmatching_condition_results[nonmatching_condition_results["score"] == 0]
    rt_nonmatching_correct = mean(nonmatching_correct["reaction_time"]) if len(nonmatching_correct) > 0 else pd.NA
    rt_nonmatching_incorrect = mean(nonmatching_incorrect["reaction_time"]) if len(nonmatching_incorrect) > 0 else pd.NA

    processed_results = {
        "overall_accuracy": overall_accuracy,
        "accuracy_matching": accuracy_matching,
        "accuracy_nonmatching": accuracy_nonmatching,
        "n_correct_matching": n_correct_matching,
        "n_incorrect_matching": n_incorrect_matching,
        "n_correct_nonmatching": n_correct_nonmatching,
        "n_incorrect_nonmatching": n_incorrect_nonmatching,
        "rt_matching_overall": rt_matching_overall,
        "rt_nonmatching_overall": rt_nonmatching_overall,
        "rt_matching_correct": rt_matching_correct,
        "rt_matching_incorrect": rt_matching_incorrect,
        "rt_nonmatching_correct": rt_nonmatching_correct,
        "rt_nonmatching_incorrect": rt_nonmatching_incorrect,
    }
    return processed_results
