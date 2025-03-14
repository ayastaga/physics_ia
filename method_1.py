import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # <-- Fix import (previously incorrect)
from scipy.signal import find_peaks

m = 40 # mass of the given trial
k = 5886 # spring constant


numbers = [2]
masses = [40, 60, 80, 100, 120, 140]

for i in numbers:
    for m in masses:
        file_name = f"physics_data/{m}g_trial_{i}.csv"

        # Load CSV
        df = pd.read_csv(file_name)
        df.columns = ["Time", "Position", "Velocity", "Acceleration"]

        # Extract time and position data
        time = df["Time"].values
        position = df["Position"].values

        from scipy.signal import find_peaks
        peaks, _ = find_peaks(position) # finds the peak using an external library
        peak_amplitudes = position[peaks] # lists down the amplitudes at those peaks

        peaks = peaks[position[peaks] >= 0.2] #keeps only peaks where the position >= 0.3
            # doing so helps eliminate any "peaks" that might be picked up due to noise/error
        peak_amplitudes = position[peaks]  # Update peak amplitudes after filtering
        
        damp_coeff_ARRAY = [] # stores ALL the values of the damping coefficient 

        a_0 = max(peak_amplitudes)  # sets A to be the highest oscillation
        # this is done in case the correct amplitude wasn't picked up and so it makes the closest approximation

        # For the nth point in the set of peaks:
        for n in peaks:
            # Find the amplitude at the nth peak
            amp = position[n]
            # Find the time at the nth peak
            t = time[n]
            
            # find the damping coefficient using equation (3)
            c = math.log(amp / a_0) * (-2 * m / t)
            # add that damping coefficient to the list of ALL damping coefficient at every instant of time
            damp_coeff_ARRAY.append(c)
                
        # find the average damping coefficient 
        avg_c = sum(damp_coeff_ARRAY) / len(damp_coeff_ARRAY)

        # find the damping ratio using equation (4)
        zeta = avg_c / (2 * math.sqrt(k * m))

        # output the damping ratio
        print(m, avg_c)

'''
# ---------------- PLOTTING ----------------
file_name_again = "140g_trial_2"
i = 2
plt.figure(figsize=(10, 5))  # Set figure size
plt.plot(time, position, label="Position-Time Graph", color="blue")  # Original data
plt.scatter(time[peaks], peak_amplitudes, color="red", marker="o", label="Peaks")  # Peaks

# Annotate peak values
for i, txt in enumerate(peak_amplitudes):
    plt.annotate(f"", (time[peaks][i], peak_amplitudes[i]), textcoords="offset points", xytext=(0,10), ha="center")

# Labels and Title
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title(f"Position-Time Graph with Peaks ({file_name_again})")
plt.legend()
plt.grid(True)

# Show plot
plt.show()
'''
