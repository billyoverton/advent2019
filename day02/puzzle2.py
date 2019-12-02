#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

def execute_program(program):
    running = True
    pointer = 0
    while running:
        opt = program[pointer]

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
            logging.critical(f"Unknown opt code {opt}")
        pointer += 4

def main(input_file):

    program = []
    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            program = [int(x.strip()) for x in line.split(",")]

    logging.info(program)

    original_program = [ x for x in program ]

    verb = 0
    noun = 0
    target = 19690720
    while noun < 100:
        program[1] = noun
        program[2] = verb

        execute_program(program)

        if program[0] == target:
            print("Answer: " + str(100 * noun + verb))
            break

        verb += 1
        if verb == 100:
            verb = 0
            noun += 1
        program = [x for x in original_program]



if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
