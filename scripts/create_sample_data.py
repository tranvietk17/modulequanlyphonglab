#!/usr/bin/env python3
"""
Script tạo dữ liệu mẫu cho hệ thống
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django
sys.path.append('dnu_lab_system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnu_lab_system.settings')
django.setup()

from django.contrib.auth.models import User
from lab_management.models import Department, Equipment, UserProfile, Booking

def create_sample_data():
    """Tạo dữ liệu mẫu"""
    
    print("📊 Tạo dữ liệu mẫu...")
    
    # 1. Tạo các khoa
    departments_data = [
        {'name': 'Khoa Công nghệ Thông tin', 'code': 'CNTT', 'description': 'Khoa đào tạo về công nghệ thông tin và phần mềm'},
        {'name': 'Khoa Điện - Điện tử', 'code': 'DDT', 'description': 'Khoa đào tạo về kỹ thuật điện và điện tử'},
        {'name': 'Khoa Cơ khí', 'code': 'CK', 'description': 'Khoa đào tạo về kỹ thuật cơ khí và chế tạo máy'},
        {'name': 'Khoa Hóa học', 'code': 'HH', 'description': 'Khoa đào tạo về hóa học và công nghệ hóa học'},
        {'name': 'Khoa Vật lý', 'code': 'VL', 'description': 'Khoa đào tạo về vật lý và ứng dụng'},
    ]
    
    departments = []
    for dept_data in departments_data:
        dept, created = Department.objects.get_or_create(
            code=dept_data['code'],
            defaults=dept_data
        )
        departments.append(dept)
        if created:
            print(f"✅ Tạo khoa: {dept.name}")
    
    # 2. Tạo thiết bị
    equipment_data = [
        # CNTT
        {'name': 'Máy chủ Dell PowerEdge R740', 'code': 'SRV001', 'department': 0, 'description': 'Máy chủ hiệu năng cao cho lab mạng', 'status': 'available'},
        {'name': 'Switch Cisco Catalyst 2960', 'code': 'SW001', 'department': 0, 'description': 'Switch mạng 24 port cho thực hành', 'status': 'available'},
        {'name': 'Router Cisco ISR 4321', 'code': 'RT001', 'department': 0, 'description': 'Router doanh nghiệp cho lab mạng', 'status': 'available'},
        {'name': 'Máy tính All-in-One HP', 'code': 'PC001', 'department': 0, 'description': 'Máy tính cho thực hành lập trình', 'status': 'maintenance'},
        
        # Điện - Điện tử
        {'name': 'Oscilloscope Tektronix TBS1052B', 'code': 'OSC001', 'department': 1, 'description': 'Máy hiện sóng 2 kênh 50MHz', 'status': 'available'},
        {'name': 'Nguồn DC Keysight E3631A', 'code': 'PS001', 'department': 1, 'description': 'Nguồn DC ba đầu ra', 'status': 'available'},
        {'name': 'Multimeter Fluke 87V', 'code': 'MM001', 'department': 1, 'description': 'Đồng hồ vạn năng chính xác cao', 'status': 'available'},
        {'name': 'Function Generator Rigol DG1022', 'code': 'FG001', 'department': 1, 'description': 'Máy phát tín hiệu 25MHz', 'status': 'reserved'},
        
        # Cơ khí
        {'name': 'Máy tiện CNC Haas ST-10', 'code': 'CNC001', 'department': 2, 'description': 'Máy tiện CNC tự động', 'status': 'available'},
        {'name': 'Máy phay CNC Haas VF-2', 'code': 'CNC002', 'department': 2, 'description': 'Máy phay CNC 3 trục', 'status': 'available'},
        {'name': 'Máy đo 3D Mitutoyo', 'code': 'CMM001', 'department': 2, 'description': 'Máy đo tọa độ 3 chiều', 'status': 'maintenance'},
        {'name': 'Máy hàn TIG Miller Dynasty', 'code': 'WLD001', 'department': 2, 'description': 'Máy hàn TIG chuyên nghiệp', 'status': 'available'},
        
        # Hóa học
        {'name': 'Máy quang phổ UV-Vis Shimadzu', 'code': 'UV001', 'department': 3, 'description': 'Máy quang phổ tử ngoại khả kiến', 'status': 'available'},
        {'name': 'Cân phân tích Sartorius', 'code': 'BAL001', 'department': 3, 'description': 'Cân phân tích độ chính xác cao', 'status': 'available'},
        {'name': 'Tủ hút khí độc', 'code': 'FH001', 'department': 3, 'description': 'Tủ hút khí độc an toàn', 'status': 'available'},
        {'name': 'Máy ly tâm Eppendorf', 'code': 'CF001', 'department': 3, 'description': 'Máy ly tâm tốc độ cao', 'status': 'broken'},
        
        # Vật lý
        {'name': 'Laser He-Ne 5mW', 'code': 'LAS001', 'department': 4, 'description': 'Laser Helium-Neon cho thí nghiệm quang học', 'status': 'available'},
        {'name': 'Kính hiển vi điện tử', 'code': 'EM001', 'department': 4, 'description': 'Kính hiển vi điện tử quét', 'status': 'available'},
        {'name': 'Máy đo phóng xạ Geiger', 'code': 'GM001', 'department': 4, 'description': 'Máy đo phóng xạ Geiger-Muller', 'status': 'available'},
        {'name': 'Bộ thí nghiệm quang học', 'code': 'OPT001', 'department': 4, 'description': 'Bộ dụng cụ thí nghiệm quang học', 'status': 'reserved'},
    ]
    
    for i, eq_data in enumerate(equipment_data):
        dept_index = eq_data.pop('department')
        eq_data['department'] = departments[dept_index]
        
        equipment, created = Equipment.objects.get_or_create(
            code=eq_data['code'],
            defaults=eq_data
        )
        if created:
            print(f"✅ Tạo thiết bị: {equipment.name}")
    
    # 3. Tạo người dùng
    users_data = [
        # Admin
        {'username': 'admin', 'email': 'admin@dnu.edu.vn', 'first_name': 'Quản trị', 'last_name': 'Viên', 'role': 'admin', 'department': 0},
        
        # Giảng viên
        {'username': 'gv_nguyen', 'email': 'nguyen.van.a@dnu.edu.vn', 'first_name': 'Nguyễn Văn', 'last_name': 'A', 'role': 'teacher', 'department': 0},
        {'username': 'gv_tran', 'email': 'tran.thi.b@dnu.edu.vn', 'first_name': 'Trần Thị', 'last_name': 'B', 'role': 'teacher', 'department': 1},
        {'username': 'gv_le', 'email': 'le.van.c@dnu.edu.vn', 'first_name': 'Lê Văn', 'last_name': 'C', 'role': 'teacher', 'department': 2},
        
        # Sinh viên
        {'username': 'sv_hoang', 'email': 'hoang.minh.d@student.dnu.edu.vn', 'first_name': 'Hoàng Minh', 'last_name': 'D', 'role': 'student', 'department': 0, 'student_id': 'DNU2021001'},
        {'username': 'sv_pham', 'email': 'pham.thi.e@student.dnu.edu.vn', 'first_name': 'Phạm Thị', 'last_name': 'E', 'role': 'student', 'department': 0, 'student_id': 'DNU2021002'},
        {'username': 'sv_vo', 'email': 'vo.van.f@student.dnu.edu.vn', 'first_name': 'Võ Văn', 'last_name': 'F', 'role': 'student', 'department': 1, 'student_id': 'DNU2021003'},
        {'username': 'sv_dao', 'email': 'dao.thi.g@student.dnu.edu.vn', 'first_name': 'Đào Thị', 'last_name': 'G', 'role': 'student', 'department': 2, 'student_id': 'DNU2021004'},
    ]
    
    for user_data in users_data:
        dept_index = user_data.pop('department')
        role = user_data.pop('role')
        student_id = user_data.pop('student_id', '')
        
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={**user_data, 'password': 'pbkdf2_sha256$600000$dummy$dummy'}  # Temporary password
        )
        
        if created:
            user.set_password('123456')  # Default password
            user.save()
            print(f"✅ Tạo người dùng: {user.get_full_name()}")
        
        # Tạo profile
        profile, profile_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'role': role,
                'student_id': student_id,
                'department': departments[dept_index],
                'phone': f'0{90000000 + user.id:08d}'
            }
        )
    
    # 4. Tạo đặt lịch mẫu
    bookings_data = [
        {
            'user': 'sv_hoang',
            'equipment': 'SRV001',
            'purpose': 'Thực hành cấu hình máy chủ web Apache và MySQL cho đồ án môn Phát triển ứng dụng web',
            'pickup_time': timezone.now() + timedelta(days=1),
            'return_time': timezone.now() + timedelta(days=1, hours=3),
            'status': 'pending'
        },
        {
            'user': 'sv_pham',
            'equipment': 'SW001',
            'purpose': 'Thực hành cấu hình VLAN và routing cho bài tập lớn môn Mạng máy tính',
            'pickup_time': timezone.now() + timedelta(days=2),
            'return_time': timezone.now() + timedelta(days=2, hours=2),
            'status': 'approved'
        },
        {
            'user': 'sv_vo',
            'equipment': 'OSC001',
            'purpose': 'Đo và phân tích tín hiệu trong mạch khuếch đại thuật toán',
            'pickup_time': timezone.now() + timedelta(days=3),
            'return_time': timezone.now() + timedelta(days=3, hours=4),
            'status': 'pending'
        },
        {
            'user': 'sv_dao',
            'equipment': 'CNC001',
            'purpose': 'Gia công chi tiết máy theo bản vẽ kỹ thuật cho đồ án tốt nghiệp',
            'pickup_time': timezone.now() + timedelta(days=5),
            'return_time': timezone.now() + timedelta(days=5, hours=6),
            'status': 'approved'
        },
    ]
    
    for booking_data in bookings_data:
        user = User.objects.get(username=booking_data['user'])
        equipment = Equipment.objects.get(code=booking_data['equipment'])
        
        booking, created = Booking.objects.get_or_create(
            user=user,
            equipment=equipment,
            pickup_time=booking_data['pickup_time'],
            defaults={
                'purpose': booking_data['purpose'],
                'return_time': booking_data['return_time'],
                'status': booking_data['status']
            }
        )
        
        if created:
            print(f"✅ Tạo đặt lịch: {user.get_full_name()} - {equipment.name}")
    
    print("\n🎉 Hoàn thành tạo dữ liệu mẫu!")
    print("\n📋 Thông tin đăng nhập:")
    print("Admin: admin / 123456")
    print("Giảng viên: gv_nguyen / 123456")
    print("Sinh viên: sv_hoang / 123456")

if __name__ == "__main__":
    create_sample_data()
