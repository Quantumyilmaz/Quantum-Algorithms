# Author: Ahmet Ege Yilmaz
# Year: 2022
# Grover's Algorithm

import math
import numpy as np
from qiskit import QuantumCircuit
from utils.misc import basis_change,get_counts,values_to_phase_matrix,float2binary
from utils.gates import PhaseEstimatorGate,GreaterThanGate

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
    qc = basis_change(qc,'x',False,[*range(qc.num_qubits)])
    qc = basis_change(qc,'h',False,[*range(qc.num_qubits)])
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

def get_grover_op(oracle,n_iqb=None):
    n = len(oracle.qubits)
    grover = QuantumCircuit(n)
    grover.compose(oracle,inplace=True)
    grover.compose(get_diffuser(n if n_iqb is None else n_iqb),inplace=True)
    return grover

def get_grover_eigenstate(n,n_iqb):
    """
    The top qubits are chosen as index qubits. 
    The bottom qubit is turned into |->, ready to be marked by phase kickback.

    n: total number of qubits required by the eigenstate
    n_iqb: number of index qubits.
    """
    grover_eigstate = QuantumCircuit(n)
    grover_eigstate.x(-1)
    grover_eigstate.h(grover_eigstate.qubits[:n_iqb]+[n-1])
    return grover_eigstate

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

# Grover's Algorithm
def Grover(t_grover,grover_eigstate,grover_op):
    circ = QuantumCircuit(grover_op.num_qubits)
    circ.compose(grover_eigstate.to_gate(),inplace=True)
    for _ in range(t_grover):
        circ.compose(grover_op.to_gate(),inplace=True)
    return circ

# Quantum Exponential Search
def QES(n_iqb,grover_eigstate,grover_op,f_check,lambda_=8/7):
    """
    n_iqb: Number of index qubits. 
    """
    assert 1<lambda_<4/3
    m = 1
    solution_found = False
    oracle_calls = 0
    while not solution_found and oracle_calls<10*np.sqrt(2**n_iqb):
        t_grover = np.random.randint(0,m)
        oracle_calls+=t_grover
        circ = Grover(t_grover=t_grover,grover_eigstate=grover_eigstate,grover_op=grover_op)
        counts = get_counts(circ,circ.qubits[:n_iqb],shots=1)
        index_ = int(max(counts, key=counts.get)[::-1],2)
        if f_check(index_):
            solution_found = True
        else:
            m = min(m*lambda_,np.sqrt(2**n_iqb))
    return index_ , oracle_calls

# Quantum Conditional Slicing
def QCS(values,threshold,condition_gate,f_check=None,t_grover=None,**kwargs):

    n_iqb = int(math.log2(len(values)))
    assert n_iqb == math.log2(len(values))

    t = (condition_gate.num_qubits - 1)//2
    n = n_iqb + 2*t + 1

    grover_eigstate = get_grover_eigenstate(n=n,n_iqb=n_iqb)
    threshold_bits = float2binary(threshold,t)
    for k,i in enumerate(threshold_bits[::-1]):
        temp = int(i)
        if temp:
            grover_eigstate.x(t+n_iqb+k)

    unitary = values_to_phase_matrix(values=values)
    grover_op = QuantumCircuit(n)
    grover_op.compose(condition_gate,[*range(n_iqb,t+n_iqb)]+[*range(t+n_iqb,2*t+n_iqb)]+[n-1],inplace=True)
    grover_op = basis_change(grover_op,PhaseEstimatorGate(unitary,t),qubits=[*range(n_iqb+t)],use_inverse_gate=True)
    grover_op = get_grover_op(oracle=grover_op,n_iqb=n_iqb)
    
    if t_grover is None and f_check is None:
        return grover_eigstate,grover_op
    elif t_grover is None:
        return QES(n_iqb=n_iqb,grover_eigstate=grover_eigstate,grover_op=grover_op,f_check=f_check,**kwargs)
    else:
        return Grover(t_grover=t_grover,grover_eigstate=grover_eigstate,grover_op=grover_op)

