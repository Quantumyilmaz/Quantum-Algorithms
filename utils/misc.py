# Author: Ahmet Ege Yilmaz
# Year: 2022
# Some useful stuff

import math
import numpy as np

import qiskit
from qiskit import QuantumCircuit,ClassicalRegister

vector = qiskit.Aer.get_backend('statevector_simulator') 
unitary = qiskit.Aer.get_backend('unitary_simulator') 
simulator = qiskit.Aer.get_backend("qasm_simulator")

def execute_circ(circ,qubits=None,backend=simulator,**kwargs):

    if qubits is not None and circ.num_clbits == 0:
        cr = ClassicalRegister(len(qubits))
        circ.add_register(cr)
        circ.measure(qubits,circ.clbits)

    return qiskit.execute(circ,backend=backend,**kwargs).result()
    
def basis_change(circ,gate,apply_to_these_qubits=None,use_inverse_gate=False):
    
    qc = QuantumCircuit(circ.num_qubits)

    if apply_to_these_qubits is None:
        apply_to_these_qubits = range(qc.num_qubits)
    
    if isinstance(gate,str):
        getattr(qc,gate)(apply_to_these_qubits)
        qc.compose(circ,inplace=True)
        getattr(qc,gate)(apply_to_these_qubits)
    else:
        qc.compose(gate,apply_to_these_qubits,inplace=True)
        qc.compose(circ,inplace=True)
        if use_inverse_gate:
            qc.compose(gate.inverse(),apply_to_these_qubits,inplace=True)
        else:
            qc.compose(gate,apply_to_these_qubits,inplace=True)
    return qc


def encode_integer(integer,reverse=False):
    
    binary_repr = [*map(int,np.binary_repr(integer)[::-1])] if reverse else [*map(int,np.binary_repr(integer))]
    n = len(binary_repr)
    qc = QuantumCircuit(n)
    for i in list(np.where(binary_repr[::-1])[0]):
        qc.x(i)
    return qc

def prepare_integers(n,integers,to_gate=True):

    circ = QuantumCircuit(len(integers)*n)

    for i,integer in enumerate(integers):
        # assert n>=len(np.binary_repr(integer))
        circ_integer = encode_integer(integer)
        circ.compose(circ_integer.to_gate(),range(i*n,i*n+circ_integer.num_qubits),inplace=True)
    
    return circ.to_gate() if to_gate else circ

def get_counts(circ,qubits,**kwargs):
    return execute_circ(circ,qubits,**kwargs).get_counts()

def counts_to_integer(counts):
    return int(max(counts,key=counts.get),2)

def matrix_to_gate(unitary_mat,to_gate=True):
    # unitary matrix -> quantum gate
    
    assert len(unitary_mat.shape)==2 and unitary_mat.shape[0] == unitary_mat.shape[1]
    n = math.log2(unitary_mat.shape[0])
    assert n == int(n)
    circ = QuantumCircuit(n)
    circ.unitary(unitary_mat,circ.qubits)

    return circ.to_gate() if to_gate else circ