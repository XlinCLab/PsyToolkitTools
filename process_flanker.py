import pandas as pd
from statistics import mean

# PsyToolkit Experiment Documentation: https://www.psytoolkit.org/experiment-library/flanker_arrows.html
CORRECT_CODING = 1
INCORRECT_CODING = 2
TOO_SLOW_CODING = 3
CONGRUENT_CODING = 1
INCONGRUENT_CODING = 0

def main(results_file: str) -> dict:
    results = pd.read_csv(results_file, sep=" ", header=None, names=["stimulus", "condition", "status", "time"])
    # Overall accuracy
    n_correct_overall = len(results[results["status"] == CORRECT_CODING])
    overall_accuracy = n_correct_overall / len(results)
    # Accuracy for congruent condition
    congruent_trials = results[results["condition"] == CONGRUENT_CODING]
    n_congruent_trials = len(congruent_trials)
    congruent_correct = congruent_trials[congruent_trials["status"] == CORRECT_CODING]
    congruent_accuracy = len(congruent_correct) / n_congruent_trials
    # Mean reaction time for correct congruent trials
    mean_rt_correct_congruent = mean(congruent_correct["time"]) if len(congruent_correct) > 0 else pd.NA
    # Mean reaction time for incorrect congruent trials
    congruent_incorrect = congruent_trials[congruent_trials["status"] == INCORRECT_CODING]
    mean_rt_incorrect_congruent = mean(congruent_incorrect["time"]) if len(congruent_incorrect) > 0 else pd.NA

    # Accuracy for incongruent condition
    incongruent_trials = results[results["condition"] == INCONGRUENT_CODING]
    n_incongruent_trials = len(incongruent_trials)
    incongruent_correct = incongruent_trials[incongruent_trials["status"] == CORRECT_CODING]
    incongruent_accuracy = len(incongruent_correct) / n_incongruent_trials
    # Mean reaction time for correct incongruent trials
    mean_rt_correct_incongruent = mean(incongruent_correct["time"]) if len(incongruent_correct) > 0 else pd.NA
    # Mean reaction time for incorrect congruent trials
    incongruent_incorrect = incongruent_trials[incongruent_trials["status"] == INCORRECT_CODING]
    mean_rt_incorrect_incongruent = mean(incongruent_incorrect["time"]) if len(incongruent_incorrect) > 0 else pd.NA

    # "Too slow" trials: raw number and mean reaction time
    too_slow_trials = results[results["status"] == TOO_SLOW_CODING]
    n_too_slow_trials = len(too_slow_trials)
    if n_too_slow_trials > 0:
        mean_rt_too_slow = mean(too_slow_trials["time"])
    else:
        mean_rt_too_slow = pd.NA
    
    # Get overall numbers of correct and incorrect responses
    n_correct_trials = len(results[results["status"] == CORRECT_CODING])
    n_incorrect_trials = len(results[results["status"] == INCORRECT_CODING])

    # Extract overall mean reaction time
    overall_mean_reaction_time = mean(results["time"])


    # Assemble dictionary of summarized results
    processed_results = {
        "n_congruent_trials": n_congruent_trials,
        "n_incongruent_trials": n_incongruent_trials,
        "n_correct_trials": n_correct_trials,
        "n_incorrect_trials": n_incorrect_trials,
        "n_too_slow_trials": n_too_slow_trials,
        "accuracy_overall": overall_accuracy,
        "accuracy_congruent": congruent_accuracy,
        "accuracy_incongruent": incongruent_accuracy,
        "rt_congruent_correct": mean_rt_correct_congruent,
        "rt_congruent_incorrect": mean_rt_incorrect_congruent,
        "rt_incongruent_correct": mean_rt_correct_incongruent,
        "rt_incongruent_incorrect": mean_rt_incorrect_incongruent,
        "rt_too_slow": mean_rt_too_slow, 
        "rt_overall": overall_mean_reaction_time,
    }

    return processed_results
