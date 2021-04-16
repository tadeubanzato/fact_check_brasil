#!/bin/sh
## check.sh
CHECK=/tmp/check.pid
if [ -f "$CHECK" ]; then
    echo "$CHECK exists."
else
    echo "$CHECK does not exist."
    cd /home/pi/telegrambot/fact_check_brasil
    screen -dm -S CHECK python3 /home/pi/telegrambot/fact_check_brasil/fact_check.py
fi
