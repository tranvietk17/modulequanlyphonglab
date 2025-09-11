#!/usr/bin/env python3
"""
Script chạy toàn bộ setup hệ thống
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Chạy command và hiển thị kết quả"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} thành công!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} thất bại!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Chạy toàn bộ setup"""
    print("🚀 Bắt đầu setup hệ thống quản lý phòng lab DNU...")
    
    # Danh sách các script cần chạy
    scripts = [
        ("python scripts/setup_project.py", "Tạo cấu trúc project"),
        ("python scripts/django_setup.py", "Tạo các file Django"),
        ("python scripts/create_templates.py", "Tạo templates HTML"),
        ("python scripts/create_user_system.py", "Tạo hệ thống người dùng"),
        ("python scripts/ai_integration_real.py", "Tích hợp AI thực tế"),
    ]
    
    success_count = 0
    for command, description in scripts:
        if run_command(command, description):
            success_count += 1
        else:
            print(f"\n⚠️  Có lỗi xảy ra khi {description.lower()}")
            choice = input("Bạn có muốn tiếp tục? (y/n): ")
            if choice.lower() != 'y':
                break
    
    print(f"\n📊 Kết quả: {success_count}/{len(scripts)} script chạy thành công")
    
    if success_count == len(scripts):
        print("\n🎉 Setup hoàn tất! Các bước tiếp theo:")
        print("1. cd dnu_lab_system")
        print("2. python -m venv venv")
        print("3. source venv/bin/activate  # Linux/Mac")
        print("   # hoặc venv\\Scripts\\activate  # Windows")
        print("4. pip install -r requirements.txt")
        print("5. cp .env.example .env")
        print("6. Chỉnh sửa file .env với thông tin thực tế")
        print("7. python manage.py makemigrations")
        print("8. python manage.py migrate")
        print("9. python manage.py createsuperuser")
        print("10. python ../scripts/create_sample_data.py")
        print("11. python manage.py runserver")
        print("\n🤖 Để sử dụng AI features:")
        print("- Thêm OPENAI_API_KEY vào file .env")
        print("- Chạy: python manage.py ai_operations --generate-descriptions")
        print("- Khởi động Celery: celery -A dnu_lab_system worker -l info")
        print("- Khởi động Celery Beat: celery -A dnu_lab_system beat -l info")
    else:
        print("\n⚠️  Setup chưa hoàn tất. Vui lòng kiểm tra lại các lỗi.")

if __name__ == "__main__":
    main()
