import time
import razer_wave as rw
import razer_device


def get_attribute(obj, attr):
    try:
        return getattr(obj, attr)
    except TypeError:
        print("Not member %s." % attr)
        return None


# Try to set attribute to object
def set_attribute(obj, attr, val):
    try:
        setattr(obj, attr, val)
        return True
    except TypeError:
        return False
    except Exception:
        return False


def main():
    print(" -- Razer device controller")
    devices = razer_device.get_devices()
    wave = rw.WaveEffect()
    wave.start()
    while True:
        cmd = input("cmd: ")
        cmd = cmd.split()
        set_attribute(wave, cmd[0], float(cmd[1]))


if __name__ == "__main__":
    main()