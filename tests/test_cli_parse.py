from py.cli import parse_ciphertext
import numpy as np

def test_parse_comma_separated():
    s = '1.0, -2.0, 3.5'
    arr = parse_ciphertext(s)
    assert isinstance(arr, np.ndarray)
    assert arr.shape[0] == 3
    assert np.allclose(arr, np.array([1.0, -2.0, 3.5]))
