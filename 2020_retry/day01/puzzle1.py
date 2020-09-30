#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

def main(input_file):

    fuel_required = 0

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            mass = int(line)
            fuel_required += ((mass//3) - 2)

    print("Fuel Required: {}".format(fuel_required))

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
