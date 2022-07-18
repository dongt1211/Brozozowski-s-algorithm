from graphviz import Digraph
class NFA:
    """A nondeterministic finite automation."""

    def __init__(self, no_state, states, no_alphabet, alphabets, start,
                 no_final, finals, no_transition, transitions):
        self.no_state = no_state
        self.states = states
        self.no_alphabet = no_alphabet
        self.alphabets = alphabets

        # Adding epsilon alphabet to the list
        # and incrementing the alphabet count
        self.alphabets.append('e')
        self.no_alphabet += 1
        self.start = start
        self.no_final = no_final
        self.finals = finals

        self.no_transition = no_transition
        self.transitions = transitions


        # Dictionaries to get index of states or alphabets
        self.states_dict = dict()
        for i in range(self.no_state):
            self.states_dict[self.states[i]] = i


        self.alphabets_dict = dict()
        for i in range(self.no_alphabet):
            self.alphabets_dict[self.alphabets[i]] = i


        # transition table is of the form
        # [From State + Alphabet pair] -> [Set of To States]
        self.transition_table = dict()
        for i in range(self.no_state):
            for j in range(self.no_alphabet):
                self.transition_table[str(i) + str(j)] = []
        for i in range(self.no_transition):
            self.transition_table[str(self.states_dict[self.transitions[i][0]])
                                  + str(self.alphabets_dict[
                                            self.transitions[i][1]])].append(
                self.states_dict[self.transitions[i][2]])

    def reverse1(self):
        new_no_alphabet = self.no_alphabet - 1
        new_no_state = self.no_state + 1
        new_states = self.states
        # Tạo một trạng thái bắt đầu mới(đặt tên là 0)
        #new_initial_state = 'q7'
        #i = 0
        #while ('q' + str(i)) in self.states:
            #i += 1
        #new_initial_state = 'q' + str(i)
        new_initial_state = input("Name new initial state: ")
        new_states.append(new_initial_state)
        # new_start:
        new_start = new_initial_state
        # new_no_final
        new_no_final = 1
        # new_final
        new_finals = []
        new_finals.append(self.start)
        # new_no_transitions
        new_no_transition = self.no_transition + self.no_final
        # Transitions như cũ nhưng đảo ngược lại

        new_transitions = [[0 for i in range(3)] for j in range(self.no_transition)]

        for i in range(self.no_transition):
            new_transitions[i][0] = self.transitions[i][2]
            new_transitions[i][1] = self.transitions[i][1]
            new_transitions[i][2] = self.transitions[i][0]
        #print(new_transitions)
        # Thêm epsilon transitions từ trạng thái bắt đầu mới đến các trạng thái bắt đầu cũ.
        for state in self.finals:
            new_transitions.append([str(new_initial_state), 'e', state])
        print(new_transitions)
        return NFA(
            new_no_state,
            new_states,
            new_no_alphabet,
            self.alphabets,
            new_start,
            new_no_final,
            new_finals,
            new_no_transition,
            new_transitions

        )


    def getEpsilonClosure(self, state):

        # Method to get Epsilon Closure of a state of NFA
        # Make a dictionary to track if the state has been visited before
        # And a array that will act as a stack to get the state to visit next
        closure = dict()
        #if not self.transition_table[str(self.states_dict[state]) + str(self.alphabets_dict['e'])]:
        if state != self.start:
                closure[self.states_dict[state]] = 0
        closure_stack = [self.states_dict[state]]

        # While stack is not empty the loop will run
        while (len(closure_stack) > 0):

            # Get the top of stack that will be evaluated now
            cur = closure_stack.pop(0)

            # For the epsilon transition of that state,
            # if not present in closure array then add to dict and push to stack
            for x in self.transition_table[
                str(cur) + str(self.alphabets_dict['e'])]:
                if x not in closure.keys():
                    closure[x] = 0
                    closure_stack.append(x)
            #closure[cur] = 1
        #print(self.states_dict(closure.keys()))
        return closure.keys()

    def getStateName(self, state_list):

        # Get name from set of states to display in the final DFA diagram
        name = ''
        for x in state_list:
            name += self.states[x]
        return name

    def isFinalDFA(self, state_list):

        # Method to check if the set of state is final state in DFA
        # by checking if any of the set is a final state in NFA
        for x in state_list:
            for y in self.finals:
                if (x == self.states_dict[y]):
                    return True
        return False


    def subset(self):
        dfa_transitions = dict()
        dfa_final_state = []#
        dfa_alphabets = []#
        for i in self.alphabets:
            if(i!='e'):
                dfa_alphabets.append(i)
        epsilon_closure = dict()
        for x in self.states:
            epsilon_closure[x] = list(self.getEpsilonClosure(str(x)))
        #print(epsilon_closure.keys())
        # First state of DFA will be epsilon closure of start state of NFA
        # This list will act as stack to maintain till when to evaluate the states
        dfa_stack = list()
        dfa_stack.append( epsilon_closure[self.start])
        dfa_initial_state = self.getStateName(epsilon_closure[self.start])#
        #print(dfa_stack)
        ## design start state of DFA
        # Check if start state is the final state in DFA
        if (self.isFinalDFA(dfa_stack[0])):
             dfa_final_state.append(self.getStateName(dfa_stack[0]))

        # Adding start state arrow to start state in DFA

        # List to store the states of DFA
        dfa_states = list()
        dfa_states.append(self.getStateName(epsilon_closure[self.start]))

        # Loop will run untill this stack is empty
        while (len(dfa_stack) > 0):
            # Getting top of the stack for current evaluation
            cur_state = dfa_stack.pop(0)
            dfa_transitions[self.getStateName(cur_state)] = dict()
            #print(cur_state)
            # Traversing through all the alphabets for evaluating transitions in DFA

            for al in range((self.no_alphabet) - 1):

                # Set to see if the epsilon closure of the set is empty or not
                from_closure = set()
                for x in cur_state:
                    # Performing Union update and adding all the new states in set
                    from_closure.update(
                        set(self.transition_table[str(x) + str(al)]))

                # Check if epsilon closure of the new set is not empty
                if (len(from_closure) > 0):
                    # Set for the To state set in DFA
                    to_state = set()
                    for x in list(from_closure):
                        #if epsilon_closure[self.states[x]] is not None:
                        to_state.update(set(epsilon_closure[self.states[x]]))
                    #print(to_state)
                    # Check if the to state already exists in DFA and if not then add it
                    if self.getStateName(list(to_state)) not in dfa_states:
                        dfa_stack.append(list(to_state))
                        dfa_states.append(self.getStateName(list(to_state)))

                        # Check if this set contains final state of NFA
                        # to get if this set will be final state in DFA
                        if (self.isFinalDFA(list(to_state))):
                            dfa_final_state.append(self.getStateName(list(to_state)))

                    dfa_transitions[self.getStateName(cur_state)][self.alphabets[al]] = self.getStateName(list(to_state))

                    # Adding edge between from state and to state


                # Else case for empty epsilon closure
                # This is a dead state(ϕ) in DFA
                else:

                    # Check if any dead state was present before this
                    # if not then make a new dead state ϕ
                    if ('ϕ') not in dfa_states:
                        #new_dict = {"ϕ ": {"":""}}
                        dfa_transitions['ϕ'] = dict()
                        # For new dead state, add all transitions to itself,
                        # so that machine cannot leave the dead state
                        dfa_states.append('ϕ')
                        for alpha in dfa_alphabets:
                           dfa_transitions['ϕ'][alpha] = 'ϕ'

                    dfa_transitions[self.getStateName(cur_state)][self.alphabets[al]] = 'ϕ'

        print("dfa_transitions: ",dfa_transitions)
        print("dfa_states:",dfa_states)
        print("dfa_initial_state",dfa_initial_state)
        print("dfa_final_state",dfa_final_state)
        print("dfa_alphabets",dfa_alphabets)
                    # Adding transition to dead state

        return DFA(dfa_states, dfa_alphabets, dfa_transitions, dfa_initial_state, dfa_final_state)
