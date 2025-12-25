import cv2
import numpy as np
import torch
from urllib.request import urlopen
from ultralytics import YOLO


model_path = "model.pt"
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f" Device used: {device}")

model = YOLO(model_path)
model.to(device)
torch.backends.cudnn.benchmark = True
print(" Model loaded:", model_path)


esp32_url = "http://192.168.1.100:81/stream"

print("ESP32-CAM connection is being established...")
stream = urlopen(esp32_url)
print(" ESP32-CAM connection established. Press ‘Q’ to exit.")


bytes_data = b""

while True:
    try:

        bytes_data += stream.read(1024)


        a = bytes_data.find(b'\xff\xd8')
        b = bytes_data.find(b'\xff\xd9')

        if a != -1 and b != -1:
            jpg = bytes_data[a:b+2]
            bytes_data = bytes_data[b+2:]


            if len(jpg) < 50:
                continue


            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is None:
                continue


            results = model(frame, device=device)
            annotated_frame = results[0].plot()


            cv2.imshow("ESP32-CAM YOLO (CUDA)", annotated_frame)


        if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q')]:
            print(" Logging out...")
            break

    except Exception as e:

        print("The frame cannot be read, skipping:", str(e))
        continue


cv2.destroyAllWindows()
print("The program has been terminated.")
