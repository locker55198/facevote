register前

def authenticate_user(username, image):
    # 連接到MySQL數據庫
    cnx = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database'
    )
    
    cursor = cnx.cursor()

    # 從數據庫獲取用戶名和圖片
    select_query = """
        SELECT username, image FROM users WHERE username = %s
    """
    cursor.execute(select_query, (username,))
    user = cursor.fetchone()

    if user:
        # 將接收到的圖片保存到本地
        image_path = f"uploads/{username}.jpg"
        with open(image_path, "wb") as file:
            file.write(image)

        # 使用YOLO進行圖片比對
        model = YOLO("models/best.pt")
        img = cv2.imread(image_path)
        results = model(img, stream=False, verbose=False)
        
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

        # 比對結果處理
        # 處理比對結果後返回結果
        # 如果比對結果符合要求，返回 "Login successful"
        # 如果比對結果不符合要求，返回 "Login failed"
        # 例如：
        if 比對結果符合要求:
            return "Login successful"
        else:
            return "Login failed"
    else:
        return "Login failed"

    cnx.commit()
    cursor.close()
    cnx.close()

    register :
    , methods=['GET', 'POST']
    if request.method == 'POST':
        username = request.form.get('username')
        image = request.files['image'].read()  # 獲取上傳的圖片文件並讀取其內容
        save_to_database(username, image)
        return jsonify({'message': 'Registration successful'})
    
    login:
    , methods=['GET', 'POST']
    if request.method == 'POST':
        username = request.form.get('username')
        image = request.files['image'].read()  # 獲取上傳的圖片文件並讀取其內容
        result = authenticate_user(username, image)
        if result == "Login successful":
            # 登錄成功的處理邏輯
            print('Login successful')
            return render_template('vote.html')
        else:
            # 登錄失敗的處理邏輯
            print('Login failed')
            return jsonify({'message': 'Login failed'})
