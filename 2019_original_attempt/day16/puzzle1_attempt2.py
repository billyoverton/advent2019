#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.DEBUG

def pattern_gen(base, position):
    pattern = [x for x in base]
    current_value = pattern.pop(0)
    current_index = position
    while True:
        yield current_value
        current_index -= 1
        if current_index == 0:
            current_index = position
            pattern.append(current_value)
            current_value = pattern.pop(0)

def FFT(input):
    base_pattern = [0, 1, 0, -1]

    output = [None] * len(input)

    for i in range(len(input)):
        pattern = pattern_gen(base_pattern, i+1)

        # Offset pattern by 1
        next(pattern)

        value = 0
        for digit in input:
            pattern_value = next(pattern)
            if pattern_value == 0:
                continue
            value += digit * pattern_value
        # Take only the ones position
        value = abs(value) % 10
        output[i] = value
    return output




def main(input_file):

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            input = [int(x) for x in line]
    logging.debug("Input Pattern: " + "".join([str(x) for x in input]))



    run_count = 100
    for x in range(run_count):
        input = FFT(input)
        logging.debug(f"After {x+1} phase: " + "".join([str(x) for x in input]))


    print("First 8 sequence: " + "".join([str(x) for x in input])[:8])
if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
