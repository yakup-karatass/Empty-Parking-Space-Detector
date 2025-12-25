1) TRAINING THE MODEL:

If you want to train the model, you should follow these steps:

- Go to "Project Codes" folder.

- Run the "ModelTrainCode.py" file.

- Enter your IDE's terminal and add the libraries with this code:
  pip install ultralytics opencv-python pyyaml tqdm torch torchvision

- Check the "yaml_file_path". If it's not correct, change the input with correct one.

- Check the "model_weights". It should be "model.pt". If it's not, change with "model.pt"

- Check the batch size and epochs. It should be appropriate to your system requirements. (Batch is generally 8,16 or 32, and epochs value depends on your desire.)

- Run the code, and you will see that model training started.

- When model training is finished, there will be a new folder. Open it, and go to "Weights"
  folder. You will find a file that name is "best.pt". It's a new model file that you've just trained. 

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

2) TRYING THE MODEL:

If you want to try the model on images and videos, you should follow these steps:

2.A) IMAGE PROCESSING:	

- Go to "Project Codes" folder

- Run the "image_processing.py" file.

- Go to your IDE's terminal and add these libraries with this code:
  pip install opencv-python numpy ultralytics supervision

- After installation, check the "IMAGE_PATH" variable. You can use the "1.jpg","2.jpg",
  "3.jpg","4.jpg" and "5.jpg" files which is added in project by 29th group members.
  These pictures contain parking lot images which is shooted by 29th group members.

- Check the "MODEL_PATH" variable. It has to be "model.pt". If it's not, change it with "model.pt".

- Run the code, and you will see that there is an output file which name is "output.jpg".

- Open the "output.jpg", and you will see the model's result.

2.B) VIDEO PROCESSING:

- Go to "Project Codes" folder.

- Run the "video_processing.py" file.

- Go to your IDE's terminal and add these libraries with this code:
  pip install opencv-python numpy ultralytics supervision

- After installation, check the "VIDEO_PATH" variable. You can use the "video2tr.mp4" and
  "car_park.mp4" which is added in project by 29th group members. These videos contain
  parking lot videos which is founded on Internet by 29th group members.

- Check the "MODEL_PATH" variable. It has to be "model.pt". If it's not, change it with "model.pt".

- Run the code, and you will see that there is an output file which name is "output_video.mp4".

- Open the "output_video.mp4", and you will see the model's result.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

3) Real-Time Detection:

If you have ESP32-CAM OV2640, you should follow these steps:

3.A) Coding ESP32-CAM OV2640

- Prepare the circuit which is needed to code ESP32-CAM OV2640:
  RX---> UOT , TX---> UOR, GND--->GND, 5V--->5V, GND--->IO0(!)
  NOTE: GND--->IO0 connection will be used when you're loading code. When uploading finished,
	You should remove GND--->IO0 connection, and reset the camera with it's button.

- When you completed preparing the circuit, go to "Project Codes" folder, and open the "Stream.ino" file which is a Arduino IDE file. (if it says you have to create a folder to use this code, choose "yes" option and create a folder.

- Click the "Select Board" and choose the "AI Thinker ESP32-CAM".

- Choose the appropriate Serial-Port (which is your camera connected).

- Look at the code, and find "*ssid" and "*password" variables. Change them with your Wi-Fi name, and password.
  ESP32-CAM OV2640 and your computer should be connected the same Wi-Fi network. Otherwise,
  you can't get a live stream.

- Connect the GND--->IO0 cable, and hit the upload button.

- When compiling is finished, and uploading is started, you should press reset button which is on the ESP32-CAM.

- After pressing the reset button, you will see some arrows like "----->".
  That means, ESP32-CAM passed the loader mode, and your code is loading.

- After uploading is finished, you should hit the reset button again to change mode from loader mode to run mode.

- After resetting ESP32-CAM, you should open Serial Monitor, and choose baud rate 115200.

- After selecting baud rate, you will see an IP adress which mentions stream adress.

- Copy the IP adress to your browser. You will see that stream is started and camera is working.

 3.B) Starting the Real-Time Detection:

- When you finished "Coding ESP32-CAM OV2640" steps, go to "Project Codes" folder, and run the "real_time_detection.py" file.

- Enter your IDE's terminal and add the libraries with this code:
  pip install opencv-python numpy torch ultralytics

- After installation, you should check "model_path" variable. It has to be "model.pt". If it's not,
  you have to change it with "model.pt"

- Also, you should check "esp32_url" variable. It has to be your ESP32-CAM OV2640 stream url.
  If it's not match with your url, you have to change it with yours.

- After checking the important parts, you can run the code. 

- If everything is OK, you will see a window that shows the ESP32-CAM's stream. 

- When you show a parking lot to ESP32-CAM OV2640, it will automatically detect occupied
  and empty parking lots.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

You can now use your model to perform real-time detection with the ESP32-CAM OV2640!

Contributors:
- Yakup KARATAŞ
- Tolga SEYMEN
- Muhammed AKSOY

