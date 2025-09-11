"""
Create additional templates for the Lab Management System
"""

import os

# My bookings template
MY_BOOKINGS_TEMPLATE = '''
{% extends 'base.html' %}

{% block title %}Đơn đặt lịch của tôi{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2><i class="fas fa-calendar-check me-2"></i>Đơn đặt lịch của tôi</h2>
    <a href="{% url 'equipment_list' %}" class="btn btn-primary">
        <i class="fas fa-plus me-1"></i>Đặt lịch mới
    </a>
</div>

{% if bookings %}
    <div class="row">
        {% for booking in bookings %}
            <div class="col-lg-6 mb-4">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">{{ booking.equipment.name }}</h6>
                        <span class="badge bg-{% if booking.status == 'pending' %}warning{% elif booking.status == 'approved' %}success{% elif booking.status == 'rejected' %}danger{% else %}secondary{% endif %}">
                            {{ booking.get_status_display }}
                        </span>
                    </div>
                    <div class="card-body">
                        <p class="card-text">
                            <strong>Phòng ban:</strong> {{ booking.equipment.department.name }}<br>
                            <strong>Thời gian nhận:</strong> {{ booking.pickup_time|date:"d/m/Y H:i" }}<br>
                            <strong>Thời gian trả:</strong> {{ booking.return_time|date:"d/m/Y H:i" }}<br>
                            <strong>Mục đích:</strong> {{ booking.purpose|truncatewords:10 }}
                        </p>
                        {% if booking.notes %}
                            <div class="alert alert-info">
                                <strong>Ghi chú từ giảng viên:</strong><br>
                                {{ booking.notes }}
                            </div>
                        {% endif %}
                        <small class="text-muted">
                            Đặt lúc: {{ booking.created_at|date:"d/m/Y H:i" }}
                        </small>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
{% else %}
    <div class="text-center py-5">
        <i class="fas fa-calendar-times fa-4x text-muted mb-3"></i>
        <h4>Bạn chưa có đơn đặt lịch nào</h4>
        <p class="text-muted">Hãy bắt đầu bằng cách chọn thiết bị cần mượn</p>
        <a href="{% url 'equipment_list' %}" class="btn btn-primary">
            <i class="fas fa-search me-1"></i>Tìm thiết bị
        </a>
    </div>
{% endif %}
{% endblock %}
'''

# Create booking template
CREATE_BOOKING_TEMPLATE = '''
{% extends 'base.html' %}

{% block title %}Đặt lịch thiết bị{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header">
                <h4><i class="fas fa-calendar-plus me-2"></i>Đặt lịch thiết bị</h4>
            </div>
            <div class="card-body">
                <div class="row mb-4">
                    <div class="col-md-4">
                        {% if equipment.image %}
                            <img src="{{ equipment.image.url }}" class="img-fluid rounded" alt="{{ equipment.name }}">
                        {% else %}
                            <div class="bg-light rounded d-flex align-items-center justify-content-center" style="height: 200px;">
                                <i class="fas fa-image fa-3x text-muted"></i>
                            </div>
                        {% endif %}
                    </div>
                    <div class="col-md-8">
                        <h5>{{ equipment.name }}</h5>
                        <p class="text-muted">
                            <i class="fas fa-building me-1"></i>{{ equipment.department.name }}
                        </p>
                        <p>{{ equipment.description|default:"Mô tả sẽ được cập nhật sớm." }}</p>
                        <span class="badge bg-success">Có sẵn</span>
                    </div>
                </div>

                <form method="post">
                    {% csrf_token %}
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="{{ form.pickup_time.id_for_label }}" class="form-label">{{ form.pickup_time.label }}</label>
                            {{ form.pickup_time }}
                            {% if form.pickup_time.errors %}
                                <div class="text-danger">{{ form.pickup_time.errors }}</div>
                            {% endif %}
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="{{ form.return_time.id_for_label }}" class="form-label">{{ form.return_time.label }}</label>
                            {{ form.return_time }}
                            {% if form.return_time.errors %}
                                <div class="text-danger">{{ form.return_time.errors }}</div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.purpose.id_for_label }}" class="form-label">{{ form.purpose.label }}</label>
                        {{ form.purpose }}
                        {% if form.purpose.errors %}
                            <div class="text-danger">{{ form.purpose.errors }}</div>
                        {% endif %}
                    </div>
                    {% if form.non_field_errors %}
                        <div class="alert alert-danger">{{ form.non_field_errors }}</div>
                    {% endif %}
                    <div class="d-flex justify-content-between">
                        <a href="{% url 'equipment_list' %}" class="btn btn-secondary">
                            <i class="fas fa-arrow-left me-1"></i>Quay lại
                        </a>
                        <button type="submit" class="btn btn-success">
                            <i class="fas fa-paper-plane me-1"></i>Gửi đơn đặt lịch
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# Admin dashboard template
ADMIN_DASHBOARD_TEMPLATE = '''
{% extends 'base.html' %}

