"""PC webcam preview: python final_detect_demo.py (Q to quit)."""
import argparse
import os
import time
from drink_detector import DrinkDetector, add_detector_arguments, validate_arguments, draw_frame


def main():
    parser = argparse.ArgumentParser(description='PC webcam drink detection preview')
    add_detector_arguments(parser)
    parser.add_argument('--camera', type=int, default=0)
    args = parser.parse_args()
    validate_arguments(args, parser)
    import cv2
    detector = DrinkDetector(args)
    camera = None
    try:
        camera = cv2.VideoCapture(args.camera, cv2.CAP_DSHOW if os.name == 'nt' else cv2.CAP_ANY)
        if not camera.isOpened():
            raise RuntimeError('Cannot open webcam. Check --camera, camera permission, and other camera apps.')
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        while True:
            started = time.perf_counter()
            ok, frame = camera.read()
            if not ok:
                raise RuntimeError('Webcam frame read failed')
            regions, detections = detector.detect(frame)
            fps = 1 / max(time.perf_counter() - started, 1e-6)
            cv2.imshow('Drink Detection - PC', draw_frame(frame, regions, detections, fps))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        if camera is not None:
            camera.release()
        detector.close()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
