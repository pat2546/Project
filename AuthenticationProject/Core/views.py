from django.shortcuts import render, redirect  # นำเข้าโมดูลสำหรับการเรนเดอร์และเปลี่ยนเส้นทาง
from django.contrib.auth.models import User  # นำเข้ารูปแบบผู้ใช้
from django.contrib.auth import authenticate, login, logout  # นำเข้าฟังก์ชันการตรวจสอบ, เข้าสู่ระบบ, และออกจากระบบ
from django.contrib.auth.decorators import login_required  # นำเข้าตกแต่งเพื่อบังคับให้ต้องเข้าสู่ระบบ
from django.contrib import messages  # นำเข้าฟังก์ชันสำหรับแสดงข้อความ
from django.conf import settings  # นำเข้าการตั้งค่าของ Django
from django.core.mail import EmailMessage  # นำเข้าฟังก์ชันสำหรับส่งอีเมล
from django.utils import timezone  # นำเข้าฟังก์ชันเพื่อจัดการเวลา
from django.urls import reverse  # นำเข้าฟังก์ชันเพื่อสร้าง URL
import uuid  # เพิ่มการนำเข้า uuid
from django.db import models  # นำเข้าการใช้งาน models
from .models import PasswordReset  # เรียกใช้งานโมเดล PasswordReset จาก models.py

def RegisterView(request):
    if request.method == "POST":  # ถ้ารับคำขอเป็น POST
        # รับค่าข้อมูลจากฟอร์ม
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False  # ตัวแปรสำหรับตรวจสอบข้อผิดพลาดข้อมูลผู้ใช้

        # ตรวจสอบว่าชื่อผู้ใช้หรืออีเมลมีอยู่แล้วหรือไม่
        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "ชื่อผู้ใช้มีอยู่แล้ว")  # แจ้งข้อผิดพลาดถ้าชื่อผู้ใช้มีอยู่แล้ว
        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "อีเมลนี้มีอยู่แล้ว")  # แจ้งข้อผิดพลาดถ้าอีเมลมีอยู่แล้ว

        # ตรวจสอบความยาวของรหัสผ่าน
        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")  # แจ้งข้อผิดพลาดถ้ารหัสผ่านสั้นเกินไป

        # ถ้ามีข้อผิดพลาดให้กลับไปที่หน้า register
        if user_data_has_error:
            return redirect('register')  # เปลี่ยนเส้นทางไปยังหน้า register
        else:
            # สร้างผู้ใช้ใหม่
            new_user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )

            # แจ้งความสำเร็จและเปลี่ยนไปหน้า login
            messages.success(request, 'สร้างบัญชีสำเร็จ')  # แจ้งให้ผู้ใช้ทราบว่าบัญชีถูกสร้างแล้ว
            return redirect('login')  # เปลี่ยนเส้นทางไปยังหน้า login

    return render(request, 'register.html')  # แสดงหน้า register

def LoginView(request):
    if request.method == "POST":  # ถ้ารับคำขอเป็น POST
        # รับค่าข้อมูลจากฟอร์ม
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ตรวจสอบข้อมูลผู้ใช้
        user = authenticate(request, username=username, password=password)

        if user is not None:  # ถ้าผู้ใช้ถูกต้อง
            login(request, user)  # เข้าสู่ระบบ
            return redirect('index')  # เปลี่ยนเส้นทางไปยังหน้า index
        else:
            messages.error(request, "รหัสผ่านไม่ถูกต้อง")  # แจ้งข้อผิดพลาดถ้าข้อมูลการเข้าสู่ระบบไม่ถูกต้อง
            return redirect('login')  # เปลี่ยนเส้นทางไปยังหน้า login

    return render(request, 'login.html')  # แสดงหน้า login

def LogoutView(request):
    logout(request)  # ออกจากระบบ
    return redirect('login')  # เปลี่ยนเส้นทางไปยังหน้า login

def ForgotPassword(request):
    if request.method == "POST":  # ถ้ารับคำขอเป็น POST
        email = request.POST.get('email')  # รับอีเมลจากฟอร์ม

        try:
            # ค้นหาผู้ใช้ตามอีเมล
            user = User.objects.get(email=email)

            # สร้างการขอรีเซ็ตรหัสผ่าน
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            # สร้างลิงก์สำหรับรีเซ็ตรหัสผ่าน
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            # สร้างข้อความอีเมล
            email_body = f'Reset your password using the link below:\n\n{full_password_reset_url}'

            # ส่งอีเมลไปยังผู้ใช้
            email_message = EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )

            email_message.fail_silently = True  # ไม่ให้แสดงข้อผิดพลาดถ้าส่งอีเมลไม่สำเร็จ
            email_message.send()  # ส่งอีเมล

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)  # เปลี่ยนเส้นทางไปยังหน้าการส่งรหัสผ่าน

        except User.DoesNotExist:  # ถ้าหาผู้ใช้ไม่พบ
            messages.error(request, f"No user with email '{email}' found")  # แจ้งข้อผิดพลาด
            return redirect('forgot-password')  # เปลี่ยนเส้นทางไปยังหน้า forgot-password

    return render(request, 'forgot_password.html')  # แสดงหน้า forgot password

