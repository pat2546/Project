from django.urls import path  # นำเข้า path จาก Django เพื่อกำหนด URL
from . import views  # นำเข้าฟังก์ชันใน views.py ของแอปพลิเคชันนี้

urlpatterns = [
    path('', views.LoginView, name='login'),  # กำหนดเส้นทางหลัก ('') ให้เรียกฟังก์ชัน LoginView และตั้งชื่อเป็น 'login'
    path('register/', views.RegisterView, name='register'),  # กำหนดเส้นทาง '/register/' ให้เรียกฟังก์ชัน RegisterView และตั้งชื่อเป็น 'register'
    path('logout/', views.LogoutView, name='logout'),  # กำหนดเส้นทาง '/logout/' ให้เรียกฟังก์ชัน LogoutView และตั้งชื่อเป็น 'logout'
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),  # กำหนดเส้นทาง '/forgot-password/' ให้เรียกฟังก์ชัน ForgotPassword และตั้งชื่อเป็น 'forgot-password'
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),  # กำหนดเส้นทาง '/password-reset-sent/<reset_id>/' ให้เรียกฟังก์ชัน PasswordResetSent โดยส่ง reset_id เป็นพารามิเตอร์
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),  # กำหนดเส้นทาง '/reset-password/<reset_id>/' ให้เรียกฟังก์ชัน ResetPassword โดยส่ง reset_id เป็นพารามิเตอร์
] 
