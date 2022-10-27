
from utils.gates import GreaterThanGate, EqualsGate
from utils.misc import prepare_integers

from qiskit import QuantumCircuit

def GreaterThan(a,b,n=10):
    # a > b
    
    circ = QuantumCircuit(2*n+1)
    circ.compose(prepare_integers(n=n,integers=[a,b],to_gate=True),inplace=True)
    circ.compose(GreaterThanGate(n=n,to_gate=True),inplace=True)
    
    return circ

def Equals(a,b,n=10):
    
    # a == b
    circ = QuantumCircuit(2*n+1)
    circ.compose(prepare_integers(n=n,integers=[a,b],to_gate=True),inplace=True)
    circ.compose(EqualsGate(n=n,to_gate=True),inplace=True)
    
    return circ

def LessThan(a,b,n=10):
    # a < b
    
    circ = QuantumCircuit(2*n+1)
    circ.compose(Equals(a=a,b=b,n=n),inplace=True)
    circ.compose(GreaterThanGate(n=n,to_gate=True),inplace=True)
    circ.compose(GreaterThanGate(n=n,to_gate=True),inplace=True)
    
    return circ


# def LessThan(a,b,n=None,to_gate=True):
#     return GreaterThan(a=b,b=a,to_gate=to_gate)


"""
a = 13 ; b = 12
circ = GreaterThan(a,b,4)
get_counts(circ,[-1])
"""