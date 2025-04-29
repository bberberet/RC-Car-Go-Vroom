#!/usr/bin/env python
# coding: utf-8

# In[11]:


# Step 1: Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np

# Step 2: Enter your measured distances (in meters) and times (in seconds)
# Replace the example values below with your actual measurements
distances = np.array([1.0, 2.0, 3.0, 4.0, 4.0, 5.0, 5.0])  # Δx in meters
times = np.array([0.246, 0.352, 0.468, 0.968, 0.89, 0.96, 0.98])  # Δt in seconds

# Step 3: Plot Δx vs Δt
plt.figure(figsize=(8, 5))
plt.scatter(times, distances, color='blue')
plt.title('Distance Traveled (Δx) vs Time (Δt)')
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.grid(True)
plt.show()

# Step 4: Calculate average speeds
avg_speeds = distances / times  # v = Δx / Δt

# Step 5: Plot v_avg vs Δt
plt.figure(figsize=(8, 5))
plt.scatter(times, avg_speeds, color='green', label='Average Speed')

# Optional: Fit a linear trendline to estimate y-intercept
coeffs = np.polyfit(times, avg_speeds, 1)
trendline = np.poly1d(coeffs)
x_fit = np.linspace(0, max(times), 100)
y_fit = trendline(x_fit)
plt.plot(x_fit, y_fit, 'k--', label='Trendline')

# Step 6: Mark estimated y-intercept (initial velocity v_i)
initial_speed = trendline(0)
plt.scatter(0, initial_speed, color='red', label=f'Estimated $v_i$ = {initial_speed:.2f} m/s')

plt.title('Average Speed vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Average Speed (m/s)')
plt.legend()
plt.grid(True)
plt.show()

# Step 7: Estimate time to roll across the US (no friction or air resistance)
# Approximate width of the continental US: 4,800,000 meters
us_distance = 4800000  # meters
time_to_cross_us = us_distance / initial_speed  # seconds

# Convert seconds to days/hours/minutes
days = time_to_cross_us // (24*3600)
hours = (time_to_cross_us % (24*3600)) // 3600
minutes = (time_to_cross_us % 3600) // 60
seconds = time_to_cross_us % 60

# Step 8: Print result in Markdown cell format
from IPython.display import Markdown

Markdown(f"""
### Estimated Initial Velocity
- Initial speed \(v_i\): **{initial_speed:.2f} m/s**

### Estimated Time to Cross the US (4800 km)
- Total time: **{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {seconds:.2f} seconds**

*(Assuming no friction or air resistance.)*
""")

