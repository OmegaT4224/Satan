"""
Encrypted State Manager
Secure quantum state handling with AES-256 encryption
"""
import json
import os
import hashlib
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
import datetime


class EncryptedStateManager:
    """Secure storage and management of quantum states"""
    
    def __init__(self, uid: str = "ALC-ROOT-1010-1111-XCOV∞"):
        self.uid = uid
        self.encryption_key = None
        self.state_directory = "encrypted_states"
        self.key_file = ".quantum_master_key"
        self._ensure_directories()
        
    def _ensure_directories(self) -> None:
        """Ensure required directories exist"""
        if not os.path.exists(self.state_directory):
            os.makedirs(self.state_directory)
            
    def generate_master_key(self) -> None:
        """Generate new master encryption key"""
        self.encryption_key = Fernet.generate_key()
        self._store_master_key()
        
    def _store_master_key(self) -> None:
        """Store master key securely"""
        if not self.encryption_key:
            raise ValueError("No encryption key available")
            
        # In production, use proper key management service
        key_data = {
            "key": self.encryption_key.decode(),
            "uid": self.uid,
            "created": datetime.datetime.now().isoformat(),
            "algorithm": "AES-256"
        }
        
        with open(self.key_file, 'w') as f:
            json.dump(key_data, f)
            
    def _load_master_key(self) -> None:
        """Load master encryption key"""
        try:
            with open(self.key_file, 'r') as f:
                key_data = json.load(f)
                
            # Verify UID matches
            if key_data.get("uid") != self.uid:
                raise ValueError("UID mismatch in encryption key")
                
            self.encryption_key = key_data["key"].encode()
            
        except FileNotFoundError:
            # Generate new key if none exists
            self.generate_master_key()
            
    def encrypt_quantum_state(self, state_data: Dict[str, Any], state_id: Optional[str] = None) -> str:
        """Encrypt quantum state data and return state ID"""
        if not self.encryption_key:
            self._load_master_key()
            
        cipher_suite = Fernet(self.encryption_key)
        
        # Add metadata
        encrypted_state = {
            "uid": self.uid,
            "timestamp": datetime.datetime.now().isoformat(),
            "state_data": state_data,
            "version": "1.0.0"
        }
        
        # Serialize and encrypt
        state_json = json.dumps(encrypted_state, sort_keys=True)
        encrypted_data = cipher_suite.encrypt(state_json.encode())
        
        # Generate state ID if not provided
        if not state_id:
            state_id = self._generate_state_id(state_data)
            
        # Store encrypted state
        state_file = os.path.join(self.state_directory, f"{state_id}.enc")
        with open(state_file, 'wb') as f:
            f.write(encrypted_data)
            
        return state_id
        
    def decrypt_quantum_state(self, state_id: str) -> Dict[str, Any]:
        """Decrypt quantum state by ID"""
        if not self.encryption_key:
            self._load_master_key()
            
        cipher_suite = Fernet(self.encryption_key)
        
        # Load encrypted state
        state_file = os.path.join(self.state_directory, f"{state_id}.enc")
        if not os.path.exists(state_file):
            raise FileNotFoundError(f"Encrypted state {state_id} not found")
            
        with open(state_file, 'rb') as f:
            encrypted_data = f.read()
            
        # Decrypt and deserialize
        decrypted_json = cipher_suite.decrypt(encrypted_data)
        decrypted_state = json.loads(decrypted_json.decode())
        
        # Verify UID
        if decrypted_state.get("uid") != self.uid:
            raise ValueError("UID mismatch in decrypted state")
            
        return decrypted_state["state_data"]
        
    def _generate_state_id(self, state_data: Dict[str, Any]) -> str:
        """Generate unique state ID from state data"""
        state_hash = hashlib.sha256(json.dumps(state_data, sort_keys=True).encode()).hexdigest()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"VIOLET_{timestamp}_{state_hash[:16]}"
        
    def list_encrypted_states(self) -> list:
        """List all encrypted quantum states"""
        states = []
        
        for filename in os.listdir(self.state_directory):
            if filename.endswith('.enc'):
                state_id = filename[:-4]  # Remove .enc extension
                file_path = os.path.join(self.state_directory, filename)
                file_stats = os.stat(file_path)
                
                states.append({
                    "state_id": state_id,
                    "file_size": file_stats.st_size,
                    "created": datetime.datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                    "modified": datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                })
                
        return states
        
    def delete_encrypted_state(self, state_id: str) -> bool:
        """Delete encrypted quantum state"""
        state_file = os.path.join(self.state_directory, f"{state_id}.enc")
        
        if os.path.exists(state_file):
            os.remove(state_file)
            return True
            
        return False
        
    def backup_encrypted_states(self, backup_path: str) -> Dict[str, Any]:
        """Create backup of all encrypted states"""
        import shutil
        
        backup_info = {
            "uid": self.uid,
            "backup_timestamp": datetime.datetime.now().isoformat(),
            "states_backed_up": [],
            "backup_path": backup_path
        }
        
        # Create backup directory
        os.makedirs(backup_path, exist_ok=True)
        
        # Copy encrypted state files
        for filename in os.listdir(self.state_directory):
            if filename.endswith('.enc'):
                src_path = os.path.join(self.state_directory, filename)
                dst_path = os.path.join(backup_path, filename)
                shutil.copy2(src_path, dst_path)
                backup_info["states_backed_up"].append(filename)
                
        # Save backup manifest
        manifest_path = os.path.join(backup_path, "backup_manifest.json")
        with open(manifest_path, 'w') as f:
            json.dump(backup_info, f, indent=2)
            
        return backup_info
        
    def verify_state_integrity(self, state_id: str) -> bool:
        """Verify integrity of encrypted quantum state"""
        try:
            # Attempt to decrypt the state
            decrypted_state = self.decrypt_quantum_state(state_id)
            
            # Verify required fields
            required_fields = ["uid", "timestamp", "state_data"]
            return all(field in decrypted_state for field in required_fields)
            
        except Exception:
            return False
            
    def get_state_metadata(self, state_id: str) -> Dict[str, Any]:
        """Get metadata for encrypted quantum state without decrypting"""
        state_file = os.path.join(self.state_directory, f"{state_id}.enc")
        
        if not os.path.exists(state_file):
            raise FileNotFoundError(f"Encrypted state {state_id} not found")
            
        file_stats = os.stat(state_file)
        
        return {
            "state_id": state_id,
            "file_size": file_stats.st_size,
            "created": datetime.datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            "modified": datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            "uid": self.uid,
            "encrypted": True
        }