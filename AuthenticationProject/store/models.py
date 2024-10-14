from django.db import models  # นำเข้าโมดูล models จาก Django เพื่อใช้สร้างโมเดล
from django.contrib.auth.models import User  # นำเข้าโมเดล User จาก Django สำหรับการจัดการผู้ใช้
from django.db.models.signals import post_save  # สัญญาณที่ใช้หลังจากบันทึกข้อมูล
from django.dispatch import receiver  # ตัวรับสัญญาณเมื่อข้อมูลถูกบันทึก

# โมเดลสำหรับสินค้า (Product)
class Product(models.Model):
    order_number = models.PositiveIntegerField(default=0, unique=True)  # หมายเลขคำสั่งซื้อ (ต้องไม่ซ้ำ)
    name = models.CharField(max_length=100)  # ชื่อสินค้า
    description = models.TextField()  # รายละเอียดสินค้า
    price = models.DecimalField(max_digits=10, decimal_places=2)  # ราคา (สูงสุด 10 หลัก มีทศนิยม 2 ตำแหน่ง)
    image_url = models.URLField(blank=True, null=True)  # URL รูปภาพสินค้า (อาจมีหรือไม่มีก็ได้)
    quantity_sold = models.IntegerField(default=0)  # บันทึกยอดขายของสินค้าแต่ละรายการ

    def __str__(self):
        return self.name  # คืนค่าชื่อสินค้าสำหรับแสดงผลในรูปแบบข้อความ

# โมเดลสำหรับคำสั่งซื้อ (Order)
class Order(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)  # ลิงก์ไปยังสินค้า, ถ้าสินค้าถูกลบ คำสั่งซื้อนั้นจะถูกลบด้วย
    name = models.CharField(max_length=100)  # ชื่อของลูกค้า
    address = models.TextField()  # ที่อยู่ของลูกค้า
    phone = models.CharField(max_length=15)  # เบอร์โทรศัพท์ของลูกค้า
    payment_method = models.CharField(max_length=50)  # วิธีการชำระเงินที่ลูกค้าเลือก
    quantity = models.PositiveIntegerField(default=1)  # จำนวนสินค้าที่ลูกค้าเลือกซื้อ

    def __str__(self):
        return f"Order {self.id} - {self.name} - Quantity: {self.quantity}"  # คืนค่าข้อความบรรยายคำสั่งซื้อ

# โมเดลสำหรับข้อมูลโปรไฟล์ผู้ใช้ (Profile)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ลิงก์ไปยัง User แต่ละคนจะมีโปรไฟล์ของตัวเอง
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # รูปโปรไฟล์ของผู้ใช้ (อาจมีหรือไม่มีก็ได้)
    name = models.CharField(max_length=100, null=True, blank=True)  # ชื่อผู้ใช้ (อาจมีหรือไม่มีก็ได้)
    address = models.CharField(max_length=255, null=True, blank=True)  # ที่อยู่ของผู้ใช้
    phone = models.CharField(max_length=15, null=True, blank=True)  # เบอร์โทรศัพท์ของผู้ใช้

    def __str__(self):
        return self.user.username  # คืนค่าชื่อผู้ใช้สำหรับแสดงผลในรูปแบบข้อความ
    

