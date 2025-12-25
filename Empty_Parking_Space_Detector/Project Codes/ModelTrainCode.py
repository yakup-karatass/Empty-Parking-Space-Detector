import os
import torch
from ultralytics import YOLO


def main():

    yaml_file_path = "Dataset/data.yaml"

    model_weights = "model.pt"

    project_name = 'parking_project'
    run_name = 'train_run_1'

    if not os.path.exists(yaml_file_path):
        print(f"🚨 ERROR: The file '{yaml_file_path}' was not found.")
        print("Please check the path in the 'yaml_file_path' variable.")
        return

    print(f"🚀 Loading model: {model_weights}...")
    try:
        model = YOLO(model_weights)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    use_device = 0 if torch.cuda.is_available() else 'cpu'
    print(f"✅ Device: {torch.cuda.get_device_name(0) if use_device == 0 else 'CPU'}")

    print(f"🚀 Starting training with '{yaml_file_path}'...")

    try:
        results = model.train(
            data=yaml_file_path,
            epochs=100,
            imgsz=640,
            batch=8,
            project=project_name,
            name=run_name,
            optimizer='AdamW',
            patience=50,
            device=use_device,

            workers=0,
            amp=False,
            cache=False,
            exist_ok=True
        )

        print("\n🏁 Training Completed Successfully!")


        save_dir = os.path.join(project_name, run_name, 'weights')
        best_model_path = os.path.join(save_dir, 'best.pt')
        print(f"Best model saved at: {os.path.abspath(best_model_path)}")

    except Exception as e:
        print(f"\n🚨 ERROR during training.")
        print(f"Details: {e}")
        return


    print("\nModel Validation started...")
    try:
        metrics = model.val()
        print(f"mAP50-95: {metrics.box.map}")
    except Exception as e:
        print(f"Validation warning: {e}")


if __name__ == '__main__':
    main()