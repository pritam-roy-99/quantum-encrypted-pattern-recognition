"""Qiskit Aer and IBM Quantum SamplerV2 experiment runner."""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import json
from .core import make_templates, estimate_swap, predict, overlap, amplitude_encode
from .circuits import experiment_circuits

def execute(mode="aer", shots=4096, backend_name=None, seed=7, output=None):
    if mode not in ("aer","ibm"): raise ValueError("mode must be aer or ibm")
    if shots < 1: raise ValueError("shots must be positive")
    templates = make_templates()
    query = [[1.0,0.85],[0.1,0.05]]
    circuits, meta = experiment_circuits(query, templates, seed=seed, masked=True)
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    if mode == "aer":
        from qiskit_aer import AerSimulator
        backend = AerSimulator(seed_simulator=seed)
        pm = generate_preset_pass_manager(backend=backend,optimization_level=1,seed_transpiler=seed)
        isa = pm.run(circuits)
        result = backend.run(isa,shots=shots).result()
        counts = [result.get_counts(i) for i in range(len(isa))]
        job_id = None
    else:
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
        service = QiskitRuntimeService()
        backend = (service.backend(backend_name) if backend_name else
                   service.least_busy(operational=True,simulator=False,min_num_qubits=4))
        pm = generate_preset_pass_manager(backend=backend,optimization_level=1,seed_transpiler=seed)
        isa = pm.run(circuits)
        sampler = SamplerV2(mode=backend)
        job = sampler.run(isa,shots=shots)
        job_id = job.job_id()
        result = job.result()
        counts = [pub.data.meas.get_counts() for pub in result]
    scores, records = {}, []
    for info, ct, qc, ref in zip(meta,counts,isa,templates.values()):
        est = estimate_swap(ct,2)
        scores[info["template"]] = est["raw_overlap"]
        records.append({"template":info["template"],"estimate":est,
                        "exact_overlap":overlap(amplitude_encode(query),amplitude_encode(ref)),
                        "depth_transpiled":qc.depth(),"counts":ct})
    out = {"timestamp_utc":datetime.now(timezone.utc).isoformat(),
           "mode":mode,"backend":backend.name,"job_id":job_id,"shots":shots,"seed":seed,
           "masked":True,"query":query,"prediction":predict(scores),"records":records,
           "security_note":"Correlated masking reveals similarity; no encrypted cloning is implemented."}
    if output is not None:
        path = Path(output)
        path.parent.mkdir(exist_ok=True,parents=True)
        path.write_text(json.dumps(out,indent=2),encoding="utf-8")
    return out
