#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

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

            orbit_map.add_edge([orbitor, target], bidirectional=True)


        current_orbital = orbit_map.neighbors("YOU")[0]
        target = orbit_map.neighbors("SAN")[0]

        distance_map, _ = orbit_map.dijkstra(current_orbital)
        logging.debug(f'Distance Map {distance_map}')

        print("Orbit Transfers: " + str(distance_map[target]))

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
