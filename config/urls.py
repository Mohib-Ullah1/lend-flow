from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from apps.core.views import health_check

def api_root(request):
    return JsonResponse({
        'name': 'LendFlow API',
        'version': 'v1',
        'status': 'running',
        'endpoints': {
            'admin': '/admin/',
            'health': '/health/',
            'auth': '/api/v1/auth/',
            'borrowers': '/api/v1/borrowers/',
            'loans': '/api/v1/loans/',
            'repayments': '/api/v1/repayments/',
            'ledger': '/api/v1/ledger/',
            'investors': '/api/v1/investors/',
            'scoring': '/api/v1/scoring/',
            'notifications': '/api/v1/notifications/',
            'reports': '/api/v1/reports/',
        },
        'frontend': 'http://localhost:8080/pages/login.html',
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health-check'),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/institutions/', include('apps.institutions.urls')),
    path('api/v1/borrowers/', include('apps.borrowers.urls')),
    path('api/v1/loans/', include('apps.loans.urls')),
    path('api/v1/repayments/', include('apps.repayments.urls')),
    path('api/v1/ledger/', include('apps.ledger.urls')),
    path('api/v1/investors/', include('apps.investors.urls')),
    path('api/v1/scoring/', include('apps.scoring.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
    path('api/v1/kyc/', include('apps.kyc.urls')),
    path('api/v1/documents/', include('apps.documents.urls')),
    path('api/v1/audit/', include('apps.audit.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
