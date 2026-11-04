# Security and scientific scope

Two amplitude-encoded images |u> and |v> are masked by a common tensor-product Pauli P. The destructive SWAP test yields
  Tr[SWAP (P|u><u|P† ⊗ P|v><v|P†)] = |<u|v>|².
This holds because SWAP commutes with P⊗P. Each pair's Bell measurement outcome 11 has SWAP eigenvalue -1; other outcomes have +1.

## Important limitations

- Common masking leaks the pairwise overlap, and can leak other relations. It does not prove complete joint-data security, semantic secrecy, or security under key reuse.
- The circuit does not implement encrypted-cloning encoder W or recovery maps D_i(S_i,N).
- This is not a quantum speedup or a universal homomorphic encryption protocol.
- All sample image patterns are synthetic 2×2 arrays, not clinical or high-resolution microscopy.
- The hardware runtime path is executable, but no actual QPU run is claimed here.
- Amplitude normalization loses absolute image brightness.
- The experiment does not inherit security guarantees of any cited prior work.

## Distinct earlier protocols

Ouyang et al., Phys. Rev. A 96, 052333 (2017), https://doi.org/10.1103/PhysRevA.96.052333, develop (n,n) secret sharing and computation.

Fisher et al., Nature Communications 5, 3074 (2014), https://doi.org/10.1038/ncomms4074, demonstrate delegated quantum computation on encrypted data.

These are important context but different constructions.
