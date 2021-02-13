USB Nest Zone Sensor
====================

This is a lightweight application which uses a USB thermometer to monitor the temperature in a room
and check if that temperature is within a set range.
If it's outside the range then an IFTTT webhook is called, which can be used to control a Nest
thermostat.

The application runs its own web server in order to display a settings page to allow control of the
temperature range.

There are 2 IFTTT webhooks, one for when the temperature is too high, and one for when it's too
low.
