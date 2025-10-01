import random
import time

class MikroTikManager:
    def __init__(self, host, username, password, port=8728):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.connected = False
    
    def connect(self):
        time.sleep(0.1)
        self.connected = True
        print(f'Mock: Connected to MikroTik at {self.host}')
        return True
    
    def get_system_resources(self):
        """Get system resources (CPU, memory, etc.)"""
        if not self.connected:
            self.connect()
        return {
            'cpu-load': random.randint(5, 45),
            'free-memory': f'{random.randint(512000, 2048000)}KiB',
            'total-memory': '2048MiB',
            'free-hdd-space': f'{random.randint(50000, 200000)}KiB',
            'total-hdd-space': '256MiB',
            'architecture': 'x86',
            'board-name': 'MikroTik RouterBoard RB750',
            'platform': 'MikroTik',
            'version': '6.49.7',
            'build-time': 'Jun/14/2023 14:30:00',
            'factory-software': '6.0',
            'cpu': 'MIPS 74Kc V4.12',
            'cpu-count': '1',
            'cpu-frequency': '680MHz',
            'cpu-model': 'MIPS 74Kc',
            'uptime': '15d 12h 30m 15s'
        }
    
    def get_active_connections(self):
        """Get active connections"""
        if not self.connected:
            self.connect()
        return {
            'pppoe': [
                {'name': 'client1', 'service': 'pppoe', 'address': '192.168.1.10'},
                {'name': 'client2', 'service': 'pppoe', 'address': '192.168.1.11'},
                {'name': 'client3', 'service': 'pppoe', 'address': '192.168.1.12'}
            ],
            'hotspot': [
                {'name': 'guest1', 'service': 'hotspot', 'address': '192.168.1.100'},
                {'name': 'guest2', 'service': 'hotspot', 'address': '192.168.1.101'}
            ]
        }
    
    def get_interface_stats(self):
        """Get interface statistics - FIXED: return list of dicts with rx-byte/tx-byte keys"""
        if not self.connected:
            self.connect()
        # Return as list of dictionaries for the view to iterate properly
        # Using 'rx-byte' and 'tx-byte' keys as expected by the view
        return [
            {'name': 'ether1', 'rx-byte': '1200000000', 'tx-byte': '800000000', 'status': 'up'},
            {'name': 'ether2', 'rx-byte': '500000000', 'tx-byte': '300000000', 'status': 'up'},
            {'name': 'wlan1', 'rx-byte': '2100000000', 'tx-byte': '1500000000', 'status': 'up'},
            {'name': 'ether3', 'rx-byte': '100000000', 'tx-byte': '50000000', 'status': 'down'},
            {'name': 'ether4', 'rx-byte': '750000000', 'tx-byte': '600000000', 'status': 'up'}
        ]
    
    def get_pppoe_users(self):
        """Get PPPoE users"""
        if not self.connected:
            self.connect()
        return [
            {'name': 'client1', 'service': 'pppoe1', 'address': '192.168.1.10', 'comment': 'Active'},
            {'name': 'client2', 'service': 'pppoe2', 'address': '192.168.1.11', 'comment': 'Active'},
            {'name': 'client3', 'service': 'pppoe3', 'address': '192.168.1.12', 'comment': 'Disabled'}
        ]
    
    def get_hotspot_users(self):
        """Get hotspot users"""
        if not self.connected:
            self.connect()
        return [
            {'name': 'guest1', 'server': 'hotspot1', 'address': '192.168.1.100'},
            {'name': 'guest2', 'server': 'hotspot1', 'address': '192.168.1.101'}
        ]
    
    def is_connected(self):
        return self.connected
    
    def disconnect(self):
        self.connected = False
        print('Mock: Disconnected from MikroTik')

# Create the global instance that real_views.py imports
mikrotik_manager = MikroTikManager('192.168.88.1', 'admin', 'password')
