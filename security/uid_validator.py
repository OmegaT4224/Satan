"""
UID Validator
Validates ALC-ROOT-1010-1111-XCOV∞ verification
"""
import re
import hashlib
import datetime
from typing import Dict, Any, List, Optional


class UIDValidator:
    """Validates and manages VIOLET-AF UID authentication"""
    
    def __init__(self):
        self.master_uid = "ALC-ROOT-1010-1111-XCOV∞"
        self.validation_log = []
        self.authorized_uids = [self.master_uid]
        
    def validate_uid(self, uid: str) -> bool:
        """Validate UID against VIOLET-AF specifications"""
        self.validation_log.append(f"🔐 UID validation started for: {uid}")
        
        # Check exact match with master UID
        if uid != self.master_uid:
            self.validation_log.append("❌ UID does not match master pattern")
            return False
            
        # Validate UID structure
        if not self._validate_uid_structure(uid):
            self.validation_log.append("❌ UID structure validation failed")
            return False
            
        # Check UID authorization
        if uid not in self.authorized_uids:
            self.validation_log.append("❌ UID not in authorized list")
            return False
            
        self.validation_log.append("✅ UID validation successful")
        return True
        
    def _validate_uid_structure(self, uid: str) -> bool:
        """Validate UID follows correct structure pattern"""
        # Pattern: ALC-ROOT-XXXX-XXXX-XCOV∞
        pattern = r"^ALC-ROOT-\d{4}-\d{4}-XCOV∞$"
        
        if not re.match(pattern, uid):
            return False
            
        # Additional checks for specific values
        parts = uid.split('-')
        if len(parts) != 5:  # Changed from 4 to 5: ['ALC', 'ROOT', '1010', '1111', 'XCOV∞']
            return False
            
        # Check specific component values
        if parts[0] != "ALC":
            return False
        if parts[1] != "ROOT":
            return False
        if parts[2] != "1010":
            return False
        if parts[3] != "1111":
            return False
        if parts[4] != "XCOV∞":
            return False
            
        return True
        
    def generate_uid_hash(self, uid: str) -> str:
        """Generate cryptographic hash of UID for verification"""
        if not self.validate_uid(uid):
            raise ValueError("Invalid UID provided for hashing")
            
        # Create hash with timestamp for uniqueness
        timestamp = datetime.datetime.now().isoformat()
        hash_data = f"{uid}:{timestamp}:VIOLET-AF"
        
        return hashlib.sha256(hash_data.encode()).hexdigest()
        
    def verify_uid_hash(self, uid: str, uid_hash: str, timestamp: str) -> bool:
        """Verify UID hash matches expected value"""
        if not self.validate_uid(uid):
            return False
            
        # Recreate hash with provided timestamp
        hash_data = f"{uid}:{timestamp}:VIOLET-AF"
        expected_hash = hashlib.sha256(hash_data.encode()).hexdigest()
        
        return expected_hash == uid_hash
        
    def create_uid_token(self, uid: str, permissions: List[str] = None) -> Dict[str, Any]:
        """Create authentication token for UID"""
        if not self.validate_uid(uid):
            raise ValueError("Invalid UID for token creation")
            
        if permissions is None:
            permissions = ["quantum_execute", "state_read", "state_write", "security_admin"]
            
        timestamp = datetime.datetime.now().isoformat()
        token_data = {
            "uid": uid,
            "permissions": permissions,
            "issued": timestamp,
            "issuer": "VIOLET-AF-SECURITY",
            "token_id": self._generate_token_id(uid, timestamp)
        }
        
        # Create token signature
        token_string = f"{uid}:{timestamp}:{':'.join(permissions)}"
        token_data["signature"] = hashlib.sha256(token_string.encode()).hexdigest()
        
        return token_data
        
    def verify_uid_token(self, token: Dict[str, Any]) -> bool:
        """Verify UID authentication token"""
        try:
            uid = token.get("uid", "")
            timestamp = token.get("issued", "")
            permissions = token.get("permissions", [])
            signature = token.get("signature", "")
            
            # Validate UID
            if not self.validate_uid(uid):
                return False
                
            # Verify signature
            token_string = f"{uid}:{timestamp}:{':'.join(permissions)}"
            expected_signature = hashlib.sha256(token_string.encode()).hexdigest()
            
            return expected_signature == signature
            
        except Exception:
            return False
            
    def _generate_token_id(self, uid: str, timestamp: str) -> str:
        """Generate unique token ID"""
        token_data = f"{uid}:{timestamp}:TOKEN"
        return hashlib.md5(token_data.encode()).hexdigest()[:16]
        
    def authorize_uid(self, uid: str) -> bool:
        """Authorize a UID for VIOLET-AF operations"""
        if not self._validate_uid_structure(uid):
            self.validation_log.append(f"❌ Cannot authorize malformed UID: {uid}")
            return False
            
        if uid not in self.authorized_uids:
            self.authorized_uids.append(uid)
            self.validation_log.append(f"✅ UID authorized: {uid}")
            return True
            
        self.validation_log.append(f"ℹ️ UID already authorized: {uid}")
        return True
        
    def revoke_uid(self, uid: str) -> bool:
        """Revoke authorization for a UID"""
        if uid == self.master_uid:
            self.validation_log.append("❌ Cannot revoke master UID")
            return False
            
        if uid in self.authorized_uids:
            self.authorized_uids.remove(uid)
            self.validation_log.append(f"✅ UID authorization revoked: {uid}")
            return True
            
        self.validation_log.append(f"ℹ️ UID was not authorized: {uid}")
        return False
        
    def list_authorized_uids(self) -> List[str]:
        """List all authorized UIDs"""
        return self.authorized_uids.copy()
        
    def get_uid_info(self, uid: str) -> Dict[str, Any]:
        """Get detailed information about a UID"""
        info = {
            "uid": uid,
            "valid_structure": self._validate_uid_structure(uid),
            "authorized": uid in self.authorized_uids,
            "is_master": uid == self.master_uid,
            "validation_timestamp": datetime.datetime.now().isoformat()
        }
        
        if info["valid_structure"]:
            parts = uid.split('-')
            info["components"] = {
                "prefix": parts[0],
                "root": parts[1],
                "sequence1": parts[2],
                "sequence2": parts[3] if len(parts) > 3 else None,
                "suffix": uid.split('-')[-1]
            }
            
        return info
        
    def get_validation_log(self) -> List[str]:
        """Get UID validation log"""
        return self.validation_log.copy()
        
    def clear_validation_log(self) -> None:
        """Clear validation log"""
        self.validation_log.clear()
        
    def emergency_reset(self) -> Dict[str, Any]:
        """Emergency reset of UID authorization system"""
        self.validation_log.append("🚨 EMERGENCY UID RESET INITIATED")
        
        # Reset to master UID only
        old_count = len(self.authorized_uids)
        self.authorized_uids = [self.master_uid]
        self.validation_log.clear()
        
        reset_info = {
            "reset_timestamp": datetime.datetime.now().isoformat(),
            "previous_uid_count": old_count,
            "current_uid_count": len(self.authorized_uids),
            "master_uid": self.master_uid,
            "emergency_reset": True
        }
        
        self.validation_log.append("✅ Emergency reset completed")
        return reset_info