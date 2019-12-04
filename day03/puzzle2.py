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

def is_horizontal(segment):
    return segment[0][1] == segment[1][1]

def is_verticle(segment):
    return segment[0][0] == segment[1][0]

def segments_intersect(a, b):
    a_vertical = is_verticle(a)
    b_vertical = is_verticle(b)

    if(a_vertical == b_vertical):
        # Lines are parallel
        if a_vertical and a[0][0] == b[0][0]:
            # Both verticle and in same column
            return (
                util.between(a[0][1], b[0][1], b[1][1])
                or util.between(a[1][1], b[0][1], b[1][1])
                or util.between(b[0][1], a[0][1], a[1][1])
                or util.between(b[1][1], a[0][1], a[1][1])
            )
        if not a_vertical and a[0][1] == b[0][1]:
            # Both horiztonal and in same row
            return (
                util.between(a[0][0], b[0][0], b[1][0])
                or util.between(a[1][0], b[0][0], b[1][0])
                or util.between(b[0][0], a[0][0], a[1][0])
                or util.between(b[1][0], a[0][0], a[1][0])
            )
    else:
        # Mixed vertical and horizontal
        vert, hori = (a, b) if a_vertical else (b, a)
        return util.between(vert[0][0], hori[0][0], hori[1][0]) and util.between(hori[0][1], vert[0][1], vert[1][1])
    return False

def segment_intersect_points(a,b):
    points = []

    a_vertical = is_verticle(a)
    b_vertical = is_verticle(b)

    if(a_vertical != b_vertical):
        # Can only intersect at a single point
        vertical, horizontal = (a, b) if a_vertical else (b, a)
        points.append( (vertical[0][0], horizontal[0][1] ) )
    else:
        # I'm sure there is a better way to do this, but i'm being lazy. I'll
        # walk the points of one line and add any intersections
        a_slope = ( a[1][0] - a[0][0], a[1][1] - a[0][1] )
        magnitude = math.sqrt(a_slope[0]**2 + a_slope[1]**2 )
        a_step = ( a_slope[0]/magnitude, a_slope[1]/magnitude)

        point = a[0]
        while point != a[1]:
            if point_in_segment(point, b):
                points.append(point)
            point = ( point[0] + a_step[0], point[1] + a_step[1])

    return points

def magnitude(p1, p2):
    logging.debug(f"Points: {p1}, {p2}")
    slope = ( p2[0] - p1[0], p2[1] - p1[1] )
    logging.debug(f"Slope: {slope}")
    mag = math.sqrt(slope[0]**2 + slope[1]**2 )
    logging.debug(f"Magnitude: {mag}")
    return mag

def step_count_to_point(point, wire_segments):
    steps = 0
    for segment in wire_segments:
        if point_in_segment(point, segment):
            steps += magnitude(segment[0], point)
            break
        else:
            steps += magnitude(segment[0], segment[1])
    return steps
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

    wire2_segments = wire_to_segments(origin, wire_paths[1])
    logging.debug("Wire2 Segments: " + str(wire1_segments))

    intersection_points = []
    for segment_a in wire1_segments:
        for segment_b in wire2_segments:
            # Determine if segment a intersects with segment b
            if(segments_intersect(segment_a, segment_b)):
                logging.debug(f"Segment Intersection: {segment_a} and {segment_b}")
                intersection_points.extend(segment_intersect_points(segment_a, segment_b))

    logging.debug("Intersection Points: " + str(intersection_points))

    min_point = None
    step_count = math.inf

    for intersection in intersection_points:
        if intersection == origin:
            continue

        dist = step_count_to_point(intersection, wire1_segments) + step_count_to_point(intersection, wire2_segments)
        if dist < step_count:
            min_point = intersection
            step_count = dist

    print(f"Combined Steps To Intersection: {step_count}")

if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
