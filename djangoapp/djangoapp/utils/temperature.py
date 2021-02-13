from temper import Temper


def get_current_temperature():
    """ Get the current temperature from the TEMPer USB device. """
    temper = Temper()
    devices: list[dict] = temper.read()
    keys = ["celsius", "internal temperature"]
    for device in devices:
        for key in keys:
            try:
                return device[key]
            except KeyError:
                continue
    raise Exception(
        f"None of the data dicts from the {len(devices)} devices read by Temper contained any of "
        f"these keys: {''.join(keys)}. Data: {devices!r}"
    )
