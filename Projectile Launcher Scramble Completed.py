#!/usr/bin/env python
# coding: utf-8

# In[19]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

# Data
height_set = {0.5, 1, 2, 2.7, 3.3, 4, 5}
time_set = {0.23, 0.33, 0.48, 0.51, 0.75, 0.82, 1.08}

# Sort for consistent pairing
heights = np.array(sorted(height_set))
times = np.array(sorted(time_set))

# Define model: t = sqrt(2h / g)
def model(h, g):
    return np.sqrt(2 * h / g)

# Fit the model to the data (find the mean experimental g)
params, _ = curve_fit(model, heights, times)
g_mean = params[0]

# Theoretical curve with g = 9.81 m/s²
g_theoretical = 9.81
theoretical_times = model(heights, g_theoretical)

# Experimental curve with the mean g from the fit
experimental_times = model(heights, g_mean)

# Plotting
plt.figure(figsize=(8, 6))

# Scatter plot of the data points
plt.scatter(heights, times, color='blue', label='Experimental Data', s=50)

# Plot theoretical curve (using g = 9.81)
plt.plot(heights, theoretical_times, color='green', linestyle='--', label=f'Theoretical Curve ($g = 9.81$ m/s²)')

# Plot experimental curve (using mean g from the fit)
plt.plot(heights, experimental_times, color='red', linestyle='-', label=f'Experimental Fit ($g = {g_mean:.2f}$ m/s²)')

# Labels and title
plt.xlabel("Height (m)")
plt.ylabel("Time (s)")
plt.title("Height vs Time with Theoretical and Experimental Fits")
plt.legend()
plt.grid(True)

# Show plot
plt.show()

# Display mean experimental g value
print(f"Mean experimental value of g: {g_mean:.2f} m/s²")

#end code block


# In[14]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Data
height_set = {0.5, 1, 2, 2.7, 3.3, 4, 5}
time_set = {0.23, 0.33, 0.48, 0.51, 0.75, 0.82, 1.08}

# Sort for consistent pairing
heights = np.array(sorted(height_set))
times = np.array(sorted(time_set))

# Calculate gravity for each height-time pair: g = 2h / t^2
gravity_values = 2 * heights / (times ** 2)

# Create a DataFrame for displaying
df = pd.DataFrame({
    'Height (m)': heights,
    'Time (s)': times,
    'Gravity Estimate (g)': gravity_values
})

# Calculate the median and mean of g
g_median = np.median(gravity_values)
g_mean = np.mean(gravity_values)

# Plot the table
fig, ax = plt.subplots(figsize=(8, 6))
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

# Add boxes for median and mean values
plt.figtext(0.5, 0.15, f"Median g = {g_median:.2f} m/s²", ha="center", fontsize=12, bbox=dict(facecolor="lightblue", alpha=0.5))
plt.figtext(0.5, 0.05, f"Mean g = {g_mean:.2f} m/s²", ha="center", fontsize=12, bbox=dict(facecolor="lightgreen", alpha=0.5))

plt.show()

#end code block


# In[16]:


# Height of the Empire State Building in meters
height_empire_state = 443.2

# Predict time using the mean experimental g
time_empire_state = np.sqrt(2 * height_empire_state / g_mean)

# Display the result
print(f"Time for the ball to reach the ground from the Empire State Building: {time_empire_state:.2f} seconds")

#End code block


# In[20]:


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

#End code block


# In[24]:


import numpy as np
import pandas as pd

# Initial horizontal speed
v0 = 5.44  # m/s

# Heights used in the experiment
heights = np.array(sorted({0.5, 1, 2, 2.7, 3.3, 4, 5}))

# Use your previously calculated mean experimental g
try:
    g_mean
except NameError:
    g_mean = 9.62  # Placeholder: replace with your calculated value

# Calculate estimated time using experimental g
times = np.sqrt(2 * heights / g_mean)

# Calculate estimated horizontal distances
estimated_distances = v0 * times

# Placeholder for actual distances (you can replace these with real measurements)
actual_distances = np.array([3.8, 4.6, 5, 5.5, 6.75, 7.25, 7.75])  # replace with real data

# Create the DataFrame
df = pd.DataFrame({
    'Height (m)': heights,
    'Time (s)': times.round(3),
    'Estimated Distance (m)': estimated_distances.round(3),
    'Actual Distance (m)': actual_distances
})

# Display the table
print("Comparison of Estimated and Actual Projectile Distances\n")
display(df

#end code block


# In our trials we fell short of the predicted distance every shot. We belive this is due to our estimated gravity being almost 7 $\frac{m}{s^2}$ above the known gravity. 
# 
# ![image.png](attachment:b78bd978-1c7f-466b-937a-2ff8349a929a.png)
# 
# #endblock

# In[25]:


import matplotlib.pyplot as plt
import numpy as np

# Given data
heights = np.array([0.5, 1.0, 2.0, 2.7, 3.3, 4.0, 5.0])  # in meters
actual_distances = np.array([3.80, 4.60, 5.00, 5.50, 6.75, 7.25, 7.75])  # in meters

# Constants
v0 = 5.44  # initial velocity in m/s
g_mean = 9.62  # experimental gravity in m/s²

# Predicted distances using d = v0 * sqrt(2h/g)
predicted_distances = v0 * np.sqrt(2 * heights / g_mean)

# Plotting
plt.figure(figsize=(8, 6))

# Scatter plot of actual distances
plt.scatter(heights, actual_distances, color='blue', label='Actual Distance', s=70)

# Line plot of predicted distances
plt.plot(heights, predicted_distances, color='red', linestyle='--', label='Predicted Distance (Experimental g & v₀)')

# Labels and title
plt.xlabel("Height (m)")
plt.ylabel("Distance Traveled (m)")
plt.title("Actual vs Predicted Projectile Distances")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

#end code block


# In[ ]:




