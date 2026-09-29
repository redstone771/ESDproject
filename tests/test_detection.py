import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch
from drink_detector import hand_rois, frame_box, DRINK_CLASSES
from final_drinkdetection import Buzzer, EmailNotifier


class DetectionTests(unittest.TestCase):
    def test_no_hand(self):
        self.assertEqual(hand_rois((480, 640, 3), SimpleNamespace(multi_hand_landmarks=None), 140), [])

    def test_roi_at_image_edge(self):
        hand = SimpleNamespace(landmark=[SimpleNamespace(x=0.01, y=0.02), SimpleNamespace(x=0.1, y=0.1)])
        self.assertEqual(hand_rois((480, 640, 3), SimpleNamespace(multi_hand_landmarks=[hand]), 140), [(0, 0, 204, 188)])

    def test_box_maps_to_non_square_roi(self):
        self.assertEqual(frame_box([80, 80, 240, 240], (100, 50, 500, 250)), (200, 100, 400, 200))
        self.assertEqual(frame_box([-10, -10, 330, 330], (100, 50, 500, 250)), (100, 50, 499, 249))

    def test_new_classes(self):
        self.assertEqual(DRINK_CLASSES, {'bottle', 'can', 'cup'})

    @patch('final_drinkdetection.threading.Timer')
    def test_buzzer_pulse_and_cleanup(self, timer):
        gpio = Mock()
        buzzer = Buzzer(gpio, 4)
        buzzer.trigger()
        buzzer.trigger()
        self.assertEqual(timer.call_count, 1)
        buzzer._stop_pulse()
        gpio.PWM.return_value.ChangeDutyCycle.assert_called_with(0)
        buzzer.close()
        buzzer.trigger()
        self.assertEqual(timer.call_count, 1)
        gpio.cleanup.assert_called_once_with(4)

    @patch.dict('os.environ', {'SMTP_USER': 'test@example.com', 'SMTP_PASSWORD': 'test-only'})
    @patch('final_drinkdetection.ThreadPoolExecutor')
    @patch('final_drinkdetection.time.monotonic', side_effect=[0, 59, 60])
    def test_email_interval(self, clock, executor):
        executor.return_value.submit.return_value.done.return_value = True
        notifier = EmailNotifier('recipient@example.com')
        notifier.notify()
        notifier.notify()
        self.assertEqual(executor.return_value.submit.call_count, 1)
        notifier.notify()
        self.assertEqual(executor.return_value.submit.call_count, 2)
        notifier.close()


if __name__ == '__main__':
    unittest.main()
