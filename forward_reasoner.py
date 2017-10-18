# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import quantities as qn
from copy import deepcopy


class Forward_QRReasoner():
    """
    Reasoner object that will perform the task of generating the state graph
    and the transitions between the states.
    Should also output a trace to explain why a transition to a certain state
    does or does not occur.
    """

    def __init__(self, model_quantities, model_dependencies):
        self.qns = model_quantities
        self.dcs = model_dependencies

    def deriv_to_magnitude(self, state):
        """
        Rule: nonzero derivative and zero magnitude --> nonzero magnitude
        """
        changed = False
        for node in state:
            if node.magnitude == "zero":
                if node.derivative == "minus":
                    node.magnitude = "minus"
                    changed = True
                elif node.derivative == "plus":
                    node.magnitude = "plus"
                    changed = True
            if node.magnitude == "plus":
                if node.derivative == "plus":
                    node.magnitude == "max"
                    changed = True
        return changed, state

    def pos_inf(self, origin, target):
        """Positive influence relation between origin and target"""
        changed = False
        if origin.magnitude == "plus" and target.derivative == "zero" and target.derivative != "plus":
            target.derivative = "plus"
            changed = True
        elif origin.magnitude == "plus" and target.derivative == "minus" and target.derivative != "zero":
            target.derivative = "zero"
            changed = True
        elif origin.magnitude == "minus" and target.derivative == "zero" and target.derivative != "minus":
            target.derivative = "minus"
            changed = True
        elif origin.magnitude == "minus" and target.derivative == "plus" and target.derivative != "zero":
            target.derivative = "zero"
            changed = True
        return changed, origin, target

    def neg_inf(self, origin, target):
        """Negative influence relation between origin and target"""
        changed = False
        if origin.magnitude == "plus" and target.derivative == "zero" and target.derivative != "minus":
            target.derivative = "minus"
            changed = True
        elif origin.magnitude == "plus" and target.derivative == "plus" and target.derivative != "zero":
            target.derivative = "zero"
            changed = True
        elif origin.magnitude == "minus" and target.derivative == "zero" and target.derivative != "plus":
            target.derivative = "plus"
            changed = True
        elif origin.magnitude == "minus" and target.derivative == "minus" and target.derivative != "zero":
            target.derivative = "zero"
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
        """
        # Make a list of newly reached states, which will be put back into this
        # function
        new_states = []
        # Propagate derivative to magnitude, this is always allowed and will
        # not generate a new state immediately, but the state with the
        # propagation is checked for applicable rules
        ch, updated_state = self.deriv_to_magnitude(state)
        if ch:
            state = updated_state

        # Save the original state which we can use to search for other
        # applicable rules from the current state
        original_state = deepcopy(state)

        for rule in self.dcs:
            if rule.name == "Influence":
                ch, updated_state = self.influence_rule(rule, state)
                if ch:
                    # We applied the influence rule, so put the new state in
                    # a list of newly generated states.
                    # print("Applied influence")
                    new_states.append(updated_state)
                    # Continue with applying other rules with the original
                    # state
                    state = deepcopy(original_state)

            if rule.name == "Proportional":
                ch, updated_state = self.proportional_rule(rule, state)
                if ch:
                    # We applied the proportional rule, so put the new state in
                    # a list of newly generated states.
                    # print("Applied proportional")
                    new_states.append(updated_state)
                    # Continue with applying other rules with the original
                    # state
                    state = deepcopy(original_state)

        # Nothing happened, return the unchanged state
        return new_states
