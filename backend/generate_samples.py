"""
Generates high-quality synthetic and realistic test audio samples (.wav)
for live demonstration and testing of VoiceShield-AI (SIH26104).
"""

import os
import numpy as np
from scipy.io import wavfile

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(SAMPLE_DIR, exist_ok=True)


def generate_test_samples():
    sample_rate = 16000
    duration = 3.0  # 3 seconds
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # 1. Authentic Human Voice Simulation (Natural micro-jitter, warm harmonics, natural decay)
    f0 = 135.0  # Fundamental pitch ~135 Hz
    # Add natural biological pitch jitter (1.2% micro-perturbation)
    jitter = 0.012 * np.sin(2 * np.pi * 5 * t) + 0.005 * np.sin(2 * np.pi * 12 * t)
    pitch_mod = f0 * (1 + jitter)
    phase = 2 * np.pi * np.cumsum(pitch_mod) / sample_rate

    # Natural vocal harmonics (Formants F1, F2, F3)
    human_voice = (
        1.0 * np.sin(phase) +
        0.6 * np.sin(2 * phase) +
        0.35 * np.sin(3 * phase) +
        0.2 * np.sin(4 * phase) +
        0.1 * np.sin(5 * phase)
    )
    # Biological amplitude shimmer modulation
    shimmer = 0.9 + 0.1 * np.sin(2 * np.pi * 3 * t)
    human_voice = human_voice * shimmer
    # Natural breathy noise
    noise = np.random.normal(0, 0.02, len(t))
    human_voice = human_voice + noise
    human_voice = human_voice / np.max(np.abs(human_voice)) * 0.9
    human_wav = (human_voice * 32767).astype(np.int16)

    human_path = os.path.join(SAMPLE_DIR, "authentic_human_sample.wav")
    wavfile.write(human_path, sample_rate, human_wav)
    print(f"[OK] Generated Authentic Voice Sample: {human_path}")

    # 2. AI Cloned / Neural Vocoder Deepfake Voice Simulation (HiFi-GAN / VALL-E clone signature)
    # Mathematical rigid harmonic structure, near-zero natural jitter (0.05%), high vocoder cutoff
    f0_clone = 140.0
    # Almost zero natural jitter
    clone_phase = 2 * np.pi * f0_clone * t
    cloned_voice = (
        1.0 * np.sin(clone_phase) +
        0.7 * np.sin(2 * clone_phase) +
        0.5 * np.sin(3 * clone_phase) +
        0.3 * np.sin(4 * clone_phase)
    )
    # Neural vocoder artifact: steep high-frequency truncation and synthetic phase buzz
    synthetic_buzz = 0.04 * np.sin(2 * np.pi * 7800 * t)
    cloned_voice = cloned_voice + synthetic_buzz
    # Rigid amplitude (lacking biological breathing modulation)
    cloned_voice = cloned_voice / np.max(np.abs(cloned_voice)) * 0.95
    cloned_wav = (cloned_voice * 32767).astype(np.int16)

    cloned_path = os.path.join(SAMPLE_DIR, "ai_cloned_impersonation_sample.wav")
    wavfile.write(cloned_path, sample_rate, cloned_wav)
    print(f"[OK] Generated AI-Cloned Attack Sample: {cloned_path}")

    # 3. Suspicious / Voice-Converted (RVC/DiffWave) Sample
    f0_suspicious = 180.0
    # Over-exaggerated phase discontinuity jitter (>5.2%)
    erratic_jitter = 0.06 * np.sin(2 * np.pi * 45 * t)
    susp_phase = 2 * np.pi * np.cumsum(f0_suspicious * (1 + erratic_jitter)) / sample_rate
    suspicious_voice = (
        0.9 * np.sin(susp_phase) +
        0.4 * np.sin(2 * susp_phase) +
        0.05 * np.random.normal(0, 0.1, len(t))
    )
    suspicious_voice = suspicious_voice / np.max(np.abs(suspicious_voice)) * 0.9
    suspicious_wav = (suspicious_voice * 32767).astype(np.int16)

    suspicious_path = os.path.join(SAMPLE_DIR, "suspicious_neural_tts_sample.wav")
    wavfile.write(suspicious_path, sample_rate, suspicious_wav)
    print(f"[OK] Generated Suspicious TTS Sample: {suspicious_path}")


if __name__ == "__main__":
    generate_test_samples()
