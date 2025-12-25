import cv2 as cv
import numpy as np
from ultralytics import YOLO
import supervision as sv
import os


VIDEO_PATH = "Example_Videos/car_park.mp4"
OUTPUT_VIDEO_PATH = "output_video.mp4"
MODEL_PATH = 'model.pt'
CONFIDENCE_THRESHOLD = 0.4

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
    print(f" Model uploaded. Classes: {model.names}")
except Exception as e:
    print(f" An error occurred while loading the model: {e}")
    exit()


def process_video(video_path: str, model: YOLO, output_path: str):

    cap = cv.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"ERROR: Video file could not be opened: {video_path}")
        return


    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv.CAP_PROP_FPS))


    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"Video is processing... (Press ‘q’ to exit)")

    frame_count = 0

    while True:
        ret, frame = cap.read()


        if not ret:
            break

        frame_count += 1


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


        out.write(annotated_frame)


        cv.imshow("Video Detection", annotated_frame)


        if cv.waitKey(1) & 0xFF == ord('q'):
            print("The process was stopped by the user.")
            break


    cap.release()
    out.release()
    cv.destroyAllWindows()
    print(f"\n Video processing completed: {output_path}")


if __name__ == '__main__':
    process_video(VIDEO_PATH, model, OUTPUT_VIDEO_PATH)