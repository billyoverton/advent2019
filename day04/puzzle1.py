#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

def valid_password(num):
    int_array = [ int(x) for x in str(num)]
    has_adjacent_duplicate = False

    if len(int_array) != 6:
        return False

    for i in range(len(int_array)-1):
        # Ensure that the next value is not decreasing
        if int_array[i+1] < int_array[i]:
            return False

        # Check if we have a adjacent duplicate
        if int_array[i] == int_array[i+1]:
            has_adjacent_duplicate = True

    return has_adjacent_duplicate

def main(start, end):

    start_num = int(start)
    end_num = int(end)

    logging.debug(f"Range Start: {start_num}")
    logging.debug(f"Range End: {end_num}")

    count = 0
    while start_num <= end_num:
        if valid_password(start_num):
            count+=1
        start_num+=1

    print(f"Valid passwords in range: {count}")
if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 3:
        logging.critical("Missing input range")
    else:
        start = timer()
        main(sys.argv[1], sys.argv[2])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
