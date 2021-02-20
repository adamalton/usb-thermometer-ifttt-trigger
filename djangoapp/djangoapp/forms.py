from django.core.exceptions import ValidationError
from django import forms

from .utils.config import save_config_data

WEEKDAY_CHOICES = (
    (1, "M"),
    (2, "T"),
    (3, "W"),
    (4, "T"),
    (5, "F"),
    (6, "S"),
    (7, "S"),
)

class ConfigForm(forms.Form):
    """ Form for allowing the user to configure the settings. """

    # ----- Commonly changed settings ----

    target_temp_max = forms.FloatField(
        initial=22.5,
        widget=forms.NumberInput(attrs={"step": "0.5", "min": "15", "max": "25"}),
    )
    target_temp_min = forms.FloatField(
        initial=21.5,
        widget=forms.NumberInput(attrs={"step": "0.5", "min": "15", "max": "25"}),
    )
    active = forms.BooleanField(
        label="Temperature control active",
        required=False,
        initial=True,
    )

    # ----- Schedule -----

    auto_disable_at = forms.TimeField(
        label="Automatically disable temperature control every day at",
        required=False,
        widget=forms.TimeInput(attrs={"placeholder": "HH:MM"}),
        help_text="Exact time will depend on cron frequency",
    )
    switch_heating_off_when_auto_disabling = forms.BooleanField(
        required=False,
        initial=True,
        help_text=(
            "This causes the max-temp-reached webhook to be fired when the automatic switch off "
            "happens, so that your heating is switched off."
        ),
    )
    auto_enable_at = forms.TimeField(
        label="Automatically re-enable temperature control every day at",
        required=False,
        widget=forms.TimeInput(attrs={"placeholder": "HH:MM"}),
        help_text="Exact time will depend on cron frequency",
    )
    auto_enable_on_days = forms.MultipleChoiceField(
        choices=WEEKDAY_CHOICES,
        label="Auto-enable on these days",
        widget=forms.CheckboxSelectMultiple,
    )

    # ----- One-time configuration -----
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
