from utils.arithmetic.qft_arithmetic import qft_subtractor
from utils.gates import OR

from qiskit import QuantumCircuit

def GreaterThan(a,b,n=None,to_gate=True):
    subtractor = qft_subtractor(subtract_from=a,subtract_this=b,n=n,to_gate=False)
    n = subtractor.num_qubits
    circ = QuantumCircuit(n+1).compose(subtractor.to_gate(),qubits=range(n))
    return circ.compose(OR(n_qubits=n,to_gate=True))

def LessThan(a,b,n=None,to_gate=True):
    return GreaterThan(a=b,b=a,to_gate=to_gate)

def Equals(a,b,n=None,to_gate=True):
    subtractor = qft_subtractor(subtract_from=max(a,b),subtract_this=min(a,b),n=n,to_gate=False)
    n = subtractor.num_qubits
    circ = QuantumCircuit(n+1)
    circ.x(-1)
    circ.compose(subtractor.to_gate(),qubits=range(n),inplace=True)
    return circ.compose(OR(n_qubits=n,to_gate=True))