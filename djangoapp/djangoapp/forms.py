from django.core.exceptions import ValidationError
from django import forms

from .utils.config import save_config_data


class ConfigForm(forms.Form):
    """ Form for allowing the user to configure the settings. """

    # All fields are required
    target_temp_max = forms.FloatField(
        initial=22.5,
        widget=forms.NumberInput(attrs={"step": "0.5", "min": "15", "max": "25"}),
    )
    target_temp_min = forms.FloatField(
        initial=21.5,
        widget=forms.NumberInput(attrs={"step": "0.5", "min": "15", "max": "25"}),
    )
    max_temp_webhook_name = forms.CharField(initial="living_room_above_max_temperature")
    min_temp_webhook_name = forms.CharField(initial="living_room_below_min_temperature")
    ifttt_webhook_key = forms.CharField(
        label="IFTTT webhook key",
        widget=forms.PasswordInput(attrs={"autocomplete": "off"}),
    )

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        if cleaned_data["target_temp_min"] >= cleaned_data["target_temp_max"]:
            msg = "Min temperature must be less than max temperature."
            raise ValidationError({
                "target_temp_max": msg,
                "target_temp_min": msg
            })
        return cleaned_data

    def save(self):
        save_config_data(self.cleaned_data)
