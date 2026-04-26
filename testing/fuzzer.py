import os
import struct
import random
import subprocess
import sys

# Constants from packet_format.h
MAGIC = b'ORBS'
IV_SIZE = 16
MAX_PAYLOAD_SIZE = 1024
MAX_SIG_SIZE = 128

def generate_malformed_packet():
    """
    Generate a packet with potential mutations to test the parser.
    """
    # Base valid structure
    magic = MAGIC
    payload_length = random.randint(0, MAX_PAYLOAD_SIZE * 2)  # Allow oversized
    sig_length = random.randint(0, MAX_SIG_SIZE * 2)
    iv = os.urandom(IV_SIZE)
    ciphertext = os.urandom(payload_length) if payload_length <= MAX_PAYLOAD_SIZE else os.urandom(MAX_PAYLOAD_SIZE)
    signature = os.urandom(sig_length) if sig_length <= MAX_SIG_SIZE else os.urandom(MAX_SIG_SIZE)

    # Mutations
    mutations = [
        lambda: (os.urandom(4), payload_length, sig_length, iv, ciphertext, signature),  # Wrong magic
        lambda: (magic, 0xFFFF, sig_length, iv, ciphertext, signature),  # Max uint16_t payload_length
        lambda: (magic, payload_length, 0xFFFF, iv, ciphertext, signature),  # Max uint16_t sig_length
        lambda: (magic, -1 & 0xFFFF, sig_length, iv, ciphertext, signature),  # Negative length (as uint16)
        lambda: (magic, payload_length, sig_length, os.urandom(IV_SIZE + random.randint(1, 10)), ciphertext, signature),  # Wrong IV size
        lambda: (magic, payload_length, sig_length, iv, os.urandom(payload_length + random.randint(1, 100)), signature),  # Oversized ciphertext
        lambda: (magic, payload_length, sig_length, iv, ciphertext, os.urandom(sig_length + random.randint(1, 50))),  # Oversized signature
    ]

    if random.random() < 0.5:  # 50% chance to mutate
        mutation = random.choice(mutations)
        magic, payload_length, sig_length, iv, ciphertext, signature = mutation()

    # Pack the packet
    try:
        fmt = f'<4sHH16s{payload_length}s{sig_length}s'
        packet = struct.pack(fmt, magic, payload_length, sig_length, iv, ciphertext, signature)
        return packet
    except struct.error:
        # If packing fails (e.g., too large), return truncated or None
        return None

def run_fuzzer(iterations=10000):
    """
    Run the fuzzer for a number of iterations, generating packets and testing the decoder.
    """
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)

    # Compile the C program if not exists
    exe_path = 'firmware/orbitsec_decoder.exe'
    if not os.path.exists(exe_path):
        print("Compiling the C program...")
        try:
            # Adjust for Windows
            subprocess.run(['gcc', '-Wall', '-Wextra', '-I./firmware/include', '-L/path/to/openssl/lib', '-lcrypto', 'firmware/src/decrypt_and_verify.c', '-o', exe_path], check=True)
        except subprocess.CalledProcessError:
            print("Failed to compile. Please ensure OpenSSL is installed and paths are correct.")
            sys.exit(1)

    crashes = 0
    timeouts = 0
    errors = 0

    for i in range(iterations):
        packet = generate_malformed_packet()
        if packet is None:
            continue  # Skip invalid packets

        # Write packet to file
        with open('data/ciphertext.bin', 'wb') as f:
            f.write(packet)

        # Run the decoder
        try:
            result = subprocess.run([exe_path], capture_output=True, text=True, timeout=10)
            if result.returncode != 0 and result.returncode != 1:  # 1 is expected for invalid packets
                print(f"Abnormal exit at iteration {i}: returncode {result.returncode}")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                errors += 1
        except subprocess.TimeoutExpired:
            print(f"Timeout at iteration {i}")
            timeouts += 1
        except Exception as e:
            print(f"Crash at iteration {i}: {e}")
            crashes += 1

    print(f"Fuzzing complete: {iterations} iterations")
    print(f"Crashes: {crashes}, Timeouts: {timeouts}, Errors: {errors}")

if __name__ == "__main__":
    run_fuzzer()