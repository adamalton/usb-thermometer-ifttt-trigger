USB Nest Zone Sensor
====================

This is a lightweight application which uses a USB thermometer to monitor the temperature in a room
and check if that temperature is within a set range.
If it's outside the range then an IFTTT webhook is called, which can be used to control a Nest
(or other smart) thermostat.

The application runs its own web server in order to display a settings page to allow control of the
temperature range.

It fires one of two IFTTT webhooks, one for when the temperature is too high, and one for when it's too
low. You'll need to have an IFTTT account and set these up to then trigger control of your smart thermostat.


Installation
------------

### Pre requisites

If you're using a Raspberry Pi with Raspbian 9 or higher, these should already be installed.

* `git`
* `python3`
* `virtualenv`


### Installation Steps

```
git clone git@github.com:adamalton/usb-thermometer-ifttt-trigger.git
sudo apt-get install virtualenv
cd usb-thermometer-ifttt-trigger
bin/install.sh
```

You might want to edit `TIME_ZONE` in `djangoapp/settings.py` if you're not in the UK.
See [list of time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for options.

Then you need to add this script to your crontab so that it is run at regular intervals.
For now, this needs to be run from the root crontab so that the script has permissions on the USB device.

Edit your cron tab:

```
sudo crontab -e
```

Then add:

```
*/5 * * * * /ABSOLUTE/PATH/TO/usb-thermometer-ifttt-trigger/bin/cronscript.sh
```

Get the server up and running to start with (so that you don't have to wait for the cron task to run):

```
bin/start_server.sh
```

Then open a web browser and go to: `http://localhost:8085`.
Or if you're accessing this from a different computer (not on your Raspberry Pi) then you'll
need to swap `localhost` for the IP address of your Raspberry Pi on your local network.


### IFTTT

You need to set up two IFTTT webhooks using the IFTTT app.
You'll need one applet along the lines of:

```When webhook "living_room_above_max_temperature` runs, set Nest temperature to <something low>.```

And another along the lines of:

```When webhook "living_room_below_min_temperature` runs, set Nest temperature to <something high>.```

Make sure that the names of the webhooks in your IFTTT applets match those that you've put in the settings page.

You'll also need to find your webhook key, which is somewhere in the IFTTT web pages if you log in!
