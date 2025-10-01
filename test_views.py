import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'billing_system.settings')
django.setup()

from clients import real_views
print('=== real_views content analysis ===')
print('Module file:', real_views.__file__)

# Check what's calling get_system_resources
import inspect
source = inspect.getsource(real_views)
lines = source.split('\n')
for i, line in enumerate(lines, 1):
    if 'get_system_resources' in line:
        print(f'Line {i}: {line.strip()}')
        # Show context
        start = max(0, i-3)
        end = min(len(lines), i+2)
        for j in range(start, end):
            print(f'  {j}: {lines[j-1]}')
