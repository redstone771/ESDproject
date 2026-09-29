# ESDproject

This repository contains the code for 'Embedded System Design' course project.

Our model, based on YOLOv5, detects beverages and triggers a buzzer alarm upon detection.    
On Raspberry Pi, email alerts can be enabled with SMTP settings.    
MediaPipe is used to detect hands and set a ROI, improving accuracy and frame rate.
 

This system is expected to be applicable in various environments such as hospitals, public transportation, and libraries.

## Index

[🗺️Roadmap](#roadmap)  
[📝Change Log](#change-log)  
[📂Dataset](#dataset)  
[🧠Model for Comparative Evaluation](#model-for-comparative-evaluation)   
[🚀 How to Use the Model](#How-to-Use-the-Model)  
[🔬Experiments](#experiments)  




## Roadmap
8주차: 데이터 수집

9주차: 데이터 수집, ROI 설정한 YOLO모델 구현

>	Fps, 최적화 등 코드 보완 필요

10주차: 데이터 수집, 라즈베리파이에서의 buzzer, picamera 코드 작성

11주차: FPS 향상을 위한 코드 보완, 실제 라즈베리파이로 실험

>	예상보다 라즈베리파이에서의 fps가 너무 낮음. 추가적인 보완 필요.

12주차: (기말고사),  기존연구에서 비교모델 찾기

13주차: 코너 케이스에 대한 ROI 코드 설정

> 코너케이스와 낮은 fps를 보완하기 위해 MediaPipe 활용

14주차: 결과정리, 비교, 분석


## Change log

[26/09/29] Updated `best.pt` and training results for bottle/can/cup detection. Added separate PC and Raspberry Pi entry points and moved dataset downloads to Roboflow.

[25/05/05] Uploaded custom dataset: 233 images with labels.

[25/05/14] Uploaded inference code for Raspberry Pi and PiCamera.

>Includes ROI setting, buzzer activation upon detecting 'drinks' and FPS display functionality.

[25/05/15] Uploaded training code, including the trained weights best.pt.

[25/05/26] Add 46 images with labels (total 279)   

[25/05/26] Uploaded `best.pt`

[25/06/10] Uploaded `final_drinkdetection.py`


## Dataset

The dataset is available on [Roboflow — Drink Detection, Version 2](https://universe.roboflow.com/s-workspace-v63wd/drink-detection-utuvg/dataset/2) instead of the bundled `dataset/` folder.

- Classes: **bottle, can, cup**
- Version 2: **695 images** (384 train / 251 validation / 60 test), CC BY 4.0
- Use `best.pt` for detection; downloading the dataset is optional.

The model was trained from `yolov5s.pt` with image size **512**, batch size **16**, and **100 epochs**. Version 2 is provided for inspection and further training; it is not confirmed as the original training snapshot.

See [Dataset download and training](docs/training.md) for Colab instructions and fine-tuning `best.pt`.

## Model for Comparative Evaluation

The following describes the original comparison setup.
  
  기본 YOLO+ 커스텀 데이터

  기본 YOLO+ 커스텀 & coco 데이터 학습
  
  기본 YOLO+ 커스텀 & coco 데이터 학습+ ROI설정 (*최종 목표)
     
## How to Use the Model

| File | Purpose |
| --- | --- |
| `final_detect_demo.py` | PC webcam preview with detection boxes and FPS |
| `final_drinkdetection.py` | Raspberry Pi camera detection with a buzzer and optional email alerts |
| `drink_detector.py` | Shared detection functions imported by both scripts |

Both programs use the included `best.pt` for **bottle, can, and cup** detection.

```bash
# PC webcam
python final_detect_demo.py

# Raspberry Pi
python final_drinkdetection.py
```

See [Setup and usage](docs/usage.md) for installation, camera/GPIO options, and email settings.
The revised scripts still need end-to-end testing on the target hardware.

## Experiments

<details>
  <summary>중간결과</summary>

노트북 & 내장웹캠

![Image](https://github.com/user-attachments/assets/fc4f456f-3b0d-4c6a-981f-c8e199b8afdd)

라즈베리파이 & picamera

![Image](https://github.com/user-attachments/assets/e3dd7413-1ae2-46ce-8cd6-c850b1fba399)

</details> 


<details>
<summary>📷 Recommended Camera Installation Environment</summary>

![Image](https://github.com/user-attachments/assets/9cd823a8-c96f-45ff-9fe8-a5d4332f915f)  
![Image](https://github.com/user-attachments/assets/fa1b72c7-9eb1-470d-92fd-94f2550e0936)  
![Image](https://github.com/user-attachments/assets/31e0666b-5520-4d71-9fdb-49232b3628a7)   


</details>



---

### 최종결과

<details>
<summary>📊 Bottle / Can / Cup Training Results</summary>

Results from the training run that produced the current `best.pt`.

* Training/validation losses, precision, recall, and mAP
![Training results](assets/results.png)

* Class confusion matrix
![Confusion matrix](assets/confusion_matrix.png)

</details>


<details>
<summary>🎥 Model Demo Video</summary>

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



