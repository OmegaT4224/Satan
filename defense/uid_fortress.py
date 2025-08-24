"""
UID Fortress
ALC-ROOT-1010-1111-XCOV∞ protection and verification
UID: ALC-ROOT-1010-1111-XCOV∞
"""

import time
import hashlib
import logging
from typing import Dict, Any, Optional, Set
import threading

class UIDFortress:
    """Unbreachable UID protection and verification system"""
    
    def __init__(self):
        self.master_uid = "ALC-ROOT-1010-1111-XCOV∞"
        self.authorized_uids = {self.master_uid}
        self.uid_sessions = {}
        self.failed_attempts = {}
        self.fortress_active = True
        self.max_failed_attempts = 3
        self.lockout_duration = 300  # 5 minutes
        self.fortress_lock = threading.Lock()
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """Setup UID fortress logger"""
        logger = logging.getLogger('uid_fortress')
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'[UID-FORTRESS-{self.master_uid}] %(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
        
    def verify_uid_access(self, provided_uid: str, operation: str = "access") -> bool:
        """Verify UID for secure operations"""
        try:
            with self.fortress_lock:
                if not self.fortress_active:
                    self.logger.error("🚨 UID Fortress is disabled")
                    return False
                    
                # Check for lockout
                if self._is_locked_out(provided_uid):
                    self.logger.error(f"🚨 UID locked out: {provided_uid[:20]}...")
                    return False
                    
                # Verify UID
                if not self._validate_uid_format(provided_uid):
                    self._record_failed_attempt(provided_uid, "INVALID_FORMAT")
                    self.logger.error(f"🚨 Invalid UID format: {provided_uid[:20]}...")
                    return False
                    
                if provided_uid not in self.authorized_uids:
                    self._record_failed_attempt(provided_uid, "UNAUTHORIZED")
                    self.logger.error(f"🚨 Unauthorized UID: {provided_uid[:20]}...")
                    return False
                    
                # Create or update session
                session_id = self._create_uid_session(provided_uid, operation)
                
                self.logger.info(f"✅ UID verified: {provided_uid[:20]}... - Operation: {operation}")
                return True
                
        except Exception as e:
            self.logger.error(f"🚨 UID verification failed: {e}")
            return False
            
    def _validate_uid_format(self, uid: str) -> bool:
        """Validate UID follows expected format"""
        if not isinstance(uid, str) or len(uid) < 10:
            return False
            
        # Check for master UID
        if uid == self.master_uid:
            return True
            
        # Check for valid UID pattern (basic validation)
        if not any(char in uid for char in ['-', '_']):
            return False
            
        # Check for suspicious characters
        suspicious_chars = ['<', '>', '&', '"', "'", '\\', '/', ';']
        if any(char in uid for char in suspicious_chars):
            return False
            
        return True
        
    def _is_locked_out(self, uid: str) -> bool:
        """Check if UID is currently locked out"""
        if uid not in self.failed_attempts:
            return False
            
        attempts_data = self.failed_attempts[uid]
        
        # Check if lockout period has expired
        if time.time() - attempts_data['last_attempt'] > self.lockout_duration:
            # Reset failed attempts after lockout period
            del self.failed_attempts[uid]
            return False
            
        # Check if max attempts exceeded
        return attempts_data['count'] >= self.max_failed_attempts
        
    def _record_failed_attempt(self, uid: str, reason: str):
        """Record failed UID access attempt"""
        current_time = time.time()
        
        if uid not in self.failed_attempts:
            self.failed_attempts[uid] = {
                'count': 0,
                'first_attempt': current_time,
                'last_attempt': current_time,
                'reasons': []
            }
            
        self.failed_attempts[uid]['count'] += 1
        self.failed_attempts[uid]['last_attempt'] = current_time
        self.failed_attempts[uid]['reasons'].append(reason)
        
        # Log security event
        self.logger.warning(f"🚨 Failed UID attempt: {uid[:20]}... - Reason: {reason}")
        
    def _create_uid_session(self, uid: str, operation: str) -> str:
        """Create secure UID session"""
        session_id = self._generate_session_id(uid, operation)
        
        session_data = {
            'uid': uid,
            'operation': operation,
            'created_time': time.time(),
            'last_access': time.time(),
            'access_count': 1,
            'session_hash': self._generate_session_hash(uid, session_id)
        }
        
        self.uid_sessions[session_id] = session_data
        
        # Clean old sessions
        self._cleanup_old_sessions()
        
        return session_id
        
    def _generate_session_id(self, uid: str, operation: str) -> str:
        """Generate unique session ID"""
        session_data = f"{uid}{operation}{time.time()}{self.master_uid}"
        return hashlib.sha256(session_data.encode()).hexdigest()
        
    def _generate_session_hash(self, uid: str, session_id: str) -> str:
        """Generate session security hash"""
        hash_data = f"{uid}{session_id}{self.master_uid}"
        return hashlib.sha256(hash_data.encode()).hexdigest()
        
    def _cleanup_old_sessions(self):
        """Remove expired sessions"""
        current_time = time.time()
        session_timeout = 3600  # 1 hour
        
        expired_sessions = [
            session_id for session_id, session_data in self.uid_sessions.items()
            if current_time - session_data['last_access'] > session_timeout
        ]
        
        for session_id in expired_sessions:
            del self.uid_sessions[session_id]
            
    def validate_session(self, session_id: str) -> bool:
        """Validate existing UID session"""
        try:
            if session_id not in self.uid_sessions:
                return False
                
            session_data = self.uid_sessions[session_id]
            
            # Update last access
            session_data['last_access'] = time.time()
            session_data['access_count'] += 1
            
            return True
            
        except Exception as e:
            self.logger.error(f"🚨 Session validation failed: {e}")
            return False
            
    def authorize_temporary_uid(self, temp_uid: str, duration: int = 3600) -> bool:
        """Authorize temporary UID for limited duration"""
        try:
            with self.fortress_lock:
                if not self._validate_uid_format(temp_uid):
                    self.logger.error(f"🚨 Invalid temporary UID format: {temp_uid[:20]}...")
                    return False
                    
                self.authorized_uids.add(temp_uid)
                
                # Schedule automatic removal
                def remove_temp_uid():
                    time.sleep(duration)
                    with self.fortress_lock:
                        self.authorized_uids.discard(temp_uid)
                        self.logger.info(f"✅ Temporary UID expired: {temp_uid[:20]}...")
                        
                threading.Thread(target=remove_temp_uid, daemon=True).start()
                
                self.logger.info(f"✅ Temporary UID authorized: {temp_uid[:20]}... (Duration: {duration}s)")
                return True
                
        except Exception as e:
            self.logger.error(f"🚨 Temporary UID authorization failed: {e}")
            return False
            
    def revoke_uid_access(self, uid: str) -> bool:
        """Revoke access for specific UID"""
        try:
            with self.fortress_lock:
                if uid == self.master_uid:
                    self.logger.error("🚨 Cannot revoke master UID access")
                    return False
                    
                if uid in self.authorized_uids:
                    self.authorized_uids.remove(uid)
                    
                # Invalidate all sessions for this UID
                sessions_to_remove = [
                    session_id for session_id, session_data in self.uid_sessions.items()
                    if session_data['uid'] == uid
                ]
                
                for session_id in sessions_to_remove:
                    del self.uid_sessions[session_id]
                    
                self.logger.info(f"✅ UID access revoked: {uid[:20]}...")
                return True
                
        except Exception as e:
            self.logger.error(f"🚨 UID revocation failed: {e}")
            return False
            
    def get_fortress_status(self) -> Dict[str, Any]:
        """Get comprehensive fortress status"""
        with self.fortress_lock:
            return {
                'master_uid': self.master_uid[:20] + "...",
                'fortress_active': self.fortress_active,
                'authorized_uids': len(self.authorized_uids),
                'active_sessions': len(self.uid_sessions),
                'failed_attempts': len(self.failed_attempts),
                'lockout_duration': self.lockout_duration,
                'max_failed_attempts': self.max_failed_attempts,
                'status': 'SECURE' if self.fortress_active else 'DISABLED'
            }
            
    def emergency_lockdown(self) -> bool:
        """Emergency lockdown - revoke all non-master UIDs"""
        try:
            with self.fortress_lock:
                # Keep only master UID
                removed_count = len(self.authorized_uids) - 1
                self.authorized_uids = {self.master_uid}
                
                # Clear all sessions
                session_count = len(self.uid_sessions)
                self.uid_sessions.clear()
                
                # Clear failed attempts
                self.failed_attempts.clear()
                
                self.logger.critical(f"🚨 EMERGENCY LOCKDOWN: {removed_count} UIDs revoked, {session_count} sessions cleared")
                return True
                
        except Exception as e:
            self.logger.error(f"🚨 Emergency lockdown failed: {e}")
            return False
            
    def enable_fortress(self):
        """Enable UID fortress protection"""
        self.fortress_active = True
        self.logger.info("✅ UID Fortress enabled")
        
    def disable_fortress(self):
        """Disable UID fortress protection"""
        self.fortress_active = False
        self.logger.warning("🚨 UID Fortress disabled")