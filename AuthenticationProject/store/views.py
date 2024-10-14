from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, Profile  # นำเข้าโมเดล Product, Order, และ Profile (ถ้าจำเป็น)
from .forms import OrderForm  # นำเข้า OrderForm เพื่อใช้ในฟอร์มคำสั่งซื้อ
from django.contrib import messages  # ใช้สำหรับแสดงข้อความเตือน
from decimal import Decimal  # ใช้สำหรับคำนวณตัวเลขทศนิยม เช่น ราคาสินค้า
from django.views import View  # ใช้ View สำหรับการสร้าง Class-based view
from django.contrib.auth.decorators import login_required  # ใช้สำหรับตรวจสอบว่าผู้ใช้ได้ล็อกอินแล้วหรือยัง
from .forms import ProfileForm  # นำเข้า ProfileForm สำหรับฟอร์มโปรไฟล์

# หน้าหลัก แสดงผลิตภัณฑ์ทั้งหมด
def index(request):
    products = Product.objects.all()  # ดึงข้อมูลผลิตภัณฑ์ทั้งหมดจากฐานข้อมูล
    return render(request, 'index.html', {'products': products})  # แสดงผลในเทมเพลต index.html พร้อมข้อมูลผลิตภัณฑ์

# ฟังก์ชันค้นหาผลิตภัณฑ์
def search_results(request):
    query = request.GET.get('q')  # รับค่าค้นหาจาก URL query string
    products = Product.objects.filter(name__icontains=query)  # ค้นหาผลิตภัณฑ์ที่มีชื่อคล้ายกับคำค้นหา
    return render(request, 'index.html', {'products': products})  # แสดงผลลัพธ์ใน index.html

# หน้าสำหรับสั่งซื้อสินค้า
def order_page(request, order_number=None):
    if order_number is None:
        return redirect('cart_page')  # ถ้าไม่มีหมายเลขสั่งซื้อ ให้เปลี่ยนไปหน้ารถเข็น

    try:
        product = Product.objects.get(order_number=order_number)  # ค้นหาผลิตภัณฑ์ตามหมายเลขสั่งซื้อ
    except Product.DoesNotExist:
        return redirect('cart_page')  # ถ้าไม่พบสินค้า ให้เปลี่ยนไปหน้ารถเข็น

    if request.method == 'POST':
        form = OrderForm(request.POST)  # รับข้อมูลจากฟอร์มคำสั่งซื้อ
        if form.is_valid():
            form.save()  # บันทึกข้อมูลคำสั่งซื้อ
            return redirect('order_success')  # ถ้าสำเร็จให้ไปที่หน้า order_success
    else:
        form = OrderForm()  # ถ้าเป็น GET ให้แสดงฟอร์มเปล่า

    return render(request, 'order_page.html', {
        'form': form,  # แสดงฟอร์ม
        'product': product  # แสดงข้อมูลสินค้า
    })

# ฟังก์ชันลบสินค้าออกจากรถเข็น
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})  # ดึงข้อมูลรถเข็นจาก session
    if str(product_id) in cart:
        del cart[str(product_id)]  # ลบสินค้าตาม product_id
        request.session['cart'] = cart  # อัปเดตข้อมูลรถเข็นใน session
        messages.success(request, 'Product removed from cart successfully.')  # แสดงข้อความสำเร็จ
    else:
        messages.error(request, 'Product not found in cart.')  # แสดงข้อความเมื่อไม่พบสินค้าในรถเข็น

    return redirect('cart_page')  # กลับไปที่หน้ารถเข็น

# ฟังก์ชันยืนยันการลบสินค้า
def confirm_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # ดึงข้อมูลสินค้าหรือแสดงหน้า 404 ถ้าไม่พบ
    if request.method == 'POST':
        cart = request.session.get('cart', {})  # ดึงข้อมูลรถเข็น
        if str(product_id) in cart:
            del cart[str(product_id)]  # ลบสินค้า
            request.session['cart'] = cart  # อัปเดตข้อมูลรถเข็น
            messages.success(request, 'Product removed from cart successfully.')
        else:
            messages.error(request, 'Product not found in cart.')

        return redirect('cart_page')

    return render(request, 'confirm_delete.html', {'product': product})  # แสดงหน้า confirm_delete

