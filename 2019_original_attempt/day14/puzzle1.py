#!/usr/bin/env python3
import sys
import logging
from timeit import default_timer as timer
import math

import util

LOG_LEVEL = logging.INFO

class Reaction(object):

    def __init__(self, reaction_string):
        reactants, product = reaction_string.split(" => ")
        reactants = [x.strip() for x in reactants.split(',')]
        product = product.split(" ")

        self.product = product[1].strip()
        self.product_amount = int(product[0])

        # Inputs as (chem, amount) tuple
        self.inputs=[]
        for reactant in reactants:
            tmp = reactant.split(" ")
            self.inputs.append((tmp[1].strip(), int(tmp[0])))

    def __str__(self):
        input_string = ", ".join([ str(x[1]) + " " + x[0] for x in self.inputs])
        return f"{input_string} => {self.product_amount} {self.product}"


def main(input_file):

    # Map of Chem => Reaction to produce chem
    reaction_table = {}

    with open(input_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            reaction = Reaction(line)
            reaction_table[reaction.product] = reaction

    ore_required = 0
    production_queue = [ ("FUEL", 1) ]
    leftovers = {}

    while len(production_queue) > 0:
        item, amount = production_queue.pop()
        reaction = reaction_table[item]

        logging.debug(f"Production: {item} * {amount}")
        logging.debug(f"Reaction: {reaction}")

        # Check if we already have some of this from a previous job
        if item in leftovers:
            amount = amount - leftovers[item]
            if amount <= 0:
                leftovers[item] = abs(amount)
                continue
            else:
                leftovers[item] = 0

        reaction_count = math.ceil(amount / reaction.product_amount)
        logging.debug(f"Reaction Count: {reaction_count}")

        produced = reaction_count * reaction.product_amount
        leftover = produced - amount

        if item in leftovers:
            leftovers[item] += leftover
        else:
            leftovers[item] = leftover

        for input in reaction.inputs:
            if input[0] == "ORE":
                ore_required += input[1]*reaction_count
            else:
                needed = input[1]*reaction_count
                if input[0] in leftovers:
                    # We have some of this already. No need to request everything
                    needed = needed - leftovers[input[0]]
                    if needed <= 0:
                        leftovers[input[0]] = abs(needed)
                        continue
                    else:
                        leftovers[input[0]] = 0
                production_queue.append( (input[0], needed) )

    print(f"Required Ore for 1 FUEL: {ore_required}")




if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s:%(module)s: %(message)s', level=LOG_LEVEL)

    if len(sys.argv) < 2:
        logging.critical("Missing input file")
    else:
        start = timer()
        main(sys.argv[1])
        end = timer()

        logging.info(f'Executed in {(end-start):.5f} seconds')
