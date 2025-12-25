import cv2 as cv
import numpy as np
from ultralytics import YOLO
import supervision as sv
import os


IMAGE_PATH = "Example_Images/5.jpg"
MODEL_PATH = 'model.pt'
CONFIDENCE_THRESHOLD = 0.4
OUTPUT_IMAGE_PATH = "output.jpg"


CLASS_COLORS = {
    'occupied': sv.Color.RED,
    'empty': sv.Color.GREEN
}

FONT = cv.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.45
FONT_THICKNESS = 1
SPACING = 5

try:
    model = YOLO(MODEL_PATH)

    print(f"Model class names: {model.names}")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
    exit()


def process_image(image_path: str, model: YOLO, output_path: str):
    # Resmi oku
    frame = cv.imread(image_path)
    if frame is None:
        print(f"ERROR: Image file could not be read: {image_path}")
        return


    results = model(frame, imgsz=640, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)


    detections = detections[detections.confidence >= CONFIDENCE_THRESHOLD]

    annotated_frame = frame.copy()


    for box, conf, class_id in zip(detections.xyxy, detections.confidence, detections.class_id):

        x1, y1, x2, y2 = [int(coord) for coord in box]


        label_name = model.names[class_id]
        color = CLASS_COLORS.get(label_name, sv.Color.WHITE)
        color_bgr = color.as_bgr()


        cv.rectangle(annotated_frame, (x1, y1), (x2, y2), color_bgr, 2)


        label_text = f"{label_name.upper()} ({conf * 100:.1f}%)"


        (text_width, text_height), baseline = cv.getTextSize(label_text, FONT, FONT_SCALE, FONT_THICKNESS)


        if label_name == 'occupied':

            text_x = x1
            text_y = y1 - SPACING


            if text_y < text_height + 5:
                text_y = y1 + text_height + SPACING

            rect_y1 = text_y - text_height - baseline
            rect_x2 = text_x + text_width

        else:

            text_x = x1
            text_y = y2 + text_height + SPACING

            rect_y1 = y2 + SPACING
            rect_x2 = text_x + text_width


        cv.rectangle(annotated_frame,
                     (text_x, rect_y1),
                     (rect_x2, text_y + baseline),
                     color_bgr, -1)


        text_color = (0, 0, 0) if color == sv.Color.WHITE else (255, 255, 255)
        cv.putText(annotated_frame, label_text, (text_x, text_y),
                   FONT, FONT_SCALE, text_color, FONT_THICKNESS)


    cv.imwrite(output_path, annotated_frame)
    print(f"\n The processed image has been saved successfully: {output_path}")


if __name__ == '__main__':
    process_image(IMAGE_PATH, model, OUTPUT_IMAGE_PATH)