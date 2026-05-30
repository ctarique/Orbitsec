# OrbitSec: High-Assurance Cryptographic Bridge

**OrbitSec** is a secure communication prototype for resource-constrained embedded systems. It uses an **Encrypt-then-Sign** sender workflow and a **Verify-then-Decrypt** receiver workflow so incoming packets are authenticated before the AES decryption path processes protected payload data.

The project was completed for **CY 510: Information Security and Assurance** at Southeast Missouri State University during April–May 2026. This repository is preserved as a completed academic security engineering project and portfolio artifact, with future expansion planned after thesis work.

---

## Overview

OrbitSec models a secure packet transmission pipeline between a Python-based uplink and a C-based firmware decoder.

The Python uplink encrypts telemetry data using AES-256-CBC, hashes the ciphertext with SHA-256, signs it using ECDSA P-256, and packages the result into a strict binary packet format.

The C firmware decoder acts as a gatekeeper. It parses packet headers, enforces bounds checks, validates the ECDSA signature, and only then allows AES decryption to proceed.

The core security idea is simple:

> Do not decrypt untrusted data until the packet has proven its authenticity and integrity.

This design reduces exposure to spoofed packets, tampered ciphertext, malformed payloads, oversized inputs, and unsafe packet-processing behavior in constrained embedded-style environments.

---

## Architecture

OrbitSec is organized around two complementary workflows.

### Python Uplink: Encrypt-then-Sign

The Python sender performs the producer-side cryptographic workflow:

1. Accept plaintext telemetry data
2. Apply PKCS#7 padding for AES block alignment
3. Encrypt the payload using AES-256-CBC
4. Hash the ciphertext with SHA-256
5. Sign the hash using ECDSA P-256
6. Package the IV, ciphertext, signature, and fixed headers into a binary packet

![Encrypt-then-Sign Python Flow](./docs/encrypt_then_sign_python.png)

### C Firmware Decoder: Verify-then-Decrypt

The C receiver performs the consumer-side gatekeeper workflow:

1. Parse fixed packet headers
2. Validate magic bytes
3. Enforce payload and signature length bounds
4. Load the sender public key
5. Verify the ECDSA signature against the ciphertext
6. Reject invalid packets before decryption
7. Initialize AES-256-CBC decryption only after verification succeeds
8. Decrypt and process validated telemetry data
9. Free cryptographic contexts and allocated memory

![Verify-then-Decrypt C Flow](./docs/verify_then_decrypt_c.png)

---

## Repository Structure

```text
.
├── docs/              # Project documentation, diagrams, reports, and validation screenshots
├── firmware/          # C implementation of the firmware decoder and gatekeeper logic
├── testing/           # Fuzzing and malformed-packet validation scripts
├── uplink/            # Python encryption, signing, hashing, and packet-generation scripts
├── .gitignore
├── INSTRUCTIONS.md
├── LICENSE
├── README.md
└── requirements.txt
```

Generated cryptographic artifacts such as keys, IVs, ciphertext packets, and fuzzed binary payloads should be treated as local test artifacts, not production secrets.

---

## Key Features

* **Encrypt-then-Sign Uplink:** Encrypts payload data with AES-256-CBC and signs the ciphertext using ECDSA P-256.
* **Verify-then-Decrypt Firmware:** Validates packet authenticity before initializing the AES decryption path.
* **Strict Binary Packet Format:** Uses fixed headers, magic bytes, payload length fields, signature length fields, IVs, ciphertext, and signatures.
* **Defensive C Firmware Design:** Uses structured parsing, strict bounds checking, and controlled failure behavior to reject unsafe input.
* **OpenSSL EVP Integration:** Uses OpenSSL EVP abstractions for signature verification and decryption behavior.
* **STRIDE Threat Modeling:** Maps spoofing, tampering, repudiation, information disclosure, denial of service, and elevation-of-privilege risks to specific mitigations.
* **Fuzz Testing:** Uses malformed packet injection to test decoder stability against bad magic bytes, invalid signatures, oversized payloads, truncation, and mutation-based attack cases.

---

## Security Posture

OrbitSec is designed to mitigate high-priority threats identified during STRIDE analysis.

| Threat Category        | Example Risk                                                        | OrbitSec Mitigation                                            |
| ---------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------- |
| Spoofing               | Unauthorized sender attempts to masquerade as the legitimate source | ECDSA P-256 signature verification before decryption           |
| Tampering              | Attacker modifies ciphertext, IV, or packet contents                | SHA-256 hashing and ECDSA signature validation                 |
| Repudiation            | Sender denies transmitting a signed packet                          | Asymmetric signature workflow using a private signing key      |
| Information Disclosure | Unauthorized observer reads transmitted payload data                | AES-256-CBC encryption                                         |
| Denial of Service      | Malformed packets attempt to exhaust memory or processing resources | Early rejection, bounds checking, and controlled failure paths |
| Elevation of Privilege | Oversized payload attempts to trigger unsafe memory behavior        | Strict length enforcement before copying or decrypting data    |

---

## Testing and Validation

OrbitSec was tested using valid packets and malformed packet cases generated by the Python uplink and fuzzing tools.

