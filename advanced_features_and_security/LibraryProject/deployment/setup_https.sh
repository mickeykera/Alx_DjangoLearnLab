#!/bin/bash
# HTTPS Setup Script for Django Library Management System
# This script helps set up HTTPS for the Django application

set -e  # Exit on any error

echo "🔒 Django HTTPS Security Setup Script"
echo "====================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root for security reasons"
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check required tools
echo "📋 Checking required tools..."

if ! command_exists openssl; then
    echo "❌ OpenSSL is required but not installed"
    exit 1
fi

if ! command_exists nginx; then
    echo "⚠️  Nginx not found. You may need to install it for production deployment"
fi

if ! command_exists certbot; then
    echo "⚠️  Certbot not found. Install it for Let's Encrypt certificates:"
    echo "   sudo apt-get install certbot python3-certbot-nginx"
fi

echo "✅ Required tools check completed"

# Create SSL directory
echo "📁 Creating SSL directory..."
mkdir -p ssl
chmod 700 ssl

# Generate self-signed certificate for development
echo "🔐 Generating self-signed SSL certificate for development..."
if [ ! -f ssl/certificate.crt ] || [ ! -f ssl/private.key ]; then
    openssl req -x509 -newkey rsa:2048 -keyout ssl/private.key -out ssl/certificate.crt -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    echo "✅ Self-signed certificate generated"
else
    echo "✅ SSL certificate already exists"
fi

# Set proper permissions
chmod 600 ssl/private.key
chmod 644 ssl/certificate.crt

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p logs
chmod 755 logs

# Update Django settings for production
echo "⚙️  Configuring Django settings for HTTPS..."

# Create production settings file
cat > LibraryProject/settings_production.py << 'EOF'
# Production settings for Django Library Management System
from .settings import *

# Override settings for production
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'localhost']

# Ensure HTTPS settings are enabled
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database configuration (update with your production database)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_library',
        'USER': 'django_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files configuration
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files configuration
MEDIA_ROOT = BASE_DIR / 'media'

# Logging configuration
LOGGING['handlers']['file']['filename'] = BASE_DIR / 'logs' / 'production.log'

# Email configuration (update with your SMTP settings)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'

# Security settings
SECRET_KEY = 'your-production-secret-key-here'  # Generate a new secret key
EOF

echo "✅ Production settings file created"

# Create systemd service file for Gunicorn
echo "🔧 Creating systemd service file..."
sudo tee /etc/systemd/system/django-library.service > /dev/null << EOF
[Unit]
Description=Django Library Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=LibraryProject.settings_production"
ExecStart=$(pwd)/venv/bin/gunicorn --config deployment/gunicorn_https.py LibraryProject.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Systemd service file created"

# Create Nginx configuration
echo "🌐 Creating Nginx configuration..."
sudo tee /etc/nginx/sites-available/django-library > /dev/null << EOF
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate $(pwd)/ssl/certificate.crt;
    ssl_certificate_key $(pwd)/ssl/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    client_max_body_size 10M;

    location /static/ {
        alias $(pwd)/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $(pwd)/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Port \$server_port;
    }
}
EOF

echo "✅ Nginx configuration created"

# Enable Nginx site
echo "🔗 Enabling Nginx site..."
sudo ln -sf /etc/nginx/sites-available/django-library /etc/nginx/sites-enabled/
sudo nginx -t && echo "✅ Nginx configuration is valid"

# Create deployment checklist
echo "📋 Creating deployment checklist..."
cat > DEPLOYMENT_CHECKLIST.md << 'EOF'
# HTTPS Deployment Checklist

## Pre-deployment
- [ ] Update domain names in configuration files
- [ ] Generate production secret key
- [ ] Configure production database
- [ ] Set up email configuration
- [ ] Update ALLOWED_HOSTS with your domain

## SSL Certificate Setup
- [ ] For production: Obtain SSL certificate from Let's Encrypt or commercial CA
- [ ] For development: Use generated self-signed certificate
- [ ] Update certificate paths in Nginx configuration

## Database Setup
- [ ] Install PostgreSQL
- [ ] Create database and user
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`

## Static Files
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Verify static files are served correctly

## Service Management
- [ ] Enable and start Django service: `sudo systemctl enable django-library && sudo systemctl start django-library`
- [ ] Enable and start Nginx: `sudo systemctl enable nginx && sudo systemctl start nginx`
- [ ] Check service status: `sudo systemctl status django-library nginx`

## Security Verification
- [ ] Test HTTPS redirect: `curl -I http://yourdomain.com`
- [ ] Verify SSL certificate: `openssl s_client -connect yourdomain.com:443`
- [ ] Check security headers: `curl -I https://yourdomain.com`
- [ ] Test SSL Labs: https://www.ssllabs.com/ssltest/

## Monitoring
- [ ] Set up log monitoring
- [ ] Configure certificate expiration alerts
- [ ] Set up security monitoring
- [ ] Create backup procedures

## Post-deployment Testing
- [ ] Test all application functionality
- [ ] Verify form submissions work
- [ ] Test file uploads
- [ ] Check admin interface
- [ ] Verify user authentication
EOF

echo "✅ Deployment checklist created"

# Final instructions
echo ""
echo "🎉 HTTPS setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update domain names in configuration files"
echo "2. Review DEPLOYMENT_CHECKLIST.md"
echo "3. For production: Obtain SSL certificate from Let's Encrypt"
echo "4. Configure production database and email settings"
echo "5. Test the deployment"
echo ""
echo "🔧 Useful commands:"
echo "   sudo systemctl status django-library    # Check Django service"
echo "   sudo systemctl status nginx             # Check Nginx service"
echo "   sudo nginx -t                           # Test Nginx configuration"
echo "   openssl s_client -connect localhost:443 # Test SSL connection"
echo ""
echo "📚 Documentation:"
echo "   - HTTPS_SECURITY_IMPLEMENTATION.md"
echo "   - SECURITY_REVIEW_REPORT.md"
echo "   - DEPLOYMENT_CHECKLIST.md"
echo ""
echo "🔒 Your Django application is now configured for secure HTTPS deployment!"
