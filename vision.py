import cv2
import time
import requests

def main():
    print("Mycelium Vision Sensing Active (Face Detection Mode).")
    
    # Load the pre-trained Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    last_presence_update = 0
    user_present = False

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to grayscale for the classifier
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            currently_present = len(faces) > 0
            
            # Notify the system if presence state changes or every 10 seconds
            if currently_present != user_present or (time.time() - last_presence_update > 10):
                user_present = currently_present
                last_presence_update = time.time()
                status = "PRESENT" if user_present else "ABSENT"
                print(f"👁️ User status: {status}")
                
                # We can send this to app.py to let the agent know it's being watched
                try:
                    requests.post("http://localhost:7000/vision/presence", json={"status": status}, timeout=1)
                except:
                    pass

            # Heartbeat for debugging
            if int(time.time()) % 15 == 0:
                print(f"Vision Heartbeat: Scanning... (Faces found: {len(faces)})")
                time.sleep(1)
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nStopping vision sensing...")
    finally:
        cap.release()

if __name__ == "__main__":
    main()
