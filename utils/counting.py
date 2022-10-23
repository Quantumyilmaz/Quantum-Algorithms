import math
from qiskit import QuantumCircuit
from utils.phase_estimator import get_phase_estimator, get_phase_estimation

def get_eigstate(n):
    
    eig_state = QuantumCircuit(n)
    eig_state.h(eig_state.qubits)

    return eig_state

def get_t(bit_accuracy,success_chance):

    eps = 1 - success_chance
    t = math.ceil(bit_accuracy + math.log2(2+1/(2*eps)))
    
    return t

def get_counter(bit_accuracy,success_chance,grover_op):
    
    eig_state = get_eigstate(len(grover_op.qubits))
    t = get_t(bit_accuracy,success_chance)

    return get_phase_estimator(eig_state,grover_op,t)

def get_count(bit_accuracy,success_chance,grover_op):

    n = len(grover_op.qubits)
    eig_state = get_eigstate(n)
    t = get_t(bit_accuracy,success_chance)
    assert t + n < 11, t + n

    # print('t: ',t,'n: ',n)

    results = get_phase_estimation(eig_state,grover_op,t)
    
    theta = 2 * math.pi * results['phase']

    N = 2**n
    M = N * math.cos(theta/2)**2

    err = (math.sqrt(2*M*N) + N/(2**(bit_accuracy+1)))*(2**(-bit_accuracy))
    
    return M, theta, err