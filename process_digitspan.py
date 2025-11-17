# PsyToolkit Experiment Documentation: https://www.psytoolkit.org/experiment-library/digitspan.html


def main(results_file: str) -> int:
    """Extract the length of the longest digit sequence correctly remembered from the digitspan output results file.
    
    Output file spec:
    The data output is other than in most experiments.
    In this experiment, there are multiple lines per trial.
    The reaction time, exactly digit sequences presented and entered are saved.
    If you are only interested in the ultimate digit span, you can just look at the second number of the last line.
    """
    with open(results_file, "r") as f:
        contents = f.readlines()
    contents = [line.strip() for line in contents if len(line.strip()) > 0]
    last_line = contents[-1]
    longest_sequence_length = int(last_line.split()[1])  # return second number of last line

    processed_results = {
        "longest_seq_len": longest_sequence_length
    }
    return processed_results
