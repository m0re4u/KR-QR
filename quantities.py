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

    def check_value(self, value, alphabet, inv_alphabet):
        if value not in alphabet and value not in inv_alphabet:
            test_value = value
            if not isinstance(test_value, int):
                test_value = inv_alphabet[value]
            if test_value > max(list(alphabet.values())):
                return max(list(alphabet.values()))
            elif test_value < min(list(alphabet.values())):
                return min(list(alphabet.values()))
        elif isinstance(value, str):
            return alphabet[value]
        else:
            return value

    def check_magnitude(self, value):
        return self.check_value(value, self.quantity.alphabet, self.quantity.inv_alphabet)

    def check_derivative(self, value):
        return self.check_value(value, DERIV_ALPHABET, INV_DERIV_ALPHABET)

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

    def set_value(self, key, field, value):
        """
        Set the value of a QuantityInstance indexed by a quantity
        """
        for instance in self.instances:
            if instance.quantity == key:
                if field == "magnitude":
                    instance.magnitude = value
                elif field == "derivative":
                    instance.derivative = value

    def decrease_value(self, key, field):
        """
        Lower the value of a QuantityInstance indexed by a quantity
        """
        for instance in self.instances:
            if instance.quantity == key:
                if field == "magnitude":
                    instance.magnitude -= 1
                elif field == "derivative":
                    instance.derivative -= 1

    def increase_value(self, key, field):
        """
        Increase the value of a QuantityInstance indexed by a quantity
        """
        for instance in self.instances:
            if instance.quantity == key:
                if field == "magnitude":
                    instance.magnitude += 1
                elif field == "derivative":
                    instance.derivative += 1

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
        return "State: {}".format(self.instances)
