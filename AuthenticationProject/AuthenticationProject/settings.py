from pathlib import Path  # นำเข้าโมดูล Path สำหรับการจัดการเส้นทางของไฟล์
import os  # นำเข้าโมดูล os เพื่อจัดการกับเส้นทางไฟล์และการตั้งค่าที่เกี่ยวข้องกับระบบปฏิบัติการ

# สร้างเส้นทางของโปรเจคโดยอิงจากตำแหน่งไฟล์นี้ (BASE_DIR คือโฟลเดอร์หลักของโปรเจค)
BASE_DIR = Path(__file__).resolve().parent.parent

# การตั้งค่าเกี่ยวกับไฟล์สื่อ เช่น รูปภาพหรือไฟล์ที่อัพโหลด
MEDIA_URL = '/media/'  # URL ที่ใช้เข้าถึงไฟล์สื่อผ่านเว็บ
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # ตำแหน่งในเครื่องที่เก็บไฟล์สื่อ

# ตั้งค่าที่สำคัญสำหรับโปรเจค
SECRET_KEY = 'django-insecure-...'  # กุญแจลับที่ใช้ในโปรดักชั่น (ควรเก็บเป็นความลับ)
DEBUG = True  # เปิดโหมด Debug สำหรับการพัฒนา (ไม่ควรเปิดในโปรดักชั่น)
ALLOWED_HOSTS = []  # กำหนดโฮสต์ที่สามารถเข้าถึงเว็บไซต์นี้ได้ (เช่น ชื่อโดเมน)

# แอปพลิเคชันที่ติดตั้งในโปรเจคนี้
INSTALLED_APPS = [
    'django.contrib.admin',  # แอปสำหรับการจัดการของผู้ดูแลระบบ
    'django.contrib.auth',  # แอปสำหรับการจัดการผู้ใช้และสิทธิ์การเข้าถึง
    'django.contrib.contenttypes',  # จัดการประเภทของเนื้อหา
    'django.contrib.sessions',  # จัดการ session ของผู้ใช้
    'django.contrib.messages',  # จัดการข้อความต่างๆ ในระบบ
    'django.contrib.staticfiles',  # จัดการไฟล์สแตติก เช่น CSS, JS
    'Core',  # แอป custom ของโปรเจคนี้
    'store',  # แอป custom อีกตัวที่เกี่ยวกับการจัดการร้านค้า
    'compressor',  # แอปสำหรับบีบอัดไฟล์สแตติกเพื่อเพิ่มประสิทธิภาพ
]

# การตั้งค่า middleware ที่ใช้ในระบบ (ทำงานระหว่าง request และ response)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # จัดการความปลอดภัย
    'django.contrib.sessions.middleware.SessionMiddleware',  # จัดการ session ของผู้ใช้
    'django.middleware.common.CommonMiddleware',  # จัดการคำขอทั่วไป
    'django.middleware.csrf.CsrfViewMiddleware',  # จัดการความปลอดภัย CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # จัดการการตรวจสอบสิทธิ์
    'django.contrib.messages.middleware.MessageMiddleware',  # จัดการข้อความที่แสดงผลในระบบ
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # ป้องกันการโจมตี clickjacking
]

# ตั้งค่า URL หลักของโปรเจค
ROOT_URLCONF = 'AuthenticationProject.urls'

# การตั้งค่าเทมเพลต (HTML) ที่ใช้ในโปรเจคนี้
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # กำหนด backend ที่ใช้ในการเรนเดอร์เทมเพลต
        'DIRS': [BASE_DIR / 'templates'],  # โฟลเดอร์ที่เก็บเทมเพลต
        'APP_DIRS': True,  # เปิดการค้นหาเทมเพลตภายในแต่ละแอป
        'OPTIONS': {
            'context_processors': [  # ตัวแปรต่างๆ ที่จะส่งไปในเทมเพลต
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# การตั้งค่า WSGI (สำหรับการ deployment)
WSGI_APPLICATION = 'AuthenticationProject.wsgi.application'

# การตั้งค่าฐานข้อมูล (ในที่นี้ใช้ SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # ใช้ SQLite เป็นฐานข้อมูล
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # เก็บฐานข้อมูลไว้ในไฟล์ db.sqlite3
    }
}

# การตั้งค่าการตรวจสอบรหัสผ่าน
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # ตรวจสอบความคล้ายกันของชื่อกับรหัสผ่าน
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},  # กำหนดความยาวขั้นต่ำของรหัสผ่าน
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},  # ตรวจสอบรหัสผ่านที่ใช้ทั่วไป
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},  # ตรวจสอบการใช้เฉพาะตัวเลขในรหัสผ่าน
]

# การตั้งค่าเกี่ยวกับภาษาและเวลา
LANGUAGE_CODE = 'en-us'  # ตั้งค่าภาษาเป็นภาษาอังกฤษ
TIME_ZONE = 'UTC'  # ตั้งค่าเขตเวลาตาม UTC
USE_I18N = True  # เปิดการรองรับการแปลภาษา
USE_TZ = True  # เปิดการจัดการเวลาให้สอดคล้องกับเขตเวลา

# การตั้งค่าไฟล์สแตติก เช่น CSS, JavaScript
STATIC_URL = '/static/'  # URL สำหรับไฟล์สแตติก
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ที่เก็บไฟล์สแตติกในระบบไฟล์
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )  # โฟลเดอร์ที่เก็บไฟล์สแตติกภายในโปรเจค

# การตั้งค่าสำหรับ compressor (บีบอัดไฟล์สแตติก)
COMPRESS_ROOT = BASE_DIR / 'static'  # ที่เก็บไฟล์บีบอัด
COMPRESS_ENABLED = True  # เปิดการใช้งานการบีบอัดไฟล์
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',  # ค้นหาไฟล์สแตติกจากระบบไฟล์
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  # ค้นหาไฟล์สแตติกในแต่ละแอป
    'compressor.finders.CompressorFinder',  # ค้นหาไฟล์ที่ต้องบีบอัด
)

# การตั้งค่าฟิลด์หลักของโมเดล
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL สำหรับหน้าเข้าสู่ระบบ
LOGIN_URL = 'login'

# การตั้งค่าอีเมลสำหรับส่งอีเมลออก (ในที่นี้ใช้ Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # ใช้ SMTP ในการส่งอีเมล
EMAIL_HOST = "smtp.gmail.com"  # เซิร์ฟเวอร์ SMTP ของ Gmail
EMAIL_PORT = 465  # พอร์ตสำหรับ SMTP (ใช้ SSL)
EMAIL_USE_SSL = True  # เปิดใช้งานการเข้ารหัส SSL
EMAIL_HOST_USER = "phatsuda.sa.67@ubu.ac.th"  # อีเมลที่ใช้ส่ง
EMAIL_HOST_PASSWORD = "dzbi qufc viux asak"  # รหัสผ่านสำหรับบัญชีอีเมล
