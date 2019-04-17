import razer_device
import threading
import time
import math


class OscilateEffect(threading.Thread):
    def __init__(self, phase=0, frequency=1, color=(255, 255, 255), device=None):
        self.device = device
        self.phase = phase
        self.frequency = frequency
        self.color = color

        # Wake ups per second
        self.rate = 5

    def run(self):
        col = 0
        rows, cols = self.device.fx.advanced.rows, self.device.fx.advanced.cols
        while True:
            sin_x = rows/2*(math.sin(col)+1)
            print(sin_x)
            self.device.fx.advanced.matrix[int(sin_x), int(col)] = self.color

            col += 1

            if col >= cols:
                col = 0

            self.device.fx.advanced.draw()

            time.sleep(1 / self.rate)


dev = razer_device.get_devices()[0]
s = OscilateEffect(device=dev)
s.run()