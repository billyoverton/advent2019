#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer
import math
import itertools

import util
from SantaInteropt import SantaInteropt

LOG_LEVEL = logging.INFO

def main(input_file):

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            memory = [int(x) for x in line.split(",")]
    logging.debug(f"Original Memory {memory}")

    amps = [ SantaInteropt([x for x in memory]) for x in range(5) ]

    valid_phases = [0,1,2,3,4]

    max_output_thrust = -math.inf
    max_phase_settings = None

    input_tests = itertools.permutations(valid_phases)

    for phase_setting in input_tests:
        logging.debug(f"Checking phase input {phase_setting}")

        last_amp_input = 0
        # run all the amps with our phase input
        for i in range(len(amps)):
            amps[i].input_buffer = [ phase_setting[i], last_amp_input ]
            amps[i].execute()
            last_amp_input = amps[i].output_buffer[0]
        thrust = amps[len(amps)-1].output_buffer[0]

        # Compare our thrust
        if thrust > max_output_thrust:
            max_output_thrust = thrust
            max_phase_settings = [ x for x in phase_setting ]

        # Reset our amps
        for amp in amps:
            amp.reset()
        last_amp_input = 0

    print(f"Maximum Thrust: {max_output_thrust}")
    print(f"Max Thrust Setting: {max_phase_settings}")

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
