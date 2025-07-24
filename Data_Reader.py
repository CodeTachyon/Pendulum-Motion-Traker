import serial
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import pandas as pd

# === Serial Data Collection ===
# Update your COM port (e.g., 'COM3' for Windows, '/dev/ttyUSB0' for Linux)
ser = serial.Serial('COM10', 9600)
angles = []
times = []

print("Reading data... Press Ctrl+C to stop.\n")

try:
    while True:
        line = ser.readline().decode().strip()
        if ',' in line:
            angle_str, time_str = line.split(',')
            angles.append(float(angle_str))
            times.append(float(time_str))
except KeyboardInterrupt:
    ser.close()
    print("Data collection finished.\n")

angles = np.array(angles)
times = np.array(times)

# === Save Raw Data ===
raw_data = pd.DataFrame({'Time (s)': times, 'Angle (degrees)': angles})
raw_data.to_csv('pendulum_data.csv', index=False)
print("Raw data saved to 'pendulum_data.csv'.")

# === Peak Detection ===
peaks, _ = find_peaks(angles, height=0, distance=20)
peak_times = times[peaks]
peak_angles = angles[peaks]

# Save peak data (optional)
peak_data = pd.DataFrame({'Peak Time (s)': peak_times, 'Peak Angle (deg)': peak_angles})
peak_data.to_csv('pendulum_peaks.csv', index=False)
print("Peak data saved to 'pendulum_peaks.csv'.")