### Baseline Handshake

A valid signed and encrypted packet is accepted by the C firmware decoder.

```text
[*] OrbitSec Firmware Decoder Initializing...
[+] Parsed Packet: Payload=80 bytes, Signature=70 bytes.
[*] Gatekeeper: Verifying ECDSA Signature against raw ciphertext...
[+] SUCCESS: Cryptographic signature validated.
[+] Gatekeeper passed. Proceeding to AES-256 decryption engine...
```

![Baseline Handshake](./docs/baseline_handshake.png)

### Spoofing Test: Bad Magic Bytes

A packet with invalid magic bytes is rejected before signature verification or decryption.

```text
[*] OrbitSec Firmware Decoder Initializing...
[+] Parsed Packet: Payload=64 bytes, Signature=70 bytes.
[-] Fatal: Invalid Magic Bytes. Dropping packet immediately.
```

![Bad Magic Spoofing Test](./docs/Bad%20Magic%20%28Spoofing%29.png)

### Tampering Test: Bad Signature

A packet with an invalid or corrupted signature is rejected at the ECDSA verification stage.

```text
[*] OrbitSec Firmware Decoder Initializing...
[+] Parsed Packet: Payload=64 bytes, Signature=70 bytes.
[*] Gatekeeper: Verifying ECDSA Signature against raw ciphertext...
[-] Fatal: OpenSSL internal verification error.
```

![Bad Signature Tampering Test](./docs/Bad%20Signature%20%28Tampering%29.png)

### Denial-of-Service Test: Oversized Payload

An oversized payload is rejected before unsafe processing.

```text
[*] OrbitSec Firmware Decoder Initializing...
[-] Fatal: Packet lengths exceed buffer limits. Dropping to prevent overflow.
```

![Oversized Payload DoS Test](./docs/Oversized%20Payload%20%28Denial%20of%20Service%29.png)

---

## Reproducing the Baseline Test

From the repository root:

```bash
python3 uplink/encrypt_and_sign.py
cd firmware
make clean
make
./orbitsec_decoder
```

Expected result: the firmware decoder parses the generated packet, verifies the ECDSA signature, and proceeds to AES-256-CBC decryption only after the gatekeeper check passes.

For additional setup and testing details, see `INSTRUCTIONS.md`.

---

## Documentation

Detailed project documentation is available in the `docs/` directory:

* [Final Project Report](./docs/OrbitSec%20Final%20Project%20Report.pdf)
* [Project Specifications](./docs/OrbitSec%20Project%20Specifications.pdf)
* [Functional and Security Requirements](./docs/OrbitSec%20Functional%20and%20Security%20Requirements.pdf)
* [STRIDE Threat Model](./docs/STRIDE%20Threat%20Model.pdf)
* [Encrypt-then-Sign Python Sequence PDF](./docs/Encrypt-then-Sign%20%28Python%29.pdf)
* [Verify-then-Decrypt C Flow PDF](./docs/Verify-then-Decrypt%20%28C%29.pdf)

---

## Academic Context

* **Course:** CY 510 - Information Security and Assurance
* **Institution:** Southeast Missouri State University
* **Timeline:** April-May 2026
* **Group:** 404: Group Not Found

### Team Members

* Tarique Chowdhury
* Cali Facio
* Hayden Blue
* Jordan Duenas
* LaBrea Franklin
* Tinotenda Mukumba

### Role and Contribution

This was completed as a group academic project. My primary role was technical lead and integration owner, with responsibility for the core security architecture, Python uplink, C firmware gatekeeper, fuzzing workflow, repository organization, documentation, and live demonstration.

Team members contributed to the final presentation, architecture visuals, review, and project delivery. The completed repository reflects the integrated final artifact submitted for the course.

---

## Project Status

**Academic Project Complete — April-May 2026**

The completed class project demonstrates a functional secure communication workflow:

* Python uplink generates encrypted and signed packets
* C firmware decoder parses packet structure and validates input
* ECDSA verification occurs before AES decryption
* Malformed packets are rejected through controlled failure paths
* Fuzzing and attack-case testing validate defensive behavior against representative spoofing, tampering, and oversized-payload scenarios

The repository is preserved as a completed academic security engineering project and may be expanded after completion of thesis work.

---

## Future Work

Potential future improvements include:

* Expanding hardware-in-the-loop testing with physical embedded targets
* Adding additional malformed-packet and adversarial fuzzing cases
* Improving test key lifecycle handling for controlled lab environments
* Evaluating authenticated encryption alternatives such as AES-GCM or ChaCha20-Poly1305
* Adding CI-based testing for the Python uplink and C decoder
* Extending the architecture toward a more complete secure embedded communication framework

---

## Security Notice

OrbitSec is an academic prototype and portfolio project. It is not intended to be used as a production cryptographic library or deployed security product.

The repository should not contain real private keys, production secrets, or sensitive deployment artifacts. Any included keys, packets, or cryptographic materials should be treated as disposable test data.

---

## Author

**Tarique Chowdhury**
M.S. Cybersecurity Candidate
Southeast Missouri State University

---

## License

This project is licensed under the MIT License.
