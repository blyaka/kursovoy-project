from django.urls import path
from .views import HomePage, delete_account_view, error_500_test, csrf_fail_test
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomePage, name='home'),
    path('delete-account/', delete_account_view, name='delete_account'),
    path('test500/', error_500_test, name='test_500'),
    path('test-csrf/', csrf_fail_test, name='test_csrf'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)