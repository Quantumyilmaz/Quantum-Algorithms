from qiskit.circuit.library import QFT
import numpy as np
from qiskit import execute
from qiskit import Aer
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

simulator = Aer.get_backend("qasm_simulator")


def qft_adder(const,add_to_this=0, n=10, to_gate=True, draw_barriers=False):
    a , b = add_to_this , const
    binary_a,binary_b = [*map(int,np.binary_repr(a))], [*map(int,np.binary_repr(b))]
    # assert n > max(len(binary_a), len(binary_b)), max(len(binary_a), len(binary_b))
    assert n >= len(np.binary_repr(a+b)),len(np.binary_repr(a+b))

    # n = max(len(binary_a), len(binary_b)) + 1

    qr_ = QuantumRegister(n*2)
    qc_ = QuantumCircuit(qr_,name= f"add {b}" + bool(a)*f"to {a}")
    apply_qft_to_these = list(range(n,2*n))

    for i in list(np.where(binary_a[::-1])[0]+n):
        qc_.x(i)
    for i in list(n-1-np.where(binary_b[::-1])[0]):    
        qc_.x(i)

         # n = max(len(binary_a), len(binary_b)) + 1

    qc_.append(QFT(n).to_gate(),apply_qft_to_these)

    counter = n
    while counter:
        for i in range(counter):
            qc_.cp(2*np.pi/2**(i+1),n-counter+i, 2*n-counter)
        if draw_barriers:
            qc_.barrier()
        counter -= 1


    qc_.append(QFT(n,inverse=True).to_gate(),apply_qft_to_these)

    for i in list(n-1-np.where(binary_b[::-1])[0]):    
        qc_.x(i)

    return qc_.to_gate() if to_gate else qc_


def qft_adder_to_integer(qc,cr=None):
    
    circuit = qc.copy()
    cr = ClassicalRegister(len(circuit.qubits)//2) if cr is None else cr
    circuit.add_register(cr)
    circuit.measure(circuit.qubits[-len(circuit.clbits):],circuit.clbits)
    results = execute(circuit,backend = simulator).result()
    
    results_counts = results.get_counts(circuit)
    
    result = {y:x for x,y in results_counts.items()}
    result = result[max(result.keys())]
    
    return (2**np.where([*map(int,result)][::-1])[0]).sum()


def qft_adder_deneme(const,add_to_this=0, n=10, to_gate=True, draw_barriers=False,n_needed=None):
    a , b = add_to_this , const
    binary_a,binary_b = [*map(int,np.binary_repr(a))], [*map(int,np.binary_repr(b))]
    # assert n > max(len(binary_a), len(binary_b)), max(len(binary_a), len(binary_b))
    n_needed = len(np.binary_repr(a+b)) if n_needed is None else n_needed
    assert n >= n_needed,n_needed

    # n = max(len(binary_a), len(binary_b)) + 1

    qr_ = QuantumRegister(n*2)
    qc_ = QuantumCircuit(qr_,name= f"add {b}" + bool(a)*f"to {a}")
    # apply_qft_to_these = list(range(n,2*n))
    apply_qft_to_these = list(range(n,n+n_needed))

    for i in list(np.where(binary_a[::-1])[0]+n):
        qc_.x(i)
    for i in list(n-1-np.where(binary_b[::-1])[0]):    
        qc_.x(i)

    # qc_.append(QFT(n).to_gate(),apply_qft_to_these)
    qc_.append(QFT(n_needed).to_gate(),apply_qft_to_these)

    counter = n_needed
    while counter:
        for i in range(counter):
            qc_.cp(2*np.pi/2**(i+1),n-counter+i, n-counter+n_needed)
        if draw_barriers:
            qc_.barrier()
        counter -= 1


    qc_.append(QFT(n_needed,inverse=True).to_gate(),apply_qft_to_these)

    for i in list(n-1-np.where(binary_b[::-1])[0]):    
        qc_.x(i)

    return qc_.to_gate() if to_gate else qc_