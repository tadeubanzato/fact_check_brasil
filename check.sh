#!/bin/sh
## check.sh
CHECK=/tmp/check.pid
if [ -f "$CHECK" ]; then
    echo "$CHECK exists."
else
    echo "$CHECK does not exist."
    cd /home/pi/telegrambot/factcheck
    screen -dm -S CHECK python3 /home/pi/telegrambot/factcheck/fact_check.py
fi
