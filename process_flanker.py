import pandas as pd
from statistics import mean

# PsyToolkit Experiment Documentation: https://www.psytoolkit.org/experiment-library/flanker_arrows.html

def main(results_file):
    results = pd.read_csv(results_file, sep=" ", header=None, names=["stimulus", "condition", "status", "time"])
    # Accuracy for congruent condition
    congruent_trials = results[results["condition"] == 1]
    n_congruent_trials = len(congruent_trials)
    congruent_correct = congruent_trials[congruent_trials["status"] == 1]
    congruent_accuracy = len(congruent_correct) / n_congruent_trials
    # Mean reaction time for correct congruent trials
    if len(congruent_correct) > 0:
        mean_rt_correct_congruent = mean(congruent_correct["time"])
    else:
        mean_rt_correct_congruent = pd.NA

    # Accuracy for incongruent condition
    incongruent_trials = results[results["condition"] == 0]
    n_incongruent_trials = len(incongruent_trials)
    incongruent_correct = incongruent_trials[incongruent_trials["status"] == 1]
    incongruent_accuracy = len(incongruent_correct) / n_incongruent_trials
    # Mean reaction time for correct incongruent trials
    if len(incongruent_correct) > 0:
        mean_rt_correct_incongruent = mean(incongruent_correct["time"])
    else:
        mean_rt_correct_incongruent = pd.NA

    # "Too slow" trials: raw number and mean reaction time
    too_slow_trials = results[results["status"] == 3]
    n_too_slow_trials = len(too_slow_trials)
    if n_too_slow_trials > 0:
        mean_rt_too_slow = mean(too_slow_trials["time"])
    else:
        mean_rt_too_slow = pd.NA
    
    # Get overall numbers of correct and incorrect responses
    n_correct_trials = len(results[results["status"] == 1])
    n_incorrect_trials = len(results[results["status"] == 2])

    # Extract overall mean reaction time
    overall_mean_reaction_time = mean(results["time"])


    # Assemble dictionary of summarized results
    processed_results = {
        "n_congruent_trials": n_congruent_trials,
        "n_incongruent_trials": n_incongruent_trials,
        "n_correct_trials": n_correct_trials,
        "n_incorrect_trials": n_incorrect_trials,
        "n_too_slow_trials": n_too_slow_trials,
        "accuracy_congruent": congruent_accuracy,
        "accuracy_incongruent": incongruent_accuracy,
        "rt_congruent_correct": mean_rt_correct_congruent,
        "rt_incongruent_correct": mean_rt_correct_incongruent,
        "rt_too_slow": mean_rt_too_slow, 
        "rt_overall": overall_mean_reaction_time,
    }

    return processed_results
