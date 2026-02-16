import time
from pioneer_sdk2 import Pioneer, Camera, Event
from pioneer_rknn import Yolo

pioneer = Pioneer()
camera = Camera()
yolo = Yolo(model_name="yolov11n")

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

current_idx = -1

def on_point_reached():
    global current_idx
    frame = camera.get_cv_frame(timeout=1.0)
    det = yolo(frame) if frame is not None else None
    print({"idx": current_idx, "detections": det})

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
