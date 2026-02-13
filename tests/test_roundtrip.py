import subprocess
import sys
from pathlib import Path
import numpy as np
from py.core import encode_message_wave, decode_message_wave, generate_waves, generate_keywaves, md5_to_seed

def test_roundtrip_bytes():
    pw='unitpw'
    msg=b'hello unit test\x00\xff'
    seed=md5_to_seed(pw)
    key_waves=generate_waves(pw,len(msg),wave_count=3)
    key_wave=generate_keywaves(len(msg),seed,key_waves)
    enc=encode_message_wave(msg,key_wave)
    dec=decode_message_wave(enc,key_wave)
    assert dec==msg

def test_parse_ciphertext_comma_separated():
    from py.cli import parse_ciphertext
    result = parse_ciphertext('1.0, -2.0, 3.5')
    expected = np.array([1.0, -2.0, 3.5])
    np.testing.assert_array_equal(result, expected)

if __name__=='__main__':
    test_roundtrip_bytes()
    test_parse_ciphertext_comma_separated()
    print('ok')