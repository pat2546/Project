from django.urls import path  # นำเข้า path สำหรับการกำหนดเส้นทาง URL
from .views import (index, order_page, remove_from_cart, confirm_delete, add_to_cart, 
                    cart_page, CheckoutView, success_page, search_results, 
                    edit_item, update_cart, sales_chart, profile_view,admin_dashboard)  # นำเข้าฟังก์ชันและคลาสจาก views ที่จะใช้ในเส้นทาง URL
from django.conf import settings  # นำเข้า settings ของ Django สำหรับการตั้งค่าต่างๆ
from django.conf.urls.static import static  # สำหรับการเสิร์ฟไฟล์ static/media
from . import views

# กำหนดเส้นทาง URL และฟังก์ชันหรือคลาสที่จัดการแต่ละเส้นทาง
urlpatterns = [
    path('index/', index, name='index'),  # เส้นทางสำหรับหน้าแรกของเว็บ (index page)
    path('search/', search_results, name='search'),  # เส้นทางสำหรับการค้นหาสินค้า
    path('order/<str:order_number>/', order_page, name='order_page'),  # เส้นทางสำหรับดูรายละเอียดคำสั่งซื้อ โดยระบุหมายเลขคำสั่งซื้อใน URL
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),  # เส้นทางสำหรับลบสินค้าจากตะกร้าสินค้า
    path('cart/confirm_delete/<int:product_id>/', confirm_delete, name='confirm_delete'),  # เส้นทางยืนยันการลบสินค้า
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),  # เส้นทางสำหรับเพิ่มสินค้าลงในตะกร้า
    path('edit-item/<int:product_id>/', edit_item, name='edit_item'),  # เส้นทางสำหรับแก้ไขรายละเอียดสินค้าที่เลือก
    path('cart/', cart_page, name='cart_page'),  # เส้นทางแสดงหน้าตะกร้าสินค้า
    path('update_cart/<int:item_id>/', update_cart, name='update_cart'),  # เส้นทางอัปเดตจำนวนสินค้าในตะกร้า
    path('checkout/', CheckoutView.as_view(), name='checkout_page'),  # เส้นทางสำหรับหน้าเช็คเอาท์ (ใช้ class-based view)
    path('success/', success_page, name='success_page'),  # เส้นทางแสดงหน้าคำสั่งซื้อสำเร็จ
    path('sales-chart/', sales_chart, name='sales_chart'),  # เส้นทางแสดงกราฟยอดขาย
    path('profile/', profile_view, name='profile'),  # เส้นทางแสดงหน้าโปรไฟล์ผู้ใช้
    path('admin_dashboard/',admin_dashboard, name='admin_dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # เส้นทางสำหรับให้ Django จัดการไฟล์ media (รูปภาพ, ไฟล์อื่นๆ)
