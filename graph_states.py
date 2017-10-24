# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import pickle
import argparse
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz
import subprocess

import quantities as qn
import dependencies as dp


def draw(states, transitions):
    G = nx.DiGraph()
    labels = {}
    for i, state in states:
        G.add_node(i)
        label_str = ""
        for value in state.instances:
            label_str += "{}\n".format(value)

        labels[i] = "{}".format(label_str)

    for transition in transitions:
        G.add_edge(transition[0], transition[1])

    A = nx.drawing.nx_agraph.to_agraph(G)
    nx.drawing.nx_agraph.write_dot(G, "graph.dot")

    try:
        subprocess.call(["dot", "-Tpng", "-ograph.png", "graph.dot"])
    except OSError as e:
        print("Error: {}".format(e))
        exit()


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
