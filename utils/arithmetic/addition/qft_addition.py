# Author: Ahmet Ege Yilmaz
# Year: 2021
# QFT Addition

import numpy as np

from utils.gates import AddGate
from utils.misc import encode_integer, get_counts, counts_to_integer

from qiskit import QuantumCircuit

def qft_adder(add_to_this, add_this, n=10, to_gate=True):

    assert n >= len(np.binary_repr(add_to_this+add_this)),len(np.binary_repr(add_to_this+add_this))

    qc = QuantumCircuit(2*n,name= f"add {add_this}" + bool(add_to_this)*f"to {add_to_this}")

    AddToThis = encode_integer(add_to_this)
    qc.compose(AddToThis.to_gate(),range(AddToThis.num_qubits),inplace=True)
    
    qc.compose(get_AdditionGate(n,add_this),inplace=True)

    return qc.to_gate() if to_gate else qc


def qft_adder_to_integer(qc):
    circ = qc.copy()
    return counts_to_integer(get_counts(circ,circ.qubits[:circ.num_qubits//2]))

def get_AdditionGate(n,add_this):
    return AddGate(n,add_this)




# qft_adder_to_integer(qft_adder(20,5,n=10,to_gate=False))