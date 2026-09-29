# Dataset and training

[Back to README](../README.md)

## Dataset

The project's images and labels are hosted on Roboflow:

**[Drink Detection - Version 2](https://universe.roboflow.com/s-workspace-v63wd/drink-detection-utuvg/dataset/2)**

| Split | Images |
| --- | ---: |
| Train | 384 |
| Validation | 251 |
| Test | 60 |
| Total | 695 |

Version 2 uses auto-orientation and a 512 x 512 stretch resize, with no augmentation. The dataset is listed under **CC BY 4.0**.
This version is available for inspection and further training; it has not been confirmed as the exact dataset version used for the included `best.pt`.

### Download to Colab

1. Open the project's **Version 2** link above.
2. Select **Download Dataset**, then **YOLOv5**. Sign in if prompted.
3. Download a ZIP to inspect locally, or show the export code and copy the URL following `curl -L`.
4. For Colab, run the cell below and paste that export URL. It downloads and extracts this project's dataset to `/content` without putting the access key in the notebook output.

<details>
<summary>Colab download cell</summary>

```python
from getpass import getpass
from pathlib import Path
import subprocess
import zipfile

download_url = getpass("Roboflow download URL: ")
archive = Path("/content/roboflow.zip")
try:
    result = subprocess.run(
        ["curl", "--fail", "--location", "--silent", "--show-error",
         download_url, "--output", str(archive)],
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError("Download failed. Check your Roboflow export URL and access.")
    if not zipfile.is_zipfile(archive):
        raise RuntimeError("Expected a ZIP file. Enter the export URL, not the project page URL.")
    with zipfile.ZipFile(archive) as dataset_zip:
        dataset_zip.extractall("/content")
finally:
    download_url = None
    archive.unlink(missing_ok=True)

print("Dataset extracted to /content")
```

</details>

Check the downloaded configuration:

```python
!cat /content/data.yaml
```

Check the image paths and the `bottle`, `can`, and `cup` labels. For fine-tuning, class order must match the existing model. If the YAML is in a subfolder, locate it with `!find /content -name data.yaml` and use that path in `--data`.

### Fine-tune the included best.pt

After downloading the dataset, run these cells in Colab, preferably with a GPU runtime. The first clone downloads this project and its weights; the second downloads the YOLOv5 training code. Neither clone downloads the Roboflow dataset.

```python
%cd /content
!git clone https://github.com/redstone771/ESDproject.git
!git clone https://github.com/ultralytics/yolov5.git
%cd /content/yolov5
!pip install -r requirements.txt

!python train.py --img 512 --batch 16 --epochs 100 --data /content/data.yaml --weights /content/ESDproject/best.pt --name drink_finetune
```

Skip a clone command if that folder already exists. This starts a new training run from `best.pt`; it does not resume an interrupted run or overwrite the input model.

Outputs are normally saved to `runs/train/drink_finetune/` under the YOLOv5 directory. Save `weights/best.pt`, `results.png`, and `results.csv` before the Colab runtime ends. Repeated run names may receive a numeric suffix; check the training log for the output path.

### Original training command

The original training run started from pretrained YOLOv5s weights:

```python
!python train.py --img 512 --batch 16 --epochs 100 --data /content/data.yaml --weights yolov5s.pt --name drink_bottle_can_cup
```

The original Roboflow version and YOLOv5 commit have not been verified, so this command documents the settings rather than guaranteeing identical results.
