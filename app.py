from flask import Flask, render_template, Response, request, jsonify
import cv2
import math
import time
import cvzone
from ultralytics import YOLO
import mysql.connector

app = Flask(__name__)

def save_to_database(username, image):
    # 连接到MySQL数据库
    cnx = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database'
    )
    
    cursor = cnx.cursor()

    # 创建保存用户名和图片的表（如果表不存在）
    create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            image BLOB
        )
    """
    cursor.execute(create_table_query)

    # 将用户名和图片插入到表中
    insert_query = """
        INSERT INTO users (username, image) VALUES (%s, %s)
    """
    cursor.execute(insert_query, (username, image))

    # 提交更改并关闭数据库连接
    cnx.commit()
    cursor.close()
    cnx.close()

@app.route('/')
def index():
    return render_template('index.html')

def detect_objects():
    confidence = 0.6
    cap = cv2.VideoCapture(0)  # For Webcam
    cap.set(3, 640)
    cap.set(4, 480)
    
    model = YOLO("models/best.pt")

    classNames = ["fake", "real"]

    prev_frame_time = 0
    new_frame_time = 0

    while True:
        new_frame_time = time.time()
        success, img = cap.read()
        results = model(img, stream=True, verbose=False)
        for r in results.pred:
            boxes = r.xyxy[0]
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                # Confidence
                conf = math.ceil((box[4] * 100)) / 100
                # Class Name
                cls = int(box[5])
                if conf > confidence:
                    if classNames[cls] == 'real':
                        color = (0, 255, 0)
                    else:
                        color = (0, 0, 255)
                    cvzone.cornerRect(img, (x1, y1, w, h), 20, 1, color, 2)
                    cvzone.putTextRect(img, f'{classNames[cls].upper()} {int(conf*100)}%',
                                       (max(0, x1), max(35, y1)), scale=2, thickness=4, colorR=color, colorB=color)

        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        print(fps)

        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        image = request.files['image'].read()  # 获取上传的图片文件并读取其内容
        save_to_database(username, image)
        return jsonify({'message': 'Registration successful'})
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/video_feed')
def video_feed():
    return Response(detect_objects(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/vote')
def vote():
    return render_template('vote.html')

if __name__ == '__main__':
    app.run()
