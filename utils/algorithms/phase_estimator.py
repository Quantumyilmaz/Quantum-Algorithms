# Author: Ahmet Ege Yilmaz
# Year: 2022
# Quantum Phase Estimation

import math
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import PhaseEstimation
from utils.misc import simulator,execute_circ


def get_t(bit_accuracy,success_chance):

    eps = 1 - success_chance
    t = math.ceil(bit_accuracy + math.log2(2+1/(2*eps)))
    
    return t

def get_phase_estimator(eig_state,unitary,t):
    """
    - eig_state: represents the quantum state, whose eigenvalue is e^(i*2*pi*theta)
    - unitary: unitary op. with phase e^(i*2*pi*theta)
    - counting qubits. higher t -> higher accuracy
    """

    phase_estimator = PhaseEstimation(t,unitary)

    circuit = QuantumCircuit(len(phase_estimator.qubits),t)
    circuit.append(eig_state.to_gate(),circuit.qubits[-len(eig_state.qubits):])
    circuit.compose(phase_estimator.to_gate(),inplace=True)

    return circuit


def get_phase_estimation(eig_state,unitary,t):
    circuit = get_phase_estimator(eig_state,unitary,t)
    circuit.measure(circuit.qubits[:t],circuit.clbits)
    
    counts = execute_circ(circuit,simulator).get_counts(circuit)

    return {'phase':2 * math.pi * int(max(counts,key=counts.get)[::-1],2)/2**t,
                'counts':counts,
                    'circuit':circuit}

def get_phase(eig_state,unitary,t):
    return get_phase_estimation(eig_state,unitary,t)['phase']



"""
circ = QuantumCircuit(1)
circ.x(0)
theta = 2*math.pi-1e-2
get_phase_estimation(circ,PhaseGate(theta),get_t(8,0.8))['phase']
"""

"""
phases = [0.1,0.2,0.3,0.4]
unitary = np.diag([np.e**(i*1j) for i in phases])
unitary = matrix_to_gate(unitary_mat=unitary,to_gate=True)
eig_state = QuantumCircuit(2)
eig_state.x([0,1])
get_phase_estimation(eig_state=eig_state,unitary=unitary,t=get_t(bit_accuracy=10,success_chance=0.8))
"""


"""
Compare 2 phases:

eig_state1 = QuantumCircuit(1)
eig_state1.x(0)
eig_state2 = eig_state1.copy()

theta1 = 0.101
theta2 = 0.1

t = get_t(9,0.8)
PhaseEstimator1 = PhaseEstimation(t,PhaseGate(theta1)).reverse_bits().to_gate()
PhaseEstimator2 = PhaseEstimation(t,PhaseGate(theta2)).reverse_bits().to_gate()

n = eig_state1.num_qubits + eig_state2.num_qubits + 2*t + 1
circ = QuantumCircuit(n)

circ.append(eig_state1.to_gate(),[0])
circ.append(eig_state2.to_gate(),[t+1])

circ.compose(PhaseEstimator1,range(eig_state1.num_qubits+t),inplace=True)
circ.compose(PhaseEstimator2,range(eig_state1.num_qubits+t,n-1),inplace=True)

circ.compose(GreaterThanGate(t),[*range(1,t+1)]+[*range(t+1+1,2*t+1+1)]+[n-1],inplace=True)

counts = get_counts(circ=circ,qubits=[-1])
int(max(counts,key=counts.get))
# get_counts(circ=circ,qubits=[*range(1,t+1)]+[*range(t+1+1,2*t+1+1)])

"""

"""
theta = 1

t = get_t(9,0.8)
n = 1 + t
eig_state = QuantumCircuit(n)
eig_state.x(0)

eig_state.compose(PhaseEstimatorGate(theta,t),range(n),inplace=True)
eig_state.draw()

2*math.pi*counts_to_integer(get_counts(circ=eig_state,qubits=[*range(1,n)]))/2**t
"""