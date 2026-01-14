import cv2
from deepface import DeepFace

# Face detection model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow("Emotion Detection", cv2.WINDOW_NORMAL)
cv2.setWindowProperty(
    "Emotion Detection",
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]

        try:
            result = DeepFace.analyze(
                face_img,
                actions=['emotion'],
                enforce_detection=False
            )
            emotion = result[0]['dominant_emotion']
        except:
            emotion = "Detecting..."

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"Emotion: {emotion}",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2)

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
