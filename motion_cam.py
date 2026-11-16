import os
import cv2, time, threading, requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TELEGRAM_TOKEN"]      # set in .env (see .env.example)
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
MIN_PIXELS = 4000      # raise it if you get false alarms, lower it if nothing triggers
MAX_SECONDS = 20       # maximum length of one clip
STOP_AFTER = 6         # seconds without motion before the clip ends
CAMERA_INDEX = int(os.environ.get("CAMERA_INDEX", "1"))       # try 1 or 2 if the wrong camera opens


def send(path):
    try:
        with open(path, "rb") as f:
            r = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendVideo",
                data={"chat_id": CHAT_ID, "caption": "there's someone in ur room girl"},
                files={"video": f},
                timeout=120,
            )
        print("Telegram:", r.status_code)
    except Exception as e:
        print("Send failed:", e)


cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    raise SystemExit("Camera not found. Try another CAMERA_INDEX (1 or 2).")

bg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)

writer, name, start, last = None, None, 0, 0
time.sleep(2)  # let the camera settle
print("Running. Press Ctrl+C to stop.")

try:
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Could not read from camera.")
            break

        mask = bg.apply(frame)
        mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)[1]
        now = time.time()

        if cv2.countNonZero(mask) > MIN_PIXELS:
            last = now
            if writer is None:
                name = time.strftime("clip_%Y%m%d_%H%M%S.mp4")
                h, w = frame.shape[:2]
                writer = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*"mp4v"), 15, (w, h))
                start = now
                print("Motion detected, recording", name)

        if writer is not None:
            writer.write(frame)
            if now - last > STOP_AFTER or now - start > MAX_SECONDS:
                writer.release()
                threading.Thread(target=send, args=(name,), daemon=True).start()
                writer = None
except KeyboardInterrupt:
    pass
finally:
    if writer is not None:
        writer.release()
    cap.release()
    print("Stopped.")