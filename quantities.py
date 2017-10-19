# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project

DERIV_ALPHABET = {"minus": -1, "zero": 0, "plus": 1}
INV_DERIV_ALPHABET = dict({v: k for k, v in DERIV_ALPHABET.items()})


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
        self.inv_alphabet = dict({v: k for k, v in alphabet.items()})

    def __repr__(self):
        return "{} has possible values: {}".format(self.name, list(self.alphabet.keys()))

    def __eq__(self, other):
        return self.name == other.name and self.alphabet == other.alphabet


class QuantityInstance():
    """
    Creates an instance of a quantity, giving it a value for the magnitude and
    the derivative
    """
    def check_magnitude(self, value):
        if value not in self.quantity.alphabet and value not in self.quantity.inv_alphabet:
            if not isinstance(value, int):
                value = self.quantity.inv_alphabet[value]
            if value > max(list(self.quantity.alphabet.values())):
                return max(list(self.quantity.alphabet.values()))
            raise ValueError("{} is not a value in {}\'s alphabet: {}".format(
                value, self.quantity.name, list(self.quantity.alphabet.keys()) + list(self.quantity.inv_alphabet.keys())
            ))
        if isinstance(value, str):
            return self.quantity.alphabet[value]
        else:
            return value

    def check_derivative(self, value):
        if value not in DERIV_ALPHABET and value not in INV_DERIV_ALPHABET:
            raise ValueError("{} is not a value in {}\'s derivative alphabet: {}".format(
                value, self.quantity.name, list(DERIV_ALPHABET.keys()) + list(INV_DERIV_ALPHABET.keys())
            ))
        if isinstance(value, str):
            return DERIV_ALPHABET[value]
        else:
            return value

    def __init__(self, quantity, magnitude, derivative):
        self.quantity = quantity
        mag = self.check_magnitude(magnitude)
        deriv = self.check_derivative(derivative)
        self.magnitude = mag
        self.derivative = deriv

    def __repr__(self):
        return "{} ({}, {})".format(self.quantity.name, self.quantity.inv_alphabet[self.magnitude], INV_DERIV_ALPHABET[self.derivative])

    def __eq__(self, other):
        return self.quantity == other.quantity and \
            self.magnitude == other.magnitude and self.derivative == other.derivative

    @property
    def magnitude(self):
        return self.__magnitude

    @magnitude.setter
    def magnitude(self, mag):
        mag = self.check_magnitude(mag)
        self.__magnitude = mag

    @property
    def derivative(self):
        return self.__derivative

    @derivative.setter
    def derivative(self, deriv):
        deriv = self.check_derivative(deriv)
        self.__derivative = deriv


class Model():
    """
    Defines a instansiation of the world, where every Quantity as defined in the
    world should have a corresponding QuantityInstance
    """
    def __init__(self, quantities, instances):
        self.qns = quantities
        self.instances = instances

    def get_value(self, key):
        """
        Return the QuantityInstance if the key is a valid quantity
        """
        for value in self.instances:
            if value.quantity == key:
                return (value.magnitude, value.derivative)

    def __eq__(self, other):
        eq_list = []
        for instance in self.instances:
            found = []
            for oth_instance in other.instances:
                if instance == oth_instance:
                    found.append(True)
                else:
                    found.append(False)
            if any(found):
                eq_list.append(True)
            else:
                eq_list.append(False)
        return all(eq_list)

    def __repr__(self):
        return "Model --> {}".format(self.instances)
