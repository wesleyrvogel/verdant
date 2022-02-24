"""
This contains a lightweight series of interface classes for 
controlling the various bits of hardware to which the Pi is 
connected. It also contains the top-level control loop for 
the hydroponics setup.
"""
import subprocess
import time


class GPIOController


class ADCController


class HumiditySensor


class CO2Sensor



# Inital resource setup


# Functional control loop
errored = False

while not errored:
    try:
        # Collect sensor measurements

        # Determine what hardware needs to be actuated

        # Wait until next control period
        time.sleep(10 * 10e3)  # Sleep in ms, so ~10s period
    except Exception as ex:
        print(ex)

# Resource deallocation

