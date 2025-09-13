# Django Security Implementation Guide

This document outlines the comprehensive security measures implemented in the Django Library Management System to protect against common web vulnerabilities.

## Overview

The security implementation addresses the following key areas:
- **Cross-Site Scripting (XSS)** prevention
- **Cross-Site Request Forgery (CSRF)** protection
- **SQL Injection** prevention
- **Content Security Policy (CSP)** implementation
- **Secure cookie handling**
- **Input validation and sanitization**
- **Security headers**
- **Logging and monitoring**

## 1. Secure Settings Configuration

### 1.1 Basic Security Settings

```python
# settings.py

# Security: HTTPS and SSL Settings
SECURE_SSL_REDIRECT = False  # Set to True in production with HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security: Cookie Security
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
CSRF_COOKIE_SAMESITE = 'Lax'  # CSRF cookie SameSite attribute
SESSION_COOKIE_SAMESITE = 'Lax'  # Session cookie SameSite attribute
```

### 1.2 Browser Security Headers

```python
# Security: Browser Security Headers
SECURE_BROWSER_XSS_FILTER = True  # Enable XSS filtering in browsers
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME type sniffing
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking attacks
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0  # HTTP Strict Transport Security
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 1.3 Content Security Policy (CSP)

```python
# Security: Content Security Policy (CSP)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")  # Allow inline scripts for Django admin
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # Allow inline styles for Django admin
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)  # Prevent embedding in frames
CSP_BASE_URI = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
```

### 1.4 Enhanced Password Validation

```python
# Security: Password Security
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,  # Minimum 8 characters
        }
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
```

## 2. CSRF Protection Implementation

### 2.1 Template CSRF Tokens

All forms include CSRF tokens to prevent Cross-Site Request Forgery attacks:

```html
<!-- bookshelf/templates/bookshelf/book_form.html -->
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### 2.2 View-Level CSRF Protection

Views use the `@csrf_protect` decorator for additional protection:

```python
from django.views.decorators.csrf import csrf_protect

@login_required
@csrf_protect
def secure_contact_view(request):
    """Secure contact form view with CSRF protection."""
    # View implementation
```

### 2.3 CSRF Settings

```python
# Security: CSRF Protection
CSRF_COOKIE_AGE = 31449600  # 1 year CSRF cookie age
CSRF_USE_SESSIONS = False  # Use cookies for CSRF tokens
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'
```

## 3. SQL Injection Prevention

### 3.1 Django ORM Usage

All database queries use Django ORM with parameterized queries:

```python
# SECURE: Using Django ORM (prevents SQL injection)
books = Book.objects.filter(title__icontains=search_query)

# SECURE: Using Q objects for complex queries
books = Book.objects.filter(
    Q(title__icontains=search_query) | Q(author__icontains=search_query)
)
```

### 3.2 Input Validation

```python
def clean_search_query(self):
    """Security: Validate and sanitize search query."""
    search_query = self.cleaned_data.get('search_query', '').strip()
    
    # Security: Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`', '$']
    for char in dangerous_chars:
        if char in search_query:
            raise forms.ValidationError(f'Search query contains invalid character: {char}')
    
    # Security: Check for SQL injection patterns
    sql_patterns = ['union', 'select', 'insert', 'update', 'delete', 'drop', 'create', 'alter']
    search_lower = search_query.lower()
    for pattern in sql_patterns:
        if pattern in search_lower:
            raise forms.ValidationError('Search query contains invalid content.')
    
    return search_query
```

## 4. XSS Prevention

### 4.1 Template Auto-Escaping

Django templates automatically escape variables:

```html
<!-- SECURE: Django automatically escapes this -->
<h1>{{ book.title }}</h1>
<p>{{ book.author }}</p>
```

### 4.2 Manual Escaping

For additional security, manual escaping is used:

```python
from django.utils.html import escape

# Security: Return sanitized data
data = {
    'id': book.id,
    'title': escape(book.title),  # Security: Escape to prevent XSS
    'author': escape(book.author),  # Security: Escape to prevent XSS
    'publication_year': book.publication_year,
    'created_at': book.created_at.isoformat(),
}
```

### 4.3 Form Validation

```python
def clean_message(self):
    """Security: Validate message field."""
    message = self.cleaned_data.get('message', '').strip()
    
    # Security: Check for potentially dangerous content
    dangerous_patterns = ['<script', 'javascript:', 'onload=', 'onerror=']
    message_lower = message.lower()
    for pattern in dangerous_patterns:
        if pattern in message_lower:
            raise forms.ValidationError('Message contains invalid content.')
    
    return message
```

## 5. Content Security Policy (CSP) Implementation

### 5.1 Custom Middleware

```python
# bookshelf/middleware.py
class SecurityHeadersMiddleware(MiddlewareMixin):
    """Middleware to add security headers including CSP."""
    
    def process_response(self, request, response):
        """Add security headers to the response."""
        # Content Security Policy (CSP)
        if hasattr(settings, 'CSP_DEFAULT_SRC'):
            csp_parts = []
            
            # Build CSP header from settings
            if hasattr(settings, 'CSP_SCRIPT_SRC'):
                csp_parts.append(f"script-src {' '.join(settings.CSP_SCRIPT_SRC)}")
            
            # Set CSP header
            if csp_parts:
                response['Content-Security-Policy'] = '; '.join(csp_parts)
        
        return response
