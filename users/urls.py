from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('user_log/', views.log, name='login_page'),
    path('sadmin/', views.sadmin, name='sadmin'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('user_login_view/',LoginView.as_view(), name='user_login_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.role_login_view, name='role_login'),
    # path('user_login_view/', views.user_login_view, name='user_login_view'),
    path('save-admin/', views.save_admin, name='save_admin'),
    path('save_user/', views.save_user, name='save_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('assign-user/', views.assign_user_to_admin, name='assign_user'),
    path('user_dashboard/', views.user_dashboard_view, name='user_dashboard'),



]