import time
from pioneer_sdk2 import Pioneer, Event

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

def on_point_reached():
    print("POINT_REACHED")

def main():
    pioneer.subscribe(on_point_reached, Event.POINT_REACHED)

    pioneer.arm()
    time.sleep(2)
    pioneer.takeoff()
    time.sleep(3)

    for i in range(len(points_x_y)):
        x, y = points_x_y[i]
        pioneer.go_to_local_point(x, y, z)

    pioneer.land()

if __name__ == "__main__":
    main()
