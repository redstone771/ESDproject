"""Shared hand-ROI detection for the PC and Raspberry Pi entry points."""
import argparse
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DRINK_CLASSES = frozenset(('bottle', 'can', 'cup'))


def add_detector_arguments(parser):
    parser.add_argument('--weights', type=pathlib.Path, default=ROOT / 'best.pt')
    parser.add_argument('--yolov5-dir', type=pathlib.Path, default=ROOT / 'yolov5')
    parser.add_argument('--conf', type=float, default=0.55)
    parser.add_argument('--iou', type=float, default=0.45)
    parser.add_argument('--margin', type=int, default=140)


def validate_arguments(args, parser):
    if not 0 < args.conf < 1 or not 0 < args.iou < 1:
        parser.error('--conf and --iou must be between 0 and 1')
    if args.margin < 0:
        parser.error('--margin must be nonnegative')


def hand_rois(frame_shape, hand_results, margin):
    """Clip landmark bounds plus padding to the image; skip empty regions."""
    height, width = frame_shape[:2]
    regions = []
    for hand in hand_results.multi_hand_landmarks or []:
        xs = [int(point.x * width) for point in hand.landmark]
        ys = [int(point.y * height) for point in hand.landmark]
        if not xs:
            continue
        x1, y1 = max(0, min(xs) - margin), max(0, min(ys) - margin)
        x2, y2 = min(width, max(xs) + margin), min(height, max(ys) + margin)
        if x2 > x1 and y2 > y1:
            regions.append((x1, y1, x2, y2))
    return regions


def frame_box(box, roi, image_size=320):
    """Undo the supplied demo's square resize and add the ROI offset."""
    x1, y1, x2, y2 = roi
    coordinates = []
    for value, offset, end in zip(box, (x1, y1, x1, y1), (x2, y2, x2, y2)):
        coordinates.append(max(offset, min(end - 1, int(float(value) * (end - offset) / image_size) + offset)))
    return tuple(coordinates)


class DrinkDetector:
    def __init__(self, args):
        weights = args.weights.resolve()
        yolov5 = args.yolov5_dir.resolve()
        if not weights.is_file():
            raise FileNotFoundError(f'Model not found: {weights}')
        if not (yolov5 / 'models' / 'common.py').is_file():
            raise FileNotFoundError(f'Clone ultralytics/yolov5 into {yolov5}, or set --yolov5-dir')
        import cv2
        import torch
        import mediapipe as mp
        if not hasattr(mp, 'solutions'):
            raise RuntimeError('This implementation needs MediaPipe Hands solutions (e.g. mediapipe==0.10.21).')
        sys.path.insert(0, str(yolov5))
        from models.common import DetectMultiBackend
        from utils.general import non_max_suppression
        from utils.torch_utils import select_device
        self.cv2, self.torch = cv2, torch
        self.nms = non_max_suppression
        self.device = select_device('cpu')
        # Linux-trained checkpoints may contain PosixPath objects. Resolve all
        # paths first and limit the Windows compatibility alias to model loading.
        original_posix = pathlib.PosixPath
        try:
            if os.name == 'nt':
                pathlib.PosixPath = pathlib.WindowsPath
            self.model = DetectMultiBackend(str(weights), device=self.device)
        finally:
            pathlib.PosixPath = original_posix
        self.model.eval()
        self.names = self.model.names
        labels = self.names.values() if isinstance(self.names, dict) else self.names
        missing = DRINK_CLASSES - {str(label).strip().lower() for label in labels}
        if missing:
            raise ValueError(f'Model is missing expected classes: {sorted(missing)}')
        self.conf, self.iou, self.margin = args.conf, args.iou, args.margin
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False, max_num_hands=2,
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
        print('Loaded classes:', self.names)

    def detect(self, frame):
        """Input is an OpenCV BGR frame. No hand means no drink inference."""
        cv2, torch = self.cv2, self.torch
        hand_results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        regions = hand_rois(frame.shape, hand_results, self.margin)
        detections = []
        for region in regions:
            x1, y1, x2, y2 = region
            crop = frame[y1:y2, x1:x2]
            rgb = cv2.cvtColor(cv2.resize(crop, (320, 320)), cv2.COLOR_BGR2RGB)
            tensor = torch.from_numpy(rgb).permute(2, 0, 1).float().div(255).unsqueeze(0).to(self.device)
            with torch.inference_mode():
                prediction = self.nms(self.model(tensor), conf_thres=self.conf, iou_thres=self.iou)[0]
            if prediction is None:
                continue
            for *box, confidence, class_id in prediction:
                label = str(self.names[int(class_id)]).strip().lower()
                if label in DRINK_CLASSES:
                    detections.append((frame_box(box, region), label, float(confidence)))
        return regions, detections

    def close(self):
        self.hands.close()


def draw_frame(frame, regions, detections, fps):
    import cv2
    for x1, y1, x2, y2 in regions:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
        cv2.putText(frame, 'Hand ROI', (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    for (x1, y1, x2, y2), label, confidence in detections:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'{label} {confidence:.2f}', (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    status = 'No hand ROI' if not regions else ('Drink detected' if detections else 'No drink detected')
    cv2.putText(frame, status, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
    cv2.putText(frame, f'FPS: {fps:.2f} | Q: quit', (10, frame.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    return frame
