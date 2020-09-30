#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

def is_collinear(p1, p2, p3):
    return 0 == ( (p1.x - p2.x)*(p2.y - p3.y) - (p2.x - p3.x)*(p1.y - p2.y) )

def main(input_file):

    astroids = []

    y = 0
    x = 0
    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            for char in line:
                if char == "#":
                    astroids.append(util.Point(x,y))
                x+=1
            y+=1
            x=0

    logging.debug("Astroids: " + ",".join(str(x) for x in astroids))

    cansee_map = { x:list() for x in astroids }

    for source in astroids:
        logging.debug(f"Checking what {source} can see...")

        possible_targets = [ x for x in astroids if x != source and x not in cansee_map[source] ]

        while len(possible_targets) > 0:
            target = possible_targets.pop()
            blockers = [ x for x in astroids if x not in [source, target] ]

            can_see_target = True

            for other in blockers:
                if not is_collinear(source, other, target):
                    continue # Not collinear so not a possible blocker
                logging.debug(f"{source} {other} {target} are collinear")

                # Check if other is between source and target (blocks target)
                # https://lucidar.me/en/mathematics/check-if-a-point-belongs-on-a-line-segment/

                k_source_other  = (target.x - source.x) * (other.x - source.x) + (target.y - source.y) * (other.y - source .y)
                k_source_target = (target.x - source.x)**2 + (target.y - source.y)**2

                if 0 < k_source_other < k_source_target:
                    logging.debug(f"{other} blocks {source}->{target}")
                    can_see_target = False
                    break

            if can_see_target:
                cansee_map[source].append(target)
                cansee_map[target].append(source)

    max_astroid = None
    max_count = 0
    for astroid in cansee_map:
        if len(cansee_map[astroid]) > max_count:
            max_astroid = astroid
            max_count = len(cansee_map[astroid])

    print(f"{max_astroid} can see the most other astroids ({max_count})")


if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
