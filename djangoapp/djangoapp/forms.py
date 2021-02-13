from django import forms

from .utils.config import save_config_data


class ConfigForm(forms.Form):
    """ Form for allowing the user to configure the settings. """

    # All fields are required
    target_temp_max = forms.FloatField(initial=22.5)
    target_temp_min = forms.FloatField(initial=21.5)
    max_temp_webhook_name = forms.CharField(initial="living_room_at_max_temperature")
    min_temp_webhook_name = forms.CharField(initial="living_room_at_min_temperature")
    ifttt_webhook_key = forms.CharField(
        label="IFTTT webhook key",
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
    )

    def save(self):
        save_config_data(self.cleaned_data)
