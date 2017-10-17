# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import pickle
import argparse
import networkx as nx
import matplotlib.pyplot as plt

import quantities as qn
import dependencies as dp
import reasoner


def draw_nodes(states):
    G = nx.Graph()
    for state in states:
        # (x,y) coordinate
        print(state)
        G.add_node(state)

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
    draw_nodes(data["states"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="")
    parser.add_argument(
        "-f", "--file", help="File for loading the state and their transitions",
        default="data.pik"
    )
    args = parser.parse_args()
    main(args.file)
