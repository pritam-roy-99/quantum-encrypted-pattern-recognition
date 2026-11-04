"""Amplitude encoding and destructive SWAP-test outcome processing."""
from __future__ import annotations
import numpy as np

def amplitude_encode(image: np.ndarray) -> np.ndarray:
    """Normalize nonnegative 2^n-pixel intensities; discards global brightness."""
    a = np.asarray(image, dtype=float)
    if a.ndim != 2 or not np.all(np.isfinite(a)) or np.any(a < 0):
        raise ValueError("image must be a finite, nonnegative 2D array")
    v = a.ravel(order="C")
    if len(v) < 2 or (len(v) & (len(v)-1)):
        raise ValueError("pixel count must be a power of two >= 2")
    norm = np.linalg.norm(v)
    if norm == 0:
        raise ValueError("cannot amplitude-encode an all-black image")
    return v.astype(complex) / norm

def overlap(a: np.ndarray, b: np.ndarray) -> float:
    """Exact squared overlap for two pure states."""
    a, b = np.asarray(a, complex), np.asarray(b, complex)
    if a.shape != b.shape or a.ndim != 1:
        raise ValueError("states must have equal 1D shape")
    return float(abs(np.vdot(a, b))**2)

def swap_sign(bitstring: str, n: int) -> int:
    """Bell measurement sign; Qiskit prints c[last]...c[0]."""
    v = int(bitstring.replace(" ", ""), 2)
    antisymmetric = sum(((v >> i) & 1) & ((v >> (n+i)) & 1) for i in range(n))
    return -1 if antisymmetric % 2 else 1

def estimate_swap(counts: dict[str, int], n: int) -> dict[str, float]:
    if n < 1: raise ValueError("n must be positive")
    total = sum(counts.values())
    if not total: raise ValueError("empty counts")
    s = sum(c * swap_sign(bits, n) for bits, c in counts.items()) / total
    return {"raw_overlap": float(s), "clipped_overlap": float(np.clip(s, 0, 1)),
            "standard_error": float(np.sqrt(max(0, 1-s*s) / total)), "shots": int(total)}

def predict(scores: dict[str, float]) -> str:
    if not scores: raise ValueError("empty scores")
    return max(scores, key=scores.get)

def make_templates() -> dict[str, np.ndarray]:
    return {"top_row": np.array([[1., 1.], [0., 0.]]),
            "left_column": np.array([[1., 0.], [1., 0.]]),
            "diagonal": np.array([[1., 0.], [0., 1.]])}
