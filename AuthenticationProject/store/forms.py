from django import forms  # นำเข้าโมดูล forms จาก Django เพื่อสร้างฟอร์ม
from .models import Order  # นำเข้ารุ่น (model) ชื่อ Order จากไฟล์ models
from .models import Profile  # นำเข้ารุ่น (model) ชื่อ Profile จากไฟล์ models


# ฟอร์มสำหรับโมเดล Order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order  # ระบุว่าใช้โมเดล Order สำหรับฟอร์มนี้
        fields = ['name', 'address', 'phone', 'payment_method', 'quantity']  # ระบุฟิลด์ที่จะใช้ในฟอร์ม
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your address here...'}),  # ตั้งค่าให้ฟิลด์ address แสดงเป็น textarea พร้อม placeholder
        }
        labels = {
            'name': 'Name',  # ป้ายแสดง "Name" สำหรับฟิลด์ name
            'address': 'Address',  # ป้ายแสดง "Address" สำหรับฟิลด์ address
            'phone': 'Phone Number',  # ป้ายแสดง "Phone Number" สำหรับฟิลด์ phone
            'payment_method': 'Payment Method',  # ป้ายแสดง "Payment Method" สำหรับฟิลด์ payment_method
        }
        help_texts = {
            'name': 'Enter your full name.',  # ข้อความช่วยแนะนำสำหรับฟิลด์ name
            'address': 'Please provide your complete address.',  # ข้อความช่วยแนะนำสำหรับฟิลด์ address
            'phone': 'Enter your phone number (e.g., 012-345-6789).',  # ข้อความช่วยแนะนำสำหรับฟิลด์ phone
            'payment_method': 'Specify your preferred payment method (e.g., Credit Card, PayPal).',  # ข้อความช่วยแนะนำสำหรับฟิลด์ payment_method
        }


# ฟอร์มสำหรับโมเดล Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # ระบุว่าใช้โมเดล Profile สำหรับฟอร์มนี้
        fields = ['profile_image', 'name', 'address', 'phone']  # ระบุฟิลด์ที่จะใช้ในฟอร์ม (เช่น profile_image, name, address, phone)
