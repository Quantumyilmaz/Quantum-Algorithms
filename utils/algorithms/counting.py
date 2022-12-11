# Author: Ahmet Ege Yilmaz
# Year: 2022
# Quantum Counting.

import math
from qiskit import QuantumCircuit
from utils.algorithms.phase_estimator import get_phase_estimator, get_phase_estimation, get_t

def get_eigstate(n):
    
    eig_state = QuantumCircuit(n)
    eig_state.h(eig_state.qubits)

    return eig_state

def get_counter(bit_accuracy,success_chance,grover_op,eig_state=None):
    
    if eig_state is None:
        eig_state = get_eigstate(len(grover_op.qubits))
    t = get_t(bit_accuracy,success_chance)

    return get_phase_estimator(eig_state,grover_op,t)

def get_count(bit_accuracy,success_chance,grover_op,eig_state=None,n=None):
    # M must be smaller than N/2 !

    if n is None:
        n = grover_op.num_qubits
    if eig_state is None:
        eig_state = get_eigstate(n)
    t = get_t(bit_accuracy,success_chance)
    assert t + grover_op.num_qubits < 26, t + grover_op.num_qubits

    print('t: ',t,'grover_op.num_qubits: ',grover_op.num_qubits)

    results = get_phase_estimation(eig_state,grover_op,t)
    
    # It gives pi +/- (theoretical) theta bcs we are using -U_s in Grover. The plus/minus comes from the positive/negative phased eigenvalue
    theta = results['phase']

    N = 2**n
    M = N * math.cos(theta/2)**2 # we use cos instead if sin because see above.

    # err = (math.sqrt(2*M*N) + N/(2**(bit_accuracy+1)))*(2**(-bit_accuracy)) #
    err = (math.sqrt(M*N) + N/(2**(bit_accuracy+2)))*(2**(-bit_accuracy)) # max error

    return M, theta, err