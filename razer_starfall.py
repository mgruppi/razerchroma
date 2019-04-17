import razer_device
import threading
import time
import math


class StarfallEffect(threading.Thread):
    def __init__(self, col=7, speed=0.5, theta=0, trail=3, color=(255, 255, 255), dev=None):

        self.device = dev
        self.rows, self.cols = dev.fx.advanced.rows, dev.fx.advanced.cols  # Device size
        self.speed = speed  # Fall speed
        self.col = col  # Column to start falling from
        self.row = 0  # Starts from top row, always
        self.theta = theta  # Angle of fall
        self.trail = trail  # Length of the trail left by star
        self.color = color

        # Wake-ups per second
        self.rate = 1

    def run(self):

        # Pre-compute trajectory of star
        trajectory = [(int(self.row), int(self.col))]  # Stars at the top
        # Next point in trajectory
        nxt = (int(self.row + (1) * math.cos(self.theta)), int(self.col + (1) * math.sin(self.theta)))
        while nxt[0] < self.rows and nxt[1] < self.cols - 1:
            trajectory.append(nxt)
            nxt = (int(nxt[0] + (1) * math.cos(self.theta)), int(nxt[1] + (1) * math.sin(self.theta)))
            print(nxt)

        print(trajectory)

        # Main loop
        for i in range(len(trajectory)):
            p = trajectory[i]
            self.device.fx.advanced.matrix[p[0], p[1]] = self.color
            self.device.fx.advanced.draw()

            time.sleep(1 / self.rate)


def main():
    dev = razer_device.get_devices()[0]
    s = StarfallEffect(dev=dev)
    s.run()


if __name__ == "__main__":
    main()
