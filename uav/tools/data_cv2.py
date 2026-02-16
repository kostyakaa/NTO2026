import time
from pioneer_sdk2 import Pioneer, Event
import cv2
import os
from datetime import datetime
pioneer = Pioneer()

points_x_y = {
    0: [0.5, 0.5],
    1: [0.5, 1.5],
    2: [0.5, 2.5],

    3: [1.5, 2.5],
    4: [1.5, 1.5],
    5: [1.5, 0.5],

    6: [2.5, 0.5],
    7: [2.5, 1.5],
    8: [2.5, 2.5],
}

z = 1
point_i = 0

def on_point_reached():
    global point_i, cap

    t = datetime.now().strftime("%d_%H-%M-%Sf")

    OUT_DIR = f"dataset_images_{t}/{point_i}"
    photos = 20

    FPS = 10

    os.makedirs(OUT_DIR, exist_ok=True)


    if not cap.isOpened():
        raise RuntimeError("camera not opened")

    i = 0
    dt = 1.0 / FPS

    while i < photos:
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

cap = cv2.VideoCapture(0)

def main():
    global point_i

    
    pioneer.subscribe(on_point_reached, Event.POINT_REACHED)

    pioneer.arm()
    time.sleep(2)
    pioneer.takeoff()
    time.sleep(3)

    for i in range(len(points_x_y)):
        point_i = i
        x, y = points_x_y[i]

        pioneer.go_to_local_point(x, y, z)
        time.sleep(1)


    pioneer.land()
    cap.release()
