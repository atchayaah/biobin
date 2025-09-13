import cv2
import torch

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/pi/yolov5/runs/train/exp4/weights/best.pt', force_reload=True)

# Start video capture (0 for the default camera)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform inference
    results = model(frame)

    # Render results on the frame
    results.render()  # Draw bounding boxes on the image

    # Display the image
    cv2.imshow('Live Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
