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
        if state.get_value(rule.origin)[0] > 0:
            state.set_value(rule.target, "derivative", "plus")
            new_states.append(deepcopy(state))
        return new_states

    def process_proportional(self, state):
        pass

    def check_vc(self, states):
        return states

    def process_relations(self, state):
        # for each rule, check if its application leads to a new state
        newstates = []
        for rule in self.dcs:
            if rule.name == "Influence":
                newstates.extend(self.process_influence(state, rule))
            elif rule.name == "Proportional":
                self.process_proportional(state)
        return newstates

    def think(self, model_instance):
        """
        Generates possible states based on the model quantities, their
        relations and an initial state.
        TODO: store transitions between states
        """
        unprocessed_states = [deepcopy(model_instance)]
        valid_states = []
        while unprocessed_states != []:
            state = unprocessed_states.pop()
            print("current state:", state)
            # Assign the current state as processed
            if state not in valid_states:
                valid_states.append(deepcopy(state))
            # Generate new states using just the quantities
            todos = self.process_quantities(deepcopy(state))

            # Generate new states using the relations
            todos.extend(self.process_relations(deepcopy(state)))

            # Check if the valuecorrespondence still holds
            next_states = self.check_vc(todos)
            # Update unprocessed state with the state that are not processed yet
            unprocessed_states.extend([x for x in next_states if x not in valid_states])

        return None, None