# multi-Quantum Conditional Slicing
def mQCS(mValues:list,mThresholds:list,mConditionGates:list,f_check=None,t_grover=None,**kwargs):

    no_of_conditions = len(mConditionGates)
    
    n_iqb = int(math.log2(len(mValues[0])))
    assert n_iqb == math.log2(len(mValues[0])) , [n_iqb,len(mValues[0])]

    t = (mConditionGates[0].num_qubits - 1)//2
    
    n = n_iqb + 2*t + 1
    n_all = n*no_of_conditions

    grover_eigstate = get_grover_eigenstate(n=n_all+1,n_iqb=n_iqb)
    for l,threshold in enumerate(mThresholds):
        threshold_bits = float2binary(threshold,t)
        for k,i in enumerate(threshold_bits[::-1]):
            temp = int(i)
            if temp:
                grover_eigstate.x(l*n+t+n_iqb+k)

    grover_op = QuantumCircuit(n_all+1)
    
    # grover_op.mcx([*range(n-1,n_all,n)],[n_all])
    # for i,(values,condition_gate) in enumerate(zip(mValues,mConditionGates)):
    #     grover_op = basis_change(grover_op,condition_gate.copy(),qubits=[*range(n*i+n_iqb,n*(i+1))],use_inverse_gate=True)
    #     phase_est = PhaseEstimatorGate(values_to_phase_matrix(values=values),t)
    #     grover_op = basis_change(grover_op,phase_est.copy(),qubits=[*range(i*n,i*n+n_iqb+t)],use_inverse_gate=True)
    # for i in range(no_of_conditions-1):
    #     for k in range(n_iqb):
    #         grover_op = basis_change(grover_op,'cx',False,k,(i+1)*n+k)

    # TODO Implement this with basis change function
    for i in range(no_of_conditions-1):
        for k in range(n_iqb):
            grover_op.cx(k,(i+1)*n+k)

    for i,(values,condition_gate) in enumerate(zip(mValues,mConditionGates)):
        phase_est = PhaseEstimatorGate(values_to_phase_matrix(values=values),t)
        grover_op.compose(phase_est.copy(),[*range(i*n,i*n+n_iqb+t)],inplace=True)
        grover_op.compose(condition_gate.copy(),[*range(n*i+n_iqb,n*i+n)],inplace=True)

    grover_op.mcx([*range(n-1,n_all,n)],[n_all])

    for i,(values,condition_gate) in enumerate(zip(mValues,mConditionGates)):
        phase_est = PhaseEstimatorGate(values_to_phase_matrix(values=values),t)
        grover_op.compose(condition_gate.copy().inverse(),[*range(n*i+n_iqb,n*i+n)],inplace=True)
        grover_op.compose(phase_est.copy().inverse(),[*range(i*n,i*n+n_iqb+t)],inplace=True)

    for i in range(no_of_conditions-1):
        for k in range(n_iqb):
            grover_op.cx(k,(i+1)*n+k)

    grover_op.compose(get_diffuser(n_iqb).to_gate(),grover_op.qubits[:n_iqb],inplace=True)

    if t_grover is None and f_check is None:
        return grover_eigstate,grover_op
    elif t_grover is None:
        return QES(n_iqb=n_iqb,grover_eigstate=grover_eigstate,grover_op=grover_op,f_check=f_check,**kwargs)
    else:
        return Grover(t_grover=t_grover,grover_eigstate=grover_eigstate,grover_op=grover_op)

# Grover Adaptive Search
def GAS(values,d):
    N = len(values)
    n_iqb = int(math.log2(N))
    assert n_iqb == math.log2(N)

    total_oracle_calls = 0
    threshold_index = np.random.choice([*range(N)])
    while total_oracle_calls <= 22.5 * np.sqrt(N)+1.4*np.log2(N)**2:
        grover_eigstate,grover_op = QCS(values=values,threshold=values[threshold_index],condition_gate=GreaterThanGate(math.ceil(-math.log2(d))))
        index_ , oracle_calls = QES(n_iqb=n_iqb,grover_eigstate=grover_eigstate,grover_op=grover_op,f_check=lambda x: values[x]>values[threshold_index])
        total_oracle_calls += oracle_calls
        if values[index_]>values[threshold_index]:
            threshold_index = index_
        # print(total_oracle_calls)
    return threshold_index