"""
Create HTML templates for the Lab Management System
"""

import os

# Base template
BASE_TEMPLATE = '''
{% load i18n %}
<!DOCTYPE html>
<html lang="{% get_current_language as LANGUAGE_CODE %}{{ LANGUAGE_CODE }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% trans "Hệ thống quản lý phòng lab DNU" %}{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .navbar-brand {
            font-weight: bold;
            color: #0d6efd !important;
        }
        .card {
            box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
            border: 1px solid rgba(0, 0, 0, 0.125);
        }
        .status-pending { color: #ffc107; }
        .status-approved { color: #198754; }
        .status-rejected { color: #dc3545; }
        .status-completed { color: #6c757d; }
        .ai-chat-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
        }
        .ai-chat-button {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(45deg, #007bff, #0056b3);
            border: none;
            color: white;
            font-size: 24px;
            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
            transition: all 0.3s ease;
        }
        .ai-chat-button:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4);
        }
        .ai-chat-panel {
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            display: none;
            position: absolute;
            bottom: 80px;
            right: 0;
        }
        .language-switcher {
            margin-left: 10px;
        }
        footer {
            background-color: #f8f9fa;
            margin-top: 50px;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">
                <i class="fas fa-flask me-2"></i>Lab DNU
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'home' %}">{% trans "Trang chủ" %}</a>
                    </li>
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'equipment_list' %}">{% trans "Thiết bị" %}</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'my_bookings' %}">{% trans "Đơn của tôi" %}</a>
                        </li>
                        {% if user.is_staff %}
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                    {% trans "Quản trị" %}
                                </a>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="{% url 'admin_dashboard' %}">Dashboard</a></li>
                                    <li><a class="dropdown-item" href="{% url 'pending_bookings' %}">{% trans "Đơn chờ duyệt" %}</a></li>
                                    <li><a class="dropdown-item" href="{% url 'all_bookings' %}">{% trans "Tất cả đơn" %}</a></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li><a class="dropdown-item" href="/admin/">Admin Panel</a></li>
                                </ul>
                            </li>
                        {% endif %}
                    {% endif %}
                </ul>
                <ul class="navbar-nav">
                    <!-- Language Switcher -->
                    <li class="nav-item dropdown language-switcher">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-globe me-1"></i>
                            {% get_current_language as LANGUAGE_CODE %}
                            {% if LANGUAGE_CODE == 'vi' %}Tiếng Việt{% else %}English{% endif %}
                        </a>
                        <ul class="dropdown-menu">
                            <li>
                                <form action="{% url 'set_language' %}" method="post" class="d-inline">
                                    {% csrf_token %}
                                    <input name="next" type="hidden" value="{{ request.get_full_path|slice:'3:' }}">
                                    <button type="submit" name="language" value="vi" class="dropdown-item">
                                        🇻🇳 Tiếng Việt
                                    </button>
                                </form>
                            </li>
                            <li>
                                <form action="{% url 'set_language' %}" method="post" class="d-inline">
                                    {% csrf_token %}
                                    <input name="next" type="hidden" value="{{ request.get_full_path|slice:'3:' }}">
                                    <button type="submit" name="language" value="en" class="dropdown-item">
                                        🇺🇸 English
                                    </button>
                                </form>
                            </li>
                        </ul>
                    </li>
                    
                    {% if user.is_authenticated %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                <i class="fas fa-user me-1"></i>{{ user.get_full_name|default:user.username }}
                            </a>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="{% url 'profile' %}">{% trans "Hồ sơ" %}</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="{% url 'logout' %}">{% trans "Đăng xuất" %}</a></li>
                            </ul>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'login' %}">{% trans "Đăng nhập" %}</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'register' %}">{% trans "Đăng ký" %}</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}
        {% endblock %}
    </main>

    <!-- AI Chat Widget -->
    {% if user.is_authenticated %}
    <div class="ai-chat-widget">
        <div class="ai-chat-panel" id="aiChatPanel">
            <div class="card h-100">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0">
                        <i class="fas fa-robot me-2"></i>{% trans "Trợ lý AI" %}
                        <button type="button" class="btn-close btn-close-white float-end" onclick="toggleAIChat()"></button>
                    </h6>
                </div>
                <div class="card-body d-flex flex-column p-0">
                    <div class="flex-grow-1 p-3" id="chatMessages" style="overflow-y: auto; max-height: 350px;">
                        <div class="alert alert-info mb-2">
                            <small>{% trans "Xin chào! Tôi có thể giúp gì cho bạn về hệ thống lab?" %}</small>
                        </div>
                    </div>
                    <div class="border-top p-3">
                        <div class="input-group">
                            <input type="text" class="form-control" id="chatInput" placeholder="{% trans 'Nhập câu hỏi...' %}">
                            <button class="btn btn-primary" onclick="sendMessage()">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <button class="ai-chat-button" onclick="toggleAIChat()">
            <i class="fas fa-robot"></i>
        </button>
    </div>
    {% endif %}

    <footer class="py-4 mt-5">
        <div class="container text-center">
            <p class="mb-0">&copy; 2024 {% trans "Hệ thống Quản lý Phòng Lab DNU" %}. All rights reserved.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function toggleAIChat() {
            const panel = document.getElementById('aiChatPanel');
            panel.style.display = panel.style.display === 'none' || panel.style.display === '' ? 'block' : 'none';
        }

        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (!message) return;

            const messagesDiv = document.getElementById('chatMessages');
            
            // Add user message
            messagesDiv.innerHTML += `
                <div class="mb-2 text-end">
                    <div class="bg-primary text-white rounded p-2 d-inline-block" style="max-width: 80%;">
                        <small>${message}</small>
                    </div>
                </div>
            `;

            input.value = '';
            messagesDiv.scrollTop = messagesDiv.scrollHeight;

            // Send to AI
            fetch('{% url "ai_chat" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                messagesDiv.innerHTML += `
                    <div class="mb-2">
                        <div class="bg-light rounded p-2 d-inline-block" style="max-width: 80%;">
                            <small><i class="fas fa-robot me-1"></i>${data.response}</small>
                        </div>
                    </div>
                `;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            })
            .catch(error => {
                console.error('Error:', error);
                messagesDiv.innerHTML += `
                    <div class="mb-2">
                        <div class="bg-danger text-white rounded p-2 d-inline-block" style="max-width: 80%;">
                            <small>{% trans "Xin lỗi, có lỗi xảy ra. Vui lòng thử lại." %}</small>
                        </div>
                    </div>
                `;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            });
        }

        // Send message on Enter key
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
    {% block extra_js %}{% endblock %}
</body>
</html>
'''

