# OrbitSec: High-Assurance Cryptographic Bridge

**OrbitSec** is a secure communication prototype for resource-constrained embedded systems. The project uses a **Verify-then-Decrypt** design so the receiver validates packet authenticity before initializing the AES decryption path or processing untrusted payload data.

---

## Overview

The system consists of a Python-based uplink that encrypts data and applies an ECDSA digital signature, and a C-based firmware decoder that acts as a gatekeeper. By validating the signature before decryption, the receiver can reject tampered or malformed packets before they reach the protected payload-processing path.

OrbitSec was developed as an academic security engineering project focused on embedded communication, cryptographic packet validation, threat modeling, and defensive firmware design.

---

## Repository Structure

* **`firmware/`**: C implementation of the secure decoder and gatekeeper logic
* **`uplink/`**: Python scripts for encryption, SHA-256 hashing, ECDSA signing, and packet generation
* **`testing/`**: Automated fuzzing and malformed-packet validation scripts
* **`docs/`**: Project documentation, threat model, architecture diagrams, and visual assets
* **`requirements.txt`**: Python dependencies for the uplink and testing tools

Generated cryptographic artifacts such as keys, IVs, and binary packets should be treated as local test artifacts and excluded from production use.

---

## Documentation

Detailed project specifications and security analysis are available in the `/docs` folder:

* [Functional and Security Requirements](./docs/Functional%20and%20Security%20Requirements.pdf)
* [STRIDE Threat Model](./docs/STRIDE%20Threat%20Model.pdf)

---

## Key Features

* **Verify-then-Decrypt Architecture:** Validates ECDSA signatures before the AES decryption path is initialized.
* **Defensive Firmware Design:** Implements strict packet parsing, bounds-aware validation, and controlled failure behavior in C.
* **Hybrid Cryptographic Workflow:** Combines AES-256-CBC for confidentiality with ECDSA P-256 signatures for authenticity and integrity.
* **Threat-Model-Driven Design:** Uses STRIDE analysis to evaluate spoofing, tampering, denial-of-service, and information disclosure risks.
* **Fuzz Testing:** Uses malformed packet injection to test decoder stability and rejection behavior under adversarial input.

---

## Security Posture

OrbitSec is designed to mitigate high-priority threats identified during the STRIDE analysis:

* **Spoofing and Tampering:** Mitigated through ECDSA P-256 signature verification before decryption.
* **Unsafe Payload Processing:** Reduced by rejecting unauthenticated packets before entering the decryption and payload-handling path.
* **Denial-of-Service Pressure:** Reduced through early-exit validation and strict packet size checks.
* **Information Disclosure:** Addressed through AES-256-CBC encryption for protected payload data.

---

## Academic Context

* **Course:** CY 510 - Information Security and Assurance
* **Institution:** Southeast Missouri State University
* **Group:** 404: Group Not Found
* **Team Members:** Tarique Chowdhury (Lead), Cali Facio, Hayden Blue, Jordan Duenas, LaBrea Franklin, Tinotenda Mukumba

---

## Current Project Status

**Phase 1 Complete**

The baseline cryptographic handshake is functional. The Python uplink generates signed, encrypted packets that are validated by the C firmware decoder before decryption.

### Handshake Validation Log

```text
[*] OrbitSec Firmware Decoder Initializing...
[+] Parsed Packet: Payload=80 bytes, Signature=70 bytes.
[*] Gatekeeper: Verifying ECDSA Signature against raw ciphertext...
[+] SUCCESS: Cryptographic signature validated.
[+] Gatekeeper passed. Proceeding to AES-256 decryption engine...
```

![Baseline Handshake](https://raw.githubusercontent.com/ctarique/orbitsec/main/docs/baseline_handshake.png)

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
