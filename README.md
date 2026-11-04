# Quantum Pattern Recognition on Pauli-Masked Image States

[![Tests](https://github.com/pritam-roy-99/quantum-encrypted-pattern-recognition/actions/workflows/tests.yml/badge.svg)](https://github.com/pritam-roy-99/quantum-encrypted-pattern-recognition/actions/workflows/tests.yml)

A reproducible Qiskit research demonstration of image-pattern recognition on a physical IBM Quantum QPU. A grayscale 2×2 image is amplitude encoded into two qubits. Query and template are compared through a four-qubit destructive SWAP test. Both registers receive the same secret two-qubit Pauli mask, leaving overlap invariant. **This is not a fully private encrypted-cloning implementation.**

## Installation

Requires Python 3.10+.

```bash
python -m pip install -e '.[test,plot]'
python -m pytest -q
qepr --mode aer --shots 4096 --output results/local.json
python examples/plot_results.py results/local.json
```

## Actual IBM Quantum hardware

```bash
python -m pip install -e '.[ibm,plot]'
# Configure QiskitRuntimeService authentication using IBM Quantum documentation.
qepr --mode ibm --backend YOUR_BACKEND_NAME --shots 4096 --output results/ibm.json
python examples/plot_results.py results/ibm.json
```

Omit --backend to select an operational available non-simulator backend. No physical job or QPU result is claimed here. IBM QPU access requires user authentication and may incur charges.

## Mathematics

For nonnegative pixel intensities I, let |I> = sum_j I_j |j> / ||I||. Pattern similarity is F(q,t) = |<q|t>|². The destructive SWAP measurement samples an observable with mean F. Correlated masking with P⊗P does not change the measured overlap.

The example includes top-row, left-column and diagonal templates, an altered top-row query, Aer simulation, IBM SamplerV2, test cases, result JSON and plotting.

**Security limitation:** sharing the same mask intentionally reveals similarity and may leak other relations. This does not implement the conceptual diagram's cloning encoder W, recovery D_i(S_i,N), or universal encrypted processing. The 2×2 example does not establish a quantum advantage. See [security analysis](docs/security_and_scope.md).

## Background

- Ouyang et al., *Computing on quantum shared secrets*, Phys. Rev. A **96**, 052333 (2017): https://doi.org/10.1103/PhysRevA.96.052333
- Fisher et al., *Quantum computing on encrypted data*, Nat. Commun. **5**, 3074 (2014): https://doi.org/10.1038/ncomms4074

These are distinct quantum cryptographic constructions; their security guarantees do not transfer to this example.

## License

MIT for code. Conceptual workflow artwork is available separately in the project ZIP and is not redistributed without a rights review.
