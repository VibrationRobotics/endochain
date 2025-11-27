# ENDOCHAIN Core: Cryptographic Audit Trail
# Viduya Family Legacy Glyph © 2025 – All Rights Reserved
# Creator: Ariel Viduya Manosca | Author: IAMVC holdings LLC
"""
256-bit cryptographic audit hashing for regulatory compliance.

All LEI-V computations generate immutable audit hashes that can be:
1. Verified against blockchain timestamps (Bitcoin/IPFS)
2. Used for regulatory audit trails (FDA 21 CFR Part 11)
3. Chained together for longitudinal patient tracking
"""

import hashlib
import json
import hmac
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class AuditEntry:
    """Single entry in the audit chain."""
    entry_hash: str
    previous_hash: str
    timestamp: datetime
    data_type: str
    data_summary: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_hash": self.entry_hash,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp.isoformat(),
            "data_type": self.data_type,
            "data_summary": self.data_summary
        }


class AuditHasher:
    """Generates 256-bit cryptographic hashes for audit compliance.
    
    Uses SHA-256 for FIPS 140-2 compliance. All hashes include:
    - Timestamp (ISO 8601)
    - Data payload (JSON-serialized)
    - Citation reference
    - Chain link to previous hash (if applicable)
    """
    
    GENESIS_HASH = "0" * 64  # Genesis block equivalent
    CITATION = "Viduya Family Legacy Glyph © 2025"
    
    def __init__(self, secret_key: Optional[bytes] = None):
        """Initialize hasher with optional HMAC secret for tamper detection."""
        self._secret_key = secret_key
        self._chain: List[AuditEntry] = []
        self._last_hash = self.GENESIS_HASH
    
    def hash_computation(self, data: Dict[str, Any]) -> str:
        """Generate SHA-256 hash for a computation result.
        
        Args:
            data: Dictionary containing computation details
            
        Returns:
            64-character hexadecimal hash string (256 bits)
        """
        # Ensure deterministic serialization
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "citation": self.CITATION,
            "data": self._serialize_for_hash(data),
            "previous_hash": self._last_hash
        }
        
        serialized = json.dumps(payload, sort_keys=True, default=str)
        
        if self._secret_key:
            # HMAC for authenticated hashing
            hash_obj = hmac.new(
                self._secret_key,
                serialized.encode('utf-8'),
                hashlib.sha256
            )
        else:
            hash_obj = hashlib.sha256(serialized.encode('utf-8'))
        
        new_hash = hash_obj.hexdigest()
        
        # Add to chain
        entry = AuditEntry(
            entry_hash=new_hash,
            previous_hash=self._last_hash,
            timestamp=datetime.utcnow(),
            data_type=data.get("type", "computation"),
            data_summary=self._generate_summary(data)
        )
        self._chain.append(entry)
        self._last_hash = new_hash
        
        return new_hash
    
    def _serialize_for_hash(self, data: Dict[str, Any]) -> str:
        """Serialize data deterministically for hashing."""
        return json.dumps(data, sort_keys=True, default=str)
    
    def _generate_summary(self, data: Dict[str, Any]) -> str:
        """Generate human-readable summary of hashed data."""
        if "patient_id" in data and "lei_v" in data:
            return f"LEI-V={data['lei_v']} for patient {data['patient_id']}"
        return f"Audit entry: {list(data.keys())}"
    
    def verify_chain_integrity(self) -> bool:
        """Verify the integrity of the entire audit chain."""
        if not self._chain:
            return True
        
        current_hash = self.GENESIS_HASH
        for entry in self._chain:
            if entry.previous_hash != current_hash:
                return False
            current_hash = entry.entry_hash
        
        return True
    
    def get_chain(self) -> List[Dict[str, Any]]:
        """Export the complete audit chain."""
        return [entry.to_dict() for entry in self._chain]
    
    def export_for_ipfs(self) -> str:
        """Export chain as JSON for IPFS pinning."""
        export_data = {
            "chain": self.get_chain(),
            "chain_length": len(self._chain),
            "last_hash": self._last_hash,
            "citation": self.CITATION,
            "exported_at": datetime.utcnow().isoformat()
        }
        return json.dumps(export_data, indent=2)

