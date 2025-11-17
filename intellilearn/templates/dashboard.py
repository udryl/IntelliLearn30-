#!/usr/bin/env python3
"""
Flask Web Interface Setup Script
Run this to add the web interface to your IntelliLearn project
"""

import os
import shutil

def create_file(path, content):
    """Create file with content"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ {path}")

def main():
    print("=" * 70)
    print(" 🌐 IntelliLearn Flask Web Interface Setup")
    print("=" * 70)
    print()
    
    base = "intellilearn"
    
    # Check if intellilearn folder exists
    if not os.path.exists(base):
        print("❌ Error: 'intellilearn' folder not found!")
        print("   Please run setup_intellilearn.py first.")
        return
    
    # Create templates directory
    templates_dir = os.path.join(base, "templates")
    os.makedirs(templates_dir, exist_ok=True)
    print(f"✓ Created {templates_dir}/")
    
    # Note: The actual HTML content should be copied from the artifacts above
    # For now, create placeholder message
    
    print()
    print("=" * 70)
    print(" 📋 NEXT STEPS:")
    print("=" * 70)
    print()
    print("1. Copy the Flask app files:")
    print("   - Copy 'app.py' to intellilearn/")
    print("   - Copy 'index.html' to intellilearn/templates/")
    print("   - Copy 'dashboard.html' to intellilearn/templates/")
    print()
    print("2. Install Flask (if not already installed):")
    print("   cd intellilearn")
    print("   pip install Flask Flask-CORS")
    print()
    print("3. Run the web server:")
    print("   python app.py")
    print()
    print("4. Open your browser:")
    print("   http://localhost:5000")
    print()
    print("=" * 70)
    print()
    print("📝 Files you need to create manually:")
    print("   (Copy content from the artifacts shown above)")
    print()
    print("   intellilearn/app.py")
    print("   intellilearn/templates/index.html")
    print("   intellilearn/templates/dashboard.html")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()