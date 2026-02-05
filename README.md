# sincrypt

Tiny sine-wave cipher that derives key waves from a password to encrypt/decrypt messages and visualize the waveform.

---

## Usage

### Encrypt

```bash
python py/cli.py encrypt -p "password" -m "hello"
```

### Decrypt

```bash
python py/cli.py decrypt -p "password" -c "[ciphertext array from encrypt]"
```

---

## Notes

- Keep the password consistent between encrypt/decrypt.
- The ciphertext is the array printed by the encrypt command.
