import mysql.connector  # นำเข้าไลบรารีสำหรับเชื่อมต่อกับฐานข้อมูล MySQL
from mysql.connector import pooling  # นำเข้าโมดูลสำหรับสร้าง connection pool เพื่อเพิ่มประสิทธิภาพการเชื่อมต่อกับฐานข้อมูล
from datetime import datetime, date  # นำเข้า datetime และ date สำหรับจัดการวันที่และเวลา
from pytz import timezone  # นำเข้าไลบรารีสำหรับจัดการเขตเวลาที่ถูกต้อง
import numpy  # นำเข้า numpy 

# Global dict สำหรับติดตามการแสดงข้อความซ้ำเมื่อมีการบันทึกการเช็คชื่อ (เพื่อแจ้งเตือนครั้งเดียวต่อวัน)
printed_attendance = {}

# สร้าง connection pool สำหรับเชื่อมต่อกับฐานข้อมูล ซึ่งจะช่วยลดภาระการเชื่อมต่อใหม่ทุกครั้ง
connection_pool = pooling.MySQLConnectionPool(
    pool_name="face_recognition_pool",  
    pool_size=5,  
    host="",  
    port=9472,  
    user="", 
    password="",  
    database="face_recognition_db"  
)
#ดึงข้อมูลที่ต้องการจากฐานข้อมูล
def get_all_faces():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, encoding FROM faces")
    faces = cursor.fetchall()
    cursor.close()
    conn.close()
    return faces

# ฟังก์ชัน get_connection() ใช้สำหรับดึงการเชื่อมต่อจาก connection pool ที่สร้างไว้
def get_connection():
    return connection_pool.get_connection()

# ฟังก์ชัน connect_db() ทำหน้าที่เรียกใช้งาน get_connection() เพื่อเชื่อมต่อกับฐานข้อมูล
def connect_db():
    return get_connection()

# ฟังก์ชัน mark_attendance() ใช้สำหรับบันทึกข้อมูลการเช็คชื่อของนักเรียน
def mark_attendance(name):
    # กำหนดเขตเวลาเป็นเวลาของประเทศไทย (Asia/Bangkok)
    tz = timezone("Asia/Bangkok")
    current_datetime = datetime.now(tz)  # ดึงวันที่และเวลาปัจจุบันตามเขตเวลาที่กำหนด
    today = current_datetime.date()  # ดึงเฉพาะส่วนของวันที่ออกมา

    # เชื่อมต่อกับฐานข้อมูล โดยดึง connection จาก connection pool
    conn = connect_db()
    cursor = conn.cursor()  

    # ตรวจสอบว่ามีนักเรียนที่มีชื่อเดียวกันบันทึกการเช็คชื่อในวันนี้แล้วหรือไม่
    cursor.execute(
        "SELECT id FROM attendance_logs WHERE student_name = %s AND DATE(attendance_time) = %s",
        (name, today)
    )
    
    # ถ้าไม่พบข้อมูล (ยังไม่มีการบันทึกชื่อในวันนี้)
    if cursor.fetchone() is None:
        sql = "INSERT INTO attendance_logs (student_name, attendance_time) VALUES (%s, %s)"
        cursor.execute(sql, (name, current_datetime))  # บันทึกข้อมูลการเช็คชื่อใหม่ลงในฐานข้อมูล
        conn.commit()  # ยืนยันการบันทึกการเปลี่ยนแปลงลงในฐานข้อมูล
        print(f"บันทึกการเข้าเรียน: {name} เวลา {current_datetime}")
    else:
        # ถ้ามีการบันทึกข้อมูลแล้ว ให้แสดงข้อความเตือนเพียงครั้งเดียวสำหรับแต่ละชื่อในแต่ละวัน
        key = (name, today)
        if key not in printed_attendance:
            print(f"มีการเข้าเรียนสำหรับ {name} ในวันที่ {today} แล้ว")
            printed_attendance[key] = True  # บันทึกว่าได้แสดงข้อความเตือนสำหรับวันนี้แล้ว

    cursor.close()  # ปิด cursor ของการรันคำสั่ง SQL
    conn.close()  # ปิดการเชื่อมต่อกับฐานข้อมูล