# Usage

[Back to README](../README.md)

## Setup

From this repository's directory:

```bash
git clone https://github.com/ultralytics/yolov5.git yolov5
python -m pip install -r yolov5/requirements.txt
python -m pip install "mediapipe==0.10.21"
```

This code uses the MediaPipe Hands `solutions` API. If you already have a working YOLOv5/PyTorch environment for this model, keep it. The installation commands are not a tested dependency lock for every platform.

Keep `best.pt` beside the scripts. Use `--weights` for a different model path or `--yolov5-dir` for an existing YOLOv5 checkout.

```text
ESDproject/
  best.pt
  drink_detector.py
  final_detect_demo.py
  final_drinkdetection.py
  yolov5/
```

## PC preview

```bash
python final_detect_demo.py
# Select another webcam if needed:
python final_detect_demo.py --camera 1
```

Press **Q** or **Ctrl+C** to exit. The window shows hand ROIs, detected classes, confidence scores, and processing FPS. Windows uses DirectShow for webcam capture.

## Raspberry Pi

Use a Raspberry Pi OS environment with Picamera2, OpenCV, and a compatible `RPi.GPIO` backend. A virtual environment must also have access to the OS camera packages. Board-specific GPIO support needs to be checked on the target device.

```bash
python final_drinkdetection.py
# Optional preview on a connected display:
python final_drinkdetection.py --preview
```

The buzzer defaults to **BCM GPIO 4**, with a 1 kHz PWM signal and 0.5-second pulses. Use `--buzzer-pin` to change the pin. Continued detection can trigger repeated pulses. Press **Ctrl+C** to stop and release the camera and GPIO.

### Email alerts

Email is optional; detection and the buzzer work without it. To enable alerts, provide a sender account you control, its app password, and a recipient address. The defaults use Gmail SMTP with STARTTLS on port 587. Other providers require matching `SMTP_HOST`, `SMTP_PORT`, and authentication settings.

In a Raspberry Pi Bash terminal:

```bash
read -r -p "Sender Gmail address: " SMTP_USER
read -r -s -p "Sender app password: " SMTP_PASSWORD
printf '\n'
export SMTP_USER SMTP_PASSWORD
read -r -p "Recipient email address: " ALERT_RECIPIENT
python final_drinkdetection.py --email "$ALERT_RECIPIENT"
```

The password is hidden during entry. These settings apply to the current terminal session. Alerts are attempted on detection, at least 60 seconds apart. Email failures do not stop the detection loop. Previously exposed credentials must be revoked; do not reuse them.

## Detection settings and checks

- Default confidence: `0.55`; NMS IoU: `0.45`; hand ROI margin: `140` pixels. Adjust with `--conf`, `--iou`, and `--margin`.
- Each hand ROI is resized to 320 x 320 for inference. Objects outside hand ROIs are not processed.
- FPS measures frame capture and detection, excluding display and logging time.
- Tests cover ROI boundaries, coordinate mapping, buzzer pulses, and email intervals. The revised code still needs end-to-end testing with the model, cameras, GPIO, and email service.

```bash
python -m unittest discover -s tests -v
```
