# PsyToolkit Experiment Documentation: https://www.psytoolkit.org/experiment-library/digitspan.html

from collections import defaultdict
from statistics import mean


def main(results_file: str) -> dict:
    """Extract the length of the longest digit sequence correctly remembered from the digitspan output results file and the number of trials before failure.
    
    Output file spec:
    The data output is other than in most experiments.
    In this experiment, there are multiple lines per trial.
    The reaction time, exactly digit sequences presented and entered are saved.
    If you are only interested in the ultimate digit span, you can just look at the second number of the last line.
    """
    with open(results_file, "r") as f:
        contents = f.readlines()
    contents = [line.strip() for line in contents if len(line.strip()) > 0]
    
    # Split into trials: 3 lines per trial
    # first line: <block> clickedStim <bitmaps of stimulus IDs>
    # second line: <block> rts <reaction times for each click>
    # third line: <block> <best_so_far> <testspan> <error_status> // <correct digit sequence> // <chosen digit sequence>
    trials = defaultdict(lambda: {})
    trial_counter = 0
    trial_lines_seen = 0
    for line in contents:
        if trial_lines_seen > 2:
           trial_lines_seen = 0 
        if trial_lines_seen == 0:
            trial_counter += 1
            block = line.split()[0]
            trials[trial_counter]["block"] = block
            clickedStim = line.split("clickedStim")[-1].split()
            trials[trial_counter]["clickedStim"] = clickedStim
        elif trial_lines_seen == 1:
            rts = line.split("rts")[-1].split()
            trials[trial_counter]["reactionTimes"] = rts
        elif trial_lines_seen == 2:
            best_so_far = int(line.split()[1])
            trials[trial_counter]["best_so_far"] = best_so_far
            current_trial_seq_length = int(line.split()[2])
            trials[trial_counter]["current_trial_seq_length"] = current_trial_seq_length
            error_status = int(line.split()[3])
            trials[trial_counter]["correct"] = error_status == 0  # NB: error_status coded as 0 = correct, 1 = incorrect
            correct_sequence = line.split("//")[1].split()
            digits_chosen = line.split("//")[-1].split()
            trials[trial_counter]["correct_sequence"] = correct_sequence
            trials[trial_counter]["digits_chosen"] = digits_chosen    
        trial_lines_seen += 1

    # N trials before failure
    n_successful_trials = len([trial_n for trial_n in trials if trials[trial_n]["correct"] is True])

    # Get length of longest sequence successfully remembered
    # Extract best_so_far value from last trial
    last_trial_n = max(trials.keys())
    longest_sequence_length = trials[last_trial_n]["best_so_far"]

    # Average reaction time across all trials
    average_rt_per_trial = [
        mean([float(val) for val in trial_data["reactionTimes"]])
        for _, trial_data in trials.items()
    ]
    overall_average_rt = mean(average_rt_per_trial)

    processed_results = {
        "longest_seq_len": longest_sequence_length,
        "n_trials_before_failure": n_successful_trials,
        "overall_mean_rt": overall_average_rt,
    }
    return processed_results
