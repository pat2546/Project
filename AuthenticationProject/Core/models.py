from django.db import models  # นำเข้าโมดูล models จาก Django สำหรับสร้างโมเดลฐานข้อมูล
from django.contrib.auth.models import User  # นำเข้าโมเดล User จาก Django เพื่อใช้ในการเชื่อมโยงผู้ใช้
import uuid  # นำเข้า uuid เพื่อสร้าง UUID ที่ไม่ซ้ำกัน

# สร้างคลาส PasswordReset ซึ่งเป็นโมเดลฐานข้อมูลสำหรับการรีเซ็ตรหัสผ่าน
class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # เชื่อมโยงโมเดล PasswordReset กับโมเดล User โดยใช้ ForeignKey
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # สร้างฟิลด์ reset_id เป็น UUID ที่ไม่ซ้ำกัน
    created_when = models.DateTimeField(auto_now_add=True)  # ฟิลด์นี้จะบันทึกวันที่และเวลาที่สร้างวัตถุ PasswordReset

    def __str__(self):  # เมธอดที่ใช้แสดงผลเมื่อเรียกดูวัตถุ PasswordReset
        return f"Password reset for {self.user.username} at {self.created_when}"  # คืนค่าสตริงที่บอกชื่อผู้ใช้และเวลาที่รีเซ็ตรหัสผ่าน
