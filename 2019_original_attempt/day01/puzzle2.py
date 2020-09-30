#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer
import math
import util

LOG_LEVEL = logging.INFO

def main(input_file):
    fuel_total = 0
    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            mass = int(line)
            fuel = math.floor(mass/3)-2
            fuel_total = fuel_total + fuel

            while True:
                fuel_mass = math.floor(fuel/3)-2
                if(fuel_mass <= 0):
                    break
                fuel = fuel_mass
                fuel_total = fuel_total + fuel
    print(f"Total Fuel (post fuel): {fuel_total}")

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
