import cv2
from ultralytics import YOLO
import torch
import time

# === CONFIG ===
MODEL_PATH = r'../embed/best.pt'  # <-- change if needed
VIDEO_PATH = r'../embed/Lab_Test.mp4'  # <-- your input video
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
CONFIDENCE_THRESHOLD = 0.2

# === LOAD MODEL ===
print(f'Using device: {DEVICE}')
model = YOLO(MODEL_PATH).to(DEVICE)

# === LOAD VIDEO ===
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# === MAIN LOOP ===
TARGET_CLASS = "Ants"
REMOVE_CLASS = "Beetles"
BOOST_FACTOR = 10

names = model.names

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, device=DEVICE)
    r = results[0]

    filtered_indices = []

    if r.boxes is not None and r.boxes.conf is not None:
        classes = r.boxes.cls.cpu().numpy()
        confs = r.boxes.conf.cpu().numpy()

        for i, (cls_id, conf) in enumerate(zip(classes, confs)):
            cls_name = names[int(cls_id)]

            # 1) Remove Beetles completely
            if cls_name == REMOVE_CLASS:
                continue

            # 2) Boost Ants confidence before filtering
            if cls_name == TARGET_CLASS:
                conf *= BOOST_FACTOR
                conf = min(conf, 1.0)

            # 3) Keep only detections that pass threshold
            if conf > CONFIDENCE_THRESHOLD:
                filtered_indices.append(i)

        # Apply indexing without modifying conf tensor
        r.boxes = r.boxes[filtered_indices]

    # Draw filtered results
    annotated_frame = r.plot()
    cv2.imshow("YOLO Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
