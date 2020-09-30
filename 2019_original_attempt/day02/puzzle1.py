#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

def main(input_file):

    program = []
    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            program = [int(x.strip()) for x in line.split(",")]

    logging.info(program)
    program[1] = 12
    program[2] = 2

    running = True
    pointer = 0
    while running:
        opt = program[pointer]

        logging.debug(f'Opt Code {opt}')
        if opt == 99:
            running = False
            continue

        arg1 = program[pointer+1]
        arg2 = program[pointer+2]
        target = program[pointer+3]

        if opt == 1:
            program[target] = program[arg1] + program[arg2]
        elif opt ==2:
            program[target] = program[arg1] * program[arg2]
        else:
            logging.critcal(f"Unknown opt code {opt}")
        pointer += 4

    print("Position 0: " + str(program[0]))


if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
