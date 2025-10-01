import random
import time

class MockMikroTikManager:
    def __init__(self, host, username, password, port=8728):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.connected = False
        self.connection = None
        self.api = None
    
    def connect(self):
        # Simulate connection delay
        time.sleep(0.5)
        
        # Mock connection - always succeeds for development
        self.connected = True
        print(f"Mock: Connected to MikroTik at {self.host}")
        return True
    
    def get_system_resources(self):
        """Get mock system resources"""
        if not self.connected:
            if not self.connect():
                return {"error": "Connection failed"}
        
        # Return mock system resources data
        return {
            "cpu-load": random.randint(5, 45),
            "free-memory": f"{random.randint(512000, 2048000)}KiB",
            "total-memory": "2048MiB",
            "free-hdd-space": f"{random.randint(50000, 200000)}KiB",
            "total-hdd-space": "256MiB",
            "architecture": "x86",
            "board-name": "MikroTik RouterBoard RB750",
            "platform": "MikroTik",
            "version": "6.49.7",
            "build-time": "Jun/14/2023 14:30:00",
            "factory-software": "6.0",
            "cpu": "MIPS 74Kc V4.12",
            "cpu-count": "1",
            "cpu-frequency": "680MHz",
            "cpu-model": "MIPS 74Kc"
        }
    
    def get_interfaces(self):
        """Get mock network interfaces"""
        if not self.connected:
            if not self.connect():
                return {"error": "Connection failed"}
        
        interfaces = [
            {"name": "ether1", "type": "ether", "running": True, "disabled": False},
            {"name": "ether2", "type": "ether", "running": True, "disabled": False},
            {"name": "ether3", "type": "ether", "running": False, "disabled": False},
            {"name": "ether4", "type": "ether", "running": True, "disabled": False},
            {"name": "ether5", "type": "ether", "running": True, "disabled": False},
            {"name": "wlan1", "type": "wlan", "running": True, "disabled": False},
        ]
        return interfaces
    
    def get_active_connections(self):
        """Get mock active connections"""
        if not self.connected:
            if not self.connect():
                return {"error": "Connection failed"}
        
        connections = [
            {"protocol": "tcp", "src-address": "192.168.1.10", "dst-address": "8.8.8.8"},
            {"protocol": "udp", "src-address": "192.168.1.20", "dst-address": "1.1.1.1"},
        ]
        return connections
    
    def is_connected(self):
        return self.connected
    
    def disconnect(self):
        if self.connected:
            print("Mock: Disconnected from MikroTik")
            self.connected = False

# For backward compatibility, you can use the same class name
MikroTikManager = MockMikroTikManager

# Test the mock implementation
if __name__ == "__main__":
    print("Testing Mock MikroTik Manager...")
    mikrotik = MockMikroTikManager('192.168.88.1', 'admin', 'password')
    if mikrotik.connect():
        print('Connected successfully (mock)')
        resources = mikrotik.get_system_resources()
        print('Mock System resources:', resources)
        interfaces = mikrotik.get_interfaces()
        print(f'Mock Interfaces: {len(interfaces)} found')
    else:
        print('Connection failed')
