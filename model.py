import cv2
import numpy as np
from ultralytics import YOLO
import smtplib
from email.mime.text import MIMEText

# Load YOLOv8 model (pre-trained on COCO dataset)
model = YOLO("yolov8s.pt")  ## You can use yolov8s, yolov8m, etc., for better accuracy

# Define classes for pedestrians, bicycles, and motorcycles
PEDESTRIAN_CLASS = 0  # COCO class ID for person
BICYCLE_CLASS = 1  # COCO class ID for bicycle
MOTORCYCLE_CLASS = 3  # COCO class ID for motorcycle

# Define FOB entry and exit points (in pixels)
FOB_ENTRY = (100, 100)
FOB_EXIT = (500, 500)


# Function to send alerts to traffic control booth
def send_alert(user_type, location):
    subject = f"Traffic Violation Alert: {user_type} detected at {location}"
    body = f"A {user_type} was detected at {location} and did not follow the FOB rules. Please take necessary action."

    # Email configuration (replace with your SMTP server details)
    sender_email = "sharmah.m1704@gmail.com"
    receiver_email = "madhu12071981@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "sharmah.m1704@gmail.com"
    smtp_password = "hr36ag9831"

    # Create email message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Send email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, [receiver_email], msg.as_string())
        print(f"Alert sent: {subject}")
    except Exception as e:
        print(f"Failed to send alert: {e}")


# Function to detect users and divert them
def detect_and_divert(frame):
    results = model(frame)  # Run YOLOv8 inference on the frame

    for result in results:
        boxes = result.boxes.xyxy  # Bounding boxes
        classes = result.boxes.cls  # Class IDs
        confidences = result.boxes.conf  # Confidence scores

        for box, cls, conf in zip(boxes, classes, confidences):
            if conf < 0.5:  # Skip low-confidence detections
                continue

            x1, y1, x2, y2 = map(int, box)  # Bounding box coordinates
            class_id = int(cls)

            # Draw bounding box and label
            label = model.names[class_id]
            color = (0, 255, 0) if class_id == PEDESTRIAN_CLASS else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # Check if the user is within FOB entry/exit points
            user_location = ((x1 + x2) // 2, (y1 + y2) // 2)  # Center of the bounding box
            if FOB_ENTRY[0] < user_location[0] < FOB_EXIT[0] and FOB_ENTRY[1] < user_location[1] < FOB_EXIT[1]:
                if class_id == BICYCLE_CLASS or class_id == MOTORCYCLE_CLASS:
                    # Divert cyclists and two-wheelers
                    cv2.putText(frame, "DIVERT TO FOB", (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                elif class_id == PEDESTRIAN_CLASS:
                    # Allow pedestrians
                    cv2.putText(frame, "USE FOB", (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                # User is not following the rules
                send_alert(label, user_location)

    return frame


# Main function to process video feed
def main():
    # Open video feed (replace with your camera feed or video file)
    cap = cv2.VideoCapture("10836-226625000_tiny.mp4")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect and divert users
        processed_frame = detect_and_divert(frame)

        # Display the processed frame
        cv2.imshow("Mixed-Mode FOB Monitoring", processed_frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()