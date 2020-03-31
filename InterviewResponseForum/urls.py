from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('responseForum.urls')),

    path('', include('accounts.urls')),

    url(r'^oauth/', include('social_django.urls', namespace='social')),
]
