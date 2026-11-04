"""Four-qubit destructive SWAP circuits with correlated Pauli masks."""
from __future__ import annotations
import numpy as np
from .core import amplitude_encode

def destructive_swap_circuit(image, template, xmask=(0,0), zmask=(0,0)):
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import StatePreparation
    a, b = amplitude_encode(image), amplitude_encode(template)
    if len(a) != 4 or len(b) != 4:
        raise ValueError("only 2x2 images are supported in this hardware demonstration")
    if len(xmask) != 2 or len(zmask) != 2 or any(v not in (0,1) for v in (*xmask,*zmask)):
        raise ValueError("mask values must be two binary entries")
    qc = QuantumCircuit(4,4)
    qc.append(StatePreparation(a), [0,1])
    qc.append(StatePreparation(b), [2,3])
    for i in range(2):
        for q in (i,i+2):
            if xmask[i]: qc.x(q)
            if zmask[i]: qc.z(q)
    for i in range(2):
        qc.cx(i,2+i)
        qc.h(i)
    qc.measure([0,1,2,3], [0,1,2,3])
    return qc

def experiment_circuits(image, templates, seed=7, masked=True):
    rng = np.random.default_rng(seed)
    circuits, metadata = [], []
    for name, template in templates.items():
        x = tuple(map(int,rng.integers(0,2,2))) if masked else (0,0)
        z = tuple(map(int,rng.integers(0,2,2))) if masked else (0,0)
        circuits.append(destructive_swap_circuit(image,template,x,z))
        metadata.append({"template": name, "xmask": list(x), "zmask": list(z)})
    return circuits, metadata
