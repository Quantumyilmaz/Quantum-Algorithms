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