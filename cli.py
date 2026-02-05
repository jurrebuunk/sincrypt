import argparse
from core import md5_to_seed, generate_waves, generate_keywaves, encode_message_wave, decode_message_wave
from plot import plot_sine_waves

def main():
    parser = argparse.ArgumentParser(description="SinMix Waveform Cipher")
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("-p", "--password", required=True)
    parser.add_argument("-m", "--message")
    parser.add_argument("-c", "--ciphertext")
    parser.add_argument("-w", "--waves", type=int, default=3, help="Number of key waves")
    args = parser.parse_args()

    if args.mode == "encrypt":
        if not args.message:
            raise ValueError("Encryption requires --message")
        data = args.message.encode("utf-8")
    else:
        if not args.ciphertext:
            raise ValueError("Decryption requires --ciphertext")
        # Expecting list-like string: b'[float,...]'
        data = eval(args.ciphertext)

    seed = md5_to_seed(args.password)
    print(f"Seed: {seed}")

    # Generate key waves
    key_waves = generate_waves(args.password, len(data), wave_count=args.waves)
    print(f"Generated {len(key_waves)} key waves.")

    # Generate summed key wave
    key_wave = generate_keywaves(len(data), seed, key_waves)

    if args.mode == "encrypt":
        encrypted_wave = encode_message_wave(data, key_wave)
        print("Encrypted wave:")
        print(encrypted_wave)
        plot_sine_waves(key_waves, seed, encrypted_wave, length=len(data), smooth_factor=20)

    else:
        decrypted = decode_message_wave(data, key_wave)
        print("Decrypted message:")
        print(decrypted.decode("utf-8"))
        plot_sine_waves(key_waves, seed, encrypted_wave=data, length=len(data), smooth_factor=20)

if __name__ == "__main__":
    main()
