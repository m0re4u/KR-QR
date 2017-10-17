# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project

DERIV_ALPHABET = ["minus", "zero", "plus"]


class Quantity():
    """
    Base class for quantities
    """
    def __init__(self, name, alphabet):
        self.name = name  # name of the quantity
        # Alphabet declares the possible values of magnitude.
        # The alphabet for derivatives always the same, namely:
        #   [minus, zero, plus]
        # The alphabet is in the form of a dict, to allow for the
        # Quantity[value] representation.
        self.alphabet = alphabet

    def __repr__(self):
        return "{} has possible values: {}".format(self.name, list(self.alphabet.keys()))

    def __eq__(self, other):
        return self.name == other.name and self.alphabet == other.alphabet


class QuantityInstance():
    """
    Creates an instance of a quantity, giving it a value for the magnitude and
    the derivative
    """
    def __init__(self, quantity, magnitude, derivative):
        self.quantity = quantity
        if magnitude not in self.quantity.alphabet:
            raise ValueError("Not a value in {}\'s alphabet: {}".format(
                self.quantity.name, list(self.quantity.alphabet.keys())
            ))
        if derivative not in DERIV_ALPHABET:
            raise ValueError("Not a valid value for a derivative: {}".format(
                DERIV_ALPHABET
            ))
        self.magnitude = magnitude
        self.derivative = derivative

    def __repr__(self):
        return "{} ({}, {})".format(self.quantity.name, self.magnitude, self.derivative)

    def __eq__(self, other):
        return self.quantity == other.quantity and \
            self.magnitude == other.magnitude and self.derivative == other.derivative

    @property
    def magnitude(self):
        return self.__magnitude

    @magnitude.setter
    def magnitude(self, mag):
        if mag not in self.quantity.alphabet:
            raise ValueError("Not a value in {}\'s alphabet: {}".format(
                self.quantity.name, list(self.quantity.alphabet.keys())
            ))
        self.__magnitude = mag

    @property
    def derivative(self):
        return self.__derivative

    @derivative.setter
    def derivative(self, deriv):
        if deriv not in DERIV_ALPHABET:
            raise ValueError("Not a value in {}\'s alphabet: {}".format(
                self.quantity.name, list(DERIV_ALPHABET)
            ))
        self.__derivative = deriv
