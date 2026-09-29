# ESDproject

Beverage detection for an Embedded System Design course project.
YOLOv5 detects **bottles, cans, and cups** near hands located by MediaPipe.

## Programs

| File | Purpose |
| --- | --- |
| `final_detect_demo.py` | PC webcam preview with detection boxes and FPS |
| `final_drinkdetection.py` | Raspberry Pi camera detection with a buzzer and optional email alerts |
| `drink_detector.py` | Shared detection functions used by both programs |

Use the included `best.pt` for detection. No dataset download or training is required to run it.

After [setup](docs/usage.md#setup), run:

```bash
# PC webcam
python final_detect_demo.py

# Raspberry Pi
python final_drinkdetection.py
```

See [Usage](docs/usage.md) for dependencies, camera options, GPIO, and email settings.

## Training

The model was fine-tuned from **YOLOv5s** for three classes: `bottle`, `can`, and `cup`.
Training used **512-pixel images, a batch size of 16, and 100 epochs**.

The project's dataset is available on [Roboflow, Version 2](https://universe.roboflow.com/s-workspace-v63wd/drink-detection-utuvg/dataset/2).
This version contains 695 images for inspection and further training; it is not confirmed as the original training snapshot.

See [Dataset and training](docs/training.md) to download the data in Colab or fine-tune the included `best.pt`.

## Results

Training and validation losses, precision, recall, and mAP from the run that produced `best.pt`:

![Training results](assets/results.png)

<details>
<summary>Class confusion matrix</summary>

![Confusion matrix](assets/confusion_matrix.png)

</details>

The revised scripts still need end-to-end testing on the target hardware. Detection is limited to hand ROIs.

[Original demos and project history](docs/experiments.md) · [Options and tests](docs/usage.md#detection-settings-and-checks)
