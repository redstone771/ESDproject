# ESDproject

This repository contains the code for 'Embedded System Design' course project.

Our model, based on YOLOv5, detects beverages and triggers a buzzer alarm upon detection.    
On Raspberry Pi, optional email alerts can be enabled with SMTP environment settings.
MediaPipe detects hands and limits beverage detection to surrounding regions of interest (ROIs).
 

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

[26/09/29] Replaced `best.pt` with the bottle/can/cup model and updated training results. Removed the bundled dataset and added Roboflow download instructions. Added separate PC preview and Raspberry Pi buzzer entry points for the new classes; SMTP credentials are supplied through environment variables.

[25/05/05] Uploaded custom dataset: 233 images with labels.

[25/05/14] Uploaded inference code for Raspberry Pi and PiCamera.

>Includes ROI setting, buzzer activation upon detecting 'drinks' and FPS display functionality.

[25/05/15] Uploaded training code, including the trained weights best.pt.

[25/05/26] Add 46 images with labels (total 279)   

[25/05/26] Uploaded `best.pt`

[25/06/10] Uploaded `final_drinkdetection.py`


## Dataset

현재 `best.pt`는 음료 용기를 **bottle, can, cup** 세 클래스로 구분해 재학습한 모델입니다.
**탐지만 실행하려면 저장소의 `best.pt`를 사용하면 됩니다. 데이터셋 다운로드나 재학습은 필요하지 않습니다.**

프로젝트의 이미지·라벨을 살펴보거나 `best.pt`를 추가 학습하려는 경우에는 **이 프로젝트 작성자의 아래 Roboflow 데이터셋**을 다운로드하세요.
이미지와 라벨은 GitHub의 `dataset/` 폴더 대신 Roboflow에서 관리합니다.

