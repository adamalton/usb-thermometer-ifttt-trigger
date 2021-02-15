#!/bin/bash

# Checks the current temperature from the USB thermometer and if it falls outside of the desired
# range, calls an IFTTT webhook.

# This should be called periodically by a cron job.

curl http://localhost:8085/check-temperature/
