"""
This contains a lightweight series of interface classes for 
controlling the various bits of hardware to which the Pi is 
connected. It also contains the top-level control loop for 
the hydroponics setup.
"""
import subprocess
import time
import RPi.GPIO as gpio


def execute_command(command):
    """
    This executes a Linux command and returns the results.
    It's basically a wrapper for a bunch of subprocess 
    stuff.
    Args:
        command: The command to execute as a string
    Retuns:
        The result of running the command as a string
    """
    process = subprocess.Popen([command], 
                               stdout=subprocess.PIPE, 
                               shell=True)

    response, error = process.communicate()
    return response


class GPIOController:
    """
    This class represents a GPIO pin set to output binary 
    values on the Pi pinout. The Pi GPIO logic level is 
    3.3V on the primary breakout header.
    """
    def __init__(self, pin, initial_state=False):
        gpio.setup(pin, gpio.OUT)
        self.pin = pin
        self.set_state(initial_state)
        

    def set_state(self, state):
        """
        Sets the state of the GPIO output.
        Args:
            state: Boolean value representing on or off
        """
        # This is where we would set the state
        gpio.output(self.pin, gpio.HIGH if state else gpio.LOW)


class ADCController:
    """
    This class represents an interface to the ADS1115
    ADC. The pimary I2C communications are implemented 
    in a Rust driver, this just wraps the ouputs of that 
    driver to be used in Python.
    """
    def __init__(self):
        self.dummy = True


class HumiditySensor:
    """
    This class represents an interface to the humidity 
    sensor.
    """
    def __init__(self):
        self.dummy = True


class CO2Sensor:
    """
    This class represents an interface to the Dracal 
    DXC120 USB CO2 sensor. The sensor is plugged directly
    into on the of the Pi's USB ports, so this just wraps 
    a serial interface.
    """
    def __init__(self):
        self.dummy = True


# Inital resource setup
gpio.setmode(gpio.BOARD)  # This sets pin addressing scheme
big_pump = GPIOController(37)  # This is the main water pump

print('Turning pump on')
big_pump.set_state(True)
time.sleep(10)
print('Truning pump off')
big_pump.set_state(False)

# Functional control loop
errored = True  # Set to true to skip the loop during dev

while not errored:
    try:
        # Collect sensor measurements

        # Determine what hardware needs to be actuated

        # Wait until next control period
        time.sleep(10)  # Sleep in s, so ~10s period
    except Exception as ex:
        print(ex)

# Resource deallocation
gpio.cleanup()  # This cleans up the GPIO resources