def PasswordResetSent(request, reset_id):
    try:
        # ตรวจสอบว่า reset_id เป็น UUID ที่ถูกต้องหรือไม่
        uuid_obj = uuid.UUID(reset_id)
        
        if PasswordReset.objects.filter(reset_id=uuid_obj).exists():  # ตรวจสอบว่า reset_id มีอยู่ในฐานข้อมูล
            return render(request, 'password_reset_sent.html')  # แสดงหน้าส่งรหัสผ่าน
        else:
            messages.error(request, 'Invalid reset id')  # แจ้งข้อผิดพลาดถ้า reset_id ไม่ถูกต้อง
            return redirect('forgot-password')  # เปลี่ยนเส้นทางไปยังหน้า forgot-password

    except ValueError:  # ถ้า reset_id ไม่ใช่ UUID ที่ถูกต้อง
        messages.error(request, 'Invalid reset id format')  # แจ้งข้อผิดพลาด
        return redirect('forgot-password')  # เปลี่ยนเส้นทางไปยังหน้า forgot-password

def ResetPassword(request, reset_id):
    try:
        # ตรวจสอบว่า reset_id เป็น UUID ที่ถูกต้องหรือไม่
        uuid_obj = uuid.UUID(reset_id)

        # ค้นหา PasswordReset ตาม reset_id
        password_reset_id = PasswordReset.objects.get(reset_id=uuid_obj)

        if request.method == "POST":  # ถ้ารับคำขอเป็น POST
            password = request.POST.get('password')  # รับรหัสผ่านใหม่
            confirm_password = request.POST.get('confirm_password')  # รับการยืนยันรหัสผ่าน

            password_have_error = False  # ตัวแปรสำหรับตรวจสอบข้อผิดพลาดรหัสผ่าน

            if password != confirm_password:  # ถ้ารหัสผ่านไม่ตรงกัน
                password_have_error = True
                messages.error(request, 'Passwords do not match')  # แจ้งข้อผิดพลาด

            if len(password) < 5:  # ถ้ารหัสผ่านสั้นเกินไป
                password_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')  # แจ้งข้อผิดพลาด

            # ตรวจสอบเวลาหมดอายุของลิงก์
            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:  # ถ้าลิงก์หมดอายุ
                password_have_error = True
                messages.error(request, 'Reset link has expired')  # แจ้งข้อผิดพลาด
                password_reset_id.delete()  # ลบการรีเซ็ตรหัสผ่าน

            if not password_have_error:  # ถ้าไม่มีข้อผิดพลาด
                user = password_reset_id.user  # ดึงผู้ใช้
                user.set_password(password)  # ตั้งค่ารหัสผ่านใหม่
                user.save()  # บันทึกการเปลี่ยนแปลง

                password_reset_id.delete()  # ลบการรีเซ็ตรหัสผ่าน

                messages.success(request, 'Password reset. Proceed to login')  # แจ้งให้ผู้ใช้ทราบว่ารหัสผ่านถูกรีเซ็ตแล้ว
                return redirect('login')  # เปลี่ยนเส้นทางไปยังหน้า login
            else:
                return redirect('reset-password', reset_id=reset_id)  # เปลี่ยนเส้นทางไปยังหน้า reset-password

        return render(request, 'reset_password.html', {'reset_id': reset_id})  # แสดงหน้า reset password

    except PasswordReset.DoesNotExist:  # ถ้าหา PasswordReset ไม่พบ
        messages.error(request, 'Invalid reset link')  # แจ้งข้อผิดพลาด
        return redirect('forgot-password')  # เปลี่ยนเส้นทางไปยังหน้า forgot-password

    except ValueError:  # ถ้า reset_id ไม่ใช่ UUID ที่ถูกต้อง
        messages.error(request, 'Invalid reset id format')  # แจ้งข้อผิดพลาด
        return redirect('forgot-password')  # เปลี่ยนเส้นทางไปยังหน้า forgot-password
