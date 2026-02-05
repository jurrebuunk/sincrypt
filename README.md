# sincrypt

Tiny sine-wave cipher that derives key waves from a password to encrypt/decrypt messages and visualize the waveform.

## Usage

Encrypt:
python py/cli.py encrypt -p "password" -m "hello"

Decrypt:
python py/cli.py decrypt -p "password" -c "[ciphertext array from encrypt]"
