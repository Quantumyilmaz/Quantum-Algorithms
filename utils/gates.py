# Author: Ahmet Ege Yilmaz
# Year: 2022
# Some useful gates

from itertools import combinations

from qiskit import QuantumCircuit


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