import os
import re
from app import create_app

# Step 1: Create app and get all endpoints
app = create_app()
app.app_context().push()

# Dictionary of all endpoints
endpoints = {rule.endpoint for rule in app.url_map.iter_rules()}

# Step 2: Path to templates folder
template_folder = os.path.join(os.path.dirname(__file__), 'app', 'templates')

# Regex to find url_for('endpoint') in templates
url_for_pattern = re.compile(r"url_for\(['\"]([^'\"]+)['\"]\)")

print(f"🔹 Scanning templates in: {template_folder}\n")

# Step 3: Scan templates
for root, dirs, files in os.walk(template_folder):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            matches = url_for_pattern.findall(content)
            for match in matches:
                if match not in endpoints:
                    print(f"⚠️ Template '{file}': url_for('{match}') does NOT exist!")
                    # Suggest closest match
                    suggestions = [ep for ep in endpoints if ep.split('.')[-1] == match.split('.')[-1]]
                    if suggestions:
                        print(f"    💡 Did you mean: {', '.join(suggestions)}?")
                    else:
                        print("    ❌ No similar endpoint found.")
