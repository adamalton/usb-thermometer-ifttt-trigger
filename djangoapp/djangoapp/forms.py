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

class BulmaForm(forms.Form):
    """ Form base class that adds CSS classes for use with the Bulma CSS library. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field, (forms.BooleanField, forms.ChoiceField)):
                field.widget.attrs['class'] = 'input'

    def is_valid(self, *args, **kwargs):
        return_value = super().is_valid(*args, **kwargs)
        for name, field in self.fields.items():
            if self.errors.get(name):
                field.widget.attrs.setdefault('class', '')
                field.widget.attrs['class'] += ' is-danger'
        return return_value


class ConfigForm(BulmaForm):
    """ Form for allowing the user to configure the settings. """

    # ----- Commonly changed settings ----

    target_temp_max = forms.FloatField(
        initial=22.5,
        widget=forms.NumberInput(attrs={"step": "0.5", "min": "15", "max": "25", "size": "3"}),
    )
    target_temp_min = forms.FloatField(
        initial=21.5,
        widget=forms.NumberInput(attrs={"step": "0.5", "min": "15", "max": "25", "size": "3"}),
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
        widget=forms.TimeInput(attrs={"placeholder": "HH:MM", "size": "3"}),
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
        widget=forms.TimeInput(attrs={"placeholder": "HH:MM", "size": "3"}),
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
        widget=forms.PasswordInput(render_value=True, attrs={"autocomplete": "off"}),
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
