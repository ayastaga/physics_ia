import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

# Enter the name of the file
name = "40g_trial_3.csv"

# Load the CSV file
df = pd.read_csv(name)

# Rename columns if needed
df.columns = ["Time", "Position", "Velocity", "Acceleration"]

# Extract time and position data
time = df["Time"].values
position = df["Position"].values

# Find peaks (local maxima)
peaks, _ = find_peaks(position)

# Extract peak times and amplitudes
peak_times = time[peaks]
peak_amplitudes = position[peaks]

# Define an exponential decay function with an offset C
def decay_func(t, A0, gamma, C):
    return A0 * np.exp(-gamma * t) + C

# Fit exponential decay to the peak values
popt, _ = curve_fit(decay_func, peak_times, peak_amplitudes, p0=[max(peak_amplitudes), 0.1, min(peak_amplitudes)])

# Extract parameters
A0, gamma, C = popt

# Compute predicted values for the detected peaks
predicted_amplitudes = decay_func(peak_times, *popt)

# Calculate R^2 value
ss_residuals = np.sum((peak_amplitudes - predicted_amplitudes) ** 2)  # Residual sum of squares
ss_total = np.sum((peak_amplitudes - np.mean(peak_amplitudes)) ** 2)  # Total sum of squares
r_squared = 1 - (ss_residuals / ss_total)

# Print the exponential equation and R^2 value
print(f"Exponential Decay Equation: A(t) = {A0:.4f} * e^(-{gamma:.4f} * t) + {C:.4f}")
print(f"Damping Coefficient (γ): {gamma:.4f}")
print(f"R² Value: {r_squared:.4f}")

# Plot the full position-time graph
plt.figure(figsize=(8,5))
plt.plot(time, position, label="Position Data", color="blue", alpha=0.6)

# Highlight detected peaks
#plt.scatter(peak_times, peak_amplitudes, color="red", label="Detected Peaks", zorder=3)

# Plot the fitted exponential decay curve
t_fit = np.linspace(time[0], time[-1], 100)
plt.plot(t_fit, decay_func(t_fit, *popt), label=f"Fitted Decay: A(t) = {A0:.2f} * e^(-{gamma:.2f} * t) + {C:.2f}", color="green")

# Labels and legend
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title(f"Damped Harmonic Motion: Exponential Fit Through Peaks\n$R^2$ = {r_squared:.4f}")
plt.legend()
plt.grid()
plt.show()
