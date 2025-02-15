import cv2
import face_recognition as face
import numpy as np
import os
import json
from db import connect_db, mark_attendance
from discord_notifier import send_discord_notification
import threading
from queue import Queue

# ฟังก์ชันสำหรับบันทึกข้อมูลใบหน้าลงในฐานข้อมูล
def save_face_to_db(name, image_path):
    # โหลดรูปภาพจาก path ที่กำหนดและแปลงรูปภาพเป็น array
    image = face.load_image_file(image_path)
    # แปลงใบหน้าในรูปให้เป็น encoding
    encodings = face.face_encodings(image)

    if not encodings:
        # หากไม่พบใบหน้าในรูปให้แสดงข้อความและออกจากฟังก์ชัน
        print(f"ไม่พบใบหน้าในรูป {image_path}")
        return

    # แปลง encoding จาก array เป็น list แล้วแปลงเป็น JSON เพื่อเก็บลงฐานข้อมูล
    encoding_json = json.dumps(encodings[0].tolist())

    # เชื่อมต่อฐานข้อมูล
    conn = connect_db()
    cursor = conn.cursor()

    # คำสั่ง SQL สำหรับบันทึกชื่อและ encoding ลงในตาราง faces
    sql = "INSERT INTO faces (name, encoding) VALUES (%s, %s)"
    cursor.execute(sql, (name, encoding_json))
    conn.commit()

    cursor.close()
    conn.close()
    print(f"บันทึก {name} ลงฐานข้อมูลเรียบร้อย")

# ฟังก์ชันสำหรับโหลดใบหน้าที่บันทึกไว้ในฐานข้อมูล
def load_faces_from_db():
    # เชื่อมต่อฐานข้อมูลและสืบค้นข้อมูลใบหน้า (ชื่อและ encoding)
    conn = connect_db()
    cursor = conn.cursor()

    sql = "SELECT name, encoding FROM faces"
    cursor.execute(sql)
    
    known_face_encodings = []
    known_face_names = []

    # อ่านข้อมูลที่ได้จากฐานข้อมูล
    for name, encoding_json in cursor.fetchall():
        # แปลง encoding จาก JSON กลับเป็น NumPy array
        encoding_array = np.array(json.loads(encoding_json))
        known_face_encodings.append(encoding_array)
        known_face_names.append(name)

    cursor.close()
    conn.close()

    # คืนค่าเป็นรายการ encoding และชื่อใบหน้าที่รู้จัก
    return known_face_encodings, known_face_names

# กำหนดโฟลเดอร์ที่เก็บรูปภาพที่อัปโหลด
IMAGE_FOLDER = "static/images"

# โหลดข้อมูลใบหน้าที่บันทึกในฐานข้อมูล


# ฟังก์ชันสำหรับอัปโหลดและประมวลผลรูปภาพที่ถูกอัปโหลดเข้ามา
def uploadPicture():
    known_face_encodings, known_face_names = load_faces_from_db() # update know faces name,encodings
    # วนลูปอ่านไฟล์ในโฟลเดอร์ IMAGE_FOLDER
    for filename in os.listdir(IMAGE_FOLDER):
        # ตรวจสอบนามสกุลไฟล์ของรูปภาพที่อนุญาต
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".webp"):
            # สร้าง path ของรูปภาพ
            img_path = os.path.join(IMAGE_FOLDER, filename)
            # โหลดรูปภาพ
            image = face.load_image_file(img_path)
            # เข้ารหัสใบหน้าในรูปภาพเพื่อตรวจสอบว่ามีใบหน้าหรือไม่
            encodings = face.face_encodings(image)
            if encodings:
                # หากพบใบหน้า ให้นำ encoding ตัวแรกเข้ารหัสและเพิ่มลงใน known_face_encodings
                known_face_encodings.append(encodings[0])
                # ตั้งชื่อจากชื่อไฟล์ (ตัดส่วนนามสกุลออก)
                name = os.path.splitext(filename)[0]
                known_face_names.append(name)
                # บันทึกใบหน้าลงฐานข้อมูล
                save_face_to_db(name, img_path)
                print("saved")
                # send_discord_notification(name)
            else:
                # หากไม่พบใบหน้าในรูป ให้แสดงข้อความและข้ามไฟล์นี้ไป
                print(f"ไม่พบใบหน้าในไฟล์ {filename}, ข้ามไฟล์นี้")

