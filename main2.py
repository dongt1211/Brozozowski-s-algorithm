from NFAnDFA import NFA, DFA
dfa = DFA(
    #4,  # number of states
    ['s0', 's1', 's2', 's3','s4'],  # array of states
    #3,  # number of alphabets
    ['a','b'],  # array of alphabets
    {'s0':{'a':'s0','b':'s1'},'s1':{'a':'s2', 'b':'s3'}, 's2':{'a':'s2', 'b':'s4'},
     's3':{'a':'s2','b':'s3'}, 's4':{'a':'s4', 'b': 's4'}},
    's0',  # start state
    #1,  # number of final states
    ['s0','s2','s4']  # array of final states
    #7,  # number of transitions
    # [['q0', 'a', 'q0'], ['q0', 'e', 'q1'], ['q1', 'b', 'q1'],
    #  ['q0', 'e', 'q2'], ['q2', 'c', 'q2'], ['q1', 'b', 'q3'],
    #  ['q2', 'c', 'q3']]

    # array of transitions with its element of type :
    # [from state, alphabet, to state]
)
nfa = NFA(
    5,  # number of states
    ['q0', 'q1', 'q2', 'q3','q4'],  # array of states
    2,  # number of alphabets
    ['a', 'b'],  # array of alphabets
    'q0',  # start state
    1,  # number of final states
    ['q3'],  # array of final states
    9,  # number of transitions
    [['q0', 'a', 'q1'], ['q0', 'a', 'q4'], ['q0', 'b', 'q2'],
     ['q1', 'e', 'q3'], ['q1', 'e', 'q2'],
     ['q2', 'a', 'q3'],['q2','a','q4'],
     ['q4', 'a', 'q2'],['q4','b','q3']]

    # array of transitions with its element of type :
    # [from state, alphabet, to state]
)
nfa.reverse1().subset().reverse2().subset().graphviz()