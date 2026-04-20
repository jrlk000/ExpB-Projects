import serial
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import logging

#------- interactive plot must be run inside the terminal to be updated  -------
# realised by cd (change directory inside current folder) and run via python3 filename


#logger configuration
DEBUG = True
logging.basicConfig(
    level=logging.INFO,
	format= '%(filename)s, %(lineno)d - %(message)s'
)

#creatae instance
logger = logging.getLogger("telemetry")

#switch between logger levels
if DEBUG:
    logger.setLevel(logging.DEBUG)

PORT = "/dev/ttyUSB0" #serial device on Ubuntu
BAUD = 115200 #serial speed
MAX_POINTS = 200

#create object through which python reads incoming data
ser = serial.Serial(PORT, BAUD, timeout=1)
'''
pyserial is used to read data from teh USB serial port

Here:
ESP32 sends text over USB
the PC reads that text through /dev/ttyUSB0
'''
times = deque(range(0, MAX_POINTS), maxlen=MAX_POINTS)
values_adc = deque((k*3.3/2**12 for k in range(0, MAX_POINTS)), maxlen=MAX_POINTS)
values_dac = deque((k*3.3/2**8 for k in range(0, MAX_POINTS)), maxlen=MAX_POINTS)


plt.ion()
fig, (ax1) = plt.subplots(1, 1)

#plot the measured analog values using the ADC and DAC of teh MycroController

#plot dac produced tension value over time.
line = ax1.plot([], [])
line1 = line[0]

#print(f"Line: {type(line)}, {line}")
#print(f"line1: {line1}, x: {line1.get_xdata()}, y: {line1.get_ydata()}")

ax1.set_title("DAC produced tension.")
ax1.set_xlabel("Time in [s]")
ax1.set_ylabel("Tension in [V]")
ax1.set_ylim(0, 3.3) #[Volt]
ax1.set_xlim(0, MAX_POINTS - 1) #Time in [sec]
plt.show(block=False)

#plot dac measured tension
"""line2 = ax1.plot([])
ax2.set_title()
ax2.set_xlabel()
ax2.set_ylabel()
ax2.set_ylim(0, 2**8)
ax2.set_xlim(0, MAX_POINTS - 1)"""

#plot dac over acd value !NOte: You have to norm both "maybe the quota with reference to the maximum of 3.3V"
####

while True:
    #read the information contained in ser
    raw = ser.readline().decode(errors="ignore").strip()
    #print(f"Material contained inside ser: {raw}.")
    #print(f"{repr(raw)}")
    #print(f"{len(raw.split(","))}")

    if not raw:
        continue

    try:
        #print("Entered try block.")
        raw_values = raw.split(",")
        t = int(float(raw_values[0]))
        dac_value = int(float(raw_values[1])) #8-bits
        #logger.debug(f"dac: {dac_value}")
        adc_value = int(float(raw_values[-1])) #12-bits
        #logger.debug(f"adc: {adc_value}")
    except ValueError:
        print('Value Error occurred.')
        continue

    #update the deque containers to update the plot.
    times.append(t)
    values_adc.append(adc_value * 3.3/2**12)
    values_dac.append(dac_value * 3.3/2**8)

    #set values inside the plot
    line1.set_xdata(list(range(len(values_dac))))
    #logger.debug(times[-1])
    line1.set_ydata(list(values_dac))
    #logger.debug(values_dac[-1])
    #ax1.relim()
    #ax1.autoscale_view(scalex=True, scaley=False)
    fig.canvas.draw()
    fig.canvas.flush_events()
    print(
         np.array(list(values_dac)[-5:], dtype=float)
          - np.array(line1.get_ydata()[-5:], dtype=float)
        )
    #print(line1.get_ydata()[-5:])
    plt.pause(0.01)
