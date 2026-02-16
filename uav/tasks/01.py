import time
from pioneer_sdk2 import Pioneer, Event

pioneer = Pioneer()

points_x_y = {
    0: [1, 1],
    1: [1, 2],
    2: [3, 4],
}
z = 2

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
