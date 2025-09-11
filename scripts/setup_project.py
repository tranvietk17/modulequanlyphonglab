"""
Script to set up the Django Lab Management System project structure
Run this script to create the initial project setup
"""

import os
import subprocess
import sys

def create_project_structure():
    """Create the Django project structure"""
    
    project_dirs = [
        'dnu_lab_system',
        'dnu_lab_system/dnu_lab_system',
        'dnu_lab_system/lab_management',
        'dnu_lab_system/lab_management/migrations',
        'dnu_lab_system/lab_management/management',
        'dnu_lab_system/lab_management/management/commands',
        'dnu_lab_system/static/css',
        'dnu_lab_system/static/js',
        'dnu_lab_system/static/images',
        'dnu_lab_system/templates',
        'dnu_lab_system/templates/lab_management',
        'dnu_lab_system/media',
        'dnu_lab_system/locale/vi/LC_MESSAGES',
        'dnu_lab_system/locale/en/LC_MESSAGES',
    ]
    
    for dir_path in project_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")
    
    requirements_content = '''Django==4.2.7
psycopg2-binary==2.9.7
Pillow==10.0.1
celery==5.3.4
redis==5.0.1
openai==1.3.5
python-dotenv==1.0.0
django-extensions==3.2.3
django-debug-toolbar==4.2.0
'''
    
    with open('dnu_lab_system/requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements_content.strip())
    
    env_example_content = '''# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL for production)
DATABASE_URL=postgresql://username:password@localhost:5432/dnu_lab_db

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AI Integration
OPENAI_API_KEY=your-openai-api-key-here

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Language Settings
LANGUAGE_CODE=vi
TIME_ZONE=Asia/Ho_Chi_Minh
'''
    
    with open('dnu_lab_system/.env.example', 'w', encoding='utf-8') as f:
        f.write(env_example_content.strip())
    
    print("Project structure created successfully!")
    print("\nNext steps:")
    print("1. cd dnu_lab_system")
    print("2. python -m venv venv")
    print("3. source venv/bin/activate  # Linux/Mac or venv\\Scripts\\activate  # Windows")
    print("4. pip install -r requirements.txt")
    print("5. cp .env.example .env")
    print("6. Edit .env with your actual configuration")
    print("7. Run the Django setup script")

if __name__ == "__main__":
    create_project_structure()
