# metier_assignment_backend
Note: {} ให้แก้เป็นข้อมูลที่ผู้รันมี
Requirement:
- PostgreSQL
   - สร้าง database สำหรับเว็บไซต์นี้ด้วยคำสั่ง CREATE DATABASE {ชื่อ database};
- Django
- Python

ขั้นตอนการรัน
1. เพิ่ม .env file ใน folder metier_assignment โดยมีเนื้อหาดังนี้:
   
   DJANGO_SECRET_KEY=SECRET_KEY

   DEBUG=True

   DJANGO_LOGLEVEL=info

   DATABASE_NAME={ชื่อ database}

   DATABASE_USERNAME={ชื่อผู้ใช้}

   DATABASE_PASSWORD={รหัสผ่าน}

   DATABASE_HOST=localhost

   DATABASE_PORT={port ของ database}

2. initialize venv โดยใช้:
    - source venv/bin/activate (MacOS/Linux)
    - venv\Scripts\activate (CMD)
    - venv\Scripts\Activate.ps1 (PowerShell)
3. อัปเดตโครงสร้างฐานข้อมูลให้ตรงกับ models โดยใช้คำสั่ง: python manage.py migrate
4. รันโปรแกรมด้วยคำสั่ง: python manage.py runserver
