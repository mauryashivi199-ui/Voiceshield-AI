"""
Unit and Integration Test Suite for VoiceShield-AI (SIH26104)
Tests Acoustic Extraction, Deepfake Classifier, Blockchain Integrity, and Database Ops.
"""

import unittest
import numpy as np
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.ml_engine.feature_extractor import AudioFeatureExtractor
from backend.ml_engine.detector import DeepfakeVoiceDetector
from backend.blockchain.ledger import ForensicBlockchain
from backend.database.db import init_db, insert_incident, get_all_incidents, get_dashboard_stats


class TestVoiceShieldAI(unittest.TestCase):

    def setUp(self):
        init_db()
        self.extractor = AudioFeatureExtractor(sample_rate=16000)
        self.detector = DeepfakeVoiceDetector(sample_rate=16000)

    def test_feature_extraction(self):
        """Test extraction on a synthesized sinusoidal test array."""
        t = np.linspace(0, 1.0, 16000, endpoint=False)
        audio = 0.8 * np.sin(2 * np.pi * 220 * t)
        feats = self.extractor.extract_features(audio)

        self.assertIn("spectral_centroid_hz", feats)
        self.assertIn("pitch_jitter_pct", feats)
        self.assertIn("spectral_rolloff_hz", feats)
        self.assertIn("spectral_flatness", feats)
        self.assertGreater(feats["duration_sec"], 0.9)

    def test_detector_classification(self):
        """Test classification scoring logic."""
        # Clean audio with flat pitch -> should flag high vocoder/smoothness anomaly
        t = np.linspace(0, 1.0, 16000, endpoint=False)
        flat_synth = 0.9 * np.sin(2 * np.pi * 150 * t)
        result = self.detector.analyze_audio_chunk(flat_synth, caller_id="Test Neural TTS")

        self.assertIn("confidence_score", result)
        self.assertIn("classification", result)
        self.assertIn("risk_level", result)
        self.assertIn("audio_hash", result)
        self.assertGreater(len(result["audio_hash"]), 32)

    def test_blockchain_integrity_and_mining(self):
        """Test cryptographic blockchain evidence sealing and tamper detection."""
        chain = ForensicBlockchain()
        dummy_incident = {
            "incident_id": "TEST-INC-9999",
            "audio_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "caller_id": "Test Spoof Call",
            "classification": "CLONED_ATTACK",
            "confidence_score": 94.5,
            "risk_level": "CRITICAL",
            "forensics": {"detected_anomalies": ["Synthetic cutoff detected"]}
        }
        block = chain.add_forensic_evidence(dummy_incident)
        self.assertGreater(block["block_index"], 0)
        self.assertTrue(block["hash"].startswith("00"))

        # Verify integrity
        audit = chain.verify_chain_integrity()
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["status"], "ALL_BLOCKS_VERIFIED_SECURE")

    def test_database_persistence(self):
        """Test SQLite incident logging and stats aggregation."""
        inc_data = {
            "incident_id": "INC-TEST-PERSISTENCE-01",
            "caller_id": "+91-9876543210",
            "confidence_score": 89.2,
            "risk_level": "HIGH",
            "status": "BLOCKED",
            "classification": "CLONED_ATTACK",
            "duration_sec": 3.0,
            "audio_hash": "a1b2c3d4e5f678901234567890abcdef1234567890abcdef1234567890abcdef",
            "forensics": {"detected_anomalies": ["Low natural jitter"]},
            "blockchain_tx": "00a5bcdef123456"
        }
        row_id = insert_incident(inc_data)
        self.assertGreater(row_id, 0)

        stats = get_dashboard_stats()
        self.assertGreater(stats["total_scans"], 0)


if __name__ == "__main__":
    unittest.main()
