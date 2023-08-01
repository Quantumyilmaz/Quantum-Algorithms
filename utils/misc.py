# Author: Ahmet Ege Yilmaz
# Year: 2022
# Some useful stuff

import math
import numpy as np

import qiskit
from qiskit import QuantumCircuit,ClassicalRegister

backend_vector = qiskit.Aer.get_backend('statevector_simulator') 
backend_unitary = qiskit.Aer.get_backend('unitary_simulator') 
backend_simulator = qiskit.Aer.get_backend("qasm_simulator")

def execute_circ(circ,qubits=None,backend=backend_simulator,**kwargs):
    temp_circ = circ.copy()
    if qubits is not None and circ.num_clbits == 0:
        cr = ClassicalRegister(len(qubits))
        temp_circ.add_register(cr)
        temp_circ.measure(qubits,temp_circ.clbits)

    return qiskit.execute(temp_circ,backend=backend,**kwargs).result()
    
def basis_change(circ,gate,use_inverse_gate=False,*args,**kwargs):
    
    qc = QuantumCircuit(circ.num_qubits)
    
    if isinstance(gate,str):
        getattr(qc,gate)(*args,**kwargs)
        qc.compose(circ,inplace=True)
        getattr(qc,gate)(*args,**kwargs)
    else:
        qc.compose(gate,*args,inplace=True)
        qc.compose(circ,inplace=True)
        if use_inverse_gate:
            qc.compose(gate.inverse(),*args,**kwargs,inplace=True)
        else:
            qc.compose(gate,*args,**kwargs,inplace=True)
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
    if qubits == 'all':
        qubits = circ.qubits
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

def get_unitary(circ):
    return execute_circ(circ,backend=backend_unitary).get_unitary()

def get_bloch_vector(circ):
    return execute_circ(circ,backend=backend_vector).get_statevector()

def float2binary(number,bit_accuracy):
    assert number<1 and  0<=number,number
    bits = ''
    for i in range(bit_accuracy):
        if number - 2**-(i+1) > 0:
            number -= 2**-(i+1)
            bits+='1'
        else:
            bits+='0'
    return bits

def bits2float(bits):
    result = 0
    for i,k in enumerate(bits):
        result += int(k)*2**-(i+1)
    return result

def values_to_phase_matrix(values):
    assert np.all([1>val>=0 for val in values])
    unitary = np.diag([np.e**(1j*2*math.pi*i) for i in values])
    return matrix_to_gate(unitary_mat=unitary,to_gate=True)