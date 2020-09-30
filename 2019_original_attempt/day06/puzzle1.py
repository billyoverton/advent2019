#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

def count_orbits(obj, orbit_map):
    current_obj = obj
    obj_neighbors = orbit_map.neighbors(obj)

    direct_orbits = len(obj_neighbors)
    indirect_orbits = 0

    # Since everything must orbit something besides COM this will cover everything
    # till we get to COM, since they will have one neighbor
    while len(obj_neighbors) > 0:
        current_obj = obj_neighbors[0]
        obj_neighbors = orbit_map.neighbors(current_obj)
        indirect_orbits += len(obj_neighbors)
    return direct_orbits, indirect_orbits

def main(input_file):

    # Graph where a edge A->B indicates A orbits B
    orbit_map = util.Graph()

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            target, orbitor = line.split(')')
            logging.debug(f'{orbitor} orbits {target}')

            orbit_map.add_edge([orbitor, target], bidirectional=False)

        logging.debug(orbit_map)
        logging.debug("COM neighbors: " +  str(orbit_map.neighbors("COM")))

        total = 0
        for obj in orbit_map.verticies:
            direct, indirect = count_orbits(obj, orbit_map)
            total = total + direct + indirect

        print(f"Total Orbits: {total}")

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
