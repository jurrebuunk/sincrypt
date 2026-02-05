import math
import hashlib
import numpy as np
from typing import List, Tuple

# === Seed from password ===
def md5_to_seed(password: str) -> float:
    md5_hex = hashlib.md5(password.encode()).hexdigest()
    seed = int(md5_hex[:8], 16) / 0xFFFFFFFF * math.pi * 2
    return seed

# === Generate variable number of key waves ===
def generate_waves(password: str, length: int, wave_count: int = 3) -> List[Tuple[float,float,float]]:
    """
    Generate n waves based on password and message length.
    Returns a list of (amplitude, frequency, phase) tuples.
    """
    # Ensure enough bytes for any wave count
    repeat = ((wave_count * 3) // 16) + 1
    base = hashlib.md5(((password + ":" + str(length)) * repeat).encode()).digest() * repeat

    waves = []
    for i in range(wave_count):
        amp = (base[i] / 255.0) + 0.5
        freq = base[i + wave_count] / 64.0
        phase = (base[i + wave_count*2] / 255.0) * math.pi*2
        waves.append((amp, freq, phase))
    return waves

# === Generate summed key wave ===
def generate_keywaves(length: int, seed: float, waves: List[Tuple[float,float,float]]) -> np.ndarray:
    key = np.zeros(length)
    for i in range(length):
        key[i] = sum(amp * math.sin(freq*i + phase + seed) for amp, freq, phase in waves)
    return key

# === Encode message into a 4th wave ===
def encode_message_wave(message: bytes, key_wave: np.ndarray) -> np.ndarray:
    """
    Encode message into 4th wave with scaling.
    Message bytes (0-255) are converted to -1..1 and added to key_wave.
    """
    # Ensure message is uint8 array
    message_arr = np.frombuffer(message, dtype=np.uint8)
    # Scale to roughly -1..1
    msg_scaled = (message_arr - 128) / 128.0
    encrypted_wave = key_wave + msg_scaled
    return encrypted_wave

def decode_message_wave(encrypted_wave: np.ndarray, key_wave: np.ndarray) -> bytes:
    """
    Decode message from encrypted wave.
    Reverse the scaling.
    """
    msg_scaled = encrypted_wave - key_wave
    message = np.clip(np.round((msg_scaled * 128) + 128), 0, 255).astype(np.uint8)
    return message.tobytes()
