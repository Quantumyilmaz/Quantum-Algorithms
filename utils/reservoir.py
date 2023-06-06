def decomposedIsing(n,interactions,couplings,tau):
    
    """
        n: no of qubits
        interactions: dict of interaction constants
        couplings: dict of coupling constants
        tau: evolution time

    """
    assert np.all((1>u)*(u>0))
    kappa = 1
    tau = 2*tau/kappa
    circ = QuantumCircuit(n)
    # encode input
    circ.ry(2*np.arcsin(np.sqrt(u[0])),0)
    circ.barrier()
    # pure terms
    pure_gate = QuantumCircuit(n)
    for i in couplings:
        if couplings[i] != 0:
            pure_gate.rz(couplings[i]*tau,i)
    # interaction terms
    interaction_gate = QuantumCircuit(n)
    for i in interactions:
        if interactions[i] != 0:
            interaction_gate.h(i)
            interaction_gate.cx(i[0],i[1])  
            interaction_gate.rz(interactions[i]*tau,i[-1])
            interaction_gate.cx(i[0],i[1])  
            interaction_gate.h(i)
            interaction_gate.barrier()

    circ.compose(pure_gate,inplace=True)
    circ.barrier()
    circ.compose(interaction_gate,inplace=True)
    return circ