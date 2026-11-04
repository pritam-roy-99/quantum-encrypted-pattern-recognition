import numpy as np
import pytest
from qepr.core import amplitude_encode,overlap,swap_sign,estimate_swap,predict,make_templates

def test_amplitude():
    assert np.allclose(amplitude_encode([[3,4],[0,0]]),[0.6,0.8,0,0])
    with pytest.raises(ValueError): amplitude_encode([[0,0],[0,0]])

def test_overlap():
    a=amplitude_encode([[1,0],[0,0]])
    b=amplitude_encode([[0,0],[0,1]])
    assert overlap(a,a)==pytest.approx(1)
    assert overlap(a,b)==pytest.approx(0)

def test_bell_sign():
    assert swap_sign("0000",2)==1
    assert swap_sign("0101",2)==-1
    assert swap_sign("1111",2)==1
    assert estimate_swap({"0000":3,"0101":1},2)["raw_overlap"]==pytest.approx(0.5)

def test_templates():
    t=make_templates()
    scores={k:overlap(amplitude_encode(t["top_row"]),amplitude_encode(v)) for k,v in t.items()}
    assert predict(scores)=="top_row"
