#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer
import re
import itertools
import random
import string

import util

LOG_LEVEL = logging.INFO

class Vector(object):
    def __init__(self, x, y , z):
        self.x = x
        self.y = y
        self.z = z

        # https://pythontips.com/2013/07/28/generating-a-random-string/
        self.__id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        logging.debug(self.__id)
    def __str__(self):
        return f"<x={self.x}, y={self.y}, z={self.z}>"
    def __hash__(self):
        return self.__id.__hash__()

def main(input_file):
    moons = {}

    pattern = re.compile("^<x=(-?[0-9]*), y=(-?[0-9]*), z=(-?[0-9]*)>")
    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            match = pattern.match(line)
            if match:
                moons[Vector(int(match.group(1)), int(match.group(2)), int(match.group(3)))] = Vector(0,0,0)

    step = 0
    target_step = 1000

    while step <= target_step:

        print(f"After {step} steps:")
        system_total_energy = 0
        for moon in moons:
            potential_energy = abs(moon.x) + abs(moon.y) + abs(moon.z)
            kinetic_energy = abs(moons[moon].x) + abs(moons[moon].y) + abs(moons[moon].z)
            total_energy = potential_energy * kinetic_energy
            print(f"pos={moon}, vel={moons[moon]}: {potential_energy}*{kinetic_energy} = {total_energy}")
            system_total_energy += total_energy

        print(f"System Total Energy: {system_total_energy}\n")
        # apply gravity
        moon_pairs = itertools.combinations(moons.keys(), 2)
        for pair in moon_pairs:
            logging.debug("Pair: " + str(pair[0]) + " , " + str(pair[1]))

            logging.debug("Velocity pre gravity: " + str(moons[pair[0]]) + " , " + str(moons[pair[1]]))
            if pair[0].x < pair[1].x:
                moons[pair[0]].x = moons[pair[0]].x + 1
                moons[pair[1]].x = moons[pair[1]].x - 1
            elif pair[0].x > pair[1].x:
                moons[pair[0]].x = moons[pair[0]].x - 1
                moons[pair[1]].x = moons[pair[1]].x + 1

            if pair[0].y < pair[1].y:
                moons[pair[0]].y = moons[pair[0]].y + 1
                moons[pair[1]].y = moons[pair[1]].y - 1
            elif pair[0].y > pair[1].y:
                moons[pair[0]].y = moons[pair[0]].y - 1
                moons[pair[1]].y = moons[pair[1]].y + 1

            if pair[0].z < pair[1].z:
                moons[pair[0]].z = moons[pair[0]].z + 1
                moons[pair[1]].z = moons[pair[1]].z - 1
            elif pair[0].z > pair[1].z:
                moons[pair[0]].z = moons[pair[0]].z - 1
                moons[pair[1]].z = moons[pair[1]].z + 1

            logging.debug("Velocity post gravity: " + str(moons[pair[0]]) + " , " + str(moons[pair[1]]))

        # apply velocity
        for moon in moons:
            target = moons[moon]
            moon.x = moon.x + target.x
            moon.y = moon.y + target.y
            moon.z = moon.z + target.z
        step += 1

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
