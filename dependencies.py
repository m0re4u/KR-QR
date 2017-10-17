# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project


class Dependency():
    """
    Base class for dependencies. Is always a directed binary relation, for
    which we can specify a origin and a target.
    """
    def __init__(self, name, origin, target):
        self.name = name
        self.origin = origin
        self.target = target

    def __repr__(self):
        return "\"{}\" from {} to {}".format(self.name, self.origin.name, self.target.name)


class ValueCorrespondence(Dependency):
    """
    Specifies a value correspondence between two values of quantities
    """
    def __init__(self, origin, target, origin_value, target_value):
        super().__init__("VC", origin, target)
        self.origin_value = origin_value
        self.target_value = target_value

    def __repr__(self):
        # Overloaded string representation because we want the name of the
        # quantities as well
        return "{} between values {} and {}".format(super().__repr__(), self.origin_value, self.target_value)


class Influence(Dependency):
    """
    Specifies an influence relation between two quantities
    """
    def __init__(self, origin, target, sign):
        super().__init__("Influence", origin, target)
        self.sign = sign

    def __repr__(self):
        return "{} with {} sign".format(super().__repr__(), self.sign)


class Proportional(Dependency):
    """
    Specifies a proportional relation between two quantities
    """
    def __init__(self, origin, target, sign):
        super().__init__("Proportional", origin, target)
        self.sign = sign

    def __repr__(self):
        return "{} with {} sign".format(super().__repr__(), self.sign)
