import os 
from datetime import datetime  
from flask import Flask, jsonify, request, render_template, redirect  
from werkzeug.utils import secure_filename  
from FaceRecognition import uploadPicture, openWebCamera, upload_new_picture
from db import get_all_faces, connect_db

app = Flask(__name__)  


# กำหนดโฟลเดอร์สำหรับเก็บรูปภาพที่อัปโหลด (อยู่ภายในโฟลเดอร์ static/images)
upload_folder = os.path.join('static', 'images')
# folder image for showing image default
loading_folder = os.path.join('static', 'images_loading')
app.config['UPLOAD'] = upload_folder  # เก็บค่า path นี้ไว้ใน config ของแอป
app.config['LOADING'] = loading_folder  # เก็บค่า path นี้ไว้ใน config ของแอป


# กำหนด route สำหรับ "/index" ซึ่งรองรับทั้ง GET และ POST
@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def displayTemplate():
    padding = "p-[65px]"
    filePath = os.path.join(app.config['LOADING'], "image_load.png")
    # เมื่อมีการร้องขอแบบ GET ให้ render หน้า index.html โดยไม่แสดง card หรือข้อความ error
    if request.method == 'GET':
        # filePath = os.path.join(app.config['LOADING'], "image_load.png")
        return render_template('index.html', path=filePath, displayCard=False, showError=False, stylePadding="p-[65px]")

    # เมื่อมีการร้องขอแบบ POST พร้อมกับรับ parameter 'code' ที่มีค่าเป็น '1'
    elif request.method == 'POST' and request.form.get('code') == '1':
        file = request.files['file']  # รับไฟล์จาก form ที่ถูกส่งมาจากหน้าเว็บ
        # secure_filename() ช่วยลดความเสี่ยงจากการใช้ชื่อไฟล์ที่ไม่ปลอดภัย
        filename = secure_filename(file.filename)
        # รวม path สำหรับเก็บไฟล์โดยใช้ค่า config ที่กำหนดไว้และชื่อไฟล์ที่ปลอดภัย
        filePath = os.path.join(app.config['UPLOAD'], filename)
        file.save(filePath)  # บันทึกไฟล์ลงในโฟลเดอร์ที่กำหนด
        now = datetime.now()  # ดึงเวลาปัจจุบัน
        current_time = now.strftime("%H:%M:%S")  # แปลงเวลาให้อยู่ในรูปแบบชั่วโมง:นาที:วินาที
        # เรียกใช้งานฟังก์ชัน upload_new_picture จากโมดูล FaceRecognition เพื่อประมวลผลไฟล์รูปที่อัปโหลด
        upload_status = upload_new_picture(filePath)
        # หากผลลัพธ์เป็น "duplicate" แสดงข้อความแจ้งเตือนว่าชื่อไฟล์ซ้ำ
        # all failed will get image default
        if upload_status == "duplicate":
            filePath = os.path.join(app.config['LOADING'], "image_load.png")
            return render_template('index.html',
                                   displayCard=False,
                                   showError=True,
                                   path=filePath,
                                   errorMessage="ไม่สามารถอัปโหลดได้: ชื่อไฟล์ซ้ำกับที่มีอยู่แล้ว",
                                   stylePadding=padding)
        # หากผลลัพธ์เป็น "no_face" แสดงข้อความแจ้งเตือนว่าไม่พบใบหน้าในรูป
        elif upload_status == "no_face":
            filePath = os.path.join(app.config['LOADING'], "image_load.png")
            return render_template('index.html',
                                   displayCard=False,
                                   showError=True,
                                   path=filePath,
                                   errorMessage="ไม่พบใบหน้าในรูปภาพที่อัปโหลด",
                                   stylePadding=padding)

        # success
        # หากการประมวลผลสำเร็จ จะส่งค่า path, filename, displayCard และเวลาอัปโหลดกลับไปยังหน้าเว็บ
        return render_template('index.html',
                               path=filePath,
                               filename=filename,
                               displayCard=True,
                               displaySubCard=True,
                               timeUploaded=current_time)

    # กรณีที่รองรับ POST โดยรับ parameter 'code' ที่มีค่าเป็น '2'
    elif request.method == 'POST' and request.form.get('code') == '2':
        filename = request.form['filename']
        # print(filename == "")
        if filename == "" : # case user didn't upload image
            filePath = os.path.join(app.config['LOADING'], "image_load.png")
        else:
            padding = ""
            filePath = os.path.join(app.config['UPLOAD'], filename)
        openWebCamera()  # เรียกใช้งานฟังก์ชันเปิด web camera เพื่อตรวจจับใบหน้า (ประมวลผลในเวลา real-time)
        # หลังจากเปิด camera แล้ว แสดงข้อมูลไฟล์และเวลาอัปโหลดบนหน้าเว็บ
        return render_template('index.html', path=filePath, displayCard=True,displaySubCard=False, stylePadding=padding )


@app.route("/face", methods=['GET'])
def show_faces():
    faces = get_all_faces() # **
    return render_template('face.html', faces=faces)

@app.route("/editface/<int:face_id>", methods=['GET', 'POST'])
def edit_face(face_id):
    if request.method == 'POST':
        new_name = request.form['name']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE faces SET name = %s WHERE id = %s", (new_name, face_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/face")
    else:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM faces WHERE id = %s", (face_id,))
        face = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('editface.html', face=face)

@app.route("/delete_face/<int:face_id>", methods=['POST'])
def delete_face(face_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faces WHERE id = %s", (face_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/face")



# เรียก run แอปพลิเคชันบนโฮสต์ localhost ที่ port 8080
app.run(host='localhost', port=8080)
