# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import quantities as qn
import itertools


class QRReasoner():
    """
    Reasoner object that will perform the task of generating the state graph
    and the transitions between the states.
    Should also output a trace to explain why a transition to a certain state
    does or does not occur.
    """

    def __init__(self, model_quantities, model_dependencies):
        self.qns = model_quantities
        self.dcs = model_dependencies

    def find_influences(self, instance):
        # Find the influences that can affect the value of the derivative of
        # the considered instance
        infs = []
        for dep in self.dcs:
            if dep.target == instance.quantity and dep.name == "Influence":
                infs.append(dep)
        return infs

    def find_value(self, state, quantity):
        # Find the instansiated value of a quantity
        for value in state:
            if value.quantity == quantity:
                return value
        return None

    def generate_states(self):
        qspace = [(k, list(v.alphabet.keys())) for k, v in self.qns.items()]
        ordered_quantities = [x[0] for x in qspace]
        all_states = list(itertools.product(*[x[1] for x in qspace], *[qn.DERIV_ALPHABET] * 3))
        all_instances = []
        for state in all_states:
            instance = []
            for i, quantity in enumerate(self.qns):
                instance.append(qn.QuantityInstance(self.qns[ordered_quantities[i]], state[i], state[i + len(self.qns)]))
            all_instances.append(instance)
        return all_instances

    def check_state(self, state):
        for cur_quantity in state:
            # Negative derivative and zero magnitude is impossible state
            if cur_quantity.magnitude == "zero" and cur_quantity.derivative == "minus":
                return False

            # Next up, check if there is an impossible derivative value in the
            # current quantity given the incoming influence relations and the
            # value of the origin quantities
            rel = self.find_influences(cur_quantity)
            if rel != []:
                positives = len([x for x in rel if x.sign == "positive" and cur_quantity.derivative == "plus" and self.find_value(state, x.origin).magnitude == "plus"])
                negatives = len([x for x in rel if x.sign == "negative" and cur_quantity.derivative == "plus" and self.find_value(state, x.origin).magnitude == "plus"])
                val = positives - negatives
                if val == -1 and cur_quantity.derivative != "minus":
                    return False
                if val == 0 and cur_quantity.derivative != "zero":
                    return False
                if val == 1 and cur_quantity.derivative != "plus":
                    return False

        for relation in self.dcs:
            # Remove violations of the value correspondences
            if relation.name == "VC":
                org = self.find_value(state, relation.origin)
                tar = self.find_value(state, relation.target)
                print(org.magnitude, tar.magnitude)
                if org.magnitude != relation.origin_value and tar.magnitude != relation.target_value:
                    return False

        return True

    def think(self):
        all_states = self.generate_states()
        print("All states: {}".format(len(all_states)))
        valid_states = [state for state in all_states if self.check_state(state)]
        print("Left over states: {}".format(len(valid_states)))