# Home template
HOME_TEMPLATE = '''
{% extends 'base.html' %}

{% block title %}Trang chủ - Hệ thống Quản lý Phòng Lab DNU{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="jumbotron bg-primary text-white p-5 rounded mb-4">
            <h1 class="display-4">Chào mừng đến với Lab DNU</h1>
            <p class="lead">Hệ thống quản lý đặt lịch thiết bị phòng thí nghiệm hiện đại và tiện lợi.</p>
            {% if not user.is_authenticated %}
                <a class="btn btn-light btn-lg" href="{% url 'register' %}" role="button">
                    <i class="fas fa-user-plus me-2"></i>Đăng ký ngay
                </a>
            {% else %}
                <a class="btn btn-light btn-lg" href="{% url 'equipment_list' %}" role="button">
                    <i class="fas fa-search me-2"></i>Tìm thiết bị
                </a>
            {% endif %}
        </div>

        <h3>Các phòng ban</h3>
        <div class="row">
            {% for department in departments %}
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="fas fa-building me-2"></i>{{ department.name }}
                            </h5>
                            <p class="card-text">{{ department.description|default:"Mô tả sẽ được cập nhật sớm." }}</p>
                            {% if user.is_authenticated %}
                                <a href="{% url 'equipment_list' %}?department={{ department.id }}" class="btn btn-primary btn-sm">
                                    Xem thiết bị
                                </a>
                            {% endif %}
                        </div>
                    </div>
                </div>
            {% empty %}
                <div class="col-12">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>Chưa có phòng ban nào được thêm.
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>

    <div class="col-lg-4">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-clock me-2"></i>Đặt lịch gần đây</h5>
            </div>
            <div class="card-body">
                {% for booking in recent_bookings %}
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <div>
                            <strong>{{ booking.equipment.name }}</strong><br>
                            <small class="text-muted">{{ booking.student.get_full_name|default:booking.student.username }}</small>
                        </div>
                        <span class="badge bg-success">Đã duyệt</span>
                    </div>
                    {% if not forloop.last %}<hr>{% endif %}
                {% empty %}
                    <p class="text-muted">Chưa có đặt lịch nào.</p>
                {% endfor %}
            </div>
        </div>

        <div class="card mt-4">
            <div class="card-header">
                <h5><i class="fas fa-question-circle me-2"></i>Hướng dẫn sử dụng</h5>
            </div>
            <div class="card-body">
                <ol>
                    <li>Đăng ký tài khoản sinh viên</li>
                    <li>Chọn thiết bị cần mượn</li>
                    <li>Điền thông tin đặt lịch</li>
                    <li>Chờ giảng viên phê duyệt</li>
                    <li>Nhận thiết bị đúng giờ</li>
                </ol>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# Equipment list template
EQUIPMENT_LIST_TEMPLATE = '''
{% extends 'base.html' %}

