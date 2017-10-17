# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project


class Quantity():
    """
    Base class for quantities
    """
    def __init__(self, name, magnitude, derivative, alphabet):
        self.name = name                # name of the quantity
        self.magnitude = magnitude      # current magnitude
        self.derivative = derivative    # current derivative
        # Alphabet declares the possible values of magnitude & derivative.
        # This is in the form of a dict, to allow the Quantity[value]
        # representation
        self.alphabet = alphabet

    def __repr__(self):
        return "{}".format(self.name)