- [Drink Detection 데이터셋 Version 2 — Roboflow Universe](https://universe.roboflow.com/s-workspace-v63wd/drink-detection-utuvg/dataset/2)

Version 2는 데이터 확인과 추가 학습을 위해 공개한 버전입니다. 기존 `best.pt`의 원래 학습 버전과 동일하다고 확인된 것은 아닙니다.
공개 페이지 기준 총 695장(학습 384장, 검증 251장, 테스트 60장)이며, Auto-Orient 및 512×512 Stretch 전처리를 사용하고 증강은 적용하지 않았습니다.
데이터셋 라이선스는 공개 페이지에 표시된 CC BY 4.0을 따릅니다.

### Colab에서 데이터셋 다운로드

1. 위 **Drink Detection Version 2** 공개 링크를 엽니다. 버전 페이지는 로그인 없이 열람할 수 있습니다.
2. 페이지에 **Object Detection v2**가 표시되는지 확인하고 **Download Dataset** 또는 **YOLOv5** 항목을 선택합니다.
3. 다운로드 창에서 **YOLOv5** 형식을 선택합니다. 다운로드 과정에서 로그인을 요청하면 본인 Roboflow 계정으로 로그인합니다.
4. 다운로드 코드 표시 옵션에서 `curl -L` 뒤의 **다운로드 URL만** 복사합니다.
   URL에는 `https://app.roboflow.com/ds/…?key=…` 형태의 접근 키가 포함될 수 있으므로 공개 저장소에 붙여 넣지 않습니다.
5. Google Colab에서 아래 셀을 실행하고 복사한 URL을 입력합니다. 입력값은 화면에 표시하지 않습니다.

```python
from getpass import getpass
from pathlib import Path
import subprocess
import zipfile

download_url = getpass("Roboflow 다운로드 URL: ")
archive = Path("/content/roboflow.zip")
try:
    result = subprocess.run(
        ["curl", "--fail", "--location", "--silent", "--show-error",
         download_url, "--output", str(archive)],
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError("다운로드 실패: Roboflow에서 URL을 다시 발급받고 접근 권한을 확인하세요.")
    if not zipfile.is_zipfile(archive):
        raise RuntimeError("ZIP 파일이 아닙니다. 프로젝트 화면 주소 대신 Export 다운로드 URL을 입력하세요.")
    with zipfile.ZipFile(archive) as dataset_zip:
        dataset_zip.extractall("/content")
finally:
    download_url = None
    archive.unlink(missing_ok=True)

print("데이터셋 압축 해제 완료")
```

이 코드는 `curl`로 ZIP을 받고, `/content`에 압축을 푼 다음 ZIP만 삭제합니다.
압축을 푼 이미지와 라벨은 남습니다. GitHub 저장소의 Clone과는 별도의 다운로드입니다.
위 공개 Version 2 페이지에서 이 프로젝트의 데이터를 다운로드합니다. 다운로드 코드가 필요하지 않다면 ZIP 다운로드 방식으로 받아 내용을 살펴볼 수도 있습니다.

### 다운로드 확인과 재학습

다음 셀로 데이터 경로와 클래스 구성을 확인합니다.

```python
!cat /content/data.yaml
```

`names`에 `bottle`, `can`, `cup`이 있는지, `train`과 `val` 경로가 실제 압축 해제 위치를 가리키는지 확인합니다.
`data.yaml`이 없다면 `!find /content -name data.yaml`로 찾은 경로를 아래 `--data`에 사용합니다.

### 저장소의 best.pt를 추가 학습하기

위에서 **작성자의 Roboflow 데이터셋**을 `/content`에 다운로드한 뒤, Colab에서 다음 셀을 실행합니다.
첫 번째 clone은 이 프로젝트의 `best.pt`를 받기 위한 것이고, 두 번째 clone은 학습 프로그램인 YOLOv5를 받기 위한 것입니다.
**Roboflow 데이터셋 자체는 git clone으로 받는 것이 아닙니다.**

```python
%cd /content
!git clone https://github.com/redstone771/ESDproject.git
!git clone https://github.com/ultralytics/yolov5.git
%cd /content/yolov5
!pip install -r requirements.txt
```

이미 clone한 폴더가 있다면 해당 clone 줄은 다시 실행하지 않아도 됩니다.
Colab의 GPU 런타임에서 학습할 수 있습니다. 아래 명령은 현재 저장소의 모델을 초기 가중치로 사용해 추가 학습합니다.

```python
!python train.py --img 512 --batch 16 --epochs 100 --data /content/data.yaml --weights /content/ESDproject/best.pt --name drink_finetune
```

기존 모델의 클래스 의미를 유지하려면 `data.yaml`의 클래스 이름뿐 아니라 **클래스 순서도 기존 모델과 일치**해야 합니다.
이 명령은 기존 학습의 중단 지점을 복구하는 `--resume`이 아니라, `best.pt`에서 새로운 학습을 시작하는 방식입니다.
입력 `best.pt`는 덮어쓰지 않으며, 새 모델은 보통 아래 위치에 저장됩니다.

```text
/content/yolov5/runs/train/drink_finetune/weights/best.pt
/content/yolov5/runs/train/drink_finetune/results.png
/content/yolov5/runs/train/drink_finetune/results.csv
```

같은 실행 이름을 반복 사용하면 폴더 이름에 숫자가 붙을 수 있으므로 학습 로그에 표시되는 저장 경로를 확인하세요.
Colab 런타임을 종료하기 전에 새 모델과 결과 파일을 함께 내려받아 보관합니다.

### 참고용 원래 학습 설정

원래 모델은 다음과 같이 사전 학습된 `yolov5s.pt`에서 시작해 이미지 크기 512, 배치 크기 16, 100에포크로 학습했습니다.
현재 프로젝트의 `best.pt`를 더 학습하려면 위의 추가 학습 명령을 사용하세요.

```python
!python train.py --img 512 --batch 16 --epochs 100 --data /content/data.yaml --weights yolov5s.pt --name drink_bottle_can_cup
```

당시 Roboflow 버전과 YOLOv5 커밋은 기록 확인이 필요하므로, 이 안내는 동일한 학습 결과의 재현을 보장하지 않습니다.

## Model for Comparative Evaluation

아래는 초기 프로젝트의 비교 실험 구성입니다. 현재 `best.pt`와 아래 새 학습 그래프는 세 클래스로 재학습한 모델에 해당합니다.
  
  기본 YOLO+ 커스텀 데이터

  기본 YOLO+ 커스텀 & coco 데이터 학습
  
  기본 YOLO+ 커스텀 & coco 데이터 학습+ ROI설정 (*최종 목표)
     
## How to Use the Model

`best.pt`와 `assets/results.png`는 같은 학습에서 얻은 모델과 기록입니다.
두 실행 파일은 `drink_detector.py`의 공통 탐지 로직을 사용합니다.

| 실행 파일 | 용도 |
| --- | --- |
| `final_detect_demo.py` | PC 웹캠에서 손 ROI, bottle/can/cup 탐지 박스, 신뢰도, 처리 FPS 표시 |
| `final_drinkdetection.py` | Raspberry Pi의 Picamera2 입력으로 음료를 탐지하고 GPIO 부저 출력 |

### 준비

이미 제공된 PC 예제가 정상 동작한 Python/YOLOv5 환경을 사용하면 됩니다.
처음 설정하는 경우 저장소 폴더에서 YOLOv5 소스와 의존성을 준비합니다.
데이터셋은 추론에 필요하지 않습니다.

```bash
git clone https://github.com/ultralytics/yolov5.git yolov5
python -m pip install -r yolov5/requirements.txt
python -m pip install "mediapipe==0.10.21"
```

이 코드는 [MediaPipe Hands solutions API](https://github.com/google-ai-edge/mediapipe/blob/v0.10.21/mediapipe/python/solutions/hands.py)를 사용합니다.
위 명령은 설치 시작점이며 모든 OS·Python·PyTorch 조합에서 검증한 고정 환경은 아닙니다.
기존에 정상 동작한 YOLOv5와 PyTorch 버전을 우선 사용하세요. 다른 경로의 YOLOv5는 `--yolov5-dir`로 지정할 수 있습니다.
`best.pt`는 실행 파일들과 같은 폴더에 두며, 다른 모델 경로는 `--weights`로 지정합니다.

```text
ESDproject-update/
  best.pt
  drink_detector.py
  final_detect_demo.py
  final_drinkdetection.py
  yolov5/
    models/
    utils/
```

### PC 웹캠 확인

```bash
python final_detect_demo.py
# 카메라가 여러 대인 경우
python final_detect_demo.py --camera 1
```

Q 또는 Ctrl+C로 종료합니다. 손이 없을 때도 영상과 상태를 표시합니다.
Windows 웹캠은 DirectShow를 사용하며, Windows에서 Linux 학습 모델을 읽는 경로 호환 처리는 모델 로드 시에만 적용합니다.

### Raspberry Pi 부저

Picamera2, OpenCV, `RPi.GPIO`가 동작하는 Raspberry Pi OS 환경과 기존 부저 회로가 필요합니다.
가상환경을 사용한다면 OS의 Picamera2/libcamera 패키지에 접근 가능한 환경을 사용하세요.
GPIO 백엔드의 호환성은 보드에 따라 다르므로 모든 Raspberry Pi 모델에서 동작을 검증한 것은 아닙니다.

```bash
python final_drinkdetection.py
# 화면이 연결돼 있고 영상도 확인하려는 경우
python final_drinkdetection.py --preview
```

부저는 기존과 동일한 **BCM GPIO 4**, 1kHz PWM, 0.5초 펄스를 사용합니다.
다른 핀은 `--buzzer-pin`으로 지정합니다. 지속 탐지 시 펄스가 반복될 수 있습니다.
부저와 이메일 처리가 영상 루프를 직접 대기시키지 않도록 분리했습니다. Ctrl+C로 종료하면 카메라와 GPIO를 정리합니다.
카메라는 [Picamera2의 OpenCV용 RGB888 형식](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)을 사용하며, 입력 배열은 BGR 순서로 처리합니다.

### 선택 기능인 이메일 알림

기본 실행은 부저만 사용합니다. 이메일이 필요하면 환경변수 `SMTP_USER`, `SMTP_PASSWORD`를 설정하고 수신자를 전달합니다.
`SMTP_HOST`와 `SMTP_PORT`의 기본값은 `smtp.gmail.com`, `587`이며 STARTTLS로 연결합니다.
비밀번호는 저장소나 코드에 넣지 않습니다. 기존 공개 코드의 인증정보는 폐기하고 새 자격증명을 사용해야 합니다.

발신 주소는 본인이 사용할 권한이 있는 메일 계정이어야 하고, 앱 비밀번호는 그 발신 계정에서 발급한 값이어야 합니다.
수신 주소는 경고를 받을 사람의 주소이며 발신 주소와 달라도 됩니다. 기본 설정은 Gmail 발신 계정용입니다.
다른 메일 서비스는 해당 서비스의 SMTP 설정과 인증 방식을 확인해야 합니다.

Raspberry Pi의 Bash 터미널에서 다음 순서로 실행합니다. 앱 비밀번호는 화면에 표시되지 않도록 입력받습니다.

```bash
read -r -p "발신 Gmail 주소: " SMTP_USER
read -r -s -p "발신 계정의 앱 비밀번호: " SMTP_PASSWORD
printf '\n'
export SMTP_USER SMTP_PASSWORD
read -r -p "경고를 받을 이메일 주소: " ALERT_RECIPIENT
python final_drinkdetection.py --email "$ALERT_RECIPIENT"
```

환경변수는 이 터미널 세션에 적용되므로 새 터미널에서는 다시 설정합니다.
이메일이 필요 없으면 위 설정 없이 `python final_drinkdetection.py`만 실행하면 됩니다.
메일은 실행 즉시가 아니라 음료를 탐지했을 때 전송을 시도합니다. 네트워크와 계정 인증이 정상이어야 수신할 수 있습니다.

탐지 시 최소 60초 간격으로 전송을 시도하며, 이메일 실패는 카메라 탐지를 중단하지 않습니다.

### 탐지 범위와 검증 상태

- 두 실행 파일 모두 `bottle`, `can`, `cup`을 처리합니다.
- 제공된 PC 코드와 같이 손 경계에 여유 영역을 더하고, ROI를 320×320으로 변환해 추론합니다.
- 기본 신뢰도 임계값은 0.55, NMS IoU는 0.45, ROI 여유는 140픽셀입니다. `--conf`, `--iou`, `--margin`으로 조정합니다.
- 손이 검출되지 않거나 음료가 손 ROI 밖에 있으면 음료 탐지도 수행되지 않습니다.
- 표시 FPS는 프레임 획득과 탐지 처리시간 기준이며 화면 표시·로그 출력 시간은 포함하지 않습니다.
- ROI 경계, 좌표 변환, 부저 타이머, 이메일 간격에 대한 모의 테스트를 포함합니다. 새 코드의 실제 카메라·모델 추론·GPIO 동작과 처리속도는 장치에서 별도 확인해야 합니다.

```bash
python -m unittest discover -s tests -v
```

아래 데모 영상은 기존 프로젝트 당시의 기록이며 새 모델과 코드로 다시 촬영한 결과가 아닙니다.

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
<summary>📊 bottle · can · cup 재학습 결과</summary>

`best.pt`와 같은 학습에서 생성한 결과입니다.

* 학습·검증 손실과 Precision, Recall, mAP 변화
  - 왼쪽 6개 그래프: train / val의 box, obj, cls loss
  - 오른쪽 4개 그래프: Precision, Recall, mAP@0.5, mAP@0.5:0.95
  - 파란색은 학습 기록, 주황색 점선은 평활화한 추세이며 서로 다른 모델의 비교가 아닙니다.

![Training and validation losses, precision, recall and mAP](assets/results.png)

* 클래스별 혼동행렬

![Confusion matrix for bottle, can and cup](assets/confusion_matrix.png)

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



