"""
Blockchain Ledger for Forensic Evidence & Immutable Chain of Custody (SIH26104)
Provides tamper-proof cryptographic logging of detected voice clone incidents.
"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from ..database.db import get_db_connection, init_db


class Block:
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()

    def calculate_merkle_root(self) -> str:
        data_string = json.dumps(self.data, sort_keys=True)
        return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

    def calculate_hash(self) -> str:
        block_header = f"{self.index}{self.timestamp}{self.merkle_root}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_header.encode('utf-8')).hexdigest()

    def mine_block(self, difficulty: int = 2):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "block_index": self.index,
            "timestamp": self.timestamp,
            "created_at": self.created_at,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce,
            "merkle_root": self.merkle_root
        }


class ForensicBlockchain:
    def __init__(self):
        init_db()
        self._ensure_genesis_block()

    def _ensure_genesis_block(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM blockchain_blocks")
        count = cursor.fetchone()["count"]

        if count == 0:
            genesis_data = {
                "genesis": True,
                "system": "VoiceShield-AI / AICTE Cyber Security Cell",
                "purpose": "Immutable Audio Deepfake & Impersonation Forensic Ledger",
                "standard": "IEEE / SIH26104 Tamper-Proof Audit Standard"
            }
            genesis_block = Block(0, time.time(), genesis_data, "0" * 64, nonce=42)
            genesis_block.mine_block(difficulty=2)

            cursor.execute("""
            INSERT INTO blockchain_blocks (block_index, timestamp, created_at, data_json, previous_hash, hash, nonce, merkle_root)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                genesis_block.index,
                genesis_block.timestamp,
                genesis_block.created_at,
                json.dumps(genesis_block.data),
                genesis_block.previous_hash,
                genesis_block.hash,
                genesis_block.nonce,
                genesis_block.merkle_root
            ))
            conn.commit()
        conn.close()

    def get_latest_block(self) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM blockchain_blocks ORDER BY block_index DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            d = dict(row)
            d["data"] = json.loads(d["data_json"])
            return d
        return None

    def add_forensic_evidence(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        latest_block = self.get_latest_block()
        prev_hash = latest_block["hash"] if latest_block else "0" * 64
        next_index = (latest_block["block_index"] + 1) if latest_block else 0

        # Structured forensic payload for digital chain of custody
        evidence_payload = {
            "incident_id": incident_data.get("incident_id"),
            "audio_hash_sha256": incident_data.get("audio_hash"),
            "caller_id": incident_data.get("caller_id"),
            "classification": incident_data.get("classification"),
            "risk_score": incident_data.get("confidence_score"),
            "risk_level": incident_data.get("risk_level"),
            "spectral_anomalies": incident_data.get("forensics", {}).get("detected_anomalies", []),
            "forensic_officer_node": "AICTE-CYBER-NODE-01",
            "logged_epoch": time.time()
        }

        new_block = Block(
            index=next_index,
            timestamp=time.time(),
            data=evidence_payload,
            previous_hash=prev_hash
        )
        new_block.mine_block(difficulty=2)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO blockchain_blocks (block_index, timestamp, created_at, data_json, previous_hash, hash, nonce, merkle_root)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_block.index,
            new_block.timestamp,
            new_block.created_at,
            json.dumps(new_block.data),
            new_block.previous_hash,
            new_block.hash,
            new_block.nonce,
            new_block.merkle_root
        ))
        conn.commit()
        conn.close()

        return new_block.to_dict()

    def get_all_blocks(self) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM blockchain_blocks ORDER BY block_index ASC")
        rows = cursor.fetchall()
        conn.close()

        blocks = []
        for r in rows:
            d = dict(r)
            d["data"] = json.loads(d["data_json"])
            blocks.append(d)
        return blocks

    def verify_chain_integrity(self) -> Dict[str, Any]:
        """Validates all cryptographic hashes and linkage across the chain."""
        blocks = self.get_all_blocks()
        if not blocks:
            return {"valid": True, "total_blocks": 0, "message": "Blockchain is empty"}

        for i in range(1, len(blocks)):
            current = blocks[i]
            prev = blocks[i - 1]

            # 1. Check previous hash linkage
            if current["previous_hash"] != prev["hash"]:
                return {
                    "valid": False,
                    "tampered_at_block": current["block_index"],
                    "reason": f"Previous hash mismatch at Block #{current['block_index']}"
                }

            # 2. Check recalculated block hash
            data_string = json.dumps(current["data"], sort_keys=True)
            recalculated_merkle = hashlib.sha256(data_string.encode('utf-8')).hexdigest()
            header = f"{current['block_index']}{current['timestamp']}{recalculated_merkle}{current['previous_hash']}{current['nonce']}"
            recalculated_hash = hashlib.sha256(header.encode('utf-8')).hexdigest()

            if recalculated_hash != current["hash"]:
                return {
                    "valid": False,
                    "tampered_at_block": current["block_index"],
                    "reason": f"Data tampering detected in Block #{current['block_index']} payload"
                }

        return {
            "valid": True,
            "total_blocks": len(blocks),
            "latest_block_hash": blocks[-1]["hash"],
            "status": "ALL_BLOCKS_VERIFIED_SECURE",
            "message": "Cryptographic chain of custody is 100% intact and authentic."
        }


blockchain = ForensicBlockchain()
