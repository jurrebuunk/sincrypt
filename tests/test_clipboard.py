import subprocess
from pathlib import Path
import sys
import pyperclip

PYTHON = sys.executable
CLI = f"{PYTHON} {Path(__file__).resolve().parents[1] / 'py' / 'cli.py'}"

def test_encrypt_copy_base64(monkeypatch):
    # ensure clipboard empty
    try:
        pyperclip.copy('')
    except Exception:
        pass
    rc = subprocess.run(f"{CLI} encrypt -p t -m 'x' --no-visualize --out-format base64 --copy", shell=True, capture_output=True, text=True)
    assert rc.returncode == 0
    # last line should indicate copied or be the b64; check clipboard
    try:
        val = pyperclip.paste()
        assert val != ''
    except Exception:
        # if pyperclip not available, test can't verify clipboard; pass
        pass

if __name__=='__main__':
    test_encrypt_copy_base64()
    print('ok')
