#!/usr/bin/env python3
import sys
import logging
import math
from timeit import default_timer as timer

import util

LOG_LEVEL = logging.INFO

DIRECTION_MAP = {
    'U': (0,1),
    'D': (0,-1),
    'L': (-1, 0),
    'R': (1, 0),
}

def split_instruction(instruction):
    direction = DIRECTION_MAP[instruction[0]]
    count = int(instruction[1:])
    return direction, count

def path_end(start, instruction):
    endx = start[0]
    endy = start[1]

    direction, count = split_instruction(instruction)

    endx = endx + (direction[0] * count)
    endy = endy + (direction[1] * count)

    return (endx, endy)

def wire_to_segments(origin, wire_path):
    segments = []
    last_point = origin
    for instruction in wire_path:
        start = last_point
        end = path_end(start, instruction)
        segments.append( (start, end) )
        last_point = end
    return segments

def point_in_segment(point, segment):
    # This is simplified as the line segments are either horizontal or vertical
    if(segment[0][0] == segment[1][0] and point[0] == segment[0][0]):
        # segment is horizontal and we are in the same "row"
        min = segment[0][1]
        max = segment[1][1]
        if min > max:
            min, max = max, min
        return min <= point[1] <= max
    elif(segment[0][1] == segment[1][1] and point[1] == segment[0][1]):
        # segment is vertical and we are in the same "column"
        min = segment[0][0]
        max = segment[1][0]
        if min > max:
            min, max = max, min
        return min <= point[0] <= max

    return False

def main(input_file):

    wire_paths = []
    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            path = line.split(',')
            wire_paths.append(path)
    logging.debug(wire_paths)

    origin = (0,0)

    # convert the first wire to a list of line segments
    # Segments are (start_point, end_point) tuples
    wire1_segments = wire_to_segments(origin, wire_paths[0])
    logging.debug("Wire1 Segments: " + str(wire1_segments))

    # Walk along the second wire, finding all intersection_points
    intersection_points = []
    last_point = origin
    for instruction in wire_paths[1]:
        direction, count = split_instruction(instruction)
        for _ in range(count):
            new_point = (last_point[0]+direction[0], last_point[1]+direction[1])

            # Check if new point is inside any of the line segments of wire 1
            for segment in wire1_segments:
                if point_in_segment(new_point, segment):
                    intersection_points.append(new_point)
                    break
                logging.debug("Point {} did not intersect".format(new_point))
            last_point = new_point

    logging.debug("Intersection Points: " + str(intersection_points))

    min_point = None
    min_distance = math.inf

    for intersection in intersection_points:
        dist = util.manhattan_distance(origin, intersection)
        if dist < min_distance:
            min_point = intersection
            min_distance = dist

    print(f"Minimal Distance To Intersection: {min_distance}")

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
