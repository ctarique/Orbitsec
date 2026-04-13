# OrbitSec: High-Assurance Cryptographic Bridge

**OrbitSec** is a secure data transfer protocol designed for communication between a high-level ground station (Python) and resource-constrained embedded firmware (C). This project focuses on implementing a "Verify-then-Decrypt" architecture to protect against unauthorized or malformed telemetry data.

### Academic Context
* **Course:** CY 510 - Information Security and Assurance
* **Institution:** Southeast Missouri State University
* **Group:** 404: Group Not Found
* **Project Lead:** Tarique Chowdhury

### Key Features
* **Memory-Safe Firmware:** Utilizes BSS-allocated buffers in C to prevent stack-based overflows and ensure a clean memory state on startup.
* **Verify-then-Decrypt Architecture:** Implements a security gate where ECDSA signatures are validated before the AES decryption engine is ever initialized.
* **Hybrid Cryptography:** Combines the speed of **AES-256-CBC** for data encryption with the non-repudiation of **ECDSA P-256** signatures.

### Current Project Status: Phase 1 Complete
The baseline cryptographic handshake is fully functional. The Python uplink can successfully generate signed, encrypted packets that are validated by the C firmware.

**Handshake Validation:**
![Baseline Handshake](docs/baseline_handshake.png)