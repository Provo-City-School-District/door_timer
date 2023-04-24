from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib, ssl

import json

file = open("/home/pi/door_timer/door_log.txt", "r")

config = json.load(open("/home/pi/door_timer/config.json"))

# Store line number for error logging.
line_number = -1

door_data = {}

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

    if door_name in door_data:
        door_data[door_name] += [f"Open for {open_time} seconds on {timestamp.date()} at {timestamp.time()}"]
    else:
        door_data[door_name] = [f"Open for {open_time} seconds on {timestamp.date()} at {timestamp.time()}"]


context = ssl.create_default_context()

# This is where we'd send the message.
with smtplib.SMTP("smtp.provo.edu", 25) as server:
    send_string = ""
    for door in door_data:
        door_string = f"{door}"
        for open_data in door_data[door]:
            door_string += f"\n   - {open_data}"

        print(door_string)

        send_string += "\n\n" + door_string

    if send_string != "":
        msg = MIMEMultipart('alternative')
        msg['From'] = 'Do Not Reply <donotreply@provo.edu>'
        msg['To'] = "door_admin@provo.edu"
        msg['Subject'] = f"Doors at {config['location_id']}, {config['location_name']}"

        msg.attach(MIMEText(send_string))

        server.sendmail("donotreply@provo.edu", config["recipients"], msg.as_string())

# Clear and close the log file.
file.close()

file = open("/home/pi/door_timer/door_log.txt", "w").close()
