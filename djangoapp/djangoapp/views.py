from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ConfigForm
from .utils.config import load_config_data, save_config_data
from .utils.ifttt import send_max_exceeded_webook, send_min_not_reached_webhook
from .utils.temperature import get_current_temperature


def home(request):
    """ View which displays the form to edit the settings. """
    if request.method == "POST":
        form = ConfigForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Configuration saved")
            return redirect("home")
    else:
        form = ConfigForm(initial=load_config_data(fail_silently=True))
    context = {
        "form": form,
    }
    return render(request, "home.html", context)


def ping(request):
    """ View that can be called to check that the server is alive. """
    return HttpResponse('Bonza')


def check_temperature(request):
    """ Check if the current temperature measured by the USB thermometer is within the set range,
        and if not then call the relevant IFTTT webhook.
    """
    config = load_config_data()
    webhook_result = ""
    message = ""

    if _is_enabled(config):
        if _should_disable(config):
            message = "Temperature checking has now been disabled."
            if _should_fire_webhook_when_disabling(config):
                webhook_result = send_max_exceeded_webook()
                message += " Webhook to switch heating off has been fired."
            _set_to_disabled(config)
            should_run_check = False
        else:
            should_run_check = True
    else:
        if _should_enable(config):
            message = "Temperature checking has been switched back on. "
            _set_to_enabled(config)
            should_run_check = True
        else:
            message = "Temperature checking is currently disabled. No check run."
            should_run_check = False

    if should_run_check:
        current = get_current_temperature()
        max_limit = config["target_temp_max"]
        min_limit = config["target_temp_min"]
        if current > max_limit:
            webhook_result = send_max_exceeded_webook()
            message += (
                f"Current temperature ({current}°C) exceeds max limit ({max_limit}°C) "
                "webhook has been sent."
            )
        elif current < min_limit:
            webhook_result = send_min_not_reached_webhook()
            message += (
                f"Current temperature ({current}°C) has not reached min limit ({min_limit}°C) "
                f"webhook has been sent."
            )
        else:
            webhook_result = None
            message += (
                f"Current temperature ({current}°C) falls within the set range "
                f"({min_limit}-{max_limit}°C)."
            )
    context = {
        "message": message,
        "webhook_result": webhook_result,
    }
    return render(request, "check_temperature.html", context)


def _is_enabled(config):
    return config["active"]


def _set_to_enabled(config):
    config["active"] = True
    save_config_data(config)


def _set_to_disabled(config):
    config["active"] = False
    save_config_data(config)


def _should_enable(config):
    enable_at = config["auto_enable_at"]
    enable_on_days = config["auto_enable_on_days"]
    now = timezone.localtime()
    today = now.weekday() + 1  # Zero-indexed
    if today in enable_on_days:
        if enable_at:
            if _is_after(now, enable_at[0], enable_at[1]):
                # Make sure that we don't re-enable after we should be disabling
                disable_at = config["auto_disable_at"]
                if not disable_at or _is_before(now, disable_at[0], disable_at[1]):
                    return True
    return False


def _should_disable(config):
    disable_at = config["auto_disable_at"]
    if disable_at:
        now = timezone.localtime()
        if _is_after(now, disable_at[0], disable_at[1]):
            return True
    return False


def _is_after(dt, hour, minute):
    """ Is the time of the given datetime at or after the given hour and minute of the day? """
    if dt.hour > hour:
        return True
    if dt.hour == hour:
        if dt.minute >= minute:
            return True
    return False


def _is_before(dt, hour, minute):
    """ Is the time of the given datetime at or before the given hour and minute of the day? """
    if dt.hour < hour:
        return True
    if dt.hour == hour:
        if dt.minute <= minute:
            return True
    return False


def _should_fire_webhook_when_disabling(config):
    return config["switch_heating_off_when_auto_disabling"]
