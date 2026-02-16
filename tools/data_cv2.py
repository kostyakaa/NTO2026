import os
import time
import cv2

OUT_DIR = "dataset_images"
FPS = 5
CAM_INDEX = 0

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        raise RuntimeError("camera not opened")

    i = 0
    dt = 1.0 / FPS

    while True:
        t0 = time.time()
        ok, frame = cap.read()
        if not ok or frame is None:
            continue

        path = os.path.join(OUT_DIR, f"{i:06d}.jpg")
        cv2.imwrite(path, frame)
        print(path)
        i += 1

        while time.time() - t0 < dt:
            time.sleep(0.001)

if __name__ == "__main__":
    main()
