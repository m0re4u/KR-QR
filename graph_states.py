# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import pickle
import argparse
import networkx as nx
import matplotlib.pyplot as plt

import quantities as qn
import dependencies as dp
import reasoner


def draw_nodes(states, transitions):
    G = nx.Graph()
    nodes = []
    for i, state in enumerate(states):
        # (x,y) coordinate
        G.add_node(i)
        nodes.append((i, state))

    edges = []
    for trans in transitions:
        origin = None
        target = None
        for i, node in nodes:
            for trans in transitions:
                if trans[0] == node:
                    for j, target in nodes:
                        if trans[1] == target:
                            edges.append((i, j))

    for edge in edges:
        G.add_edge(edge[0], edge[1])

    # draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos)

    # show graph
    plt.show()


def main(filename):
    with open(filename, "rb") as f:
        print("Opening {}".format(filename))
        data = pickle.load(f)
    print("Loaded data!")
    draw_nodes(data["states"], data["transitions"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="")
    parser.add_argument(
        "-f", "--file", help="File for loading the state and their transitions",
        default="data.pik"
    )
    args = parser.parse_args()
    main(args.file)
