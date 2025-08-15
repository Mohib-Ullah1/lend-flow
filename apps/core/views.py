from django.http import JsonResponse
from django.db import connection


def health_check(request):
    checks = {}
    try:
        connection.ensure_connection()
        checks['database'] = 'ok'
    except Exception:
        checks['database'] = 'error'

    status = 200 if all(v == 'ok' for v in checks.values()) else 503
    return JsonResponse({
        'status': 'healthy' if status == 200 else 'degraded',
        'checks': checks,
    }, status=status)
