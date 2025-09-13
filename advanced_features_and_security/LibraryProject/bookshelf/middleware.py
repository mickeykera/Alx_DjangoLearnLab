"""
Custom middleware for security enhancements including Content Security Policy (CSP).
"""

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers including Content Security Policy (CSP).
    """
    
    def process_response(self, request, response):
        """
        Add security headers to the response.
        """
        # Content Security Policy (CSP)
        if hasattr(settings, 'CSP_DEFAULT_SRC'):
            csp_parts = []
            
            # Default source
            if hasattr(settings, 'CSP_DEFAULT_SRC'):
                csp_parts.append(f"default-src {' '.join(settings.CSP_DEFAULT_SRC)}")
            
            # Script source
            if hasattr(settings, 'CSP_SCRIPT_SRC'):
                csp_parts.append(f"script-src {' '.join(settings.CSP_SCRIPT_SRC)}")
            
            # Style source
            if hasattr(settings, 'CSP_STYLE_SRC'):
                csp_parts.append(f"style-src {' '.join(settings.CSP_STYLE_SRC)}")
            
            # Image source
            if hasattr(settings, 'CSP_IMG_SRC'):
                csp_parts.append(f"img-src {' '.join(settings.CSP_IMG_SRC)}")
            
            # Font source
            if hasattr(settings, 'CSP_FONT_SRC'):
                csp_parts.append(f"font-src {' '.join(settings.CSP_FONT_SRC)}")
            
            # Connect source
            if hasattr(settings, 'CSP_CONNECT_SRC'):
                csp_parts.append(f"connect-src {' '.join(settings.CSP_CONNECT_SRC)}")
            
            # Frame ancestors
            if hasattr(settings, 'CSP_FRAME_ANCESTORS'):
                csp_parts.append(f"frame-ancestors {' '.join(settings.CSP_FRAME_ANCESTORS)}")
            
            # Base URI
            if hasattr(settings, 'CSP_BASE_URI'):
                csp_parts.append(f"base-uri {' '.join(settings.CSP_BASE_URI)}")
            
            # Object source
            if hasattr(settings, 'CSP_OBJECT_SRC'):
                csp_parts.append(f"object-src {' '.join(settings.CSP_OBJECT_SRC)}")
            
            # Set CSP header
            if csp_parts:
                response['Content-Security-Policy'] = '; '.join(csp_parts)
        
        # Additional security headers
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        }
        
        # Add headers if not already present
        for header, value in security_headers.items():
            if header not in response:
                response[header] = value
        
        return response


class SecurityLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log security-related events.
    """
    
    def process_request(self, request):
        """
        Log potentially suspicious requests.
        """
        import logging
        logger = logging.getLogger('django.security')
        
        # Log suspicious user agents
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        suspicious_agents = ['sqlmap', 'nikto', 'nmap', 'scanner']
        if any(agent in user_agent.lower() for agent in suspicious_agents):
            logger.warning(f'Suspicious user agent detected: {user_agent} from {request.META.get("REMOTE_ADDR")}')
        
        # Log requests with suspicious parameters
        for param, value in request.GET.items():
            if any(pattern in value.lower() for pattern in ['<script', 'javascript:', 'union select']):
                logger.warning(f'Potential XSS/SQL injection attempt in GET parameter {param}: {value} from {request.META.get("REMOTE_ADDR")}')
        
        return None
