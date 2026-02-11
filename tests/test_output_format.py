import subprocess, json
from pathlib import Path
# Use the same python executable that's running the tests (works in CI and locally)
import sys
PY = Path(sys.executable)
CLI = PY.as_posix() + ' ' + (Path(__file__).resolve().parents[1] / 'py' / 'cli.py').as_posix()

def run(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def test_encrypt_base64_and_decrypt():
    # encrypt to base64
    rc,out,err = run(f"{CLI} encrypt -p testpw -m 'hi' --no-visualize --out-format base64")
    assert rc == 0
    # out should be base64 string
    import base64
    decoded = base64.b64decode(out.splitlines()[-1])
    # parsed should be comma-separated floats
    s = decoded.decode('utf-8')
    assert ',' in s
    # now decrypt using that base64 as ciphertext
    b64 = out.splitlines()[-1]
    rc2,out2,err2 = run(f"{CLI} decrypt -p testpw -c '{b64}' --no-visualize")
    assert rc2 == 0
    assert 'Decrypted message:' in out2
    assert 'hi' in out2

if __name__=='__main__':
    test_encrypt_base64_and_decrypt()
    print('ok')
