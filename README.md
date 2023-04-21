# Installation

```
git clone https://github.com/Provo-City-School-District/door_timer.git

crontab -e

@reboot /bin/python3 /home/pi/door_timer/door_timer.py >home/pi/door_timer/print_log.txt
0 16 * * * /bin/python3 /home/pi/door_timer/door_parser.py

cd door_timer
```
The ```>home/pi/door_timer/print_log.txt``` **should** route all
print statements to a txt file in the door_timer folder.

### Config Setup

If the config file is already within the door_configs folder,
```
mv door_configs/"correct-config.json" config.json
```
*If* it isn't already there, then edit the one the system comes with.
Then adjust recipients, adjust location id and location name. And add
the doors that are connected to the pi.
```
nano config.json
```
### Final Setup
Final Step is to restart the pi with
```
sudo shutdown -r now
```
With this everything should now work correctly.