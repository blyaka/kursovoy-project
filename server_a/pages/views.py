from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from utils.log_utils import log_event, send_log

User = get_user_model()


def HomePage(request):
    return render(request, 'pages/home.html')


def custom_csrf_failure(request, reason=""):
    log_event("CSRF_FAIL", request.user, request)
    send_log()
    return render(request, 'pages/csrf_fail.html', status=403)


def custom_error_500(request):
    log_event("ERROR_500", request.user, request)
    send_log()
    return render(request, 'pages/500.html', status=500)


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        log_event("ACTION_DELETE_ACCOUNT", request.user, request)
        send_log()
        request.user.delete()
        logout(request)
        return redirect('/')
    return render(request, 'pages/delete_account.html')


def error_500_test(request):
    raise Exception("Тестовое исключение для 500")


def csrf_fail_test(request):
    if request.method == 'POST':
        return render(request, 'pages/csrf_ok.html')
    return render(request, 'pages/csrf_fail_test.html')
