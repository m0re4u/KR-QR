# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import pickle
import random
import argparse
from copy import deepcopy

import quantities as qn
import dependencies as dp
import reasoner


def main(filename):
    # Declare alphabets
    a1 = {"zero": "zero", "plus": "plus"}
    a2 = {"zero": "zero", "plus": "plus", "max": "max"}
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
    print("Model created!")
    print()
    rs = reasoner.QRReasoner(model_qns, model_dcs)
    state_list, transitions = rs.think()

    print("Possible states:")
    for i, state in state_list:
        print("  State: {} --> {}".format(i, state))
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
