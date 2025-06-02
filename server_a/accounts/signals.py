from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from utils.log_utils import log_event, send_log

User = get_user_model()

@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    log_event("LOGIN_SUCCESS", user, request)
    send_log()

@receiver(user_login_failed)
def on_login_fail(sender, credentials, request, **kwargs):
    class FakeUser:
        username = credentials.get('username', 'UNKNOWN')
        is_authenticated = False
    log_event("LOGIN_FAIL", FakeUser(), request)
    send_log()

@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    log_event("LOGOUT", user, request)
    send_log()
