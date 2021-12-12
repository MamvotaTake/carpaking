from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('manager/', views.manager, name='manager'),
    path('employee/', views.employee, name='employee'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('remove_employee/<int:employee_id>', views.remove_employee, name='remove_employee'),
    path('update_employee/<str:employee_id>', views.update_employee, name='update_employee'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword', views.forgotPassword, name='forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('resetPassword', views.resetPassword, name='resetPassword'),



]
