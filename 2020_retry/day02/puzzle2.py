#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer
from SantaInteropt import SantaInteropt

import util

LOG_LEVEL = logging.INFO

def main(input_file):

    program = None
    with open(input_file) as f:
        program = f.readline().strip()

    memory = [int(x) for x in program.split(',')]

    interopt = SantaInteropt(memory)

    is_found = False
    for noun in range(100):
        for verb in range(100):
            interopt.reset()
            interopt.memory[1] = noun
            interopt.memory[2] = verb
            interopt.execute()
            logging.debug(f'Noun: {noun}, Verb: {verb}, Result: {interopt.memory[0]}')
            if interopt.memory[0] == 19690720:
                # We found our noun/verb combo
                logging.info(f'Noun: {noun}')
                logging.info(f'Verb: {verb}')
                print(f'Answer: {100*noun+verb}')
                is_found = True
                break
        if is_found:
            break;
if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
