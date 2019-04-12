from openrazer.client import DeviceManager


# Returns: a list of available devices
# Arguments:
#    - filter_advanced: returns only devices that are capable of advanced effects
def get_devices(filter_advanced=True):
    device_manager = DeviceManager()

    devices = []
    for d in device_manager.devices:
        if d.fx.advanced:
            print("Found device %s" % d.name)
            devices.append(d)

    print("Found {} Razer devices".format(len(devices)))

    # Set this to false or daemon will try to set the effects to all devices
    device_manager.sync_effects = False

    return devices

