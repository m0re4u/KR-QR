# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import argparse
import quantities as qn
import dependencies as dp
import reasoner


def main():
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
    print()
    for i in range(10):
        res = rs.think(model_instance)
        print("State {}:\n{}".format(i, res))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="")
    # parser.add_argument("-d", "--download", help="", action="store_true")
    args = parser.parse_args()
    main()
