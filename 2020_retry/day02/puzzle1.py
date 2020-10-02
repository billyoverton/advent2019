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

    memory[1] = 12
    memory[2] = 2

    interopt = SantaInteropt(memory)
    interopt.execute()
    print(interopt.memory[0])

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
