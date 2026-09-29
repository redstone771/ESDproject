"""Raspberry Pi: Picamera2 + GPIO buzzer, optional email and preview."""
import argparse
import os
import smtplib
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from email.mime.text import MIMEText
from drink_detector import DrinkDetector, add_detector_arguments, validate_arguments, draw_frame


class Buzzer:
    """A timer stops each pulse without blocking camera processing."""
    def __init__(self, gpio, pin):
        self.gpio, self.pin = gpio, pin
        self.lock = threading.Lock()
        self.timer = None
        self.active = False
        self.closed = False
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.OUT, initial=gpio.LOW)
        self.pwm = gpio.PWM(pin, 1000)
        self.pwm.start(0)

    def trigger(self):
        with self.lock:
            if self.active or self.closed:
                return
            self.pwm.ChangeDutyCycle(50)
            self.active = True
            self.timer = threading.Timer(0.5, self._stop_pulse)
            self.timer.daemon = True
            self.timer.start()

    def _stop_pulse(self):
        with self.lock:
            if not self.closed:
                self.pwm.ChangeDutyCycle(0)
                self.active = False

    def close(self):
        with self.lock:
            self.closed = True
            if self.timer:
                self.timer.cancel()
            self.pwm.stop()
            self.gpio.cleanup(self.pin)


class EmailNotifier:
    """Opt-in SMTP alerts, at most one attempt per 60 seconds."""
    def __init__(self, recipient):
        self.recipient = recipient
        self.user = os.environ.get('SMTP_USER')
        self.password = os.environ.get('SMTP_PASSWORD')
        if not self.user or not self.password:
            raise ValueError('--email requires SMTP_USER and SMTP_PASSWORD environment variables')
        self.host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        self.port = int(os.environ.get('SMTP_PORT', '587'))
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future = None
        self.last_attempt = float('-inf')

    def notify(self):
        now = time.monotonic()
        if now - self.last_attempt < 60 or (self.future is not None and not self.future.done()):
            return
        self.last_attempt = now
        self.future = self.executor.submit(self._send)

    def _send(self):
        message = MIMEText('A bottle, can or cup was detected near a hand.')
        message['Subject'] = 'Drink detection alert'
        message['From'], message['To'] = self.user, self.recipient
        try:
            with smtplib.SMTP(self.host, self.port, timeout=10) as smtp:
                smtp.starttls()
                smtp.login(self.user, self.password)
                smtp.sendmail(self.user, [self.recipient], message.as_string())
            print('Email alert sent')
        except Exception as exc:
            print(f'Email alert failed ({type(exc).__name__}); camera detection continues.')

    def close(self):
        self.executor.shutdown(wait=False, cancel_futures=True)


def main():
    parser = argparse.ArgumentParser(description='Raspberry Pi drink detection and buzzer')
    add_detector_arguments(parser)
    parser.add_argument('--buzzer-pin', type=int, default=4, help='BCM GPIO number (default 4)')
    parser.add_argument('--preview', action='store_true', help='Show OpenCV window; Q exits')
    parser.add_argument('--email', help='Optional alert recipient; SMTP credentials come from environment')
    args = parser.parse_args()
    validate_arguments(args, parser)
    if not 0 <= args.buzzer_pin <= 27:
        parser.error('--buzzer-pin must be a BCM GPIO number between 0 and 27')
    from picamera2 import Picamera2
    import RPi.GPIO as GPIO
    detector = camera = buzzer = notifier = None
    camera_started = False
    try:
        if args.email:
            notifier = EmailNotifier(args.email)
        detector = DrinkDetector(args)
        camera = Picamera2()
        # Picamera2 RGB888 capture_array uses byte order B,G,R, matching OpenCV.
        camera.configure(camera.create_preview_configuration(main={'format': 'RGB888', 'size': (640, 480)}))
        camera.start()
        camera_started = True
        buzzer = Buzzer(GPIO, args.buzzer_pin)
        while True:
            started = time.perf_counter()
            frame = camera.capture_array('main')
            regions, detections = detector.detect(frame)
            if detections:
                buzzer.trigger()
                if notifier:
                    notifier.notify()
            fps = 1 / max(time.perf_counter() - started, 1e-6)
            print(f'FPS: {fps:.2f} | drink: {bool(detections)}', flush=True)
            if args.preview:
                import cv2
                cv2.imshow('Drink Detection - Raspberry Pi', draw_frame(frame, regions, detections, fps))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except KeyboardInterrupt:
        pass
    finally:
        if buzzer:
            buzzer.close()
        if camera:
            if camera_started:
                camera.stop()
            camera.close()
        if detector:
            detector.close()
        if notifier:
            notifier.close()
        if args.preview:
            import cv2
            cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
