# Log Entry Example
# Door Name,TimeOpen,Timestamp

import json
import time

from lib import gpio_loader
from lib import date

import RPi.GPIO as GPIO

config = json.load(open("config.json"))

# Loads the GPIOs and Enables them.
gpio_systems = gpio_loader.load_gpios(config)

file = None

try:
    # Open the log in append mode.
    file = open("door_log.txt", "a")

    while True:
        for door in gpio_systems:
            if GPIO.input(door.gpio) == 0 and door.closed:
                continue

            # The Door Was Just Opened
            if GPIO.input(door.gpio) == 1 and door.closed:
                door.open_time = time.time()

                time.sleep(0.2)

                print(f"{door.name} is Open")

                door.closed = False

            # The Door Was Just Closed
            if GPIO.input(door.gpio) == 0 and not door.closed:
                # This is the actual time that the door is closed
                close_time = time.time()

                # Set the total time and format it to look correct.
                total_time = close_time - door.open_time

                # If the door was open for 180 seconds, we need to log it.
                if total_time > 180:
                    total_time = "{0:.2f}".format(total_time)

                    # Write the data to the file
                    file.write(f"{door.name},{total_time},{date.date()}\n")
                    file.flush()

                # Print out the system for people actively watching it.
                print(door.name, total_time, date.date())

                # Tell the program that the door is now closed
                door.closed = True

                # Clean up our extra data, and reset the open time of the door
                del total_time
                del close_time
                door.open_time = 0

        # As to not spam the system with calls that aren't needed.
        time.sleep(0.25)


finally:
    # Clean up the data and close the file and the connection to the database
    print("Quit!")

    # Make sure the file was actually opened, and if it was, close it.
    if file:
        file.close()

    # Unload the GPIO system
    gpio_loader.unload_gpios()