{% block title %}Dashboard Quản trị{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2><i class="fas fa-tachometer-alt me-2"></i>Dashboard Quản trị</h2>
    <div>
        <a href="{% url 'pending_bookings' %}" class="btn btn-warning me-2">
            <i class="fas fa-clock me-1"></i>Đơn chờ duyệt ({{ pending_bookings }})
        </a>
        <a href="/admin/" class="btn btn-primary">
            <i class="fas fa-cog me-1"></i>Admin Panel
        </a>
    </div>
</div>

<div class="row mb-4">
    <div class="col-lg-3 col-md-6 mb-3">
        <div class="card bg-warning text-white">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h4>{{ pending_bookings }}</h4>
                        <p class="mb-0">Đơn chờ duyệt</p>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-clock fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-lg-3 col-md-6 mb-3">
        <div class="card bg-primary text-white">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h4>{{ total_bookings }}</h4>
                        <p class="mb-0">Tổng đơn đặt lịch</p>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-calendar fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-lg-3 col-md-6 mb-3">
        <div class="card bg-success text-white">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h4>{{ total_equipment }}</h4>
                        <p class="mb-0">Tổng thiết bị</p>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-microscope fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-lg-3 col-md-6 mb-3">
        <div class="card bg-info text-white">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h4>{{ total_students }}</h4>
                        <p class="mb-0">Sinh viên đã đặt</p>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-users fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-chart-line me-2"></i>Hoạt động gần đây</h5>
            </div>
            <div class="card-body">
                <p class="text-muted">Biểu đồ thống kê sẽ được thêm trong phiên bản tiếp theo.</p>
            </div>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-tasks me-2"></i>Công việc cần làm</h5>
            </div>
            <div class="card-body">
                <ul class="list-unstyled">
                    <li class="mb-2">
                        <a href="{% url 'pending_bookings' %}" class="text-decoration-none">
                            <i class="fas fa-clock text-warning me-2"></i>
                            Duyệt {{ pending_bookings }} đơn chờ
                        </a>
                    </li>
                    <li class="mb-2">
                        <a href="/admin/booking/equipment/" class="text-decoration-none">
                            <i class="fas fa-plus text-success me-2"></i>
                            Thêm thiết bị mới
                        </a>
                    </li>
                    <li class="mb-2">
                        <a href="/admin/booking/department/" class="text-decoration-none">
                            <i class="fas fa-building text-info me-2"></i>
                            Quản lý phòng ban
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# Seed data script
SEED_DATA_SCRIPT = '''
"""
Seed data for Lab Management System
Run this after migrations to populate initial data
"""

import os
import django
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab_management.settings')
django.setup()

from booking.models import Department, Equipment

def create_seed_data():
    """Create initial data for the system"""
    
    # Create departments
    departments_data = [
        {
            'name': 'Khoa Công nghệ Thông tin',
            'description': 'Phòng lab chuyên về lập trình, mạng máy tính và an toàn thông tin'
        },
        {
            'name': 'Khoa Điện - Điện tử',
            'description': 'Phòng lab về mạch điện, vi xử lý và hệ thống nhúng'
        },
        {
            'name': 'Khoa Cơ khí',
            'description': 'Phòng lab về gia công cơ khí, CAD/CAM và robot'
        },
        {
            'name': 'Khoa Hóa học',
            'description': 'Phòng lab hóa học phân tích và tổng hợp'
        }
    ]
    
    departments = []
    for dept_data in departments_data:
        dept, created = Department.objects.get_or_create(
            name=dept_data['name'],
            defaults={'description': dept_data['description']}
        )
        departments.append(dept)
        if created:
            print(f"Created department: {dept.name}")
    
    # Create equipment
    equipment_data = [
        # IT Department
        {
            'name': 'Máy tính Dell OptiPlex 7090',
            'department': departments[0],
            'description': 'Máy tính để bàn hiệu năng cao cho lập trình và phát triển phần mềm'
        },
        {
            'name': 'Router Cisco 2901',
            'department': departments[0],
            'description': 'Router doanh nghiệp cho thực hành cấu hình mạng'
        },
        {
            'name': 'Máy chủ HP ProLiant DL380',
            'department': departments[0],
            'description': 'Máy chủ cho thực hành quản trị hệ thống và cloud computing'
        },
        
        # Electronics Department
        {
            'name': 'Oscilloscope Tektronix TBS1052B',
            'department': departments[1],
            'description': 'Máy hiện sóng số 2 kênh, băng thông 50MHz'
        },
        {
            'name': 'Arduino Uno R3',
            'department': departments[1],
            'description': 'Bo mạch vi điều khiển cho các dự án IoT và embedded'
        },
        {
            'name': 'Multimeter Fluke 87V',
            'department': departments[1],
            'description': 'Đồng hồ vạn năng chính xác cao cho đo lường điện'
        },
        
        # Mechanical Department
        {
            'name': 'Máy phay CNC Haas VF-2',
            'department': departments[2],
            'description': 'Máy phay CNC 3 trục cho gia công chi tiết cơ khí chính xác'
        },
        {
            'name': 'Máy in 3D Ultimaker S3',
            'department': departments[2],
            'description': 'Máy in 3D chuyên nghiệp cho tạo mẫu nhanh'
        },
        
        # Chemistry Department
        {
            'name': 'Cân phân tích Sartorius Entris',
            'department': departments[3],
            'description': 'Cân phân tích độ chính xác 0.1mg cho phòng lab hóa học'
        },
        {
            'name': 'Máy quang phổ UV-Vis',
            'department': departments[3],
            'description': 'Thiết bị phân tích quang phổ tử ngoại - khả kiến'
        }
    ]
    
    for equip_data in equipment_data:
        equipment, created = Equipment.objects.get_or_create(
            name=equip_data['name'],
            department=equip_data['department'],
            defaults={'description': equip_data['description']}
        )
        if created:
            print(f"Created equipment: {equipment.name}")
    
    # Create admin user if not exists
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@dnu.edu.vn',
            password='admin123',
            first_name='Quản trị',
            last_name='Hệ thống'
        )
        print("Created admin user: admin/admin123")
    
    # Create sample teacher
    if not User.objects.filter(username='teacher1').exists():
        teacher = User.objects.create_user(
            username='teacher1',
            email='teacher1@dnu.edu.vn',
            password='teacher123',
            first_name='Nguyễn',
            last_name='Văn Giảng',
            is_staff=True
        )
        print("Created teacher user: teacher1/teacher123")
    
    # Create sample student
    if not User.objects.filter(username='student1').exists():
        student = User.objects.create_user(
            username='student1',
            email='student1@dnu.edu.vn',
            password='student123',
            first_name='Trần',
            last_name='Thị Học'
        )
        print("Created student user: student1/student123")
    
    print("\\nSeed data created successfully!")
    print("\\nLogin credentials:")
    print("Admin: admin/admin123")
    print("Teacher: teacher1/teacher123") 
    print("Student: student1/student123")

if __name__ == "__main__":
    create_seed_data()
'''

def create_additional_files():
    """Create additional template and script files"""
    
    files_content = {
        'lab_management/templates/booking/my_bookings.html': MY_BOOKINGS_TEMPLATE,
        'lab_management/templates/booking/create_booking.html': CREATE_BOOKING_TEMPLATE,
        'lab_management/templates/booking/admin_dashboard.html': ADMIN_DASHBOARD_TEMPLATE,
        'lab_management/seed_data.py': SEED_DATA_SCRIPT,
    }
    
    for file_path, content in files_content.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"Created: {file_path}")

if __name__ == "__main__":
    create_additional_files()
    print("Additional templates and scripts created successfully!")
