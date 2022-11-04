# Author: Ahmet Ege Yilmaz
# Year: 2022
# Equality and inequalities.

from utils.gates import GreaterThanGate, EqualsGate, LessThanGate
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
    circ.compose(prepare_integers(n=n,integers=[a,b],to_gate=True),inplace=True)
    circ.compose(LessThanGate(n=n,to_gate=True),inplace=True)
    
    return circ


"""
get_counts(LessThan(a,b,4),[-1])
"""