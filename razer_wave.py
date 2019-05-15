import colorsys
from time import sleep
import math
import threading

import razer_device


# ========= UTILS ==============
def gamma_correction(rgb):
    # Not exactly sRGB (n**2.2), this is
    # slightly darker, looks more neon:
    return tuple(map(lambda x: x ** 2.28, rgb))


def get_rgb(hue, sat=1.0, val=1.0):
    rgb = colorsys.hsv_to_rgb(hue, sat, val)
    rgb_gamma = rgb # gamma_correction(rgb)
    return tuple(map(lambda x: int(255 * x), rgb_gamma))


# x is col, y is row
def rotate_point(x, y, theta):
    x_ = x * math.cos(theta) - y * math.sin(theta)
    y_ = x * math.sin(theta) + y * math.cos(theta)
    return int(x_), int(y_)


# Make sure hue remains within hue_bounds
def clamp_hue(hue, hue_bounds):
    if hue < hue_bounds[0]:
        return hue + (hue_bounds[1] - hue_bounds[0])
    elif hue > hue_bounds[1]:
        return hue - (hue_bounds[1] - hue_bounds[0])
    else:
        return hue


class WaveEffect(threading.Thread):
    # Class attributes:
    # 	- wave_speed: negative speeds will reverse the trajectory
    # 	- wave_width: Fraction of the keyboard taken by a single wave. Low values mean small waves.
    # 	- hue_bounds: where to set bounds to hue. Bounds (0,1) means it will do a rainbow with all colors
    # 	- direction: angle in radians to describe the direction of the wave
    def __init__(self, wave_speed=0.005, wave_width=1.25, hue_bounds=(0, 1), theta=0, devices=None):
        super(WaveEffect,self).__init__()  # thread class initializer
        if devices is None:
            self.devices = razer_device.get_devices(filter_advanced=True)  # Get all devices that are advanced-capable
        else:
            self.devices = devices
        self.wave_speed = wave_speed
        self.wave_width = wave_width
        self.wave_split = False  # Controls whether to split wave into two

        # Assert hue_bound limits
        assert hue_bounds[0] < hue_bounds[1], "Error: hue_bounds needs lower_bound < upper_bound."
        if hue_bounds[0] < 0:  # Bounds should not be outside (0,1)
            hue_bounds[0] = 0
        if hue_bounds[1] > 1:
            hue_bounds[1] = 1

        self.hue_bounds = hue_bounds
        self.hue = hue_bounds[0]
        self.theta = theta  # Direction of wave

        # Wake-ups per second
        self.rate = 30

    def __getattr__(self, attr):
        return self[attr]

    def update_hue(self):
        self.hue += self.wave_speed
        # Keep hue in (a,b) interval. There's no need to go beyond that.
        self.hue = clamp_hue(self.hue, self.hue_bounds)

    def run(self):
        # Main loop
        while True:
            for dev in self.devices:
                rows, cols = dev.fx.advanced.rows, dev.fx.advanced.cols

                # Rotation: for each point p in matrix, rotate p in -theta direction
                # Check which column the rotated p belongs to
                # Set p to the hue of that color

                # But first, we need to compute the hue for each column in the matrix
                hue_array = [0] * cols  # Stores the hue for each column
                for col in range(cols):
                    if self.wave_split:
                        # To do split, hue must be symmetric around the center column.
                        col_hue = self.hue + math.fabs(cols/2-1 - col)/(self.wave_width * dev.fx.advanced.cols)
                    else:
                        # We remove the symmetry by adding negative values to the left side
                        col_hue = self.hue + (cols / 2 - 1 - col) / (self.wave_width * dev.fx.advanced.cols)

                    col_hue = clamp_hue(col_hue, self.hue_bounds)  # Keep hue within bounds
                    hue_array[col] = col_hue

                # Now apply color to matrix
                for col in range(cols):
                    for row in range(rows):
                        # Shift points for rotation
                        r = rotate_point(int(col - (cols-1) / 2), int(row - rows / 2), self.theta)  # Rotate
                        # Shift points back to actual place
                        r = (int(r[0] + (cols-1) / 2), int(r[1] + rows / 2))

                        # Make sure we're not out of bounds
                        try:
                            dev.fx.advanced.matrix[row, col] = get_rgb(hue_array[r[0]])
                        except:
                            print("Error: out of bounds: ", r[0], r[1])

                dev.fx.advanced.draw()

            # Update hue with wave_speed
            self.update_hue()

            # Sleep before updating again
            sleep(1/self.rate)
