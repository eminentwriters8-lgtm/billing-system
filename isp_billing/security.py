# ADVANCED SECURITY SYSTEM
# Copyright (c) 2025 Martin Mutinda

import re
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

class SecurityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # IP whitelisting for admin area
        if request.path.startswith('/admin/'):
            allowed_ips = ['127.0.0.1', '192.168.1.0/24']
            client_ip = self.get_client_ip(request)
            
            if not self.ip_in_ranges(client_ip, allowed_ips):
                return HttpResponseForbidden("Access denied")
                
        # SQL injection protection
        if self.detect_sql_injection(request):
            return HttpResponseForbidden("Suspicious activity detected")
            
        # XSS protection
        if self.detect_xss(request):
            return HttpResponseForbidden("Potential XSS attack detected")
            
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
        
    def ip_in_ranges(self, ip, ranges):
        # Simple IP range checking - enhance for production
        for range_ip in ranges:
            if ip.startswith(range_ip.replace('.0/24', '.')):
                return True
        return ip in ranges
        
    def detect_sql_injection(self, request):
        sql_patterns = [
            r'union.*select',
            r'insert.*into',
            r'drop.*table',
            r'delete.*from',
            r'1=1',
            r'OR.*1=1'
        ]
        
        for param in request.GET.values():
            if any(re.search(pattern, str(param), re.IGNORECASE) for pattern in sql_patterns):
                return True
        return False
        
    def detect_xss(self, request):
        xss_patterns = [
            r'<script>',
            r'javascript:',
            r'onload=',
            r'onerror=',
            r'alert\('
        ]
        
        for param in request.GET.values():
            if any(re.search(pattern, str(param), re.IGNORECASE) for pattern in xss_patterns):
                return True
        return False

class AuditLogger:
    def __init__(self):
        self.audit_file = 'logs/security_audit.log'
        
    def log_action(self, user, action, details):
        timestamp = datetime.now().isoformat()
        log_entry = f"{timestamp} | User: {user} | Action: {action} | Details: {details}\n"
        
        with open(self.audit_file, 'a') as f:
            f.write(log_entry)

audit_logger = AuditLogger()
