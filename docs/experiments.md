# Experiments and project history

[Back to README](../README.md)

## Experiments

The demos below are from the original project and were not re-recorded with the updated model and scripts.

<details>
  <summary>Early experiments</summary>

Laptop and built-in webcam

![Image](https://github.com/user-attachments/assets/fc4f456f-3b0d-4c6a-981f-c8e199b8afdd)

Raspberry Pi and Pi Camera

![Image](https://github.com/user-attachments/assets/e3dd7413-1ae2-46ce-8cd6-c850b1fba399)

</details>

<details>
<summary>Camera placement</summary>

![Image](https://github.com/user-attachments/assets/9cd823a8-c96f-45ff-9fe8-a5d4332f915f)
![Image](https://github.com/user-attachments/assets/fa1b72c7-9eb1-470d-92fd-94f2550e0936)
![Image](https://github.com/user-attachments/assets/31e0666b-5520-4d71-9fdb-49232b3628a7)

</details>

---

### Training results

<details>
<summary>Bottle / can / cup training results</summary>

These plots were generated during the same training run as the included `best.pt`.

Training and validation losses, precision, recall, and mAP:
- Left six plots: train/validation box, objectness, and classification loss.
- Right four plots: precision, recall, mAP@0.5, and mAP@0.5:0.95.
- Blue: recorded values. Orange: smoothed trend, not a second model.

![Training and validation losses, precision, recall and mAP](../assets/results.png)

Class confusion matrix:

![Confusion matrix for bottle, can and cup](../assets/confusion_matrix.png)

</details>

<details>
<summary>Original project demos</summary>

* **Final Model**
  ![Image](https://github.com/user-attachments/assets/a057fc08-da42-4771-b00f-6004a60cbd4b)
  ![Image](https://github.com/user-attachments/assets/78a53ba7-87fb-4dd6-a1ad-d0710e6cb37a)

* Model Behavior Without a Drink
  ![Image](https://github.com/user-attachments/assets/f3754cc3-ccf6-4c57-aecd-0c1795e5300e)

* Model Performance on Corner Case
  ![Image](https://github.com/user-attachments/assets/bb3400a9-2714-4aff-8fcf-27467c2150ac)

* Comparison Model: Without ROI
  ![Image](https://github.com/user-attachments/assets/12580495-fa02-4e9f-9c3a-5722016f93e2)
  ![Image](https://github.com/user-attachments/assets/f8da88cf-784d-444e-a959-7a1d92ed3464)

</details>

## Project history

| Week | Work |
| --- | --- |
| 8 | Collected images |
| 9 | Built the initial YOLO and ROI pipeline |
| 10 | Added Raspberry Pi camera and buzzer control |
| 11 | Tested on Raspberry Pi and investigated low FPS |
| 12 | Reviewed comparison models during final exam week |
| 13 | Added MediaPipe hand ROIs to address speed and corner cases |
| 14 | Collected results and compared approaches |

The original comparisons used custom data, custom + COCO data, and custom + COCO data with ROI processing. The current weights and training curves belong to the later bottle/can/cup model.

## Change log

- **2026-09-29:** Updated the model and training plots, moved dataset distribution to Roboflow, and separated PC preview from Raspberry Pi alerts.
- **2025-06-10:** Added `final_drinkdetection.py`.
- **2025-05-26:** Added 46 labeled images (279 total) and updated `best.pt`.
- **2025-05-15:** Added training code and model weights.
- **2025-05-14:** Added Raspberry Pi inference, ROI processing, and buzzer output.
- **2025-05-05:** Added the initial 233 labeled images.
