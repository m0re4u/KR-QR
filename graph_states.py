# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import pickle
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph

import quantities as qn
import dependencies as dp


def draw_nodes(states, transitions):
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

    A = to_agraph(G)
    # draw graph
    # k controls the distance between the nodes and varies between 0 and 1
    # iterations is the number of times simulated annealing is run
    # pos = graphviz_layout(G)
    # pos = nx.spring_layout(G, k=0.50, iterations=50)
    # nx.draw_networkx_nodes(G, pos, node_size=1000, node_shape="8")
    # nx.draw_networkx_edges(G, pos)
    # nx.draw_networkx_labels(G, pos, labels, font_size=8)

    # # show graph
    plt.show()


def main(filename):
    with open(filename, "rb") as f:
        print("Opening {}".format(filename))
        data = pickle.load(f)
    print("Loaded data: {} states and {} transitions!".format(len(data["states"]), len(data["transitions"])))
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
