# Author: Ahmet Ege Yilmaz
# Year: 2022
# Some useful gates

from itertools import combinations
import math

from utils.misc import basis_change,encode_integer

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
    if to_gate:
        circ = circ.to_gate()
    return circ

def AddGate(n,add_this):
    additionGate = QuantumCircuit(2*n)
    
    counter = n
    while counter:
        for i in range(counter):
            additionGate.cp(2*math.pi/2**(i+1),2*n-counter+i, n-counter)
        counter -= 1
    
    additionGate = basis_change(additionGate,QFT(n).to_gate(),range(n),True)
    
    AddThis = encode_integer(add_this,reverse=False)

    return basis_change(additionGate,AddThis.to_gate(),range(2*n-AddThis.num_qubits,2*n)).to_gate()

def SubtractGate(n,subtract_this):
    return AddGate(n,subtract_this).inverse()

def larger_than(a,b):...
















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