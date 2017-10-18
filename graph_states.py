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
    G = nx.DiGraph()
    labels = {}
    for i, state in states:
        G.add_node(i)
        labels[i] = "{}".format(i)

    for transition in transitions:
        G.add_edge(transition[0], transition[1])

    # draw graph
    pos = nx.shell_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=600)
    nx.draw_networkx_labels(G, pos, labels)

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
