from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ConfigForm
from .utils.config import load_config_data
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
    current = get_current_temperature()
    config = load_config_data()
    max_limit = config["target_temp_max"]
    min_limit = config["target_temp_min"]
    if current > max_limit:
        webhook_result = send_max_exceeded_webook()
        message = (
            f"Current temperature ({current}°C) exceeds max limit ({max_limit},°C) "
            "webhook has been sent."
        )
    elif current < min_limit:
        webhook_result = send_min_not_reached_webhook()
        message = (
            f"Current temperature ({current}°C) has not reached min limit ({min_limit}°C) "
            f"webhook has been sent."
        )
    else:
        webhook_result = None
        message = (
            f"Current temperature ({current}°C) falls within the set range "
            f"({min_limit}-{max_limit}°C)."
        )
    context = {
        "message": message,
        "webhook_result": webhook_result,
    }
    return render(request, "check_temperature.html", context)
