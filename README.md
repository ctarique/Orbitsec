# OrbitSec: High-Assurance Cryptographic Bridge

**OrbitSec** is a secure communication framework that uses a **Verify-then-Decrypt** paradigm to protect low-power devices from memory-based attacks. 

### Overview
[cite_start]The system consists of a Python-based sender that encrypts data and applies a digital signature, and a C-based receiver that acts as a gatekeeper[cite: 5, 13]. [cite_start]By validating the signature before ever touching the encrypted content, the system can instantly drop tampered or malicious data[cite: 6, 22]. 

### Repository Structure
* **`firmware/`**: C implementation of the secure decoder and "Gatekeeper" logic.
* **`uplink/`**: Python scripts for data encryption, SHA-256 hashing, and ECDSA signing.
* **`data/`**: Storage for cryptographic artifacts (keys, IVs, and binary packets).
* **`docs/`**: Official project documentation and visual assets.
* **`testing/`**: Home for the automated fuzzer and performance benchmarking scripts.

### Documentation
Detailed project specifications and risk analyses are available in the `/docs` folder:
* [Functional and Security Requirements](./docs/Functional%20and%20Security%20Requirements.pdf)
* [STRIDE Threat Model](./docs/STRIDE%20Threat%20Model.pdf)

### Key Features
* [cite_start]**Verify-then-Decrypt Architecture:** Implements a security gate where ECDSA signatures are validated before the AES decryption engine is ever initialized[cite: 7, 28].
* [cite_start]**Memory-Safe Firmware:** Developed in C with a focus on preventing buffer overflows and ensuring a clean memory state[cite: 7, 44].
* [cite_start]**Hybrid Cryptography:** Combines AES-256-CBC for data confidentiality with ECDSA P-256 for authenticity and non-repudiation[cite: 7, 41].

### Security Posture
The architecture is designed to mitigate high-priority threats identified in our STRIDE analysis:
* [cite_start]**Spoofing & Tampering**: Mitigated via ECDSA P-256 digital signatures[cite: 7].
* [cite_start]**Denial of Service**: Mitigated through early-exit signature validation and strict memory bounds checking[cite: 7, 8].
* [cite_start]**Information Disclosure**: Secured via AES-256-CBC encryption[cite: 8].

### Academic Context
* **Course:** CY510-01 - Information Security and Assurance
* **Institution:** Southeast Missouri State University
  **Instructor:** Dr. George Li
* **Group:** 404: Group Not Found
* [cite_start]**Team Members:** Tarique Chowdhury (Lead), Cali Facio, Hayden Blue, Jordan Duenas, LaBrea Franklin, Tinotenda Mukumba[cite: 3, 11].

### Current Project Status: Phase 1 Complete
The baseline cryptographic handshake is fully functional. The Python uplink successfully generates signed, encrypted packets that are validated by the C firmware.

**Handshake Validation Log:**
```text
[*] OrbitSec Firmware Decoder Initializing...
[+] Parsed Packet: Payload=80 bytes, Signature=70 bytes.
[*] Gatekeeper: Verifying ECDSA Signature against raw ciphertext...
[+] SUCCESS: Cryptographic signature validated.
[+] Gatekeeper passed. Proceeding to AES-256 decryption engine...