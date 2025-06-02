import logging
from django.utils.timezone import now
import requests

logger = logging.getLogger('django')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def log_event(event_type, user, request):
    ip = get_client_ip(request)
    username = user.username if user and user.is_authenticated else "Anonymous"
    logger.info(f"[{event_type}] user={username} ip={ip} time={now()}")


def send_log():
    try:
        with open('app.log', 'rb') as f:
            r = requests.post("http://127.0.0.1:5000/api/upload", files={"file": f})
            print(f"[SEND_LOG] status={r.status_code} response={r.text}")
    except Exception as e:
        print(f"[SEND_LOG] Ошибка: {e}")
