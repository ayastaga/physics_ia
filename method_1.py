import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # <-- Fix import (previously incorrect)
from scipy.signal import find_peaks

# Constants
m = 80
k = 5886

numbers = [2, 3, 4, 5]

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

    # Calculate damping ratio (Zeta)
    damp_coeff = []
    a_0 = max(peak_amplitudes)  # Max amplitude of the first peak

    for elem in peaks:
        amp = position[elem]
        t = time[elem]
            
        if amp < a_0:  # Ensure decay
            c = math.log(amp / a_0) * (-2 * m / t)
            damp_coeff.append(c)
            
    len_damp_coeff = len(damp_coeff)
    avg_c = sum(damp_coeff) / len_damp_coeff if len_damp_coeff > 0 else None
    zeta = avg_c / (2 * math.sqrt(k * m))
    print(zeta)

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