# ฟังก์ชันแก้ไขสินค้า
def edit_item(request, product_id):
    item = get_object_or_404(Product, id=product_id)  # ค้นหาสินค้า

    if request.method == 'POST':
        item.name = request.POST.get('name')  # รับค่าชื่อจากฟอร์ม
        item.price = request.POST.get('price')  # รับค่าราคา
        item.quantity_sold = request.POST.get('quantity')  # รับค่าจำนวนที่ขายแล้ว
        item.save()  # บันทึกการเปลี่ยนแปลงลงในฐานข้อมูล
        messages.success(request, "Item updated successfully!")
        return redirect('cart_page')  # กลับไปหน้ารถเข็น

    return render(request, 'Edit.html', {'item': item, 'product_id': product_id})  # แสดงหน้าแก้ไข

# ฟังก์ชันอัปเดตรถเข็น
def update_cart(request, item_id):
    cart = request.session.get('cart', {})  # ดึงข้อมูลรถเข็น
    if str(item_id) in cart:
        quantity = request.POST.get('quantity')  # รับค่าจำนวนสินค้า
        cart[str(item_id)]['quantity'] = int(quantity)  # อัปเดตจำนวนสินค้าในรถเข็น
        request.session['cart'] = cart  # อัปเดต session
        messages.success(request, 'Quantity updated successfully.')
    else:
        messages.error(request, 'Product not found in cart.')

    return redirect('cart_page')  # กลับไปหน้ารถเข็น

# ฟังก์ชันเพิ่มสินค้าลงในรถเข็น
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # ค้นหาสินค้า
    cart = request.session.get('cart', {})  # ดึงข้อมูลรถเข็น

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1  # เพิ่มจำนวนสินค้า
    else:
        cart[str(product_id)] = {  # เพิ่มสินค้าลงในรถเข็น
            'name': product.name,
            'price': str(product.price),
            'quantity': 1,
            'image_url': product.image_url
        }

    request.session['cart'] = cart  # อัปเดต session
    return redirect('cart_page')  # กลับไปหน้ารถเข็น

# หน้าแสดงสินค้าที่อยู่ในรถเข็น
def cart_page(request):
    cart = request.session.get('cart', {})  # ดึงข้อมูลรถเข็น
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())  # คำนวณราคาสินค้าทั้งหมด
    return render(request, 'cart_page.html', {'cart': cart, 'total': total})  # แสดงหน้ารถเข็นพร้อมยอดรวม

# หน้าชำระเงิน
class CheckoutView(View):
    def get(self, request):
        cart = request.session.get('cart', {})  # ดึงข้อมูลสินค้าจาก session
        cart_items = []  # รายการสินค้าในรถเข็น
        total_price = Decimal('0.00')  # ยอดรวมสินค้าเริ่มต้นที่ 0

        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)  # ค้นหาสินค้า
            item_total = product.price * item['quantity']  # คำนวณราคาของสินค้าชิ้นนั้น
            total_price += item_total  # เพิ่มราคาสินค้าในยอดรวม

            cart_items.append({
                'name': product.name,  # ชื่อสินค้า
                'price': product.price,  # ราคาสินค้า
                'quantity': item['quantity'],  # จำนวนสินค้า
                'total': item_total,  # ราคารวมของสินค้าชิ้นนั้น
                'image_url': item['image_url'],  # รูปภาพของสินค้า
            })

        shipping_fee = Decimal('100.00')  # ค่าจัดส่ง
        final_total = total_price + shipping_fee  # ราคารวมสุดท้าย

        form = OrderForm()  # สร้างฟอร์มใหม่
        context = {
            'cart_items': cart_items,  # ข้อมูลสินค้าในรถเข็น
            'total_price': total_price,  # ยอดรวมสินค้า
            'shipping_fee': shipping_fee,  # ค่าจัดส่ง
            'final_total': final_total,  # ยอดรวมทั้งหมด
            'form': form,  # ฟอร์มคำสั่งซื้อ
        }
        return render(request, 'checkout_page.html', context)  # แสดงผลในเทมเพลต checkout_page.html

    def post(self, request):
        form = OrderForm(request.POST)  # รับข้อมูลจากฟอร์ม
        if form.is_valid():
            order = form.save()  # บันทึกคำสั่งซื้อ
            return redirect('success_page')  # ถ้าสำเร็จ เปลี่ยนหน้าไปที่ success_page
        # ถ้าฟอร์มไม่ถูกต้อง แสดงหน้าชำระเงินอีกครั้ง
        cart = request.session.get('cart', {})
        cart_items = []
        total_price = Decimal('0.00')

        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            item_total = product.price * item['quantity']
            total_price += item_total

            cart_items.append({
                'name': product.name,
                'price': product.price,
                'quantity': item['quantity'],
                'total': item_total,
                'image_url': item['image_url'],
            })

        shipping_fee = Decimal('100.00')
        final_total = total_price + shipping_fee

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'shipping_fee': shipping_fee,
            'final_total': final_total,
            'form': form,  # ส่งฟอร์มที่ไม่ถูกต้องกลับไป
        }
        return render(request, 'cart_page.html', context)


