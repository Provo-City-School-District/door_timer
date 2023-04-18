from datetime import datetime

from pysnmp.hlapi import *

file = open("door_log.txt", "r")

# Store line number for error logging.
line_number = -1

door_data = {}

for line in file.readlines():
    line_number += 1
    line.replace("\n", '')
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
        door_data[door_name] += [f"Open for {open_time} at {timestamp}"]
    else:
        door_data[door_name] = [f"Open for {open_time} at {timestamp}"]


# This is where we'd send the message.
for door in door_data:
    send_string = f"{door}"
    for open_data in door_data[door]:
        send_string += f"\n   - {open_data}"

    print(send_string)

    # TODO: Change this to run send the correct message to the system.
    next(sendNotification(
        SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget(('smtp.provo.edu ', 25)),
        ContextData(),
        'trap',
        # TODO Figure out what the ObjectIdentity is.
        # In theory, this should just send the log as the send_string above, I just don't know it well enough.
        [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'), OctetString(send_string))]
    ))

# Clear and close the log file.
file.close()

file = open("door_log.txt", "w").close()
