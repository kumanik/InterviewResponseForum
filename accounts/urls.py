from .views import *
from django.urls import path
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from accounts import views

urlpatterns = [

    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/login/', login_view, name='login'),

    path('accounts/register/', register_view, name='register'),

    path('accounts/logout/', logout_view,{ 'template_name': 'registration/logout.html',}, name='logout'),

    path('logged_out/', logged_out, name='logged_out'),

    path('accounts/profile/', view_profile, name='profile'),

    path('accounts/profile/add_employment/', views.EmploymentCreateView.as_view(), name='add_employment'),

    path('accounts/profile/delete_employment/<int:pk>', views.EmploymentDeleteView.as_view(), name='delete_employment'),

    path('accounts/profile/add_education/', views.EducationCreateView.as_view(), name='add_education'),

    path('accounts/profile/delete_education/<int:pk>', views.EducationDeleteView.as_view(), name='delete_education'),

]