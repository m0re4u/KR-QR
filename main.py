# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import os
import pickle
import argparse
from copy import deepcopy

import quantities as qn
import dependencies as dp
import simple_reasoner

TERMINAL_ROWS, TERMINAL_COLUMNS = os.popen('stty size', 'r').read().split()


def main(filename):
    # Declare alphabets
    a1 = {"zero": 0, "plus": 1}
    a2 = {"zero": 0, "plus": 1, "max": 2}
    # Specify model quantities
    model_qns = {
        "Inflow": qn.Quantity("Inflow", a1),
        "Outflow": qn.Quantity("Outflow", a2),
        "Volume": qn.Quantity("Volume", a2)
    }
    # Define relations between quantities
    model_dcs = [
        dp.Influence(model_qns["Inflow"], model_qns["Volume"], "positive"),
        dp.Influence(model_qns["Outflow"], model_qns["Volume"], "negative"),
        dp.Proportional(model_qns["Volume"], model_qns["Outflow"], "positive"),
        dp.ValueCorrespondence(
            model_qns["Volume"], model_qns["Outflow"],
            model_qns["Volume"].alphabet["max"], model_qns["Outflow"].alphabet["max"]
        ),
        dp.ValueCorrespondence(
            model_qns["Volume"], model_qns["Outflow"],
            model_qns["Volume"].alphabet["zero"], model_qns["Outflow"].alphabet["zero"]
        )
    ]
    # Create initial state for the reasoner
    model_instances = qn.Model(model_qns, [
        qn.QuantityInstance(model_qns["Inflow"], "zero", "plus"),
        qn.QuantityInstance(model_qns["Volume"], "zero", "zero"),
        qn.QuantityInstance(model_qns["Outflow"], "zero", "zero")
    ])
    print("Model created!")

    print("=" * int(TERMINAL_COLUMNS))
    # Simple reasoner
    print("Starting simple reasoner")
    simrs = simple_reasoner.Simple_QRReasoner(model_qns, model_dcs)

    state_list, transitions = simrs.think(model_instances)
    with open(filename, "wb") as outfile:
        pickle.dump({"states": state_list, "transitions": transitions}, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="")
    parser.add_argument(
        "-f", "--file", help="Output file containing the states and their \
        transitions",
        default="data.pik"
    )
    args = parser.parse_args()
    main(args.file)
