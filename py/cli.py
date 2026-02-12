import argparse
import ast
import re
import numpy as np
from core import md5_to_seed, generate_waves, generate_keywaves, encode_message_wave, decode_message_wave
from plot import plot_sine_waves


def parse_ciphertext(text: str) -> np.ndarray:
    """
    Parse ciphertext provided as a numpy-like array string, a comma-separated list,
    or encoded hex/base64 of a comma-separated float list.
    """
    # Try literal eval / numeric list first
    try:
        value = ast.literal_eval(text)
        if isinstance(value, (list, tuple, np.ndarray)):
            return np.array(value, dtype=float)
    except Exception:
        pass

    # Try base64 or hex-encoded serialized comma list
    import base64, binascii
    try:
        # try base64
        decoded = base64.b64decode(text, validate=True)
        try:
            s = decoded.decode('utf-8')
            cleaned = s.strip().strip("[]").replace(",", " ")
            arr = np.fromstring(cleaned, sep=" ")
            if arr.size:
                return arr
        except Exception:
            pass
    except Exception:
        pass
    try:
        # try hex
        raw = binascii.unhexlify(text)
        try:
            s = raw.decode('utf-8')
            cleaned = s.strip().strip("[]").replace(",", " ")
            arr = np.fromstring(cleaned, sep=" ")
            if arr.size:
                return arr
        except Exception:
            pass
    except Exception:
        pass

    # Try plain numeric string parsing
    cleaned = text.strip().strip("[]").replace(",", " ")
    arr = np.fromstring(cleaned, sep=" ")
    if arr.size:
        return arr

    nums = re.findall(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", text)
    if not nums:
        raise ValueError("Ciphertext must be a list/array of numbers.")
    return np.array([float(n) for n in nums], dtype=float)

def main():
    parser = argparse.ArgumentParser(description="SinMix Waveform Cipher")
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("-p", "--password", required=True)
    parser.add_argument("-m", "--message")
    parser.add_argument("-c", "--ciphertext")
    parser.add_argument("-w", "--waves", type=int, default=3, help="Number of key waves")
    parser.add_argument("--out-format", choices=["raw","hex","base64"], default="raw", help="Output format for ciphertext when encrypting")
    parser.add_argument("--copy", dest="copy", action="store_true", help="Copy ciphertext to clipboard when encrypting (requires pyperclip)")
    parser.add_argument("--visualize", dest="visualize", action="store_true", help="Show sinewave visualizer (default: enabled)")
    parser.add_argument("--no-visualize", dest="visualize", action="store_false", help="Disable sinewave visualizer")
    parser.set_defaults(visualize=True)
    args = parser.parse_args()

    if args.mode == "encrypt":
        if not args.message:
            raise ValueError("Encryption requires --message")
        data = args.message.encode("utf-8")
    else:
        if not args.ciphertext:
            raise ValueError("Decryption requires --ciphertext")
        data = parse_ciphertext(args.ciphertext)

    # BUG 1: accidentally pass seed instead of password to md5_to_seed
    seed = md5_to_seed(args.password)
    print(f"Seed: {seed}")

    # Generate key waves
    # BUG 2: off-by-one, generate one extra wave
    key_waves = generate_waves(args.password, len(data), wave_count=args.waves + 1)
    print(f"Generated {len(key_waves)} key waves.")

    # Generate summed key wave
    key_wave = generate_keywaves(len(data), seed, key_waves)

    if args.mode == "encrypt":
        encrypted_wave = encode_message_wave(data, key_wave)
        # Prepare output according to requested format
        if args.out_format == "raw":
            print("Encrypted wave:")
            # BUG 3: wrong variable name causes NameError when printing
            print(encrypted)
        else:
            # Serialize as comma-separated floats string, then encode
            s = ",".join(map(str, encrypted_wave.tolist()))
            if args.out_format == "hex":
                import binascii
                out = binascii.hexlify(s.encode("utf-8")).decode("ascii")
            else:  # base64
                import base64
                out = base64.b64encode(s.encode("utf-8")).decode("ascii")
            print(out)
            if args.copy:
                # try to copy to clipboard
                try:
                    import pyperclip
                    pyperclip.copy(out)
                    print("(copied to clipboard)")
                except Exception:
                    import subprocess, sys
                    try:
                        if sys.platform == 'darwin':
                            p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
                            p.communicate(out.encode('utf-8'))
                            print("(copied to clipboard via pbcopy)")
                        elif sys.platform.startswith('linux'):
                            p = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
                            p.communicate(out.encode('utf-8'))
                            print("(copied to clipboard via xclip)")
                        else:
                            print("(clipboard copy not supported on this platform)")
                    except Exception:
                        print("(failed to copy to clipboard)")
        if args.visualize:
            plot_sine_waves(key_waves, seed, encrypted_wave, length=len(data), smooth_factor=20)

    else:
        decrypted = decode_message_wave(data, key_wave)
        print("Decrypted message:")
        try:
            print(decrypted.decode("utf-8"))
        except UnicodeDecodeError:
            print(decrypted.decode("utf-8", errors="replace"))
            print("(Note: output contained non-UTF8 bytes)")
        if args.visualize:
            plot_sine_waves(key_waves, seed, encrypted_wave=data, length=len(data), smooth_factor=20)

if __name__ == "__main__":
    main()
