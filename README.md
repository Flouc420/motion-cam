# motion-cam

A tiny motion-detection camera in Python. When something moves in front of the camera, it records a short clip and sends it to you on Telegram.

Built for an **InnoMaker USB 2.0 UVC 1080P day/night camera (IR-cut)**, but any USB webcam that OpenCV can open will work.

## How it works

1. OpenCV grabs frames from the camera.
2. A background subtractor (`MOG2`) compares each frame to what the scene normally looks like.
3. If enough pixels changed (`MIN_PIXELS`), recording starts.
4. Recording stops after `STOP_AFTER` seconds without motion, or after `MAX_SECONDS` max.
5. The `.mp4` clip is sent to your Telegram chat in a background thread, so the camera keeps watching while it uploads.

## Setup

**1. Create a Telegram bot**

- Talk to [@BotFather](https://t.me/BotFather) → `/newbot` → copy the token.
- Send your new bot a message, then open `https://api.telegram.org/bot<TOKEN>/getUpdates` to find your `chat.id`.

**2. Install**

```bash
git clone https://github.com/Flouc420/motion-cam.git
cd motion-cam
py -m pip install -r requirements.txt     # Windows (use python3 on Linux)
```

**3. Configure**

Copy `.env.example` to `.env` and fill in your values:

```
TELEGRAM_TOKEN=123456:your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
CAMERA_INDEX=1
```

`.env` is git-ignored — your token never ends up on GitHub.

**4. Run**

```bash
py motion_cam.py
```

Press `Ctrl+C` to stop.

## Tuning

| Setting | Default | Meaning |
|---|---|---|
| `MIN_PIXELS` | 4000 | Raise if you get false alarms, lower if nothing triggers |
| `MAX_SECONDS` | 20 | Longest clip |
| `STOP_AFTER` | 6 | Seconds of calm before the clip ends |
| `CAMERA_INDEX` | 1 | Try 0, 1 or 2 if the wrong camera opens |

## Status / next steps

- Done: Works on Windows 11 (Python 3.13, `cv2.CAP_DSHOW` backend)
- Next: Port to a low-power always-on board so the PC can stay off
- Next: Daily/night mode tuning for the IR-cut filter

## Stack

Python · OpenCV · requests · python-dotenv · Telegram Bot API
