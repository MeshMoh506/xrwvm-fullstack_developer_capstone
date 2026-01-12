from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),

    # FIXED: change registration → register
    path('register', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)