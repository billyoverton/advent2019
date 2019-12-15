#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer
import math

import util

LOG_LEVEL = logging.INFO

def is_collinear(p1, p2, p3):
    return 0 == ( (p1.x - p2.x)*(p2.y - p3.y) - (p2.x - p3.x)*(p1.y - p2.y) )

# WTF did this work? I just got annoyed and started swapping and negating
# everything on these two functions
def vector(a,b):
    return ((b.y-a.y), (b.x-a.x))

def vector_angle(vec):
    return math.atan2(vec[1],vec[0])

def can_see_list(source, astroids):
    # Get the list of visable astroids
    possible_targets = [ x for x in astroids ]
    can_see = []
    while len(possible_targets) > 0:
        target = possible_targets.pop()
        blockers = [ x for x in astroids if x not in [source, target] ]

        can_see_target = True

        for other in blockers:
            if not is_collinear(source, other, target):
                continue # Not collinear so not a possible blocker
            #logging.debug(f"{source} {other} {target} are collinear")

            # Check if other is between source and target (blocks target)
            # https://lucidar.me/en/mathematics/check-if-a-point-belongs-on-a-line-segment/

            k_source_other  = (target.x - source.x) * (other.x - source.x) + (target.y - source.y) * (other.y - source .y)
            k_source_target = (target.x - source.x)**2 + (target.y - source.y)**2

            if 0 < k_source_other < k_source_target:
                #logging.debug(f"{other} blocks {source}->{target}")
                can_see_target = False
                break

        if can_see_target:
            can_see.append(target)
    return can_see
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

    laser_location = util.Point(26,28)
    #laser_location = util.Point(11,13)

    # Other astroids
    astroids = list(filter(lambda x: x != laser_location, astroids))
    logging.debug("Astroids: " + ",".join(str(x) for x in astroids))

    destroyed_count = 0
    target_count = 200

    while destroyed_count < target_count:
        can_see = can_see_list(laser_location, astroids)
        can_see.sort(key=lambda x: -vector_angle(vector(laser_location,x)))
        #logging.debug("Can See: " + ",".join(str(x) for x in can_see))

        for target in can_see:
            destroyed_count+=1
            logging.debug(f"Blowing up {target} - #{destroyed_count}")
            astroids.remove(target)

            if destroyed_count == target_count:
                print("Answer: " + str((target.x * 100)+target.y))
                break

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
