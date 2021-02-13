import logging
import urllib.request

from .config import load_config_data

BASE_WEBHOOK_URL = "https://maker.ifttt.com/trigger/{event}/with/key/{key}"



def send_max_exceeded_webook():
    config = load_config_data()
    url = BASE_WEBHOOK_URL.format(
        event=config["max_temp_webhook_name"],
        key=config["ifttt_webhook_key"]
    )
    return _call_url(url)


def send_min_not_reached_webhook():
    config = load_config_data()
    url = BASE_WEBHOOK_URL.format(
        event=config["min_temp_webhook_name"],
        key=config["ifttt_webhook_key"]
    )
    return _call_url(url)


def _call_url(url):
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf8")  # Assuming UTF8, but hopefully fine!
        logging.info("Webhook result: %s", content)
        return content
