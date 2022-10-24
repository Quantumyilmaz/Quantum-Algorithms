from itertools import combinations

from qiskit import QuantumCircuit


def OR(n_qubits):
    circ = QuantumCircuit(n_qubits)
    for i in range(n_qubits):
        circ.x(i)
    for i in range(1,n_qubits):
        for comb in combinations(range(n_qubits),i+1):
            circ.mcx(comb[:-1],comb[-1:])
    return circ.to_gate()
