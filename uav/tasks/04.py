import time
import math
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

z = 2.0
current_idx = -1

FOV_X_DEG = 70.0
FOV_Y_DEG = 55.0

def bbox_center(det):
    if isinstance(det, dict):
        x1, y1, x2, y2 = det["x1"], det["y1"], det["x2"], det["y2"]
    else:
        x1, y1, x2, y2 = det[0], det[1], det[2], det[3]
    return (0.5 * (x1 + x2), 0.5 * (y1 + y2))

def pixel_to_xy(u, v, w, h, x0, y0, z_m):
    Wm = 2.0 * z_m * math.tan(math.radians(FOV_X_DEG) * 0.5)
    Hm = 2.0 * z_m * math.tan(math.radians(FOV_Y_DEG) * 0.5)
    du = (u - 0.5 * w) * (Wm / w)
    dv = (v - 0.5 * h) * (Hm / h)
    dx = dv
    dy = -du
    return (x0 + dx, y0 + dy)

def on_point_reached():
    global current_idx

    frame = camera.get_cv_frame(timeout=1.0)
    dets = yolo(frame) if frame is not None else None

    x0, y0 = points_x_y[current_idx]

    if frame is None or not dets:
        print({"idx": current_idx, "point": (x0, y0), "detections": dets, "xy": None})
        return

    u, v = bbox_center(dets[0])
    h, w = frame.shape[:2]
    x, y = pixel_to_xy(u, v, w, h, x0, y0, z)

    print({"idx": current_idx, "point": (x0, y0), "det_center": (float(u), float(v)), "xy": (float(x), float(y)), "detections": dets})

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
