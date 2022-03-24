"""
This contains a lightweight series of interface classes for 
controlling the various bits of hardware to which the Pi is 
connected.
"""
import subprocess
import time
import datetime
import os
import csv
from enum import Enum
import RPi.GPIO as gpio
import serial


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


class ADS1115Range(Enum):
    """
    This represents a full-scale voltage range for the 
    ADS1115 ADC IC.
    """
    Range0_256V = 0
    Range0_512V = 1
    Range1_024V = 2
    Range2_048V = 3
    Range4_096V = 4
    Range6_144V = 5


class ADCController:
    """
    This class represents an interface to the ADS1115
    ADC. The pimary I2C communications are implemented 
    in a Rust driver, this just wraps the ouputs of that 
    driver to be used in Python.
    """
    def __init__(self, channel_count=4, initial_range=ADS1115Range.Range6_144V):
        self.channel_count = channel_count
        self.fsr = initial_range

    def set_full_scale_range(self, fsr):
        """
        This sets the full scale range to use when making
        measurements.
        Args:
            fsr: ADS1115Range enum representing deisred range
        """
        self.fsr = fsr

    def get_channel_reading(self, channel):
        """
        Reads a channel from the ADC using the 
        pre-specified full scale range.
        Args:
            channel: 0-3, the channel to read from
        """
        command = '~/Code/verdant/rust/ads1115-driver/target/release/ads1115-driver {} {}'.format(channel, self.fsr.value)
        response = execute_command(command)
        return float(response)


class ConductivitySensor:
    """
    This class interfaces with an Atlas Scientific 
    conductivity sensor.
    """
    def __init__(self, serial_path, k_val=0.1, timeout=1.0):
        self.k_val = k_val
        self.ser = serial.Serial(serial_path,
                                 timeout=timeout)
        self.set_sensitivity_value(self.k_val)

        # Let's disable continuous reads by default
        self.set_continuous_read_state(False)

    def _write_to_device(self, write_string):
        """
        This writes to the device via its serial port.
        A CR is appended to the end of the write string
        via this method.
        Args:
            write_string: String to write to device
        """
        self.ser.write(bytes('{}\r'.format(write_string), 
                       'utf8'))

    def _read_from_device(self):
        """
        This reads from the device up to the standard 
        timeout period. This is a blocking method during
        that time.
        Returns:
            String responses from the device in array form.
        """
        # Let's set a large buffer size and split the response
        return self.ser.read(10000).decode().strip().split('\r')

    def write_and_read_response(self, write_string):
        """
        This writes a string to the device and reads 
        any response if may return. It removes any confirmation
        (ie *OK) responses for simplicity.
        Args:
            write_string: String to write to the device
        Returns:
            String responses from the device in array form.
        """
        self._write_to_device(write_string)
        response = self._read_from_device()
        if '*OK' in response:
            response.remove('*OK')

        return response
    
    def set_sensitivity_value(self, k_val):
        """
        Sets the sensitivty of the sensor.
        """
        response = self.write_and_read_response('K,{}'.format(k_val))

    def set_continuous_read_state(self, read_continuously):
        """
        This turns on or off continuous reading on the device.
        Args:
            read_continuously: bool of the desired read state
        """
        rate = '1' if read_continuously else '0'
        response = self.write_and_read_response('C,{}'.format(rate))

    def get_conductivity(self):
        """
        This gets the conductivity as measured by the sensor.
        Returns:
            A float value of the conductivity as read by the sensor
        """
        response = self.write_and_read_response('R')
        return float(response[0])

    def close_connection(self):
        """
        This closes the serial connection to the device.
        """
        self.ser.close()


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


class GPIOFrequencyCounter:
    """
    This class runs some threads in the background to 
    count rising edges on a hardware GPIO with the 
    intention of determining frequency.
    """
    def _init__(self, pin):
        gpio.setup(pin, )
        self.pin = pin
        self.counts = 0
        self.counting = False
    
    def begin_counting(self):
        """
        This will begin the counting process for the 
        hardware pin.
        """
        return 0


class StateLogger:
    """
    This is a small class that will log sensor measurements
    and the time they were taken to a CSV file.
    """
    def __init__(self, log_dir):
        time_str = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
        filename = 'verdant_log_{}.txt'.format(time_str)
        filepath = os.path.join(log_dir, filename)
        self.log_file = open(filepath, 'w')
        self.writer = csv.writer(self.log_file)
        fields = ['Time', 'CO2 (ppm)', 'Conductivity (us/cm)']
        self.writer.writerow(fields)

    def log_values(self, co2, conductivity):
        current_time = str(datetime.datetime.now())
        self.writer.writerow([current_time, co2, conductivity])
