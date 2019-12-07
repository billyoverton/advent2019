#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util
from SantaInteropt import SantaInteropt

LOG_LEVEL = logging.INFO

def get_digit(number, n):
    return number // 10**n % 10

def main(input_file):

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            memory = [int(x) for x in line.split(",")]

    logging.debug(f"Original Memory {memory}")

    computer = SantaInteropt(memory)
    computer.input_buffer = [5]
    computer.execute()

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
