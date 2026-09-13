# SIH26104 — Official Presentation Pitch Deck

## Slide 1: Title Slide
- **Project Title:** VoiceShield-AI — Autonomous Real-Time Voice Cloning Detection & Prevention
- **Problem Statement ID:** SIH26104
- **Organization:** AICTE – Cyber Security Cell
- **Theme:** Blockchain & Cybersecurity
- **Team Name & Members:** [Your Team Name / Leader / Members]

---

## Slide 2: The Problem — The Surge of Voice Cloning Cybercrime
- **The Threat:** Generative AI allows attackers to clone any human voice with just 3 seconds of reference audio.
- **Critical Attack Vectors:**
  - CEO fraud & unauthorized corporate financial wire transfers.
  - Emergency extortion calls to vulnerable families.
  - Banking customer support & biometric voice bypass.
- **The Gap:** Existing solutions take 3+ seconds to analyze, lack court-admissible evidence, and have high false positives.

---

## Slide 3: Our Solution — VoiceShield-AI
- **Real-Time Defense:** $<200\text{ ms}$ ultra-low latency detection on live telephone/VoIP streams.
- **Multi-Vector Acoustic & Biophysical Inspection:** Evaluates vocal cord micro-jitter, amplitude shimmer, Wiener spectral entropy, and high-frequency vocoder phase artifacts.
- **Autonomous Mitigation:** Real-time caller alert overlay, automated call interception/muting, and biometric challenge triggers.
- **Blockchain Evidence Ledger:** Immutable, cryptographically verifiable chain of custody for law enforcement and AICTE cyber crime investigations.

---

## Slide 4: Real-Time Detection Engine (Acoustic + Bio-Liveness)
- **Biophysical Vocal Liveness:** Human vocal folds exhibit involuntary micro-tremors ($0.5\% \le \text{Jitter} \le 2.5\%$). Neural synthesizers are either unnaturally smooth or exhibit erratic phase spikes.
- **Neural Vocoder Cutoff Inspection:** Detects steep spectral roll-offs above 7.5 kHz typical of diffusion and HiFi-GAN vocoders.
- **Explainable AI (XAI):** Provides human-interpretable diagnostics rather than a black-box percentage.

---

## Slide 5: Blockchain Forensic Ledger (Theme Compliance)
- Every detected attack generates a cryptographically sealed block.
- **Stored Data:** Audio SHA-256 hash, caller ID, timestamp, acoustic anomalies, and validator signature.
- **1-Click Forensic Certificate:** Generates tamper-proof PDF reports compliant with the Indian Evidence Act for fast police FIR filing.

---

## Slide 6: System Architecture & Data Flow
- **Ingestion:** WebSockets audio stream chunks (500ms).
- **Processing Layer:** Pure Python FFT & DSP feature extraction + Multi-Vector Ensemble scoring.
- **Storage Layer:** SQLite 3 ACID relational store + SHA-256 Merkle Blockchain Ledger.
- **UI / Dashboard:** Cyber Defense Command Center with live oscilloscope and real-time threat meter.

---

## Slide 7: Innovation & Key USPs
1. **Sub-200ms Latency:** 10x faster than traditional batch audio models.
2. **Blockchain Proof-of-Custody:** First voice security system with court-admissible immutable evidence.
3. **Hardware Agnostic:** Runs on standard CPU/server instances without requiring multi-GPU clusters.
4. **Explainable Diagnostics (XAI):** Detailed acoustic metrics provided for each flagged call.

---

## Slide 8: Live Demonstration & Workflow
- **Live Mic Streaming:** Normal speech speaks -> Immediate "Authentic Human Voice" green shield.
- **Simulated Neural Attack:** Injects cloned audio -> Real-time red alert, call intercept trigger, and block # auto-minted on blockchain.
- **Blockchain Explorer:** Live cryptographic verification showing 100% chain integrity.

---

## Slide 9: Technology Stack & Feasibility
- **Backend:** Python 3, FastAPI, NumPy, SciPy, WebSockets, Uvicorn
- **Database:** SQLite 3
- **Blockchain:** SHA-256 Merkle Chain with PoW block validation
- **Frontend:** Tailwind CSS, HTML5 Canvas Oscilloscope, Chart.js

---

## Slide 10: Scalability, Impact & Future Roadmap
- **Telecom & VoIP Integration:** Gateway plugin for Asterisk, Twilio, FreeSWITCH, and WhatsApp/Telegram VoIP.
- **Commercialization:** SaaS API for banking call centers, fintech apps, and enterprise security.
- **Future Roadmap:** Multi-language phonetic support, distributed Hyperledger blockchain nodes.
