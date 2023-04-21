# Installation

```
git clone https://github.com/Provo-City-School-District/door_timer.git

crontab -e

@reboot /bin/python3 /home/pi/door_timer/door_timer.py
0 16 * * * /bin/python3 /home/pi/door_timer/door_parser.py
```
