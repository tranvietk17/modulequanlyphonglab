"""
Create user authentication system for the Lab Management System
"""

import os

# users/views.py
USERS_VIEWS_PY = '''
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from .forms import StudentRegistrationForm, UserProfileForm
from lab_management.models import UserProfile, Department

def register(request):
    """Đăng ký tài khoản sinh viên"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                role='student',
                student_id=form.cleaned_data.get('student_id', ''),
                department_id=form.cleaned_data.get('department'),
                phone=form.cleaned_data.get('phone', '')
            )
            
            username = form.cleaned_data.get('username')
            messages.success(request, _('Tài khoản {} đã được tạo thành công!').format(username))
            login(request, user)
            return redirect('home')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    """Xem và chỉnh sửa hồ sơ"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, role='student')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            
            # Update user info
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            
            messages.success(request, _('Hồ sơ đã được cập nhật thành công!'))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'registration/profile.html', {
        'form': form,
        'profile': profile
    })
'''

# users/forms.py
USERS_FORMS_PY = '''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from lab_management.models import UserProfile, Department

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_('Email'))
    first_name = forms.CharField(max_length=30, required=True, label=_('Họ'))
    last_name = forms.CharField(max_length=30, required=True, label=_('Tên'))
    student_id = forms.CharField(max_length=20, required=False, label=_('Mã sinh viên'))
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label=_('Khoa'),
        empty_label=_('Chọn khoa')
    )
    phone = forms.CharField(max_length=15, required=False, label=_('Số điện thoại'))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'student_id', 'department', 'phone', 'password1', 'password2')
        labels = {
            'username': _('Tên đăng nhập'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['password1'].label = _('Mật khẩu')
        self.fields['password2'].label = _('Xác nhận mật khẩu')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label=_('Họ'))
    last_name = forms.CharField(max_length=30, required=True, label=_('Tên'))
    email = forms.EmailField(required=True, label=_('Email'))
    
    class Meta:
        model = UserProfile
        fields = ['student_id', 'department', 'phone']
        labels = {
            'student_id': _('Mã sinh viên'),
            'department': _('Khoa'),
            'phone': _('Số điện thoại'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
'''

# users/urls.py
USERS_URLS_PY = '''
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
]
'''

# Login template
LOGIN_TEMPLATE = '''
{% extends 'base.html' %}

{% block title %}Đăng nhập{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header text-center">
                <h4><i class="fas fa-sign-in-alt me-2"></i>Đăng nhập</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label for="{{ form.username.id_for_label }}" class="form-label">Tên đăng nhập</label>
                        {{ form.username }}
                        {% if form.username.errors %}
                            <div class="text-danger">{{ form.username.errors }}</div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.password.id_for_label }}" class="form-label">Mật khẩu</label>
                        {{ form.password }}
                        {% if form.password.errors %}
                            <div class="text-danger">{{ form.password.errors }}</div>
                        {% endif %}
                    </div>
                    {% if form.non_field_errors %}
                        <div class="alert alert-danger">{{ form.non_field_errors }}</div>
                    {% endif %}
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-sign-in-alt me-2"></i>Đăng nhập
                        </button>
                    </div>
                </form>
                <hr>
                <div class="text-center">
                    <p>Chưa có tài khoản? <a href="{% url 'register' %}">Đăng ký ngay</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# Register template
REGISTER_TEMPLATE = '''
{% extends 'base.html' %}

{% block title %}Đăng ký{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header text-center">
                <h4><i class="fas fa-user-plus me-2"></i>Đăng ký tài khoản sinh viên</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="{{ form.first_name.id_for_label }}" class="form-label">{{ form.first_name.label }}</label>
                            {{ form.first_name }}
                            {% if form.first_name.errors %}
                                <div class="text-danger">{{ form.first_name.errors }}</div>
                            {% endif %}
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="{{ form.last_name.id_for_label }}" class="form-label">{{ form.last_name.label }}</label>
                            {{ form.last_name }}
                            {% if form.last_name.errors %}
                                <div class="text-danger">{{ form.last_name.errors }}</div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.username.id_for_label }}" class="form-label">{{ form.username.label }}</label>
                        {{ form.username }}
                        {% if form.username.errors %}
                            <div class="text-danger">{{ form.username.errors }}</div>
                        {% endif %}
                        <div class="form-text">Tên đăng nhập phải duy nhất và không chứa ký tự đặc biệt.</div>
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.email.id_for_label }}" class="form-label">Email</label>
                        {{ form.email }}
                        {% if form.email.errors %}
                            <div class="text-danger">{{ form.email.errors }}</div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.student_id.id_for_label }}" class="form-label">{{ form.student_id.label }}</label>
                        {{ form.student_id }}
                        {% if form.student_id.errors %}
                            <div class="text-danger">{{ form.student_id.errors }}</div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.department.id_for_label }}" class="form-label">{{ form.department.label }}</label>
                        {{ form.department }}
                        {% if form.department.errors %}
                            <div class="text-danger">{{ form.department.errors }}</div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.phone.id_for_label }}" class="form-label">{{ form.phone.label }}</label>
                        {{ form.phone }}
                        {% if form.phone.errors %}
                            <div class="text-danger">{{ form.phone.errors }}</div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.password1.id_for_label }}" class="form-label">{{ form.password1.label }}</label>
                        {{ form.password1 }}
                        {% if form.password1.errors %}
                            <div class="text-danger">{{ form.password1.errors }}</div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        <label for="{{ form.password2.id_for_label }}" class="form-label">{{ form.password2.label }}</label>
                        {{ form.password2 }}
                        {% if form.password2.errors %}
                            <div class="text-danger">{{ form.password2.errors }}</div>
                        {% endif %}
                    </div>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-success">
                            <i class="fas fa-user-plus me-2"></i>Đăng ký
                        </button>
                    </div>
                </form>
                <hr>
                <div class="text-center">
                    <p>Đã có tài khoản? <a href="{% url 'login' %}">Đăng nhập</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

def create_user_files():
    """Create user authentication files"""
    
    files_content = {
        'lab_management/users/views.py': USERS_VIEWS_PY,
        'lab_management/users/forms.py': USERS_FORMS_PY,
        'lab_management/users/urls.py': USERS_URLS_PY,
        'lab_management/templates/users/login.html': LOGIN_TEMPLATE,
        'lab_management/templates/users/register.html': REGISTER_TEMPLATE,
    }
    
    for file_path, content in files_content.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"Created: {file_path}")

if __name__ == "__main__":
    create_user_files()
    print("User authentication system created successfully!")
