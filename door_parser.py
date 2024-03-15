from collections import defaultdict
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib, ssl

import json

file = open("/home/pi/door_timer/door_log.txt", "r")

config = json.load(open("/home/pi/door_timer/config.json"))

# Store line number for error logging.
line_number = -1

door_data = defaultdict(list)

def get_hour_band(timestamp):
    if 1 <= timestamp.hour < 5:
        return '1am-5am'
    elif 5 <= timestamp.hour < 6:
        return '5am-6am'
    elif 6 <= timestamp.hour < 7:
        return '6am-7am'
    elif 7 <= timestamp.hour < 8:
        return '7am-8am'
    elif 8 <= timestamp.hour < 9:
        return '8am-9am'
    elif 9 <= timestamp.hour < 10:
        return '9am-10am'
    elif 10 <= timestamp.hour < 11:
        return '10am-11am'
    elif 11 <= timestamp.hour < 12:
        return '11am-12pm'
    elif 12 <= timestamp.hour < 13:
        return '12pm-1pm'
    elif 13 <= timestamp.hour < 14:
        return '1pm-2pm'
    elif 14 <= timestamp.hour < 15:
        return '2pm-3pm'
    elif 15 <= timestamp.hour < 16:
        return '3pm-4pm'
    elif 16 <= timestamp.hour < 17:
        return '4pm-5pm'
    elif 17 <= timestamp.hour < 24:
        return '5pm-12pm'
    else:
        return '12am-1am'

for line in file.readlines():
    line_number += 1
    line = line.replace("\n", '')
    split_line = line.split(',')

    try:
        door_name = split_line[0]
        open_time = float(split_line[1])
        timestamp = datetime.fromisoformat(split_line[2])
    except IndexError:
        print(f"Error: Line {line_number} is missing data")
        continue
    except TypeError:
        print(f"Error: Line {line_number} is formatted incorrectly")
        continue
    except ValueError:
        print(f"Error: Line {line_number} is formatted incorrectly")
        continue

    hour_band = get_hour_band(timestamp)
    door_data[door_name].append({"timestamp": timestamp, "open_time": open_time, "hour_band": hour_band})


context = ssl.create_default_context()

# This is where we'd send the message.
with smtplib.SMTP("smtp.provo.edu", 25) as server:
    send_string = ""
    for door in door_data:
        door_string = f"{door}"
        sorted_data = sorted(door_data[door], key=lambda x: x['timestamp'])
        grouped_data = defaultdict(list)
        for data in sorted_data:
            grouped_data[data['hour_band']].append(data)

        for hour_band in grouped_data:
            door_string += f"\n\t{hour_band}"
            for data in grouped_data[hour_band]:
                hours, remainder = divmod(data['open_time'], 3600)
                minutes, seconds = divmod(remainder, 60)
                if hours > 0:
                    door_string += f"\n\t   - Open for {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds on {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
                else:
                    door_string += f"\n\t   - Open for {int(minutes)} minutes, and {int(seconds)} seconds on {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"
        print(door_string)

        send_string += "\n\n" + door_string

    if send_string != "":
        msg = MIMEMultipart('alternative')
        msg['From'] = 'Door Sensor Report <donotreply@provo.edu>'
        msg['To'] = "door_admin@provo.edu"
        msg['Subject'] = f"Doors at {config['location_id']}, {config['location_name']}"

        msg.attach(MIMEText(send_string))

        server.sendmail("donotreply@provo.edu", config["recipients"], msg.as_string())

# Clear and close the log file.
file.close()

file = open("/home/pi/door_timer/door_log.txt", "w").close()