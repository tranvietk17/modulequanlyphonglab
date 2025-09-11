#!/usr/bin/env python3
"""
Script tích hợp AI thực tế vào hệ thống Django
"""

import os

def create_ai_integration():
    """Tạo tích hợp AI thực tế"""
    
    print("🤖 Tạo tích hợp AI thực tế...")
    
    # 1. Celery tasks for background AI processing
    tasks_content = '''
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import logging

from .models import Equipment, Booking, User
from .ai_services import ai_service

logger = logging.getLogger(__name__)

@shared_task
def generate_equipment_ai_content(equipment_id):
    """Background task để tạo nội dung AI cho thiết bị"""
    try:
        equipment = Equipment.objects.get(id=equipment_id)
        
        # Generate AI description
        if not equipment.ai_description:
            ai_description = ai_service.generate_equipment_description(
                equipment.name, 
                equipment.specifications
            )
            equipment.ai_description = ai_description
        
        # Generate usage tips
        if not equipment.usage_tips:
            usage_tips = ai_service.generate_usage_tips(
                equipment.name,
                equipment.description
            )
            equipment.usage_tips = usage_tips
        
        equipment.save()
        logger.info(f"Generated AI content for equipment {equipment.name}")
        
    except Equipment.DoesNotExist:
        logger.error(f"Equipment {equipment_id} not found")
    except Exception as e:
        logger.error(f"Failed to generate AI content for equipment {equipment_id}: {e}")

@shared_task
def send_booking_notification(booking_id, status_change):
    """Gửi email thông báo với nội dung AI"""
    try:
        booking = Booking.objects.get(id=booking_id)
        
        # Generate AI email content
        email_content = ai_service.generate_smart_email(booking, status_change)
        
        # Email subject
        status_map = {
            'approved': 'Đặt lịch được duyệt',
            'rejected': 'Đặt lịch bị từ chối',
            'completed': 'Đặt lịch hoàn thành',
            'cancelled': 'Đặt lịch bị hủy'
        }
        
        subject = f"[DNU Lab] {status_map.get(status_change, 'Cập nhật đặt lịch')}"
        
        # Send email
        send_mail(
            subject=subject,
            message=email_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.user.email],
            fail_silently=False
        )
        
        logger.info(f"Sent notification email for booking {booking_id}")
        
    except Booking.DoesNotExist:
        logger.error(f"Booking {booking_id} not found")
    except Exception as e:
        logger.error(f"Failed to send notification for booking {booking_id}: {e}")

@shared_task
def analyze_booking_patterns():
    """Phân tích pattern đặt lịch để cải thiện hệ thống"""
    try:
        # Get recent bookings
        recent_bookings = Booking.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).select_related('user', 'equipment')
        
        # Analyze patterns
        patterns = {}
        for booking in recent_bookings:
            key = f"{booking.equipment.department.name}_{booking.user.userprofile.role}"
            if key not in patterns:
                patterns[key] = {
                    'count': 0,
                    'avg_duration': 0,
                    'success_rate': 0,
                    'equipment_types': set()
                }
            
            patterns[key]['count'] += 1
            patterns[key]['avg_duration'] += booking.duration_hours
            patterns[key]['equipment_types'].add(booking.equipment.name)
            
            if booking.status in ['approved', 'completed']:
                patterns[key]['success_rate'] += 1
        
        # Calculate averages
        for pattern in patterns.values():
            if pattern['count'] > 0:
                pattern['avg_duration'] /= pattern['count']
                pattern['success_rate'] = (pattern['success_rate'] / pattern['count']) * 100
                pattern['equipment_types'] = list(pattern['equipment_types'])
        
        # TODO: Store patterns in database or cache for AI recommendations
        logger.info(f"Analyzed {len(patterns)} booking patterns")
        
    except Exception as e:
        logger.error(f"Failed to analyze booking patterns: {e}")

@shared_task
def send_maintenance_reminders():
    """Gửi nhắc nhở bảo trì thiết bị"""
    try:
        # Find equipment needing maintenance
        equipment_list = Equipment.objects.filter(
            status='available',
            warranty_date__lte=timezone.now().date() + timedelta(days=30)
        )
        
        if not equipment_list:
            return
        
        # Get admin users
        admin_users = User.objects.filter(
            userprofile__role__in=['admin', 'teacher']
        )
        
        for equipment in equipment_list:
            # Generate AI maintenance recommendation
            maintenance_advice = ai_service.chat_assistant(
                f"Tạo lời khuyên bảo trì cho thiết bị {equipment.name}. "
                f"Thiết bị đã mua từ {equipment.purchase_date}, "
                f"bảo hành đến {equipment.warranty_date}. "
                f"Mô tả: {equipment.description}"
            )
            
            # Send to admins
            for admin in admin_users:
                send_mail(
                    subject=f"[DNU Lab] Nhắc nhở bảo trì thiết bị {equipment.name}",
                    message=f"""
Thiết bị cần được kiểm tra bảo trì:

Tên thiết bị: {equipment.name}
Mã thiết bị: {equipment.code}
Khoa: {equipment.department.name}
Ngày mua: {equipment.purchase_date}
Hết bảo hành: {equipment.warranty_date}

Lời khuyên từ AI:
{maintenance_advice}

Vui lòng kiểm tra và cập nhật trạng thái thiết bị.
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin.email],
                    fail_silently=True
                )
        
        logger.info(f"Sent maintenance reminders for {len(equipment_list)} equipment")
        
    except Exception as e:
        logger.error(f"Failed to send maintenance reminders: {e}")

@shared_task
def cleanup_old_ai_chats():
    """Dọn dẹp chat AI cũ"""
    try:
        from .models import AIChat
        
        # Delete chats older than 90 days
        old_chats = AIChat.objects.filter(
            created_at__lt=timezone.now() - timedelta(days=90)
        )
        
        count = old_chats.count()
        old_chats.delete()
        
        logger.info(f"Cleaned up {count} old AI chat records")
        
    except Exception as e:
        logger.error(f"Failed to cleanup old AI chats: {e}")
'''
    
    with open('dnu_lab_system/lab_management/tasks.py', 'w', encoding='utf-8') as f:
        f.write(tasks_content.strip())
    
    # 2. Management command for AI operations
    management_dir = 'dnu_lab_system/lab_management/management'
    commands_dir = f'{management_dir}/commands'
    
    os.makedirs(management_dir, exist_ok=True)
    os.makedirs(commands_dir, exist_ok=True)
    
    # Create __init__.py files
    with open(f'{management_dir}/__init__.py', 'w') as f:
        f.write('')
    with open(f'{commands_dir}/__init__.py', 'w') as f:
        f.write('')
    
    # AI management command
    ai_command_content = '''
from django.core.management.base import BaseCommand
from django.utils import timezone
from lab_management.models import Equipment, Booking
from lab_management.ai_services import ai_service
from lab_management.tasks import generate_equipment_ai_content
import time

class Command(BaseCommand):
    help = 'AI operations for lab management system'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--generate-descriptions',
            action='store_true',
            help='Generate AI descriptions for equipment without them'
        )
        parser.add_argument(
            '--analyze-bookings',
            action='store_true',
            help='Analyze booking patterns with AI'
        )
        parser.add_argument(
            '--equipment-id',
            type=int,
            help='Process specific equipment ID'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=10,
            help='Batch size for processing (default: 10)'
        )
    
    def handle(self, *args, **options):
        if options['generate_descriptions']:
            self.generate_descriptions(options)
        
        if options['analyze_bookings']:
            self.analyze_bookings()
    
    def generate_descriptions(self, options):
        """Generate AI descriptions for equipment"""
        self.stdout.write('🤖 Generating AI descriptions for equipment...')
        
        # Filter equipment
        equipment_qs = Equipment.objects.all()
        
        if options['equipment_id']:
            equipment_qs = equipment_qs.filter(id=options['equipment_id'])
        else:
            # Only process equipment without AI descriptions
            equipment_qs = equipment_qs.filter(
                models.Q(ai_description='') | models.Q(ai_description__isnull=True)
            )
        
        total = equipment_qs.count()
        if total == 0:
            self.stdout.write(self.style.WARNING('No equipment found to process'))
            return
        
        self.stdout.write(f'Found {total} equipment to process')
        
        batch_size = options['batch_size']
        processed = 0
        
        for equipment in equipment_qs.iterator(chunk_size=batch_size):
            try:
                self.stdout.write(f'Processing: {equipment.name}')
                
                # Generate description
                if not equipment.ai_description:
                    description = ai_service.generate_equipment_description(
                        equipment.name,
                        equipment.specifications
                    )
                    equipment.ai_description = description
                    self.stdout.write(f'  ✅ Generated description')
                
                # Generate usage tips
                if not equipment.usage_tips:
                    tips = ai_service.generate_usage_tips(
                        equipment.name,
                        equipment.description
                    )
                    equipment.usage_tips = tips
                    self.stdout.write(f'  ✅ Generated usage tips')
                
                equipment.save()
                processed += 1
                
                # Rate limiting
                time.sleep(1)  # Wait 1 second between requests
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Error processing {equipment.name}: {e}')
                )
                continue
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Processed {processed}/{total} equipment')
        )
    
    def analyze_bookings(self):
        """Analyze booking patterns"""
        self.stdout.write('📊 Analyzing booking patterns...')
        
        # Get recent bookings
        recent_bookings = Booking.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=30)
        ).select_related('user', 'equipment', 'equipment__department')
        
        if not recent_bookings.exists():
            self.stdout.write(self.style.WARNING('No recent bookings found'))
            return
        
        # Analyze by department
        dept_stats = {}
        user_stats = {}
        equipment_stats = {}
        
        for booking in recent_bookings:
            dept_name = booking.equipment.department.name
            user_role = booking.user.userprofile.role
            equipment_name = booking.equipment.name
            
            # Department stats
            if dept_name not in dept_stats:
                dept_stats[dept_name] = {'total': 0, 'approved': 0, 'avg_duration': 0}
            dept_stats[dept_name]['total'] += 1
            dept_stats[dept_name]['avg_duration'] += booking.duration_hours
            if booking.status in ['approved', 'completed']:
                dept_stats[dept_name]['approved'] += 1
            
            # User role stats
            if user_role not in user_stats:
                user_stats[user_role] = {'total': 0, 'approved': 0}
            user_stats[user_role]['total'] += 1
            if booking.status in ['approved', 'completed']:
                user_stats[user_role]['approved'] += 1
            
            # Equipment stats
            if equipment_name not in equipment_stats:
                equipment_stats[equipment_name] = {'total': 0, 'avg_duration': 0}
            equipment_stats[equipment_name]['total'] += 1
            equipment_stats[equipment_name]['avg_duration'] += booking.duration_hours
        
        # Calculate averages and display results
        self.stdout.write('\\n📈 Department Statistics:')
        for dept, stats in dept_stats.items():
            avg_duration = stats['avg_duration'] / stats['total']
            approval_rate = (stats['approved'] / stats['total']) * 100
            self.stdout.write(
                f'  {dept}: {stats["total"]} bookings, '
                f'{approval_rate:.1f}% approved, '
                f'{avg_duration:.1f}h avg duration'
            )
        
        self.stdout.write('\\n👥 User Role Statistics:')
        for role, stats in user_stats.items():
            approval_rate = (stats['approved'] / stats['total']) * 100
            self.stdout.write(
                f'  {role}: {stats["total"]} bookings, {approval_rate:.1f}% approved'
            )
        
        self.stdout.write('\\n🔧 Most Popular Equipment:')
        sorted_equipment = sorted(
            equipment_stats.items(), 
            key=lambda x: x[1]['total'], 
            reverse=True
        )[:10]
        
        for equipment, stats in sorted_equipment:
            avg_duration = stats['avg_duration'] / stats['total']
            self.stdout.write(
                f'  {equipment}: {stats["total"]} bookings, {avg_duration:.1f}h avg'
            )
        
        self.stdout.write(self.style.SUCCESS('✅ Analysis complete'))
'''
    
    with open(f'{commands_dir}/ai_operations.py', 'w', encoding='utf-8') as f:
        f.write(ai_command_content.strip())
    
    # 3. Celery configuration
    celery_content = '''
import os
from celery import Celery
from django.conf import settings

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnu_lab_system.settings')

app = Celery('dnu_lab_system')

# Configure Celery using settings from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app configs
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    'analyze-booking-patterns': {
        'task': 'lab_management.tasks.analyze_booking_patterns',
        'schedule': 86400.0,  # Run daily
    },
    'send-maintenance-reminders': {
        'task': 'lab_management.tasks.send_maintenance_reminders',
        'schedule': 604800.0,  # Run weekly
    },
    'cleanup-old-ai-chats': {
        'task': 'lab_management.tasks.cleanup_old_ai_chats',
        'schedule': 86400.0,  # Run daily
    },
}

app.conf.timezone = 'Asia/Ho_Chi_Minh'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
'''
    
    with open('dnu_lab_system/dnu_lab_system/celery.py', 'w', encoding='utf-8') as f:
        f.write(celery_content.strip())
    
    # 4. Update __init__.py for Celery
    init_content = '''
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
'''
    
    with open('dnu_lab_system/dnu_lab_system/__init__.py', 'w', encoding='utf-8') as f:
        f.write(init_content.strip())
    
    # 5. Create translation files
    create_translation_files()
    
    print("✅ Tạo Celery tasks và management commands")
    print("✅ Tạo file dịch đa ngôn ngữ")
    print("\n🎉 Hoàn thành tích hợp AI thực tế!")

