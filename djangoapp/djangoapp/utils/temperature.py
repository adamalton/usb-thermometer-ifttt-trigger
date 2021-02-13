from temper import Temper


def get_current_temperature():
    temper = Temper()
    results: list[dict] = temper.read()
    first = results[0]
    temp = first["celsius"]
    return temp
