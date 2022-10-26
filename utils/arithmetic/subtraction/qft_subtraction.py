# Author: Ahmet Ege Yilmaz
# Year: 2021
# QFT Addition

import numpy as np

from utils.arithmetic.addition.qft_addition import qft_adder_to_integer
from utils.gates import SubtractGate
from utils.misc import encode_integer

from qiskit import QuantumCircuit

def qft_subtractor(subtract_from_this, subtract_this, n=10, to_gate=True):

    assert subtract_from_this - subtract_this >= 0
    assert n >= len(np.binary_repr(max(subtract_from_this,subtract_this)))

    qc = QuantumCircuit(2*n,name= f"subtract {subtract_this}" + bool(subtract_from_this)*f"from {subtract_from_this}")

    SubtractFromThis = encode_integer(subtract_from_this)
    qc.compose(SubtractFromThis.to_gate(),range(SubtractFromThis.num_qubits),inplace=True)

    qc.compose(get_SubtractionGate(n,subtract_this),inplace=True)

    return qc.to_gate() if to_gate else qc

def qft_subtractor_to_integer(qc):
    return qft_adder_to_integer(qc)

def get_SubtractionGate(n,subtract_this):
    return SubtractGate(n,subtract_this)


# qft_subtractor_to_integer(qft_subtractor(12,5,n=4,to_gate=False))