```

### 5.2 Security Headers

```python
# Additional security headers
security_headers = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
}
```

## 6. Input Validation and Sanitization

### 6.1 Form Validation

```python
class ContactForm(forms.Form):
    """Secure contact form with comprehensive validation."""
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'maxlength': '100'})
    )
    
    def clean_name(self):
        """Security: Validate name field."""
        name = self.cleaned_data.get('name', '').strip()
        
        # Security: Check for valid characters
        name_validator = RegexValidator(
            regex=r'^[a-zA-Z\s\-\']+$',
            message='Name can only contain letters, spaces, hyphens, and apostrophes.'
        )
        name_validator(name)
        
        return name
```

### 6.2 View-Level Validation

```python
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def secure_search_view(request):
    """Secure search view with input validation."""
    
    # Security: Validate and sanitize input parameters
    search_query = request.GET.get('search_query', '').strip()
    
    # Security: Input validation
    if search_query:
        # Security: Limit search query length to prevent DoS
        if len(search_query) > 100:
            messages.error(request, 'Search query is too long.')
            logger.warning(f'Long search query attempted: {len(search_query)} characters')
        else:
            # Security: Use Django ORM with parameterized queries
            books = Book.objects.filter(title__icontains=search_query)
```

## 7. Security Logging and Monitoring

### 7.1 Logging Configuration

```python
# Security: Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

### 7.2 Security Event Logging

```python
import logging
logger = logging.getLogger('django.security')

# Log security events
logger.warning(f'Long search query attempted by user {request.user.username}: {len(search_query)} characters')
logger.info(f'User {request.user.username} searched for "{search_query}"')
logger.warning(f'Contact form validation failed for user {request.user.username}: {form.errors}')
```

### 7.3 Suspicious Activity Detection

```python
class SecurityLoggingMiddleware(MiddlewareMixin):
    """Middleware to log security-related events."""
    
    def process_request(self, request):
        """Log potentially suspicious requests."""
        logger = logging.getLogger('django.security')
        
        # Log suspicious user agents
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        suspicious_agents = ['sqlmap', 'nikto', 'nmap', 'scanner']
        if any(agent in user_agent.lower() for agent in suspicious_agents):
            logger.warning(f'Suspicious user agent detected: {user_agent}')
        
        # Log requests with suspicious parameters
        for param, value in request.GET.items():
            if any(pattern in value.lower() for pattern in ['<script', 'javascript:', 'union select']):
                logger.warning(f'Potential XSS/SQL injection attempt in GET parameter {param}: {value}')
```

## 8. Session Security

### 8.1 Session Configuration

```python
# Security: Session Security
SESSION_COOKIE_AGE = 3600  # 1 hour session timeout
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Expire session when browser closes
SESSION_SAVE_EVERY_REQUEST = True  # Save session on every request
```

### 8.2 Cookie Security

```python
# Security: Cookie Security
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
```

## 9. File Upload Security

### 9.1 Upload Limits

```python
# Security: File Upload Security
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB max file size
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB max data upload
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000  # Max number of form fields
```

### 9.2 Media File Security

```python
# Security: Media Files Security
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
```

## 10. Testing Security Measures

### 10.1 Manual Testing Checklist

#### CSRF Protection Testing
- [ ] Test forms without CSRF tokens (should fail)
- [ ] Test forms with valid CSRF tokens (should work)
- [ ] Test cross-origin form submissions

#### XSS Prevention Testing
- [ ] Test input fields with script tags
- [ ] Test output escaping in templates
- [ ] Test JavaScript injection attempts

#### SQL Injection Testing
- [ ] Test search fields with SQL keywords
- [ ] Test parameter manipulation
- [ ] Test union-based injection attempts

#### Input Validation Testing
- [ ] Test fields with invalid characters
- [ ] Test fields exceeding length limits
- [ ] Test fields with special characters

### 10.2 Security Headers Testing

Use browser developer tools or online tools to verify:
- [ ] Content-Security-Policy header
- [ ] X-Frame-Options header
- [ ] X-Content-Type-Options header
- [ ] X-XSS-Protection header

### 10.3 Logging Verification

Check security logs for:
- [ ] Suspicious user agents
- [ ] Failed validation attempts
- [ ] Long input attempts
- [ ] SQL injection patterns

## 11. Production Deployment Security

### 11.1 Environment Variables

```python
# Use environment variables for sensitive settings
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
```

### 11.2 Production Settings

```python
# Production-specific security settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

## 12. Security Best Practices

### 12.1 Development Guidelines

1. **Always use Django forms** for input validation
2. **Never use string formatting** in database queries
3. **Always escape user input** in templates
4. **Use HTTPS in production**
5. **Regularly update dependencies**
6. **Monitor security logs**
7. **Test security measures regularly**

### 12.2 Code Review Checklist

- [ ] All forms include CSRF tokens
- [ ] All database queries use Django ORM
- [ ] All user input is validated
- [ ] All output is properly escaped
- [ ] Security headers are configured
- [ ] Logging is implemented for security events
- [ ] File uploads are properly validated
- [ ] Session security is configured

## 13. Security Monitoring

### 13.1 Regular Security Tasks

1. **Review security logs** weekly
2. **Update dependencies** monthly
3. **Test security measures** quarterly
4. **Review user permissions** regularly
5. **Monitor for suspicious activity**

### 13.2 Incident Response

1. **Identify the threat**
2. **Contain the incident**
3. **Investigate the scope**
4. **Implement fixes**
5. **Update security measures**
6. **Document lessons learned**

This comprehensive security implementation provides multiple layers of protection against common web vulnerabilities while maintaining usability and performance.
