import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # <-- Fix import (previously incorrect)
from scipy.signal import find_peaks

# Constants
m = 40
k = 5886

numbers = [1, 2, 3, 4]

for i in numbers:
    file_name = f"{m}g_trial_{i}.csv"

    # Load CSV
    df = pd.read_csv(file_name)
    df.columns = ["Time", "Position", "Velocity", "Acceleration"]

    # Extract time and position data
    time = df["Time"].values
    position = df["Position"].values

    # Find peaks
    peaks, _ = find_peaks(position)
    peak_amplitudes = position[peaks]

    peaks = peaks[position[peaks] >= 0.2]  # Keep only peaks where position >= 0.3
    peak_amplitudes = position[peaks]  # Update peak amplitudes after filtering

    # Compute logarithmic decrement and damping ratio
    if len(peak_amplitudes) >= 2:
        deltas = np.log(peak_amplitudes[:-1] / peak_amplitudes[1:])
        delta_mean = np.mean(deltas)  # Average logarithmic decrement
        damping_ratio = delta_mean / np.sqrt(4 * np.pi**2 + delta_mean**2)
        print(f"{damping_ratio}")
    else:
        print("Not enough peaks to calculate damping ratio.")


'''
# ---------------- PLOTTING ----------------
plt.figure(figsize=(10, 5))  # Set figure size
plt.plot(time, position, label="Position-Time Graph", color="blue")  # Original data
plt.scatter(time[peaks], peak_amplitudes, color="red", marker="o", label="Peaks")  # Peaks

# Annotate peak values
for i, txt in enumerate(peak_amplitudes):
    plt.annotate(f"", (time[peaks][i], peak_amplitudes[i]), textcoords="offset points", xytext=(0,10), ha="center")

# Labels and Title
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title(f"Damped Oscillation with Peaks ({file_name})")
plt.legend()
plt.grid(True)

# Show plot
plt.show()
'''