{% block title %}Danh sách thiết bị{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2><i class="fas fa-microscope me-2"></i>Danh sách thiết bị</h2>
    
    <form method="get" class="d-flex">
        <select name="department" class="form-select me-2" onchange="this.form.submit()">
            <option value="">Tất cả phòng ban</option>
            {% for department in departments %}
                <option value="{{ department.id }}" {% if selected_department == department.id %}selected{% endif %}>
                    {{ department.name }}
                </option>
            {% endfor %}
        </select>
    </form>
</div>

<div class="row">
    {% for equipment in equipments %}
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card h-100">
                {% if equipment.image %}
                    <img src="{{ equipment.image.url }}" class="card-img-top" style="height: 200px; object-fit: cover;">
                {% else %}
                    <div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 200px;">
                        <i class="fas fa-image fa-3x text-muted"></i>
                    </div>
                {% endif %}
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">{{ equipment.name }}</h5>
                    <p class="card-text">
                        <small class="text-muted">
                            <i class="fas fa-building me-1"></i>{{ equipment.department.name }}
                        </small>
                    </p>
                    <p class="card-text flex-grow-1">{{ equipment.description|default:"Mô tả sẽ được cập nhật sớm." }}</p>
                    <div class="mt-auto">
                        {% if equipment.is_available %}
                            <span class="badge bg-success mb-2">Có sẵn</span><br>
                            <a href="{% url 'create_booking' equipment.id %}" class="btn btn-primary">
                                <i class="fas fa-calendar-plus me-1"></i>Đặt lịch
                            </a>
                        {% else %}
                            <span class="badge bg-danger mb-2">Không có sẵn</span><br>
                            <button class="btn btn-secondary" disabled>Không thể đặt</button>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    {% empty %}
        <div class="col-12">
            <div class="alert alert-info text-center">
                <i class="fas fa-info-circle me-2"></i>
                {% if selected_department %}
                    Không có thiết bị nào trong phòng ban này.
                {% else %}
                    Chưa có thiết bị nào được thêm.
                {% endif %}
            </div>
        </div>
    {% endfor %}
</div>
{% endblock %}
'''

def create_template_files():
    """Create all template files"""
    
    templates = {
        'lab_management/templates/base.html': BASE_TEMPLATE,
        'lab_management/templates/booking/home.html': HOME_TEMPLATE,
        'lab_management/templates/booking/equipment_list.html': EQUIPMENT_LIST_TEMPLATE,
    }
    
    for file_path, content in templates.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"Created template: {file_path}")

if __name__ == "__main__":
    create_template_files()
    print("Template files created successfully!")
