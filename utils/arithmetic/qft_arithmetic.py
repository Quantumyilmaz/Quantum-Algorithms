# Author: Ahmet Ege Yilmaz
# Year: 2021
# QFT Addition & Subtraction

import numpy as np

from utils.gates import AddGate,SubtractGate
from utils.misc import encode_integer, get_counts, counts_to_integer

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT

"""
qft_adder_to_integer(qft_adder(20,5,n=10,to_gate=False))
"""

def qft_adder(add_to,add_this, n=10, to_gate=True, draw_barriers=False):
    a , b = add_to , add_this
    assert n >= len(np.binary_repr(a+b)),len(np.binary_repr(a+b))

    qc = QuantumCircuit(2*n,name= f"add {add_this}" + bool(add_to)*f" to {add_to}")

    AddTo = encode_integer(add_to)
    qc.compose(AddTo.to_gate(),range(AddTo.num_qubits),inplace=True)

    qc.compose(AddGate(n=n,add_this=add_this),inplace=True)

    return qc.to_gate() if to_gate else qc


"""
qft_subtractor_to_integer(qft_subtractor(12,5,n=4,to_gate=False))
"""

def qft_subtractor(subtract_from, subtract_this, n=None, to_gate=True):

    assert subtract_from - subtract_this >= 0

    n_ = len(np.binary_repr(subtract_from))
    if n is None:
        n = n_
    else:
        assert n >= n_

    qc = QuantumCircuit(2*n,name= f"subtract {subtract_this}" + bool(subtract_from)*f" from {subtract_from}")

    SubtractFromThis = encode_integer(subtract_from)
    qc.compose(SubtractFromThis.to_gate(),range(SubtractFromThis.num_qubits),inplace=True)

    qc.compose(SubtractGate(n,subtract_this),inplace=True)

    return qc.to_gate() if to_gate else qc




def qft_arithmetic_to_integer(qc):
    circ = qc.copy()
    return counts_to_integer(get_counts(circ,circ.qubits[:circ.num_qubits//2]))
