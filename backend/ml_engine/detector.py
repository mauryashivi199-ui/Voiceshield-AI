"""
AI-Powered Real-Time Voice Cloning Detection & Forensic Classification Engine
Combines Multi-spectral Analysis, Biophysical Liveness, and Vocoder Artifact Checks.
"""

import hashlib
import time
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from .feature_extractor import AudioFeatureExtractor


class DeepfakeVoiceDetector:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.extractor = AudioFeatureExtractor(sample_rate=sample_rate)

    def analyze_audio_chunk(self, audio_array: np.ndarray, caller_id: str = "Unknown Caller") -> Dict[str, Any]:
        """
        Analyzes a chunk of audio (e.g. 500ms - 3s) in real-time.
        Returns detailed classification, risk score, and explainable forensics.
        """
        start_time = time.time()

        # Compute SHA-256 hash of raw audio buffer for blockchain evidence
        audio_bytes = audio_array.tobytes()
        audio_hash = hashlib.sha256(audio_bytes).hexdigest()

        # 1. Extract multi-dimensional acoustic & biological features
        feats = self.extractor.extract_features(audio_array)

        # 2. Multi-Vector Deepfake Scoring Engine
        scores, anomalies = self._compute_vector_scores(feats)

        # Weighted Ensemble Probability (0.0 to 100.0)
        # Weights: Vocoder Artifacts (35%), Biophysical Liveness (35%), Spectral Dynamics (30%)
        vocoder_score = scores["vocoder_artifact_score"]
        liveness_score = scores["biophysical_liveness_score"]
        spectral_score = scores["spectral_dynamics_score"]

        # Combined AI Clone Probability Score
        cloned_probability = (vocoder_score * 0.35) + (liveness_score * 0.35) + (spectral_score * 0.30)
        cloned_probability = max(1.2, min(99.4, cloned_probability))

        # 3. Determine Risk Classification & Automated Mitigation Actions
        if cloned_probability >= 75.0:
            classification = "CLONED_ATTACK"
            risk_level = "CRITICAL" if cloned_probability >= 88.0 else "HIGH"
            mitigation = "CALL_INTERCEPT_AND_ALERT"
            status = "BLOCKED"
        elif cloned_probability >= 45.0:
            classification = "SUSPICIOUS_VOICE"
            risk_level = "MEDIUM"
            mitigation = "WARN_USER_OTP_CHALLENGE"
            status = "FLAGGED"
        else:
            classification = "AUTHENTIC_VOICE"
            risk_level = "LOW"
            mitigation = "SAFE_ALLOW_STREAM"
            status = "VERIFIED"

        latency_ms = round((time.time() - start_time) * 1000, 2)

        incident_id = f"INC-{int(time.time()*1000)}-{audio_hash[:6].upper()}"

        return {
            "incident_id": incident_id,
            "timestamp": time.time(),
            "caller_id": caller_id,
            "confidence_score": round(cloned_probability, 1),
            "classification": classification,
            "risk_level": risk_level,
            "status": status,
            "mitigation_action": mitigation,
            "latency_ms": latency_ms,
            "audio_hash": audio_hash,
            "forensics": {
                "detected_anomalies": anomalies,
                "acoustic_features": feats,
                "vector_breakdown": {
                    "vocoder_artifacts": round(vocoder_score, 1),
                    "biophysical_liveness_anomaly": round(liveness_score, 1),
                    "spectral_distortion": round(spectral_score, 1)
                }
            }
        }

    def _compute_vector_scores(self, feats: Dict[str, Any]) -> Tuple[Dict[str, float], List[str]]:
        """
        Evaluates heuristic and spectral markers against standard synthetic voice profiles.
        """
        anomalies = []

        jitter = feats.get("pitch_jitter_pct", 1.0)
        shimmer = feats.get("amplitude_shimmer_pct", 3.0)
        flatness = feats.get("spectral_flatness", 0.001)
        hf_energy = feats.get("high_freq_energy_ratio", 0.01)
        centroid = feats.get("spectral_centroid_hz", 1500)
        harmonics = feats.get("harmonics_regularity_ratio", 0.5)

        # Vector 1: Biophysical Liveness & Micro-Perturbation (Natural Vocal Fold Jitter: 0.5% - 2.8%)
        # AI clones often have near-zero jitter (over-smoothed) or erratic phase jitter (>4.0%)
        liveness_score = 15.0
        if jitter < 0.25:
            liveness_score += 65.0
            anomalies.append(f"Unnaturally smooth vocal pitch jitter ({jitter}% < 0.25% threshold) indicates mathematical synthesis")
        elif jitter > 4.5:
            liveness_score += 55.0
            anomalies.append(f"Excessive pitch micro-instability ({jitter}% > 4.5%) indicates neural vocoder phase discontinuity")

        if shimmer < 0.8:
            liveness_score += 20.0
            anomalies.append(f"Sub-biological amplitude shimmer ({shimmer}%), lacking natural respiratory modulation")

        # Vector 2: Synthetic Vocoder Artifacts (HiFi-GAN, MelGAN, DiffWave, Tacotron)
        vocoder_score = 10.0
        if hf_energy < 0.0005 and centroid > 800:
            vocoder_score += 60.0
            anomalies.append(f"Sharp high-frequency spectral cutoff (>7.5kHz attenuation: {hf_energy}) typical of 16kHz/22kHz neural vocoders")

        if flatness > 0.008:
            vocoder_score += 30.0
            anomalies.append(f"Elevated spectral flatness ({flatness}) indicative of neural reconstruction noise floor")

        # Vector 3: Spectral Dynamics & Harmonic Regularity
        spectral_score = 10.0
        if harmonics > 0.85:
            spectral_score += 50.0
            anomalies.append(f"Overly rigid harmonic distribution (Ratio: {harmonics}), characteristic of cloned formant transfer")
        elif harmonics < 0.15 and feats.get("rms_energy", 0) > 0.05:
            spectral_score += 40.0
            anomalies.append(f"Degraded harmonic structure, indicative of low-bitrate neural audio codec")

        # Clamp all vector scores to 0-100
        scores = {
            "vocoder_artifact_score": max(5.0, min(99.0, vocoder_score)),
            "biophysical_liveness_score": max(5.0, min(99.0, liveness_score)),
            "spectral_dynamics_score": max(5.0, min(99.0, spectral_score))
        }

        return scores, anomalies


detector = DeepfakeVoiceDetector()
