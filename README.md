# Quantum Pattern Recognition on Pauli-Masked Image States

An experimental Qiskit package for recognizing 2×2 amplitude-encoded image patterns by measuring overlaps on four qubits. A shared Pauli mask on query and template preserves their swap overlap, but does not provide complete joint-data privacy.

## Install

```bash
pip install -e '.[test]'
pytest -q
qepr --mode aer --shots 4096 --output results/local.json
```

## Run on an IBM Quantum QPU

```bash
pip install -e '.[ibm]'
# Configure your IBM Quantum account with QiskitRuntimeService
qepr --mode ibm --backend YOUR_BACKEND --shots 4096 --output results/qpu.json
```

This repository contains executable IBM Runtime code, **not measured QPU results**. It does **not** implement the full encrypted-cloning encoder and recovery maps. Pattern similarity is intentionally leaked by the shared-mask overlap estimator.

See `docs/security_and_scope.md` for limitations.

## Background references

- Ouyang et al., *Computing on quantum shared secrets*, Phys. Rev. A **96**, 052333 (2017), https://doi.org/10.1103/PhysRevA.96.052333
- Fisher et al., *Quantum computing on encrypted data*, Nat. Commun. **5**, 3074 (2014), https://doi.org/10.1038/ncomms4074

These works implement different cryptographic schemes; their security guarantees are not inherited by this example.
