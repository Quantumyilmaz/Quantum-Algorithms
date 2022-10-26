from utils.arithmetic.qft_arithmetic import qft_subtractor
from utils.gates import OR

from qiskit import QuantumCircuit

def GreaterThan(a,b,n=None,to_gate=True):
    subtractor = qft_subtractor(subtract_from=a,subtract_this=b,n=n,to_gate=False)
    n = subtractor.num_qubits
    circ = QuantumCircuit(n+1).compose(subtractor.to_gate(),qubits=range(n))
    return circ.compose(OR(n_qubits=n,to_gate=True))