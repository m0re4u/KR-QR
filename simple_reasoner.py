# author: Michiel van der Meer - 2017
# Knowledge Representation course, QR project
import quantities as qn
from copy import deepcopy


class Simple_QRReasoner():
    """
    Reasoner object that will perform the task of generating the state graph
    and the transitions between the states.
    Should also output a trace to explain why a transition to a certain state
    does or does not occur.
    """

    def __init__(self, model_quantities, model_dependencies):
        # Model contains the quantities, dependencies between them and an
        # initial state
        self.qns = model_quantities
        self.dcs = model_dependencies

    def process_quantities(self, state):
        """
        Generate new states given some states, only based on the quantities and
        their derivatives.
        """
        original = deepcopy(state)
        newstates = []
        for quantity_value in state.instances:
            if quantity_value.derivative > 0:
                quantity_value.magnitude += 1
                newstates.append(deepcopy(state))
            if quantity_value.derivative < 0:
                quantity_value.magnitude -= 1
                newstates.append(deepcopy(state))
        return newstates

    def process_influence(self, state, rule):
        new_states = []
        if rule.sign == "positive":
            if state.get_value(rule.origin)[0] > 0:
                new_state = deepcopy(state)
                new_state.increase_value(rule.target, "derivative")
                new_states.append(new_state)
        elif rule.sign == "negative":
            if state.get_value(rule.origin)[0] > 0:
                new_state = deepcopy(state)
                new_state.decrease_value(rule.target, "derivative")
                new_states.append(new_state)
        return new_states

    def process_proportional(self, state, rule):
        new_states = []
        if rule.sign == "positive":
            if state.get_value(rule.origin)[1] > 0:
                new_state = deepcopy(state)
                new_state.increase_value(rule.target, "derivative")
                new_states.append(new_state)
            if state.get_value(rule.origin)[1] < 0:
                new_state = deepcopy(state)
                new_state.decrease_value(rule.target, "derivative")
                new_states.append(deepcopy(new_state))

        return new_states

    def check_vc(self, states):
        valid = []
        for state in states:
            all_hold = []
            for rule in self.dcs:
                if rule.name == "VC":
                    if state.get_value(rule.origin)[0] == rule.origin_value:
                        if state.get_value(rule.target)[0] != rule.target_value:
                            all_hold.append(False)
                        else:
                            all_hold.append(True)
                    else:
                        all_hold.append(True)
            if all(all_hold):
                valid.append(state)
        return valid

    def process_relations(self, state):
        # for each rule, check if its application leads to a new state
        newstates = []
        for rule in self.dcs:
            if rule.name == "Influence":
                newstates.extend(self.process_influence(state, rule))
            elif rule.name == "Proportional":
                newstates.extend(self.process_proportional(state, rule))
        return newstates

    def think(self, model_instance):
        """
        Generates possible states based on the model quantities, their
        relations and an initial state.
        """
        unprocessed_states = [(0, deepcopy(model_instance))]
        valid_states = []
        state_counter = 0
        transitions = []
        while unprocessed_states != []:
            index, state = unprocessed_states.pop()
            print("current state: {} --> {}".format(index, state))
            # Assign the current state as processed
            if (index, state) not in valid_states:
                valid_states.append((index, deepcopy(state)))
            # Generate new states using just the quantities
            todos = self.process_quantities(deepcopy(state))

            # Generate new states using the relations
            todos.extend(self.process_relations(deepcopy(state)))

            # Check if the valuecorrespondence still holds
            next_states = self.check_vc(todos)
            # Update the list of states that needs to be processed, and
            # record the transitions from states to both new and already
            # existing states.
            for next_state in next_states:
                if next_state not in [x[1] for x in valid_states]:
                    state_counter += 1
                    unprocessed_states.append((state_counter, next_state))
                    transitions.append((index, state_counter))
                else:
                    for i, val in valid_states:
                        if next_state == val:
                            transitions.append((index, i))
        return valid_states, transitions
