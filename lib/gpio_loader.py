import RPi.GPIO as GPIO


# Create the class that stores the data for each door.
class GPIOSystem:
    def __init__(self, name, gpio: int):
        self.name = name
        self.gpio: int = gpio
        self.closed: bool = True
        self.open_time: float = 0


# Loads all gpios and returns a list of GPIOSystems
def load_gpios(config) -> [GPIO]:
    gpio_systems = []
    for gpio in config.get("doors"):
        gpio_systems += [GPIOSystem(gpio["name"], gpio["port"])]
        print(f"Added GPIO System with Name: {gpio['name']}, on port {gpio['port']}")

    GPIO.setmode(GPIO.BCM)

    # Init all the GPIOs
    gpio_list = []
    for system in gpio_systems:
        gpio_list += [system.gpio]

    GPIO.setup(gpio_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    return gpio_systems


# Unloads all gpios
def unload_gpios():
    GPIO.cleanup()
