from temper import Temper


def get_current_temperature():
    temper = Temper()
    devices: list[dict] = temper.read()
    for device in devices:
        try:
            return device["celsius"]
        except KeyError:
            continue
    raise Exception(
        f"None of the {len(devices)} devices read by Temper had a 'celsius' item. Data: {devices!r}"
    )
