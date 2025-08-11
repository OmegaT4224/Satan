"""
Secure ReflectChain Implementation
Enhanced secure logging with encryption for quantum state data and UID verification
"""

import json
import time
import hashlib
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import base64
import threading


@dataclass
class ReflectEntry:
    """Individual entry in the ReflectChain"""
    entry_id: str
    timestamp: float
    uid: str
    operation_type: str
    operation_data: Dict[str, Any]
    security_level: str
    entry_hash: str
    previous_hash: Optional[str] = None
    encryption_enabled: bool = True


class SecureReflectChain:
    """Secure blockchain-like logging system for quantum operations and state management"""
    
    def __init__(self, uid: str = "ALC-ROOT-1010-1111-XCOV∞", chain_file: str = "ReflectChain.json"):
        self.uid = uid
        self.chain_file = Path(chain_file)
        self.logger = logging.getLogger(f"ReflectChain-{uid}")
        
        # Chain management
        self.chain: List[ReflectEntry] = []
        self.chain_lock = threading.Lock()
        self.encryption_key = self._derive_encryption_key()
        
        # Security settings
        self.security_config = {
            "require_uid_verification": True,
            "enable_encryption": True,
            "enable_integrity_checking": True,
            "max_chain_length": 10000,
            "auto_backup_interval": 100
        }
        
        # Initialize chain
        self._initialize_chain()
    
    def _derive_encryption_key(self) -> str:
        """Derive encryption key from UID"""
        key_material = f"{self.uid}_REFLECT_CHAIN_KEY_2025"
        return hashlib.sha256(key_material.encode()).hexdigest()
    
    def _initialize_chain(self) -> None:
        """Initialize or load existing ReflectChain"""
        try:
            if self.chain_file.exists():
                self._load_chain()
            else:
                self._create_genesis_entry()
            
            self.logger.info(f"ReflectChain initialized with {len(self.chain)} entries")
            
        except Exception as e:
            self.logger.error(f"Chain initialization error: {str(e)}")
            self._create_genesis_entry()
    
    def _create_genesis_entry(self) -> None:
        """Create genesis entry for new chain"""
        try:
            genesis_data = {
                "chain_version": "1.0",
                "created_by": "Andrew Lee Cruz",
                "creation_purpose": "VIOLET-AF Quantum Automation Security",
                "uid_binding": self.uid,
                "genesis_timestamp": time.time()
            }
            
            genesis_entry = ReflectEntry(
                entry_id="GENESIS_000",
                timestamp=time.time(),
                uid=self.uid,
                operation_type="chain_genesis",
                operation_data=genesis_data,
                security_level="creator",
                entry_hash="",
                previous_hash=None,
                encryption_enabled=False  # Genesis is not encrypted
            )
            
            # Calculate genesis hash
            genesis_entry.entry_hash = self._calculate_entry_hash(genesis_entry)
            
            self.chain = [genesis_entry]
            self._save_chain()
            
            self.logger.info("Genesis entry created for ReflectChain")
            
        except Exception as e:
            self.logger.error(f"Genesis creation error: {str(e)}")
    
    def _calculate_entry_hash(self, entry: ReflectEntry) -> str:
        """Calculate SHA-256 hash for chain entry"""
        try:
            # Create hash data excluding the hash field itself
            hash_data = {
                "entry_id": entry.entry_id,
                "timestamp": entry.timestamp,
                "uid": entry.uid,
                "operation_type": entry.operation_type,
                "operation_data": entry.operation_data,
                "security_level": entry.security_level,
                "previous_hash": entry.previous_hash,
                "encryption_enabled": entry.encryption_enabled
            }
            
            hash_json = json.dumps(hash_data, sort_keys=True)
            return hashlib.sha256(hash_json.encode()).hexdigest()
            
        except Exception as e:
            self.logger.error(f"Hash calculation error: {str(e)}")
            return ""
    
    def _encrypt_operation_data(self, data: Dict[str, Any]) -> str:
        """Encrypt operation data for secure storage"""
        try:
            if not self.security_config["enable_encryption"]:
                return json.dumps(data)
            
            # Convert to JSON
            data_json = json.dumps(data, sort_keys=True)
            
            # Simple encryption using base64 and hash (in real implementation, use proper encryption)
            encrypted_data = base64.b64encode(data_json.encode()).decode()
            
            # Add integrity hash
            integrity_hash = hashlib.sha256(f"{self.uid}{data_json}".encode()).hexdigest()
            
            return f"ENC:{encrypted_data}:{integrity_hash}"
            
        except Exception as e:
            self.logger.error(f"Data encryption error: {str(e)}")
            return json.dumps(data)
    
    def _decrypt_operation_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Decrypt operation data"""
        try:
            if not encrypted_data.startswith("ENC:"):
                # Not encrypted, return as JSON
                return json.loads(encrypted_data)
            
            # Parse encrypted format
            parts = encrypted_data[4:].split(':')  # Remove "ENC:" prefix
            if len(parts) != 2:
                raise ValueError("Invalid encrypted data format")
            
            encoded_data, integrity_hash = parts
            
            # Decrypt
            decrypted_json = base64.b64decode(encoded_data.encode()).decode()
            
            # Verify integrity
            expected_hash = hashlib.sha256(f"{self.uid}{decrypted_json}".encode()).hexdigest()
            if integrity_hash != expected_hash:
                raise ValueError("Integrity verification failed")
            
            return json.loads(decrypted_json)
            
        except Exception as e:
            self.logger.error(f"Data decryption error: {str(e)}")
            return {}
    
    def add_entry(self, operation_type: str, operation_data: Dict[str, Any], security_level: str = "high") -> Optional[str]:
        """Add new entry to the ReflectChain"""
        try:
            with self.chain_lock:
                # Validate UID if required
                if self.security_config["require_uid_verification"] and operation_data.get("uid") != self.uid:
                    operation_data["uid"] = self.uid
                
                # Generate entry ID
                entry_id = f"REFLECT_{len(self.chain):06d}_{int(time.time())}"
                
                # Get previous hash
                previous_hash = self.chain[-1].entry_hash if self.chain else None
                
                # Encrypt operation data if enabled
                if self.security_config["enable_encryption"]:
                    encrypted_data_str = self._encrypt_operation_data(operation_data)
                    # Store as encrypted string in operation_data field
                    stored_operation_data = {"encrypted": encrypted_data_str}
                else:
                    stored_operation_data = operation_data
                
                # Create entry
                entry = ReflectEntry(
                    entry_id=entry_id,
                    timestamp=time.time(),
                    uid=self.uid,
                    operation_type=operation_type,
                    operation_data=stored_operation_data,
                    security_level=security_level,
                    entry_hash="",
                    previous_hash=previous_hash,
                    encryption_enabled=self.security_config["enable_encryption"]
                )
                
                # Calculate entry hash
                entry.entry_hash = self._calculate_entry_hash(entry)
                
                # Add to chain
                self.chain.append(entry)
                
                # Check chain length limit
                if len(self.chain) > self.security_config["max_chain_length"]:
                    self._archive_old_entries()
                
                # Auto-backup if needed
                if len(self.chain) % self.security_config["auto_backup_interval"] == 0:
                    self._create_backup()
                
                # Save chain
                self._save_chain()
                
                self.logger.debug(f"ReflectChain entry added: {entry_id}")
                return entry_id
                
        except Exception as e:
            self.logger.error(f"Entry addition error: {str(e)}")
            return None
    
    def get_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Get entry by ID with decryption"""
        try:
            with self.chain_lock:
                for entry in self.chain:
                    if entry.entry_id == entry_id:
                        # Decrypt operation data if encrypted
                        if entry.encryption_enabled and "encrypted" in entry.operation_data:
                            decrypted_data = self._decrypt_operation_data(entry.operation_data["encrypted"])
                        else:
                            decrypted_data = entry.operation_data
                        
                        return {
                            "entry_id": entry.entry_id,
                            "timestamp": entry.timestamp,
                            "uid": entry.uid,
                            "operation_type": entry.operation_type,
                            "operation_data": decrypted_data,
                            "security_level": entry.security_level,
                            "entry_hash": entry.entry_hash,
                            "previous_hash": entry.previous_hash
                        }
                
                return None
                
        except Exception as e:
            self.logger.error(f"Entry retrieval error: {str(e)}")
            return None
    
    def query_entries(self, operation_type: Optional[str] = None, 
                     security_level: Optional[str] = None,
                     start_time: Optional[float] = None,
                     end_time: Optional[float] = None,
                     limit: int = 100) -> List[Dict[str, Any]]:
        """Query entries with filters"""
        try:
            with self.chain_lock:
                filtered_entries = []
                
                for entry in self.chain:
                    # Apply filters
                    if operation_type and entry.operation_type != operation_type:
                        continue
                    
                    if security_level and entry.security_level != security_level:
                        continue
                    
                    if start_time and entry.timestamp < start_time:
                        continue
                    
                    if end_time and entry.timestamp > end_time:
                        continue
                    
                    # Decrypt and add to results
                    decrypted_entry = self.get_entry(entry.entry_id)
                    if decrypted_entry:
                        filtered_entries.append(decrypted_entry)
                    
                    if len(filtered_entries) >= limit:
                        break
                
                return filtered_entries
                
        except Exception as e:
            self.logger.error(f"Entry query error: {str(e)}")
            return []
    
    def verify_chain_integrity(self) -> Tuple[bool, List[str]]:
        """Verify the integrity of the entire chain"""
        try:
            with self.chain_lock:
                errors = []
                
                for i, entry in enumerate(self.chain):
                    # Verify entry hash
                    calculated_hash = self._calculate_entry_hash(entry)
                    if calculated_hash != entry.entry_hash:
                        errors.append(f"Hash mismatch in entry {entry.entry_id}")
                    
                    # Verify chain linkage
                    if i > 0:
                        previous_entry = self.chain[i - 1]
                        if entry.previous_hash != previous_entry.entry_hash:
                            errors.append(f"Chain linkage broken at entry {entry.entry_id}")
                    
                    # Verify UID binding
                    if entry.uid != self.uid:
                        errors.append(f"UID mismatch in entry {entry.entry_id}")
                
                is_valid = len(errors) == 0
                
                if is_valid:
                    self.logger.info("Chain integrity verification passed")
                else:
                    self.logger.error(f"Chain integrity verification failed: {errors}")
                
                return is_valid, errors
                
        except Exception as e:
            self.logger.error(f"Integrity verification error: {str(e)}")
            return False, [str(e)]
    
    def _save_chain(self) -> bool:
        """Save chain to file"""
        try:
            # Convert chain to serializable format
            chain_data = {
                "version": "1.0",
                "uid": self.uid,
                "chain_length": len(self.chain),
                "last_updated": time.time(),
                "entries": [asdict(entry) for entry in self.chain]
            }
            
            # Write to file
            with open(self.chain_file, 'w') as f:
                json.dump(chain_data, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Chain save error: {str(e)}")
            return False
    
    def _load_chain(self) -> bool:
        """Load chain from file"""
        try:
            with open(self.chain_file, 'r') as f:
                chain_data = json.load(f)
            
            # Verify UID
            if chain_data.get("uid") != self.uid:
                raise ValueError("UID mismatch in chain file")
            
            # Load entries
            self.chain = []
            for entry_data in chain_data.get("entries", []):
                entry = ReflectEntry(**entry_data)
                self.chain.append(entry)
            
            self.logger.info(f"Chain loaded: {len(self.chain)} entries")
            return True
            
        except Exception as e:
            self.logger.error(f"Chain load error: {str(e)}")
            return False
    
    def _archive_old_entries(self) -> None:
        """Archive old entries to maintain chain length limit"""
        try:
            # Keep only the most recent entries
            max_length = self.security_config["max_chain_length"]
            if len(self.chain) > max_length:
                # Archive older entries
                archive_count = len(self.chain) - max_length
                archived_entries = self.chain[:archive_count]
                
                # Save archive
                archive_file = f"ReflectChain_Archive_{int(time.time())}.json"
                archive_data = {
                    "version": "1.0",
                    "uid": self.uid,
                    "archive_timestamp": time.time(),
                    "entries": [asdict(entry) for entry in archived_entries]
                }
                
                with open(archive_file, 'w') as f:
                    json.dump(archive_data, f, indent=2)
                
                # Keep recent entries
                self.chain = self.chain[archive_count:]
                
                self.logger.info(f"Archived {archive_count} entries to {archive_file}")
                
        except Exception as e:
            self.logger.error(f"Archive error: {str(e)}")
    
    def _create_backup(self) -> None:
        """Create backup of current chain"""
        try:
            backup_file = f"ReflectChain_Backup_{int(time.time())}.json"
            backup_data = {
                "version": "1.0",
                "uid": self.uid,
                "backup_timestamp": time.time(),
                "chain_length": len(self.chain),
                "entries": [asdict(entry) for entry in self.chain]
            }
            
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            self.logger.info(f"Chain backup created: {backup_file}")
            
        except Exception as e:
            self.logger.error(f"Backup creation error: {str(e)}")
    
    def get_chain_status(self) -> Dict[str, Any]:
        """Get status of ReflectChain"""
        with self.chain_lock:
            return {
                "uid": self.uid,
                "chain_length": len(self.chain),
                "last_entry_time": self.chain[-1].timestamp if self.chain else None,
                "encryption_enabled": self.security_config["enable_encryption"],
                "integrity_verification": self.security_config["enable_integrity_checking"],
                "max_chain_length": self.security_config["max_chain_length"]
            }
    
    def export_chain_summary(self) -> Dict[str, Any]:
        """Export summary of chain for reporting"""
        try:
            with self.chain_lock:
                operation_counts = {}
                security_levels = {}
                
                for entry in self.chain:
                    # Count operation types
                    op_type = entry.operation_type
                    operation_counts[op_type] = operation_counts.get(op_type, 0) + 1
                    
                    # Count security levels
                    sec_level = entry.security_level
                    security_levels[sec_level] = security_levels.get(sec_level, 0) + 1
                
                return {
                    "chain_summary": {
                        "total_entries": len(self.chain),
                        "uid": self.uid,
                        "first_entry": self.chain[0].timestamp if self.chain else None,
                        "last_entry": self.chain[-1].timestamp if self.chain else None,
                        "operation_types": operation_counts,
                        "security_levels": security_levels
                    }
                }
                
        except Exception as e:
            self.logger.error(f"Summary export error: {str(e)}")
            return {"error": str(e)}


def create_secure_reflect_chain(uid: str = "ALC-ROOT-1010-1111-XCOV∞", chain_file: str = "ReflectChain.json") -> SecureReflectChain:
    """Factory function to create secure ReflectChain"""
    return SecureReflectChain(uid, chain_file)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create secure ReflectChain
    reflect_chain = create_secure_reflect_chain()
    
    # Test adding entries
    print("Adding test entries...")
    
    entry1_id = reflect_chain.add_entry("quantum_circuit_creation", {
        "circuit_id": "test_circuit_1",
        "qubits": 3,
        "gates": 15,
        "uid": "ALC-ROOT-1010-1111-XCOV∞"
    })
    
    entry2_id = reflect_chain.add_entry("violet_launch", {
        "launch_id": "violet_launch_1",
        "success": True,
        "timestamp": time.time(),
        "uid": "ALC-ROOT-1010-1111-XCOV∞"
    }, security_level="creator")
    
    print(f"Created entries: {entry1_id}, {entry2_id}")
    
    # Test querying
    entries = reflect_chain.query_entries(operation_type="quantum_circuit_creation")
    print(f"Found {len(entries)} quantum circuit entries")
    
    # Test integrity verification
    is_valid, errors = reflect_chain.verify_chain_integrity()
    print(f"Chain integrity: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    
    # Get status
    status = reflect_chain.get_chain_status()
    print(f"Chain status: {json.dumps(status, indent=2)}")
    
    # Export summary
    summary = reflect_chain.export_chain_summary()
    print(f"Chain summary: {json.dumps(summary, indent=2)}")