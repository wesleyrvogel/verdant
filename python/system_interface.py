"""
This contains a lightweight series of interface classes for 
controlling the various bits of hardware to which the Pi is 
connected.
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
        """
        This is the class init method.
        Args:
            pin: GPIO pin number on the Pi
            initial_state: bool, desired initial on/off state
        """
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
    def __init__(self, sensor_id=0):
        """
        This creates a Dracal DXC120 CO2 sensor.
        Args:
            sensor_id: The sensor ID to query
        """
        self.sensor_id = sensor_id

    def get_co2_concentration(self):
        """
        This returns the concentration of CO2 as read by 
        the sensor in ppm. The typical reading in an 
        indoor atmosphere should be between approximately 
        400 and 1000 ppm.
        """
        command = 'sudo ~/Code/dracal_source/usbtenki-2.1.23/client/usbtenkiget -i {}'.format(self.sensor_id)
        response = execute_command(command)
        return float(response)

