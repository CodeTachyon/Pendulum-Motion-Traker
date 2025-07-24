import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# === Load Data ===
raw_data = pd.read_csv("pendulum_data.csv")
peak_data = pd.read_csv("pendulum_peaks.csv")

times = raw_data['Time (s)'].to_numpy()
angles = raw_data['Angle (degrees)'].to_numpy()
peak_times = peak_data['Peak Time (s)'].to_numpy()
peak_angles = peak_data['Peak Angle (deg)'].to_numpy()

# === Frequency and Amplitude ===
amplitude = np.mean(np.abs(peak_angles))
periods = np.diff(peak_times)
frequency = 1 / np.mean(periods)

# === Exponential Decay Fit ===
def exponential_decay(t, A0, gamma):
    return A0 * np.exp(-gamma * t)

popt, _ = curve_fit(exponential_decay, peak_times, np.abs(peak_angles))
A0_fit, gamma_fit = popt
tau = 1 / gamma_fit

print("\n=== Pendulum Damping Fit Results ===")
print(f"Estimated Amplitude ≈ {amplitude:.2f} degrees")
print(f"Estimated Frequency ≈ {frequency:.3f} Hz")
print(f"Fitted Decay: A(t) = {A0_fit:.2f} * exp(-{gamma_fit:.4f} * t)")
print(f"Damping Coefficient γ ≈ {gamma_fit:.4f} s⁻¹")
print(f"Damping Time Constant τ ≈ {tau:.2f} s")

# === Plotting ===
plt.figure(figsize=(10, 5))
plt.plot(times, angles, label="Anglular Displacement Over Time ", alpha=0.5)
plt.plot(peak_times, peak_angles, 'ro', label="Detected Peaks")

t_fit = np.linspace(peak_times[0], peak_times[-1], 500)
amp_fit = exponential_decay(t_fit, A0_fit, gamma_fit)
plt.plot(t_fit, amp_fit, 'g--', label="Exponential Fit")

plt.title("Pendulum Motion with Damping Envelope Fit")
plt.xlabel("Time (s)")
plt.ylabel("Angle (degrees)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
