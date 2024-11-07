import cv2
import numpy as np
from deepface import DeepFace

# โหลด Haar Cascade สำหรับตรวจจับใบหน้าและดวงตา
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def detect_liveness(frame):
    # แปลงภาพเป็นขาวดำ
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # ตรวจจับใบหน้าในภาพ
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return False  # ไม่มีใบหน้าพบ

    # ตรวจจับการกระพริบตาและการหันหน้า
    for (x, y, w, h) in faces:
        face_roi = gray[y:y + h, x:x + w]
        
        # ตรวจจับดวงตาภายในใบหน้า
        eyes = eye_cascade.detectMultiScale(face_roi)
        
        # ถ้ามีดวงตาในภาพและตรวจจับการเคลื่อนไหวของดวงตา (กระพริบตา)
        if len(eyes) > 0:
            return True  # สามารถพิจารณาว่าผู้ใช้เป็นบุคคลจริงจากการกระพริบตา

    return False  # ไม่พบการกระพริบตาหรือการหันหน้า

# เริ่มการจับภาพจากกล้อง
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # ตรวจจับใบหน้าและการวิเคราะห์อื่นๆ ด้วย DeepFace
        result = DeepFace.analyze(frame, actions=['age', 'gender', 'emotion'], enforce_detection=False)
        print(result)
        
        # ตรวจจับ Liveness (การกระพริบตา, การหันหน้า)
        is_live = detect_liveness(frame)
        if is_live:
            cv2.putText(frame, "Live", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Not Live", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    except Exception as e:
        print("No face detected")

    cv2.imshow('frame', frame)
    
    # กด q เพื่อหยุดโปรแกรม
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
