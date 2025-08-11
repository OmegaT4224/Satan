"""
Main security scanning engine for VIOLET-AF quantum logic automation system.
Provides comprehensive security scanning for quantum circuit operations and dependencies.
"""

import os
import hashlib
import subprocess
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid


class SecurityScanner:
    """Main security scanning engine for quantum operations."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the security scanner with configuration."""
        self.scan_id = str(uuid.uuid4())
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        self.scan_results = {
            'scan_id': self.scan_id,
            'timestamp': datetime.utcnow().isoformat(),
            'findings': [],
            'status': 'initialized'
        }
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load security configuration."""
        default_config = {
            'scan_modes': ['dependency', 'code', 'quantum'],
            'severity_levels': ['critical', 'high', 'medium', 'low'],
            'quantum_validation': True,
            'logging_level': 'INFO'
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    import yaml
                    user_config = yaml.safe_load(f)
                    default_config.update(user_config)
            except Exception as e:
                logging.warning(f"Failed to load config from {config_path}: {e}")
        
        return default_config
    
    def _setup_logger(self) -> logging.Logger:
        """Setup secure logging."""
        logger = logging.getLogger(f'SecurityScanner.{self.scan_id}')
        logger.setLevel(getattr(logging, self.config.get('logging_level', 'INFO')))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def scan_dependencies(self) -> List[Dict[str, Any]]:
        """Scan Python dependencies for vulnerabilities."""
        findings = []
        
        try:
            # Check if requirements.txt exists
            if os.path.exists('requirements.txt'):
                with open('requirements.txt', 'r') as f:
                    dependencies = f.read().strip().split('\n')
                
                for dep in dependencies:
                    if dep.strip():
                        finding = self._check_dependency_security(dep.strip())
                        if finding:
                            findings.append(finding)
            
            # Also check installed packages
            try:
                result = subprocess.run(['pip', 'list', '--format=json'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    packages = json.loads(result.stdout)
                    for pkg in packages:
                        finding = self._check_package_security(pkg)
                        if finding:
                            findings.append(finding)
            except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
                self.logger.warning(f"Failed to check installed packages: {e}")
                
        except Exception as e:
            self.logger.error(f"Dependency scan failed: {e}")
            findings.append({
                'type': 'dependency_scan_error',
                'severity': 'medium',
                'description': f"Failed to complete dependency scan: {e}",
                'timestamp': datetime.utcnow().isoformat()
            })
        
        return findings
    
    def _check_dependency_security(self, dependency: str) -> Optional[Dict[str, Any]]:
        """Check a specific dependency for security issues."""
        # Basic security checks for common vulnerable packages
        vulnerable_patterns = {
            'pickle': 'Pickle module can execute arbitrary code',
            'eval': 'Eval function can execute arbitrary code',
            'exec': 'Exec function can execute arbitrary code',
        }
        
        for pattern, description in vulnerable_patterns.items():
            if pattern in dependency.lower():
                return {
                    'type': 'vulnerable_dependency',
                    'severity': 'high',
                    'dependency': dependency,
                    'description': description,
                    'recommendation': f'Avoid using {pattern} or implement proper sandboxing',
                    'timestamp': datetime.utcnow().isoformat()
                }
        
        return None
    
    def _check_package_security(self, package: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Check an installed package for security issues."""
        # This is a simplified check - in production, you'd integrate with
        # vulnerability databases like OSV, Snyk, etc.
        known_vulnerable = {
            'pillow': ['8.0.0', '8.1.0'],  # Example vulnerable versions
            'requests': ['2.25.0']         # Example vulnerable versions
        }
        
        pkg_name = package.get('name', '').lower()
        pkg_version = package.get('version', '')
        
        if pkg_name in known_vulnerable:
            if pkg_version in known_vulnerable[pkg_name]:
                return {
                    'type': 'vulnerable_package',
                    'severity': 'high',
                    'package': pkg_name,
                    'version': pkg_version,
                    'description': f'Package {pkg_name} {pkg_version} has known vulnerabilities',
                    'recommendation': 'Update to latest secure version',
                    'timestamp': datetime.utcnow().isoformat()
                }
        
        return None
    
    def scan_code(self, path: str = '.') -> List[Dict[str, Any]]:
        """Scan code for security vulnerabilities."""
        findings = []
        
        try:
            for root, dirs, files in os.walk(path):
                # Skip security-sensitive directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
                
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        file_findings = self._scan_python_file(file_path)
                        findings.extend(file_findings)
                        
        except Exception as e:
            self.logger.error(f"Code scan failed: {e}")
            findings.append({
                'type': 'code_scan_error',
                'severity': 'medium',
                'description': f"Failed to complete code scan: {e}",
                'timestamp': datetime.utcnow().isoformat()
            })
        
        return findings
    
    def _scan_python_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Scan a Python file for security issues."""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Security patterns to check
            security_patterns = {
                'eval(': ('high', 'Use of eval() can execute arbitrary code'),
                'exec(': ('high', 'Use of exec() can execute arbitrary code'),
                'subprocess.call': ('medium', 'Subprocess calls may be vulnerable to injection'),
                'os.system': ('high', 'os.system() calls can execute arbitrary commands'),
                'pickle.loads': ('high', 'pickle.loads() can execute arbitrary code'),
                'input(': ('low', 'Raw input handling should be validated'),
            }
            
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                for pattern, (severity, description) in security_patterns.items():
                    if pattern in line:
                        findings.append({
                            'type': 'code_security_issue',
                            'severity': severity,
                            'file': file_path,
                            'line': line_num,
                            'pattern': pattern,
                            'description': description,
                            'code_snippet': line.strip(),
                            'timestamp': datetime.utcnow().isoformat()
                        })
            
        except Exception as e:
            self.logger.warning(f"Failed to scan file {file_path}: {e}")
        
        return findings
    
    def scan_quantum_operations(self, operations: List[str]) -> List[Dict[str, Any]]:
        """Scan quantum operations for security issues."""
        findings = []
        
        for operation in operations:
            finding = self._validate_quantum_operation(operation)
            if finding:
                findings.append(finding)
        
        return findings
    
    def _validate_quantum_operation(self, operation: str) -> Optional[Dict[str, Any]]:
        """Validate a quantum operation for security."""
        # Basic quantum operation security checks
        suspicious_patterns = [
            'UNKNOWN',  # Unknown operations from the existing code
            'EXEC',     # Execution operations
            'SYSTEM',   # System calls
        ]
        
        for pattern in suspicious_patterns:
            if pattern in operation.upper():
                return {
                    'type': 'quantum_security_issue',
                    'severity': 'medium',
                    'operation': operation,
                    'description': f'Quantum operation contains suspicious pattern: {pattern}',
                    'recommendation': 'Validate operation before execution',
                    'timestamp': datetime.utcnow().isoformat()
                }
        
        return None
    
    def perform_full_scan(self, scan_path: str = '.') -> Dict[str, Any]:
        """Perform a comprehensive security scan."""
        self.logger.info(f"Starting full security scan with ID: {self.scan_id}")
        
        try:
            # Scan dependencies
            if 'dependency' in self.config['scan_modes']:
                self.logger.info("Scanning dependencies...")
                dep_findings = self.scan_dependencies()
                self.scan_results['findings'].extend(dep_findings)
            
            # Scan code
            if 'code' in self.config['scan_modes']:
                self.logger.info("Scanning code...")
                code_findings = self.scan_code(scan_path)
                self.scan_results['findings'].extend(code_findings)
            
            # Scan quantum operations (if any are found in code)
            if 'quantum' in self.config['scan_modes']:
                self.logger.info("Scanning quantum operations...")
                quantum_ops = self._extract_quantum_operations(scan_path)
                quantum_findings = self.scan_quantum_operations(quantum_ops)
                self.scan_results['findings'].extend(quantum_findings)
            
            self.scan_results['status'] = 'completed'
            self.scan_results['summary'] = self._generate_summary()
            
        except Exception as e:
            self.logger.error(f"Full scan failed: {e}")
            self.scan_results['status'] = 'failed'
            self.scan_results['error'] = str(e)
        
        self.logger.info(f"Security scan completed. Found {len(self.scan_results['findings'])} findings.")
        return self.scan_results
    
    def _extract_quantum_operations(self, path: str) -> List[str]:
        """Extract quantum operations from code."""
        operations = []
        
        try:
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
                
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Look for quantum-related operations
                        lines = content.split('\n')
                        for line in lines:
                            line = line.strip()
                            if (line.startswith('op_') or 
                                'quantum' in line.lower() or 
                                'CALL' in line or 
                                'ML' in line):
                                operations.append(line)
                                
        except Exception as e:
            self.logger.warning(f"Failed to extract quantum operations: {e}")
        
        return operations
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of scan results."""
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        type_counts = {}
        
        for finding in self.scan_results['findings']:
            severity = finding.get('severity', 'unknown')
            finding_type = finding.get('type', 'unknown')
            
            if severity in severity_counts:
                severity_counts[severity] += 1
            
            type_counts[finding_type] = type_counts.get(finding_type, 0) + 1
        
        return {
            'total_findings': len(self.scan_results['findings']),
            'severity_breakdown': severity_counts,
            'finding_types': type_counts,
            'scan_duration': datetime.utcnow().isoformat()
        }
    
    def export_results(self, output_path: str) -> bool:
        """Export scan results to a file."""
        try:
            with open(output_path, 'w') as f:
                json.dump(self.scan_results, f, indent=2)
            self.logger.info(f"Results exported to {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to export results: {e}")
            return False