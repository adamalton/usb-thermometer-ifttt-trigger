import json
import os

dn = os.path.dirname
CONFIG_FILE_PATH = os.path.join(dn(dn(dn(dn(os.path.abspath(__file__))))), "data", "config.json")


class NotConfigured(Exception):
    """ Exception which is raised when the config has not been set up yet. """
    pass


def save_config_data(data):
    with open(CONFIG_FILE_PATH, "w") as f:
        f.write(json.dumps(data))


def load_config_data(fail_silently=False):
    try:
        with open(CONFIG_FILE_PATH) as f:
            return json.loads(f.read())
    except IOError as e:
        if not fail_silently:
            raise NotConfigured("Config file not found") from e