def upload_new_picture(file_path):
    known_face_encodings, known_face_names = load_faces_from_db() # update know faces name,encodings
    # ตรวจสอบว่าชื่อไฟล์ซ้ำหรือไม่
    name = os.path.splitext(os.path.basename(file_path))[0]
    if name in known_face_names:
        os.remove(file_path)  # ลบไฟล์ที่อัปโหลดแล้วซ้ำ
        return "duplicate"
        
    # โหลดรูปภาพ
    image = face.load_image_file(file_path)
    # เข้ารหัสใบหน้าในรูปภาพเพื่อตรวจสอบว่ามีใบหน้าหรือไม่
    encodings = face.face_encodings(image)
    if encodings:
        # บันทึกใบหน้าลงฐานข้อมูล
        save_face_to_db(name, file_path)
        print("saved")
        return "success"
    else:
        # หากไม่พบใบหน้าในรูป ให้แสดงข้อความและข้ามไฟล์นี้ไป
        os.remove(file_path)  # ลบไฟล์ที่ไม่มีใบหน้า
        print(f"ไม่พบใบหน้าในไฟล์ {file_path}, ข้ามไฟล์นี้")
        return "no_face"

# ฟังก์ชันสำหรับเปิดกล้องเว็บเพื่อทำการตรวจจับใบหน้าแบบเรียลไทม์
def openWebCamera():
    known_face_encodings, known_face_names = load_faces_from_db()  # update known faces and encodings
    video_capture = cv2.VideoCapture(0)
    frame_queue = Queue(maxsize=2)  # คิวสำหรับส่งเฟรมไปประมวลผล
    detection_result = {}         # ตัวแปรเก็บผลลัพธ์จากการตรวจจับ
    result_lock = threading.Lock()

    # Thread สำหรับประมวลผลตรวจจับใบหน้า
    def detection_thread():
        while True:
            frame = frame_queue.get()
            if frame is None:  # สัญญาณให้หยุด thread
                break

            # ลดขนาดเพื่อประมวลผลเร็วขึ้นและเปลี่ยนเป็นโมเดล cnn สำหรับ GPU (ถ้ารองรับ)
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            try:
                face_locations = face.face_locations(rgb_small_frame, model="hog")
                face_encodings = face.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                face_percents = []
                for encoding in face_encodings:
                    face_distances = face.face_distance(known_face_encodings, encoding)
                    best_index = np.argmin(face_distances)
                    face_percent_value = 1 - face_distances[best_index]

                    if face_percent_value >= 0.5:  # หากตรงกันพอ
                        name = known_face_names[best_index]
                        mark_attendance(name)
                        send_discord_notification(name)
                    else:
                        name = "UNKNOWN"
                        face_percent_value = 0

                    face_names.append(name)
                    face_percents.append(round(face_percent_value * 100, 2))
            except Exception as e:
                print("พบข้อผิดพลาดในการตรวจจับใบหน้า:", e)
                face_locations, face_names, face_percents = [], [], []

            with result_lock:
                detection_result["locations"] = face_locations
                detection_result["names"] = face_names
                detection_result["percents"] = face_percents

    # เริ่ม thread ตรวจจับใบหน้า
    t = threading.Thread(target=detection_thread)
    t.daemon = True
    t.start()

    # วนลูปอ่านข้อมูลจากกล้องและแสดงผล
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("ไม่สามารถอ่านข้อมูลกล้องได้")
            break

        if not frame_queue.full():
            frame_queue.put(frame.copy())

        with result_lock:
            locations = detection_result.get("locations", [])
            names = detection_result.get("names", [])
            percents = detection_result.get("percents", [])

        # วาดกรอบและแสดงชื่อพร้อมเปอร์เซ็นต์บนแต่ละใบหน้า
        for (top, right, bottom, left), name, percent in zip(locations, names, percents):
            # ปรับขนาดพิกเซลกลับคืน (คูณด้วย 2 เนื่องจากลดขนาดลง 50%)
            top, right, bottom, left = top * 2, right * 2, bottom * 2, left * 2
            color = (46, 2, 209) if name == "UNKNOWN" else (255, 102, 51)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, top - 30), (right, top), color, cv2.FILLED)
            cv2.rectangle(frame, (left, bottom), (right, bottom + 30), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, top - 6), font, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, f"MATCH: {percent}%", (left + 6, bottom + 23), font, 0.6, (255, 255, 255), 1)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    # ส่ง None เพื่อบอกให้ thread หยุดทำงาน
    frame_queue.put(None)
    cv2.destroyAllWindows()