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
    # print("Quantities: {}".format(model_qns))
    # print("Relations: {}".format(model_dcs))
    print()
    rs = reasoner.QRReasoner(model_qns, model_dcs)
    model_instance = [
        qn.QuantityInstance(model_qns["Inflow"], "zero", "plus"),
        qn.QuantityInstance(model_qns["Volume"], "zero", "zero"),
        qn.QuantityInstance(model_qns["Outflow"], "zero", "zero")
    ]
    print("Begin state:\n{}".format(model_instance))
    # print()
    # print()
    # unseen_states = []
    # state_list = []
    # transitions = []
    # unseen_states.extend(rs.think(model_instance))
    # while unseen_states != []:
    #     # Select a state to continue with
    #     selection = unseen_states.pop()
    #     # print(selection)
    #     # Copy the current selection to the list of processed states
    #     state_list.append(deepcopy(selection))
    #     # Apply rules on the current state, generating new states
    #     new_states = rs.think(selection)
    #     # For the new states, check if we have seen them before, and put them
    #     # in the queue if we have not
    #     for state in new_states:
    #         trans = (selection, state)
    #         if trans not in transitions:
    #             transitions.append(trans)
    #         if state not in state_list:
    #             unseen_states.append(state)

    state_list, transitions = rs.think()
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
