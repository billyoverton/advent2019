#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

def build_pattern(base, position):
    pattern = []
    for x in base:
        for y in range(position):
            pattern.append(x)
    return pattern

def FFT(input):
    base_pattern = [0, 1, 0, -1]

    output = [None] * len(input)

    for i in range(len(input)):
        pattern = build_pattern(base_pattern, i+1)

        # Offset pattern by 1
        pattern.append(pattern.pop(0))

        value = 0
        debug_string = ""
        for digit in input:

            pattern_value = pattern.pop(0)

            debug_string = debug_string + f"{digit}*{pattern_value} + "

            value += digit * pattern_value

            pattern.append(pattern_value)

        # Take only the ones position
        value = abs(value) % 10
        output[i] = value
        debug_string = debug_string + f" = {value}"
        logging.debug(debug_string)
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
