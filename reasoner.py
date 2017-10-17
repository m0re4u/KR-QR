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

    def pos_inf(self, origin, target):
        """Positive influence relation between origin and target"""
        changed = False
        if origin.magnitude == "plus" and target.derivative == "zero":
            target.derivative = "plus"
            changed = True
        elif origin.magnitude == "minus" and target.derivative == "zero":
            target.derivative = "minus"
            changed = True
        return changed, origin, target

    def neg_inf(self, origin, target):
        """Negative influence relation between origin and target"""
        changed = False
        if origin.magnitude == "plus" and target.derivative == "zero" and target.derivative != "minus":
            target.derivative = "minus"
            changed = True
        elif origin.magnitude == "minus" and target.derivative == "zero" and target.derivative != "plus":
            target.derivative = "plus"
            changed = True
        return changed, origin, target

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
                        if rule.sign == "positive":
                            ch, node, t_node = self.pos_inf(node, t_node)
                            if ch:
                                return True, state
                        elif rule.sign == "negative":
                            ch, node, t_node = self.neg_inf(node, t_node)
                            if ch:
                                return True, state
        # Nothing changed, so return a false change and the same state
        return False, state

    def pos_prop(self, origin, target):
        """Positive proportional relation between origin and target"""
        changed = False
        if origin.derivative == "plus" and target.derivative == "zero" and target.derivative != "plus":
            target.derivative = "plus"
            changed = True
        elif origin.derivative == "plus" and target.derivative == "minus" and target.derivative != "zero":
            target.derivative = "zero"
            changed = True
        elif origin.derivative == "minus" and target.derivative == "zero" and target.derivative != "minus":
            target.derivative = "minus"
            changed = True
        elif origin.derivative == "minus" and target.derivative == "plus" and target.derivative != "zero":
            target.derivative = "zero"
            changed = True
        elif origin.magnitude == "plus" and target.magnitude == "zero" and target.magnitude != "plus":
            target.magnitude = "plus"
            changed = True
        elif origin.magnitude == "plus" and target.magnitude == "minus" and target.magnitude != "zero":
            target.magnitude = "zero"
            changed = True
        elif origin.magnitude == "minus" and target.magnitude == "zero" and target.magnitude != "minus":
            target.magnitude = "minus"
            changed = True
        elif origin.magnitude == "minus" and target.magnitude == "plus" and target.magnitude != "zero":
            target.magnitude = "zero"
            changed = True
        return changed, origin, target

    def neg_prop(self, origin, target):
        """Negative proportional relation between origin and target"""
        changed = False
        if origin.derivative == "plus" and target.derivative == "zero" and target.derivative != "minus":
            target.derivative = "minus"
            changed = True
        elif origin.derivative == "plus" and target.derivative == "plus" and target.derivative != "zero":
            target.derivative = "zero"
            changed = True
        elif origin.derivative == "minus" and target.derivative == "zero" and target.derivative != "plus":
            target.derivative = "plus"
            changed = True
        elif origin.derivative == "minus" and target.derivative == "minus" and target.derivative != "zero":
            target.derivative = "zero"
            changed = True
        elif origin.magnitude == "plus" and target.magnitude == "zero" and target.magnitude != "minus":
            target.magnitude = "minus"
            changed = True
        elif origin.magnitude == "plus" and target.magnitude == "plus" and target.magnitude != "zero":
            target.magnitude = "zero"
            changed = True
        elif origin.magnitude == "minus" and target.magnitude == "zero" and target.magnitude != "plus":
            target.magnitude = "plus"
            changed = True
        elif origin.magnitude == "minus" and target.magnitude == "minus" and target.magnitude != "zero":
            target.magnitude = "zero"
            changed = True
        return changed, origin, target

    def proportional_rule(self, rule, state):
        """
        Rule:   proportional relation between origin and target causes:
                - derivative of origin changes derivative of target
                - magnitude of origin changes magnitude of target
        """
        for node in state:
            if rule.origin == node.quantity:
                for t_node in state:
                    if rule.target == t_node.quantity:
                        # Found an proportional rule with its two quantities
                        if rule.sign == "positive":
                            ch, node, t_node = self.pos_prop(node, t_node)
                            if ch:
                                return True, state
                        elif rule.sign == "negative":
                            ch, node, t_node = self.neg_prop(node, t_node)
                            if ch:
                                return True, state
        # Nothing changed, so return a false change and the same state
        return False, state

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
            state = updated_state

        for rule in self.dcs:
            # Handle influence rule
            if rule.name == "Influence" and rule.sign == "positive":
                ch, updated_state = self.influence_rule(rule, state)
                if ch:
                    print("Applied influence")
                    return updated_state
            # Handle proportional rule
            if rule.name == "Proportional" and rule.sign == "positive":
                ch, updated_state = self.proportional_rule(rule, state)
                if ch:
                    print("Applied proportional")
                    return updated_state
        # Nothing happened, return the unchanged state
        return state