def create_translation_files():
    """Tạo file dịch đa ngôn ngữ"""
    
    # Vietnamese translations
    vi_po_content = '''
# Vietnamese translations for DNU Lab System
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Language: vi\\n"

msgid "Lab Room Management System"
msgstr "Hệ thống quản lý phòng lab"

msgid "Equipment"
msgstr "Thiết bị"

msgid "Bookings"
msgstr "Đặt lịch"

msgid "Users"
msgstr "Người dùng"

msgid "Departments"
msgstr "Khoa"

msgid "Available"
msgstr "Có sẵn"

msgid "Maintenance"
msgstr "Bảo trì"

msgid "Broken"
msgstr "Hỏng"

msgid "Reserved"
msgstr "Đã đặt"

msgid "Pending"
msgstr "Chờ duyệt"

msgid "Approved"
msgstr "Đã duyệt"

msgid "Rejected"
msgstr "Từ chối"

msgid "Completed"
msgstr "Hoàn thành"

msgid "Cancelled"
msgstr "Đã hủy"

msgid "Student"
msgstr "Sinh viên"

msgid "Teacher"
msgstr "Giảng viên"

msgid "Admin"
msgstr "Quản trị viên"

msgid "Book Equipment"
msgstr "Đặt lịch thiết bị"

msgid "My Bookings"
msgstr "Lịch của tôi"

msgid "Admin Dashboard"
msgstr "Bảng điều khiển"

msgid "Login"
msgstr "Đăng nhập"

msgid "Register"
msgstr "Đăng ký"

msgid "Logout"
msgstr "Đăng xuất"

msgid "Profile"
msgstr "Hồ sơ"

msgid "Search"
msgstr "Tìm kiếm"

msgid "AI Assistant"
msgstr "Trợ lý AI"

msgid "Hello! How can I help you with the lab system?"
msgstr "Xin chào! Tôi có thể giúp gì cho bạn về hệ thống lab?"

msgid "Type your question..."
msgstr "Nhập câu hỏi..."
'''
    
    with open('dnu_lab_system/locale/vi/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(vi_po_content.strip())
    
    # English translations
    en_po_content = '''
# English translations for DNU Lab System
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Language: en\\n"

msgid "Hệ thống quản lý phòng lab DNU"
msgstr "DNU Lab Room Management System"

msgid "Thiết bị"
msgstr "Equipment"

msgid "Đặt lịch"
msgstr "Bookings"

msgid "Người dùng"
msgstr "Users"

msgid "Khoa"
msgstr "Departments"

msgid "Có sẵn"
msgstr "Available"

msgid "Bảo trì"
msgstr "Maintenance"

msgid "Hỏng"
msgstr "Broken"

msgid "Đã đặt"
msgstr "Reserved"

msgid "Chờ duyệt"
msgstr "Pending"

msgid "Đã duyệt"
msgstr "Approved"

msgid "Từ chối"
msgstr "Rejected"

msgid "Hoàn thành"
msgstr "Completed"

msgid "Đã hủy"
msgstr "Cancelled"

msgid "Sinh viên"
msgstr "Student"

msgid "Giảng viên"
msgstr "Teacher"

msgid "Quản trị viên"
msgstr "Admin"

msgid "Đặt lịch thiết bị"
msgstr "Book Equipment"

msgid "Lịch của tôi"
msgstr "My Bookings"

msgid "Bảng điều khiển"
msgstr "Dashboard"

msgid "Đăng nhập"
msgstr "Login"

msgid "Đăng ký"
msgstr "Register"

msgid "Đăng xuất"
msgstr "Logout"

msgid "Hồ sơ"
msgstr "Profile"

msgid "Tìm kiếm"
msgstr "Search"

msgid "Trợ lý AI"
msgstr "AI Assistant"

msgid "Xin chào! Tôi có thể giúp gì cho bạn về hệ thống lab?"
msgstr "Hello! How can I help you with the lab system?"

msgid "Nhập câu hỏi..."
msgstr "Type your question..."
'''
    
    with open('dnu_lab_system/locale/en/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(en_po_content.strip())

if __name__ == "__main__":
    create_ai_integration()
