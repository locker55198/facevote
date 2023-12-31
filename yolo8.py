from ultralytics import YOLO
import cv2
import math
import cvzone

def detect_objects():
    confidence = 0.6
    cap = cv2.VideoCapture(0)  # For Webcam
    cap.set(3, 640)
    cap.set(4, 480)
    
    model = YOLO("model/best.pt")

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


    
