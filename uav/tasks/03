# 03_flight_blocking_ai_send.py
import time
import requests
from pioneer_sdk2 import Pioneer, Camera, Event
from pioneer_rknn import Yolo

SERVER_URL = "http://192.168.1.10:8000/detections"
DRONE_ID = "pioneer-01"

pioneer = Pioneer()
camera = Camera()
yolo = Yolo(model_name="yolov11n")

points_x_y = {
    0: [1, 1],
    1: [1, 2],
    2: [3, 4],
}
z = 2

current_idx = -1

def on_point_reached():
    global current_idx
    frame = camera.get_cv_frame(timeout=1.0)
    det = yolo(frame) if frame is not None else []

    x, y = points_x_y[current_idx]
    payload = {
        "drone_id": DRONE_ID,
        "ts": time.time(),
        "point_index": current_idx,
        "point": {"x": x, "y": y, "z": z},
        "detections": det,
    }

    try:
        requests.post(SERVER_URL, json=payload, timeout=2.0)
    except Exception:
        pass

def main():
    global current_idx
    pioneer.subscribe(on_point_reached, Event.POINT_REACHED)

    pioneer.arm()
    time.sleep(2)
    pioneer.takeoff()
    time.sleep(3)

    for i in range(len(points_x_y)):
        current_idx = i
        x, y = points_x_y[i]
        pioneer.go_to_local_point(x, y, z)

    pioneer.land()

if __name__ == "__main__":
    main()
