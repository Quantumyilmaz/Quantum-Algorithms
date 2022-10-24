# Author: Ahmet Ege Yilmaz
# Year: 2022
# Some useful stuff

import qiskit
from qiskit import QuantumCircuit

vector = qiskit.Aer.get_backend('statevector_simulator') 
unitary = qiskit.Aer.get_backend('unitary_simulator') 
simulator = qiskit.Aer.get_backend("qasm_simulator")

def execute_circ(circ,backend,**kwargs):
    return qiskit.execute(circ,backend=backend,**kwargs).result()
    
def basis_change(circ,gate_name):
    qc = QuantumCircuit(len(circ.qubits))
    getattr(qc,gate_name)(qc.qubits)
    qc.compose(circ,inplace=True)
    # qc.append(circ,qc.qubits)
    getattr(qc,gate_name)(qc.qubits)
    return qc