import time
import razer_wave as rw
import razer_device


def get_attribute(obj, attr):
    try:
        return getattr(obj, attr)
    except TypeError:
        print("Not member %s." % attr)
        return None
    except ValueError:
        print("Value is not acceptable.")
        return None


# Try to set attribute to object
def set_attribute(obj, attr, val):
    try:
        if attr in ["wave_speed", "theta"]:
            val = float(val)
        elif attr == "wave_split":
            val = bool(val)
        setattr(obj, attr, val)
        return True
    except TypeError:
        return False
    except ValueError:
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
        set_attribute(wave, cmd[0], cmd[1])


if __name__ == "__main__":
    main()