class DFA():
    def __init__(self,dfa_states, dfa_alphabets, dfa_transitions, dfa_initial_state, dfa_final_state):
        self.dfa_states = dfa_states
        self.dfa_alphabets = dfa_alphabets
        self.dfa_transitions = dfa_transitions
        self.dfa_initial_sate = dfa_initial_state
        self.dfa_final_sate = dfa_final_state
        self.graph = Digraph()
    def reverse2(self):
        new_no_alphabet = len(self.dfa_alphabets)
        #dfa_sates
        new_no_state = len(self.dfa_states) + 1
        #print(new_no_state)
        new_states = self.dfa_states
        new_initial_state = input("Name new initial state: ")
        #i = 0
        #while ('q' + str(i)) in NFA:
           # i += 1
        #new_initial_state = 'q' + str(i)
        new_states.append(new_initial_state)
        #dfa_state
        new_start = new_initial_state
        #dfa_state
        new_no_final = 1
        new_finals = []
        new_finals.append(self.dfa_initial_sate)
        #new_transitions number:
        old_no_transitions = 0
        for i, j in self.dfa_transitions.items():
            old_no_transitions += len(j)
        new_no_transition = old_no_transitions + len(self.dfa_final_sate)
        #new_transitions:
        new_transitions = [[0 for i in range(3)] for j in range(old_no_transitions)]
        from_s = []
        input_s = []
        to_s = []
        for i, j in self.dfa_transitions.items():
            from_s.append(i)

            for a, b in j.items():
                input_s.append(a)
                to_s.append(b)
        #print(from_s)
        #print(input_s)
        #print(to_s)
        for i in range(old_no_transitions):

            new_transitions[i][0] = to_s[i]
            new_transitions[i][1] = input_s[i]
            new_transitions[i][2] = from_s[i//len(self.dfa_alphabets)]
        for state in self.dfa_final_sate:
            new_transitions.append([str(new_initial_state), 'e', state])
        #print(new_transitions)
        return NFA(
            new_no_state,
            new_states,
            new_no_alphabet,
            self.dfa_alphabets,
            new_start,
            new_no_final,
            new_finals,
            new_no_transition,
            new_transitions

        )
    def graphviz(self):
        for x in self.dfa_states:
            if(x not in self.dfa_final_sate):
                self.graph.attr('node', shape='circle')
                self.graph.node(x)
            else:
                self.graph.attr('node', shape='doublecircle')
                self.graph.node(x)
        # Adding start state arrow in NFA diagram
        self.graph.attr('node', shape='none')
        self.graph.node('')
        self.graph.edge('', self.dfa_initial_sate)
        # Adding edge between states in NFA from the transitions array
        for i,j in self.dfa_transitions.items():
            for a,b in j.items():
                self.graph.edge(i, b, label = a)
        self.graph.render('dfa', view=True)
