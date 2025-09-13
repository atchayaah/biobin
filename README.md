
# Biobin

An AI-powered pick-and-place robotic system designed for safe handling and disposal of biomedical waste (cotton, syringes).
This project uses YOLOv5 object detection to identify waste items in real time and a robotic arm controlled by Arduino + Raspberry Pi to segregate them into designated bins.


## 📝Features

🔹 Real-time Object Detection – Detects cotton & syringes using YOLOv5

🔹Automated Segregation – Robotic arm picks and places waste in respective bins

🔹 Obstacle Avoidance – Ultrasonic sensors for safe navigation

🔹 Scalable & Cost-Effective – Suitable for small and large hospitals

🔹 Reduced Human Exposure – Improves safety for healthcare workers


## Tech Stack

**Software & Libraries**:

    Python 3.12 – Core programming language

    YOLOv5 + PyTorch – Object detection

    OpenCV – Image processing & live video streaming

    Flask / Streamlit (Optional) – UI interface for control

    Roboflow – Dataset annotation & preprocessing


**Hardware Components**:

    Raspberry Pi 4 (4GB) – Runs YOLOv5 detection

    Arduino Uno – Controls servo motors & robotic arm

    USB Camera – Captures live feed

    12V DC Geared Motors – For robot movement

    Ultrasonic Sensors – For obstacle detection

    Servo Motors – Pick & place mechanism
## Deployment

To deploy this project run

1️⃣ Clone the Repository
    git clone https://github.com/atchayaah/biobin.git
    cd biobin

2️⃣ Install Dependencies
    pip install -r requirements.txt

3️⃣ Train the Model (Optional)

If you want to retrain YOLOv5 on your dataset:

    python train.py --data data.yaml --weights yolov5s.pt --img 640 --epochs 100

4️⃣ Run Live Detection
    python test.py


Press q to stop live feed.


## 🔬Workflow

1. Dataset Preparation:

- 7 annotated images (cotton, syringes) using Roboflow
- Exported in YOLOv5 format

2. Model Training:

- YOLOv5s used for transfer learning
- Fine-tuned on custom dataset

3. Real-Time Detection:

- Raspberry Pi captures live frames
- YOLOv5 model predicts bounding boxes & classes

4. Waste Segregation:

- Arduino receives classification results
- Robotic arm sorts objects into correct bins
## Use Cases

📌 Hospital Waste Management: Safer segregation of biomedical waste

📌 Research Labs: Reduce exposure to infectious materials

📌 Sustainable Healthcare: Minimizes environmental impact

## Research & References

- Roboflow Dataset: View Dataset
- YOLOv5 Docs: Ultralytics YOLOv5
## 📜License

This project is **patent-protected**.
The invention described here is covered under the Provisional Patent filed for "Safe Handling and Disposal of Biomedical Wastes" 

**Patent Application Number:202441104299**

