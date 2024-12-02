import math
from pathlib import Path
import re

def parse_input(fname: str):
    input_file = Path(__file__).parent.resolve() / fname
    lines = input_file.read_text().split("\n")
    lines = [line.split() for line in lines]
    lines = list(filter(lambda line: line != [""] and line, lines))

    directions = lines[0][0]

    desert_graph = lines[1:]
    desert_graph = [
        [re.sub(r'\W+', "", entry) for entry in node] for node in desert_graph
    ]
    desert_graph = [
        list(filter(None, node)) for node in desert_graph
    ]
    desert_graph = {
        node[0]: (node[1], node[2]) for node in desert_graph
    }

    return directions, desert_graph

def get_number_of_steps(
        directions: str, desert_graph: dict,
        starting_node = "AAA", ending_condition=lambda s: s == "ZZZ"
):
    ii = 0
    current_node = starting_node

    while True:
        if ending_condition(current_node):
            return ii

        next_step = directions[ii % len(directions)]

        if next_step == "L":
            current_node = desert_graph[current_node][0]
        else:
            current_node = desert_graph[current_node][1]

        ii += 1

### Part 1
# Starting at AAA, follow the left/right instructions.
# How many steps are required to reach ZZZ?
print(get_number_of_steps(*parse_input("example_2308.txt")))
print(get_number_of_steps(*parse_input("example2_2308.txt")))
print(get_number_of_steps(*parse_input("input_2308.txt")))


### Part 2
# Simultaneously start on every node that ends with A.
# How many steps does it take before you're only on nodes that end with Z?
def get_multiple_steps(directions: str, desert_graph: dict):
    starting_nodes = [node for node in desert_graph if node[-1] == "A"]

    cycle_lengths = {
        node: get_number_of_steps(
            directions, desert_graph, node, lambda s: s[-1] == "Z"
        ) for node in starting_nodes
    }

    return math.lcm(*cycle_lengths.values())

print(get_multiple_steps(*parse_input("example3_2308.txt")))
print(get_multiple_steps(*parse_input("input_2308.txt")))
