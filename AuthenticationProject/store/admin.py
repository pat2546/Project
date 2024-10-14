from django.contrib import admin  # นำเข้าโมดูล admin เพื่อจัดการกับหน้าจัดการของแอดมิน
from .models import Product  # นำเข้ารุ่น (model) ชื่อ Product จากไฟล์ models ของแอปพลิเคชันนี้
from .models import Order  # นำเข้ารุ่น (model) ชื่อ Order จากไฟล์ models ของแอปพลิเคชันนี้

# ใช้ decorator @admin.register เพื่อทำให้ Product ปรากฏในหน้าจัดการของแอดมิน
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):  # กำหนดว่าเราจะปรับแต่งการแสดงผลของ Product ในหน้าแอดมินอย่างไร
    list_display = ('order_number','name', 'price', 'image_url')  # แสดงคอลัมน์ order_number, name, price และ image_url ในหน้าจัดการของแอดมิน

# ใช้ decorator @admin.register เพื่อทำให้ Order ปรากฏในหน้าจัดการของแอดมิน
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):  # กำหนดว่าเราจะปรับแต่งการแสดงผลของ Order ในหน้าแอดมินอย่างไร
    list_display = ('name', 'address', 'phone', 'payment_method',)  # แสดงคอลัมน์ name, address, phone และ payment_method ในหน้าจัดการของแอดมิน
