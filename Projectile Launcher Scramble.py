#!/usr/bin/env python
# coding: utf-8

# In[1]:


#a set for height values
height_set = {.5,1,2,2.7, 3.3, 4, 5}

#a set for time values
time_set = {.23,.33,.48,.51,.75,.82,1.08}

#Displays sets
print("Height set:", height_set)
print("Time set:", time_set)


# In[6]:


get_ipython().system('pip install scipy')


# In[15]:


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


# In[12]:


get_ipython().system('pip install pandas')


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


# In[16]:


# Height of the Empire State Building in meters
height_empire_state = 443.2

# Predict time using the mean experimental g
time_empire_state = np.sqrt(2 * height_empire_state / g_mean)

# Display the result
print(f"Time for the ball to reach the ground from the Empire State Building: {time_empire_state:.2f} seconds")


# In[ ]:




