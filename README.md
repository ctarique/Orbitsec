# OrbitSec: High-Assurance Cryptographic Bridge

**OrbitSec** is a secure communication framework that uses a **Verify-then-Decrypt** paradigm to protect low-power devices from memory-based attacks. 

### Overview
The system consists of a Python-based sender that encrypts data and applies a digital signature, and a C-based receiver that acts as a gatekeeper. By validating the signature before ever touching the encrypted content, the system can instantly drop tampered or malicious data. This prevents the device from ever processing "poisoned" inputs that could cause a crash or buffer overflow. To prove its resilience, the project includes a fuzzer to bombard the system with garbage data and demonstrate that the gatekeeper remains stable under active attack.

### Key Features
* **Verify-then-Decrypt Architecture:** Implements a security gate where ECDSA signatures are validated before the AES decryption engine is ever initialized.
* **Memory-Safe Firmware:** Developed in C with a focus on preventing buffer overflows and ensuring a clean memory state.
* **Hybrid Cryptography:** Combines AES-256-CBC for data confidentiality with ECDSA P-256 for authenticity and non-repudiation.
* **Automated Fuzzing:** Includes a Python fuzzer designed to stress-test the C firmware’s error handling through bit-flipping and data truncation.

### Academic Context
* **Course:** CY 510 - Information Security and Assurance
* **Institution:** Southeast Missouri State University
* **Group:** 404: Group Not Found
* **Team Members:**
  * Tarique Chowdhury (Project Lead)
  * Cali Facio
  * Hayden Blue
  * Jordan Duenas
  * LaBrea Franklin
  * Tinotenda Mukumba

### Current Project Status: Phase 1 Complete
The baseline cryptographic handshake is fully functional. The Python uplink successfully generates signed, encrypted packets that are validated by the C firmware.

**Handshake Validation:**
![Baseline Handshake](docs/baseline_handshake.png)