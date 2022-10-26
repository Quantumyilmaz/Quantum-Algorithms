# Author: Ahmet Ege Yilmaz
# Year: 2022
# Some useful gates

import math
from itertools import combinations
import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT


def OR(n_qubits,to_gate=True):
    n = n_qubits+1
    circ = QuantumCircuit(n)
    for i in range(n_qubits):
        circ.cx(i,-1)
    for i in range(1,n_qubits):
        for comb in combinations(range(n_qubits),i+1):
            circ.mcx(list(comb),-1)

    return circ.to_gate() if to_gate else circ

def AddGate(n,add_this):

    addGate = QuantumCircuit(2*n)
    binary_b = [*map(int,np.binary_repr(add_this))]
    apply_qft_to_these = range(n)

    for i in list(2*n-1-np.where(binary_b[::-1])[0]):  
        addGate.x(i)

    addGate.append(QFT(n).to_gate(),apply_qft_to_these)

    counter = n
    while counter:
        for i in range(counter):
            addGate.cp(2*math.pi/2**(i+1),2*n-counter+i, n-counter)
        counter -= 1


    addGate.append(QFT(n,inverse=True).to_gate(),apply_qft_to_these)

    for i in list(2*n-1-np.where(binary_b[::-1])[0]):
        addGate.x(i)

    return addGate.to_gate()

def SubtractGate(n,subtract_this):
    return AddGate(n=n,add_this=subtract_this).inverse()

















######## OR check ################################################################
# n = 3
# for i in range(n+1):
#     for tuple_ in combinations(range(n),i):
#         comb = np.zeros(n)
#         comb[list(tuple_)] = 1
#         expected_answer = np.any(comb==1)
        
#         circ = QuantumCircuit(n+1,1)
#         for i,k in enumerate(comb):
#             if k:
#                 circ.x(i)

#         circ.compose(OR(n),circ.qubits,inplace=True)
#         circ.measure(-1,cbit=0)

#         ans = list(execute_circ(circ,backend=simulator).get_counts().keys())
#         assert len(ans) == 1
#         assert int(ans[0]) == expected_answer , ans
#         print(tuple_,comb,ans)
#################################################################################