from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('responseForum.urls')),

    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/login/', login_view, name='login'),

    path('accounts/register/', register_view, name='register'),

    path('accounts/logout/', logout_view, name='logout'),
]
