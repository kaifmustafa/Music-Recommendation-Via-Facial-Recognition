import cv2
from fer import FER

# Webcam start
cap = cv2.VideoCapture(0)

detector = FER(mtcnn=True)

print("Camera started. Press 'q' to capture emotion.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.imshow("Live Camera", frame)

    # Press 'q' to detect emotion and exit camera
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Detect emotion
        result = detector.top_emotion(frame)
        emotion, score = result if result else ("neutral", 0)
        print(f"Detected Emotion: {emotion}")
        break

cap.release()
cv2.destroyAllWindows()

# Save emotion in file for Flask to read
with open("current_emotion.txt", "w") as f:
    f.write(emotion)

print("Emotion saved. You can now open the Flask web app.")