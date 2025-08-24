"""
Threat Detection Engine
Continuous surveillance of automation processes
UID: ALC-ROOT-1010-1111-XCOV∞
"""

import time
import hashlib
import logging
from typing import Dict, Any, List, Optional, Set
from collections import deque

class ThreatDetectionEngine:
    """Continuous threat surveillance with real-time analysis"""
    
    def __init__(self):
        self.security_uid = "ALC-ROOT-1010-1111-XCOV∞"
        self.threat_level = "GREEN"  # GREEN, YELLOW, ORANGE, RED
        self.detected_threats = deque(maxlen=1000)
        self.baseline_metrics = {}
        self.anomaly_threshold = 3.0
        self.logger = self._setup_logger()
        self.active_scans = 0
        
    def _setup_logger(self):
        """Setup threat detection logger"""
        logger = logging.getLogger('threat_detection')
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'[THREAT-DETECTION-{self.security_uid}] %(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
        
    def detect_tampering(self, result: Any) -> bool:
        """Detect result tampering with statistical analysis"""
        self.active_scans += 1
        
        try:
            # Generate result fingerprint
            result_hash = self._generate_result_hash(result)
            
            # Check against known good patterns
            if self._is_suspicious_result(result, result_hash):
                self._log_threat("RESULT_TAMPERING", f"Suspicious result hash: {result_hash[:16]}...")
                return True
                
            # Statistical anomaly detection
            if self._detect_statistical_anomaly(result):
                self._log_threat("STATISTICAL_ANOMALY", "Result shows statistical anomalies")
                return True
                
            self.logger.debug(f"✅ Result validation passed: {result_hash[:8]}...")
            return False
            
        except Exception as e:
            self.logger.error(f"🚨 Tampering detection error: {e}")
            return True  # Fail safe - assume tampering on error
            
    def _generate_result_hash(self, result: Any) -> str:
        """Generate cryptographic hash of result"""
        result_str = str(result) + str(time.time()) + self.security_uid
        return hashlib.sha256(result_str.encode()).hexdigest()
        
    def _is_suspicious_result(self, result: Any, result_hash: str) -> bool:
        """Check if result shows signs of tampering"""
        # Check for impossible values
        if isinstance(result, (int, float)):
            if result > 1e10 or result < -1e10:
                return True
                
        # Check for suspicious patterns in hash
        if result_hash.startswith('00000') or result_hash.endswith('00000'):
            # Too many zeros might indicate manipulation
            return True
            
        return False
        
    def _detect_statistical_anomaly(self, result: Any) -> bool:
        """Detect statistical anomalies in results"""
        if not isinstance(result, (int, float)):
            return False
            
        # Simple anomaly detection based on recent results
        recent_results = [t['result'] for t in list(self.detected_threats)[-10:] 
                         if isinstance(t.get('result'), (int, float))]
        
        if len(recent_results) < 3:
            return False  # Not enough data
            
        # Basic statistical check
        mean_val = sum(recent_results) / len(recent_results)
        variance = sum((x - mean_val) ** 2 for x in recent_results) / len(recent_results)
        std_dev = variance ** 0.5
        
        if std_dev > 0:
            z_score = abs(result - mean_val) / std_dev
            return z_score > self.anomaly_threshold
            
        return False
        
    def scan_environment(self) -> Dict[str, Any]:
        """Comprehensive environment security scan"""
        scan_results = {
            'timestamp': time.time(),
            'scan_id': self.active_scans,
            'threats_detected': [],
            'security_level': self.threat_level
        }
        
        # File system scan
        fs_threats = self._scan_filesystem()
        scan_results['threats_detected'].extend(fs_threats)
        
        # Network scan
        net_threats = self._scan_network()
        scan_results['threats_detected'].extend(net_threats)
        
        # Process scan
        proc_threats = self._scan_processes()
        scan_results['threats_detected'].extend(proc_threats)
        
        # Update threat level based on findings
        self._update_threat_level(scan_results['threats_detected'])
        scan_results['security_level'] = self.threat_level
        
        self.logger.info(f"🔍 Environment scan complete: {len(scan_results['threats_detected'])} threats")
        
        return scan_results
        
    def _scan_filesystem(self) -> List[Dict[str, Any]]:
        """Scan filesystem for threats"""
        threats = []
        
        try:
            import os
            
            # Check for suspicious files
            suspicious_extensions = ['.exe', '.bat', '.cmd', '.scr']
            current_dir = os.getcwd()
            
            for root, dirs, files in os.walk(current_dir):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in suspicious_extensions):
                        threats.append({
                            'type': 'SUSPICIOUS_FILE',
                            'path': os.path.join(root, file),
                            'severity': 'MEDIUM'
                        })
                        
        except Exception as e:
            self.logger.debug(f"Filesystem scan error: {e}")
            
        return threats
        
    def _scan_network(self) -> List[Dict[str, Any]]:
        """Scan for network-based threats"""
        threats = []
        
        try:
            # Basic network checks
            import socket
            
            # Check for unusual open ports
            localhost = '127.0.0.1'
            suspicious_ports = [1337, 31337, 4444, 5555]
            
            for port in suspicious_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((localhost, port))
                sock.close()
                
                if result == 0:
                    threats.append({
                        'type': 'SUSPICIOUS_PORT',
                        'port': port,
                        'severity': 'HIGH'
                    })
                    
        except Exception as e:
            self.logger.debug(f"Network scan error: {e}")
            
        return threats
        
    def _scan_processes(self) -> List[Dict[str, Any]]:
        """Scan running processes for threats"""
        threats = []
        
        try:
            import psutil
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    proc_info = proc.info
                    
                    # Check for high CPU usage
                    if proc_info['cpu_percent'] and proc_info['cpu_percent'] > 80:
                        threats.append({
                            'type': 'HIGH_CPU_PROCESS',
                            'process': proc_info['name'],
                            'cpu_percent': proc_info['cpu_percent'],
                            'severity': 'MEDIUM'
                        })
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except ImportError:
            self.logger.debug("psutil not available for process scanning")
            
        return threats
        
    def _update_threat_level(self, threats: List[Dict[str, Any]]):
        """Update overall threat level based on detected threats"""
        if not threats:
            self.threat_level = "GREEN"
            return
            
        high_severity_count = sum(1 for t in threats if t.get('severity') == 'HIGH')
        medium_severity_count = sum(1 for t in threats if t.get('severity') == 'MEDIUM')
        
        if high_severity_count > 0:
            self.threat_level = "RED"
        elif medium_severity_count > 3:
            self.threat_level = "ORANGE"
        elif medium_severity_count > 0:
            self.threat_level = "YELLOW"
        else:
            self.threat_level = "GREEN"
            
    def _log_threat(self, threat_type: str, details: str):
        """Log detected threat"""
        threat_entry = {
            'timestamp': time.time(),
            'type': threat_type,
            'details': details,
            'threat_level': self.threat_level
        }
        
        self.detected_threats.append(threat_entry)
        self.logger.warning(f"🚨 THREAT DETECTED: {threat_type} - {details}")
        
    def get_security_status(self) -> Dict[str, Any]:
        """Get comprehensive security status"""
        return {
            'security_uid': self.security_uid,
            'threat_level': self.threat_level,
            'active_scans': self.active_scans,
            'recent_threats': list(self.detected_threats)[-10:],
            'total_threats_detected': len(self.detected_threats),
            'last_scan': time.time()
        }