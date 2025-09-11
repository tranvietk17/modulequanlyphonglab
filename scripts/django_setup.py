"""
Django Lab Management System - Complete Setup
Hệ thống Quản lý Phòng Lab DNU
"""

# dnu_lab_system/dnu_lab_system/settings.py
SETTINGS_PY = '''
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')

DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lab_management',
    'django_extensions',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # For i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'dnu_lab_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'dnu_lab_system.wsgi.application'

# Database
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'vi')
TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Ho_Chi_Minh')
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('vi', 'Tiếng Việt'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Authentication
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# AI Integration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Celery Configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Debug Toolbar
if DEBUG:
    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
    ]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'lab_management': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
'''

# dnu_lab_system/dnu_lab_system/urls.py
MAIN_URLS_PY = '''
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lab_management.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''

# dnu_lab_system/lab_management/models.py
MODELS_PY = '''
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Department(models.Model):
    """Model cho phòng ban/khoa"""
    name = models.CharField(max_length=100, verbose_name=_("Tên phòng ban"))
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Mã phòng ban"))
    description = models.TextField(blank=True, verbose_name=_("Mô tả"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Phòng ban")
        verbose_name_plural = _("Phòng ban")
        ordering = ['name']
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Mở rộng thông tin người dùng"""
    ROLE_CHOICES = [
        ('student', _('Sinh viên')),
        ('teacher', _('Giảng viên')),
        ('admin', _('Quản trị viên')),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=20, blank=True, verbose_name=_("Mã sinh viên"))
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, verbose_name=_("Số điện thoại"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Hồ sơ người dùng")
        verbose_name_plural = _("Hồ sơ người dùng")
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

class Equipment(models.Model):
    """Model cho thiết bị"""
    STATUS_CHOICES = [
        ('available', _('Có sẵn')),
        ('maintenance', _('Bảo trì')),
        ('broken', _('Hỏng')),
        ('reserved', _('Đã đặt')),
    ]
    
    name = models.CharField(max_length=200, verbose_name=_("Tên thiết bị"))
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Mã thiết bị"))
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name=_("Phòng ban"))
    description = models.TextField(blank=True, verbose_name=_("Mô tả"))
    specifications = models.TextField(blank=True, verbose_name=_("Thông số kỹ thuật"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name=_("Trạng thái"))
    image = models.ImageField(upload_to='equipment/', blank=True, null=True, verbose_name=_("Hình ảnh"))
    purchase_date = models.DateField(null=True, blank=True, verbose_name=_("Ngày mua"))
    warranty_date = models.DateField(null=True, blank=True, verbose_name=_("Hết bảo hành"))
    
    # AI-generated fields
    ai_description = models.TextField(blank=True, verbose_name=_("Mô tả AI"))
    usage_tips = models.TextField(blank=True, verbose_name=_("Mẹo sử dụng"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Thiết bị")
        verbose_name_plural = _("Thiết bị")
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def is_available(self):
        return self.status == 'available'
    
    @property
    def duration_hours(self):
        """Calculate duration in hours"""
        if hasattr(self, 'pickup_time') and hasattr(self, 'return_time'):
            delta = self.return_time - self.pickup_time
            return delta.total_seconds() / 3600
        return 0

class Booking(models.Model):
    """Model cho đơn đặt lịch"""
    STATUS_CHOICES = [
        ('pending', _('Đang chờ duyệt')),
        ('approved', _('Đã được duyệt')),
        ('rejected', _('Bị từ chối')),
        ('completed', _('Hoàn thành')),
        ('cancelled', _('Đã hủy')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Người dùng"))
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name=_("Thiết bị"))
    pickup_time = models.DateTimeField(verbose_name=_("Thời gian nhận"))
    return_time = models.DateTimeField(verbose_name=_("Thời gian trả"))
    purpose = models.TextField(verbose_name=_("Mục đích sử dụng"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_("Trạng thái"))
    notes = models.TextField(blank=True, verbose_name=_("Ghi chú từ giảng viên"))
    risk_assessment = models.TextField(blank=True, verbose_name=_("Đánh giá rủi ro AI"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='approved_bookings', verbose_name=_("Được duyệt bởi"))
    
    class Meta:
        verbose_name = _("Đơn đặt lịch")
        verbose_name_plural = _("Đơn đặt lịch")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.equipment.name} - {self.get_status_display()}"
    
    @property
    def duration_hours(self):
        """Calculate booking duration in hours"""
        delta = self.return_time - self.pickup_time
        return delta.total_seconds() / 3600
    
    def is_conflicting(self):
        """Kiểm tra xung đột thời gian với các đơn khác"""
        conflicting_bookings = Booking.objects.filter(
            equipment=self.equipment,
            status__in=['approved', 'pending'],
            pickup_time__lt=self.return_time,
            return_time__gt=self.pickup_time
        ).exclude(id=self.id)
        return conflicting_bookings.exists()

class AIChat(models.Model):
    """Model cho chat AI"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(verbose_name=_("Tin nhắn"))
    response = models.TextField(verbose_name=_("Phản hồi"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Chat AI")
        verbose_name_plural = _("Chat AI")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
'''

# dnu_lab_system/lab_management/views.py
VIEWS_PY = '''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from .models import Equipment, Booking, Department, UserProfile, AIChat
from .forms import BookingForm
import json

def home(request):
    """Trang chủ"""
    departments = Department.objects.all()
    recent_bookings = Booking.objects.filter(status='approved')[:5]
    context = {
        'departments': departments,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'lab_management/home.html', context)

@login_required
def equipment_list(request):
    """Danh sách thiết bị theo phòng ban"""
    department_id = request.GET.get('department')
    equipments = Equipment.objects.filter(status='available')
    
    if department_id:
        equipments = equipments.filter(department_id=department_id)
    
    departments = Department.objects.all()
    context = {
        'equipments': equipments,
        'departments': departments,
        'selected_department': int(department_id) if department_id else None,
    }
    return render(request, 'lab_management/equipment_list.html', context)

@login_required
def create_booking(request, equipment_id):
    """Tạo đơn đặt lịch mới"""
    equipment = get_object_or_404(Equipment, id=equipment_id, status='available')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.equipment = equipment
            
            # Kiểm tra xung đột thời gian
            if booking.is_conflicting():
                messages.error(request, 'Thiết bị đã được đặt trong khoảng thời gian này!')
                return render(request, 'lab_management/create_booking.html', {
                    'form': form, 'equipment': equipment
                })
            
            booking.save()
            messages.success(request, 'Đơn đặt lịch đã được gửi thành công!')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    
    return render(request, 'lab_management/create_booking.html', {
        'form': form, 
        'equipment': equipment
    })

@login_required
def my_bookings(request):
    """Danh sách đơn đặt lịch của người dùng"""
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'lab_management/my_bookings.html', {'bookings': bookings})

def is_teacher(user):
    """Kiểm tra user có phải là giảng viên (staff)"""
    return user.is_staff

@login_required
@user_passes_test(is_teacher)
def admin_dashboard(request):
    """Dashboard cho giảng viên"""
    pending_bookings = Booking.objects.filter(status='pending').count()
    total_bookings = Booking.objects.count()
    total_equipment = Equipment.objects.count()
    total_users = UserProfile.objects.count()
    
    context = {
        'pending_bookings': pending_bookings,
        'total_bookings': total_bookings,
        'total_equipment': total_equipment,
        'total_users': total_users,
    }
    return render(request, 'lab_management/admin_dashboard.html', context)

@login_required
@user_passes_test(is_teacher)
def pending_bookings(request):
    """Danh sách đơn chờ duyệt"""
    bookings = Booking.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'lab_management/pending_bookings.html', {'bookings': bookings})

@login_required
@user_passes_test(is_teacher)
def approve_booking(request, booking_id):
    """Phê duyệt đơn đặt lịch"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')
        
        if action == 'approve':
            booking.status = 'approved'
            booking.approved_by = request.user
            booking.notes = notes
            booking.save()
            
            # Gửi email thông báo
            try:
                send_mail(
                    subject=f'Đơn đặt lịch thiết bị {booking.equipment.name} đã được phê duyệt',
                    message=f'''
Xin chào {booking.user.get_full_name() or booking.user.username},

Đơn đặt lịch thiết bị của bạn đã được phê duyệt:
- Thiết bị: {booking.equipment.name}
- Thời gian nhận: {booking.pickup_time.strftime("%d/%m/%Y %H:%M")}
- Thời gian trả: {booking.return_time.strftime("%d/%m/%Y %H:%M")}
- Ghi chú: {notes}

Vui lòng đến đúng giờ để nhận thiết bị.

Trân trọng,
Hệ thống Quản lý Phòng Lab DNU
                    ''',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[booking.user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Đơn đặt lịch đã được phê duyệt!')
            
        elif action == 'reject':
            booking.status = 'rejected'
            booking.notes = notes
            booking.save()
            messages.success(request, 'Đơn đặt lịch đã bị từ chối!')
        
        return redirect('pending_bookings')
    
    return render(request, 'lab_management/approve_booking.html', {'booking': booking})

@login_required
@user_passes_test(is_teacher)
def all_bookings(request):
    """Tất cả đơn đặt lịch"""
    status_filter = request.GET.get('status', '')
    bookings = Booking.objects.all().order_by('-created_at')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'status_choices': Booking.STATUS_CHOICES,
    }
    return render(request, 'lab_management/all_bookings.html', context)

@login_required
def ai_chat(request):
    """Chat AI"""
    if request.method == 'POST':
        message = request.POST.get('message')
        response = "AI response here"  # Placeholder for AI response
        ai_chat = AIChat.objects.create(user=request.user, message=message, response=response)
        return JsonResponse({'response': response})
    
    return render(request, 'lab_management/ai_chat.html')
'''

# dnu_lab_system/lab_management/forms.py
FORMS_PY = '''
from django import forms
from .models import Booking
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pickup_time', 'return_time', 'purpose']
        widgets = {
            'pickup_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'return_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'purpose': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Mô tả mục đích sử dụng thiết bị...'}
            ),
        }
        labels = {
            'pickup_time': 'Thời gian nhận',
            'return_time': 'Thời gian trả',
            'purpose': 'Mục đích sử dụng',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        pickup_time = cleaned_data.get('pickup_time')
        return_time = cleaned_data.get('return_time')
        
        if pickup_time and return_time:
            if pickup_time >= return_time:
                raise forms.ValidationError('Thời gian trả phải sau thời gian nhận!')
            
            if pickup_time <= timezone.now():
                raise forms.ValidationError('Thời gian nhận phải trong tương lai!')
        
        return cleaned_data
'''

# dnu_lab_system/lab_management/urls.py
URLS_PY = '''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('booking/create/<int:equipment_id>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('ai-chat/', views.ai_chat, name='ai_chat'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('pending-bookings/', views.pending_bookings, name='pending_bookings'),
    path('approve-booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('all-bookings/', views.all_bookings, name='all_bookings'),
]
'''

# dnu_lab_system/lab_management/admin.py
ADMIN_PY = '''
from django.contrib import admin
from .models import Department, Equipment, Booking, UserProfile, AIChat

admin.site.register(Department)
admin.site.register(Equipment)
admin.site.register(Booking)
admin.site.register(UserProfile)
admin.site.register(AIChat)
'''

# dnu_lab_system/lab_management/ai_services.py
AI_SERVICES_PY = '''
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_ai_description(equipment_name):
    """Generate AI description for equipment"""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Write a description for the equipment: {equipment_name}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_usage_tips(equipment_name):
    """Generate usage tips for equipment"""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Provide usage tips for the equipment: {equipment_name}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

def generate_risk_assessment(booking_purpose):
    """Generate risk assessment for booking purpose"""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Assess the risk for the booking purpose: {booking_purpose}",
        max_tokens=100
    )
    return response.choices[0].text.strip()
'''

def create_django_files():
    """Create all Django files"""
    
    files_content = {
        'dnu_lab_system/dnu_lab_system/settings.py': SETTINGS_PY,
        'dnu_lab_system/dnu_lab_system/urls.py': MAIN_URLS_PY,
        'dnu_lab_system/lab_management/models.py': MODELS_PY,
        'dnu_lab_system/lab_management/views.py': VIEWS_PY,
        'dnu_lab_system/lab_management/forms.py': FORMS_PY,
        'dnu_lab_system/lab_management/urls.py': URLS_PY,
        'dnu_lab_system/lab_management/admin.py': ADMIN_PY,
        'dnu_lab_system/lab_management/ai_services.py': AI_SERVICES_PY,
    }
    
    for file_path, content in files_content.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"Created: {file_path}")
    
    # Create __init__.py files
    init_files = [
        'dnu_lab_system/dnu_lab_system/__init__.py',
        'dnu_lab_system/lab_management/__init__.py',
        'dnu_lab_system/lab_management/migrations/__init__.py',
        'dnu_lab_system/lab_management/management/__init__.py',
        'dnu_lab_system/lab_management/management/commands/__init__.py',
    ]
    
    for init_file in init_files:
        os.makedirs(os.path.dirname(init_file), exist_ok=True)
        with open(init_file, 'w') as f:
            f.write('')
        print(f"Created: {init_file}")

if __name__ == "__main__":
    create_django_files()
    print("\nDjango project files created successfully!")
    print("\nNext steps:")
    print("1. cd dnu_lab_system")
    print("2. python manage.py makemigrations")
    print("3. python manage.py migrate")
    print("4. python manage.py createsuperuser")
    print("5. python manage.py runserver")
