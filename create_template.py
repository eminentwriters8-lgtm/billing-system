import os

if not os.path.exists('templates/base.html'):
    base_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Billing System{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .card { border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .card-header { border-radius: 10px 10px 0 0 !important; }
        .progress { border-radius: 10px; }
        .badge { border-radius: 6px; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/clients/dashboard/">🌍 Africa Online Networks</a>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
    
    os.makedirs('templates', exist_ok=True)
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(base_content)
    print('✅ Created base template')
else:
    print('✅ Base template already exists')