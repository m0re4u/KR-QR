# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import quantities as qn
from copy import deepcopy


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
        DERIV_ALPHABET = ["minus", "zero", "plus"]

    def deriv_to_magnitude(self, state):
        """
        Rule: nonzero derivative and zero magnitude --> nonzero magnitude
        """
        for node in state:
            if node.magnitude == "zero":
                if node.derivative == "minus":
                    node.magnitude = "minus"
                elif node.derivative == "plus":
                    node.magnitude = "plus"
        return state

    def influence_rule(self, rule, state):
        """
        Rule:   influence relation between origin and target causes magnitude
                of origin to influence the derivative of the target
        """
        # check out current model to see if we can apply the rule
        for node in state:
            if rule.origin == node.quantity:
                for t_node in state:
                    if rule.target == t_node.quantity:
                        # Found an influence rule with its two quantities
                        if node.magnitude == "plus" and t_node.derivative == "zero":
                            t_node.derivative = "plus"
                            return state
                        if node.magnitude == "minus" and t_node.derivative == "zero":
                            t_node.derivative = "minus"
                            return state
        return state

    def proportional_rule(self, rule, state):
        """
        Rule:   proportional relation between origin and target causes:
                - derivative of origin changes derivative of target
                - magnitude of origin changes magnitude of target
        """
        for node in state:
            if rule.origin == node.quantity:
                # Found a rule applying to a node we have
                for t_node in state:
                    # find the target node
                    if rule.target == t_node.quantity:
                        if node.derivative == "plus" and t_node.derivative == "zero":
                            t_node.derivative = "plus"
                            return state
                        if node.derivative == "minus" and t_node.derivative == "zero":
                            t_node.derivative = "minus"
                            return state
        return state

    def think(self, state):
        """
        Generates possible states based on the model quantities, their
        relations and an initial state.
        New states are generated using propagation rules. If one of the rules
        has changed the state, we return that state and stop applying other
        rules.
        """
        # Save initial state to check if anything changed at the end
        begin_state = deepcopy(state)
        updated_state = self.deriv_to_magnitude(state)
        if updated_state != begin_state:
            return updated_state

        for rule in self.dcs:
            # Handle influence rule
            if rule.name == "Influence" and rule.sign == "positive":
                updated_state = self.influence_rule(rule, state)
                if updated_state != begin_state:
                    return updated_state
            # Handle proportional rule
            if rule.name == "Proportional" and rule.sign == "positive":
                updated_state = self.proportional_rule(rule, state)
                if updated_state != begin_state:
                    return updated_state
        # Nothing happened, return the unchanged state
        return state
