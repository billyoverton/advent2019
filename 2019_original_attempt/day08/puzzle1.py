#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer
import math

import util

LOG_LEVEL = logging.INFO

def main(input_file):

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            input_digits = [int(x) for x in line]

    logging.debug(input_digits)

    image_width = 25
    image_height = 6
    digits_per_layer = image_width * image_height
    num_layers = len(input_digits) // digits_per_layer
    logging.debug(f"Number of layers {num_layers}")

    image_layers = [ util.init_grid(image_height, image_width) for x in range(num_layers)]
    logging.debug(image_layers)

    current_layer = 0
    layer_x = 0
    layer_y = 0
    for i in range(len(input_digits)):

        logging.debug(f"Layer {current_layer} x:{layer_x} y: {layer_y} = {input_digits[i]}")

        image_layers[current_layer][layer_y][layer_x] = input_digits[i]

        layer_x += 1
        if layer_x == image_width:
            layer_x = 0
            layer_y += 1

        if (i+1) % digits_per_layer == 0 and i != 0:
            logging.debug("New Layer")
            current_layer += 1
            layer_x = 0
            layer_y = 0

    logging.debug(image_layers)

    # Find the layer with the lowest 0s
    lowest_zero_layer = None
    lowest_zero_count = math.inf
    for layer in image_layers:
        count = 0
        for y in range(len(layer)):
            for x in range(len(layer[y])):
                if layer[y][x] == 0:
                    count += 1
        if count < lowest_zero_count:
            lowest_zero_count = count
            lowest_zero_layer = layer

    logging.debug(f"Lowest Zero Layer: {lowest_zero_layer}")

    one_count = 0
    two_count = 0
    for y in range(len(lowest_zero_layer)):
        for x in range(len(lowest_zero_layer[y])):
            if lowest_zero_layer[y][x] == 1:
                one_count += 1
            elif lowest_zero_layer[y][x] == 2:
                two_count += 1

    answer = one_count * two_count
    print(f"Answer: {answer}")



if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