# ฟังก์ชัน success_page สำหรับแสดงหน้าสำเร็จหลังจากชำระเงิน
def success_page(request):
    return render(request, 'success_page.html')  # แสดงเทมเพลต success_page.html


# ฟังก์ชันสำหรับแสดงกราฟการขาย
def sales_chart(request):
    products = Product.objects.all()  # ดึงข้อมูลสินค้าทั้งหมด
    labels = [product.name for product in products]  # ชื่อสินค้า
    data = [product.quantity_sold for product in products]  # จำนวนสินค้าที่ขายได้

    context = {
        'labels': labels,  # ส่งชื่อสินค้าไปยังกราฟ
        'data': data,  # ส่งจำนวนสินค้าที่ขายไปยังกราฟ
    }

    return render(request, 'sales_chart.html', context)  # แสดงกราฟในเทมเพลต sales_chart.html


# ฟังก์ชันสำหรับแสดงและแก้ไขโปรไฟล์ผู้ใช้
@login_required
def profile_view(request):
    try:
        profile = request.user.profile  # ค้นหาโปรไฟล์ของผู้ใช้ปัจจุบัน
    except Profile.DoesNotExist:
        profile = None  # ถ้าไม่พบโปรไฟล์ ให้กำหนดค่าเป็น None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # ฟอร์มสำหรับแก้ไขโปรไฟล์
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # กำหนดผู้ใช้ให้กับโปรไฟล์
            profile.save()  # บันทึกโปรไฟล์
            messages.success(request, 'Profile updated successfully!')
            return redirect('index')  # เปลี่ยนเส้นทางไปยังหน้าหลัก
    else:
        form = ProfileForm(instance=profile)  # โหลดโปรไฟล์เก่ามาแสดงในฟอร์ม

    return render(request, 'profile.html', {'form': form})  # แสดงฟอร์มในเทมเพลต profile.html


def admin_dashboard(request):
    # ดึงข้อมูลผลิตภัณฑ์ทั้งหมด
    products = Product.objects.all()
    # ดึงข้อมูลคำสั่งซื้อทั้งหมด
    orders = Order.objects.all()

    if request.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        order_number = request.POST.get('order_number')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image_url = request.POST.get('image_url')

        # บันทึกข้อมูลสินค้าใหม่
        new_product = Product(
            order_number=order_number,
            name=name,
            description=description,
            price=price,
            image_url=image_url
        )
        new_product.save()

        # Redirect ไปที่หน้า dashboard เพื่อรีเฟรชหน้า
        return redirect('admin_dashboard')

    # ส่งข้อมูลไปยังเทมเพลต
    return render(request, 'admin_dashboard.html', {'products': products, 'orders': orders})