# Author: Ahmet Ege Yilmaz
# Year: 2022
# Grover's Algorithm

import numpy as np
from qiskit import QuantumCircuit
from utils.misc import basis_change

def state_parser(state):
    if isinstance(state,int):
        state = [*map(int,np.binary_repr(state))] # for state=6 this gives [1,1,0]
    elif isinstance(state,str):
        state = [*map(int,state)]
    elif isinstance(state,list):
        assert np.all([isinstance(x,int) for x in state])
    elif isinstance(state,np.ndarray):
        state = state.tolist()
    else:
        raise Exception('Unsupported way of writing the state for GroverSolver function.')

    assert state.count(0) + state.count(1) == len(state) , state

    return state

# No of Grover reflections
def get_t_grover(n,no_of_expected_solutions):
    # How many rotation angles (theta) fit inside the difference between the starting angle (theta/2) and the desired angle (pi/2)

    N = 2**n
    theta = 2*np.arcsin(np.sqrt(no_of_expected_solutions/N))
    t = 0.5 * (np.pi/theta-1) # No of Grover reflections
    # t_min_max = np.array([np.floor(t),np.ceil(t)])
    # t = t_min_max[np.argmin(np.abs(np.pi/2 - (2*t_min_max + 1) * theta))]
    # return int(t)
    return round(t)

def get_diffuser(n):
    # TODO Find out why it does not work, if the qubits are not consecutively placed.
    qc = QuantumCircuit(n)
    qc.h(-1)
    qc.mct(qc.qubits[:-1],-1)
    qc.h(-1)
    qc = basis_change(qc,'x')
    qc = basis_change(qc,'h')
    return qc

# def get_diffuser(nqubits):
#     qc = QuantumCircuit(nqubits)
#     # Apply transformation |s> -> |00..0> (H-gates)
#     for qubit in range(nqubits):
#         qc.h(qubit)
#     # Apply transformation |00..0> -> |11..1> (X-gates)
#     for qubit in range(nqubits):
#         qc.x(qubit)
#     # Do multi-controlled-Z gate
#     qc.h(nqubits-1)
#     qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli
#     qc.h(nqubits-1)
#     # Apply transformation |11..1> -> |00..0>
#     for qubit in range(nqubits):
#         qc.x(qubit)
#     # Apply transformation |00..0> -> |s>
#     for qubit in range(nqubits):
#         qc.h(qubit)
#     return qc
#     # We will return the diffuser as a gate
#     U_s = qc.to_gate()
#     U_s.name = "U$_s$"
#     return U_s

def get_grover_op(oracle):
    n = len(oracle.qubits)
    grover = QuantumCircuit(n)
    grover.compose(oracle,inplace=True)
    grover.compose(get_diffuser(n),inplace=True)
    return grover

def GroverSolver(good_states):

    m = len(good_states) #no_of_solutions
    # assert m>0
    if m == 0:
         n = 2
         states = []
         t = 0
    else:
        states = [*map(state_parser,good_states)]
        assert len(set(tuple(i) for i in states)) == len(states), f'Multiple identical "good" states were given!: {states}'
        n = max([*map(len,states)])
        while 2*m >= 2**n:
            n+=1
        states = [*map(lambda x: [0]*(n-len(x)) + x,states)]
        # n_min = min([*map(lambda x: n - x.index(1),states)])
        t = get_t_grover(n,no_of_expected_solutions=len(states))

    circ = QuantumCircuit(n)
    circ.h(circ.qubits)

    # Oracle
    oracle = QuantumCircuit(n)
    unitary = np.identity(2**n)
    for state in states:
        index_to_negate = sum([i*2**k for k,i in enumerate(state[::-1])])
        unitary[index_to_negate,index_to_negate] = -1
    oracle.unitary(unitary,oracle.qubits)

    grover = get_grover_op(oracle=oracle)
    
    
    for _ in range(t):
        circ.append(grover.to_gate(),circ.qubits)

    return {'circuit':circ, 'states':states, 'grover_op': grover}