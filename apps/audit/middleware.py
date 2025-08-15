from .models import AuditLog

class AuditMiddleware:
    AUDIT_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method in self.AUDIT_METHODS and hasattr(request, 'user') and request.user.is_authenticated:
            if '/api/' in request.path and response.status_code < 400:
                try:
                    AuditLog.objects.create(
                        institution_id=getattr(request.user, 'institution_id', None),
                        user_id=request.user.id,
                        username=request.user.username,
                        action=request.method,
                        resource_type=request.path.strip('/').split('/')[-1] if request.path else '',
                        ip_address=request.META.get('REMOTE_ADDR'),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                    )
                except Exception:
                    pass

        return response
