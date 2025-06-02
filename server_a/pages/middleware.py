from utils.log_utils import log_event, send_log

class AdminAccessLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not request.user.is_staff:
            log_event("ACTION_OPEN_ADMIN", request.user, request)
            send_log()
        return self.get_response(request)
