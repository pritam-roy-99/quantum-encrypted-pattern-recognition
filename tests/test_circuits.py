import pytest
pytest.importorskip("qiskit")
from qiskit.quantum_info import Statevector
from qepr.circuits import destructive_swap_circuit
from qepr.core import amplitude_encode,overlap,swap_sign

@pytest.mark.parametrize("image,template",[
    ([[1,1],[0,0]],[[1,1],[0,0]]),
    ([[1,0],[0,0]],[[0,0],[0,1]]),
    ([[1,1],[0,0]],[[1,0],[1,0]])
])
def test_swap_expectation_exact(image,template):
    for x,z in [((0,0),(0,0)),((1,0),(0,1)),((1,1),(1,1))]:
        qc=destructive_swap_circuit(image,template,x,z)
        qc.remove_final_measurements(inplace=True)
        probs=Statevector.from_instruction(qc).probabilities_dict()
        expectation=sum(p*swap_sign(bits,2) for bits,p in probs.items())
        assert expectation==pytest.approx(overlap(amplitude_encode(image),amplitude_encode(template)),abs=1e-10)
