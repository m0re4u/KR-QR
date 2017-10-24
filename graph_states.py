# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import pickle
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph
import subprocess

import quantities as qn
import dependencies as dp


def draw(states, transitions):
    G = Digraph()
    labels = {}
    for i, state in states:
        label_str = "State: {}\n".format(i)
        for value in state.instances:
            label_str += "{}\n".format(value)
        G.node(str(i), label_str)

    for transition in transitions:
        G.edge(str(transition[0]), str(transition[1]))

    G.render('graphs/graph.gv', view=True)


def main(filename):
    with open(filename, "rb") as f:
        print("Opening {}".format(filename))
        data = pickle.load(f)
    print("Loaded data: {} states and {} transitions!".format(len(data["states"]), len(data["transitions"])))
    draw(data["states"], data["transitions"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="")
    parser.add_argument(
        "-f", "--file", help="File for loading the state and their transitions",
        default="data.pik"
    )
    args = parser.parse_args()
    main(args.file)
