import os
import torch

# Change the working directory to your YOLOv5 folder
yolo_path = '/home/pi/yolov5'  # Path to your YOLOv5 directory
os.chdir(yolo_path)

# Check for GPU availability
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

# Define parameters
data_file = '/home/pi/robo_ws/data.yaml'  # Path to your dataset YAML file
img_size = 640  # Image size for training
epochs = 50  # Number of epochs
batch_size = 16  # Batch size
weights = 'yolov5s.pt'  # Pretrained weights (ensure it's in the correct directory or provide full path)

# Build the command for training
command = f"python train.py --img {img_size} --batch {batch_size} --epochs {epochs} --data {data_file} --weights {weights} --device {device}"
print(f"Running command: {command}")

# Run the training command
os.system(command)
