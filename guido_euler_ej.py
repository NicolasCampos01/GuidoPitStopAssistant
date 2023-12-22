

# Commented out IPython magic to ensure Python compatibility.
# MÉTODO DE EULER

#This code is as straightforward as running it, entering the desired circuit, and reviewing the graphically presented data.
#The user is prompted to input a Formula 1 circuit, and the code then utilizes the FastF1 library to fetch telemetry data from the 2021 qualifying session for the specified circuit.

# %reset -f
import fastf1
import numpy as np
import matplotlib.pyplot as plt

circuit = input("Enter your circuit: ")

#FastF1 code for extracting lap telemetry
session = fastf1.get_session(2021, circuit, 'Q')
session.load()
lap = session.laps.pick_fastest()
telemetry = lap.get_telemetry()
speeds = telemetry['Speed'].values / 3.6  # Km/hr to m/s
dt = 0.01

x = np.array(telemetry['X'].values)
y = np.array(telemetry['Y'].values)

# Our original array of time
time_in_nanosecs = telemetry['Time'].values

# Convert to seconds and extract the numerical values
time_data_array_seconds = time_in_nanosecs.astype(float) / 1e9

#round to two decimal places
time = np.round(time_data_array_seconds, decimals=2)

# dt = time[i] - time[i-1]

# Constants
mass = 900
g = 9.81  # (m/s^2)
reference_area = 2.0
air_density = 1.225
rolling_resistance_coefficient = 0.01
friction_coefficient = 0.9

#air resistance coefficient
air_resistance_coefficient = 0.7

# Calculate resistive forces
rolling_resistance_force = rolling_resistance_coefficient * mass * g

# Initialize accumulative wear array
accumulative_wear = np.zeros_like(speeds)

# Calculate resistive forces and accumulative wear
for i in range(len(speeds)):
    air_resistance_force = 0.5 * air_density * (speeds[i] ** 2) * air_resistance_coefficient * reference_area
    net_force = speeds[i] ** 2 * friction_coefficient - rolling_resistance_force - air_resistance_force

    work_done = dt * net_force

    # Wear calculation (simplified)
    wear = work_done / (mass * g)

    # Update accumulative wear
    accumulative_wear[i] = accumulative_wear[i - 1] + wear if i > 0 else wear

# Function to calculate normal force
def normal_force(mass, g):
    return mass * g

normal = normal_force(mass, g)

# Function to calculate resistive force (simplified)
def resistive_force(normal):
    return friction_coefficient * normal

friction = resistive_force(normal)

# Function to simulate car motion using Euler's method
def simulate_race(x, y, speeds, dt):
    num_steps = len(x)
    tire_wear = np.zeros(num_steps)  # Placeholder for tire wear
    pit_stop_markers = []  # To store points for optimal pit stops
    lap_count = 1  # Counter for lap count
    total_distance = 0.0  # Track the total distance covered
    accelerations = np.zeros(num_steps)

    for i in range(1, num_steps):
        v = speeds[i]   # Convert speed to m/s
        rolling_resistance_force = rolling_resistance_coefficient * mass * g
        air_resistance_force = 0.5 * air_density * (v ** 2) * air_resistance_coefficient * reference_area
        net_force = v ** 2 * friction_coefficient - rolling_resistance_force - air_resistance_force

        x[i] = x[i-1] + v * np.cos(np.arctan2(y[i] - y[i-1], x[i] - x[i-1])) * dt
        y[i] = y[i-1] + v * np.sin(np.arctan2(y[i] - y[i-1], x[i] - x[i-1])) * dt
        speeds[i] += (net_force / mass) * dt

        accelerations[i] = (v - speeds[i-1]) / dt

        # Simulate tire wear
        tire_wear[i] = (tire_wear[i-1] - 0.001 * v + 0.0001 * accelerations[i])

        # Update the total distance covered
        total_distance += np.sqrt((x[i] - x[i-1])**2 + (y[i] - y[i-1])**2)

    return tire_wear, lap_count, accelerations

# Simulate the race and get tire wear, pit stop markers, and accelerations
tire_wear, lap_count, accelerations = simulate_race(x, y, speeds, dt)

x = np.array(telemetry['X'].values)
y = np.array(telemetry['Y'].values)

# Plot the speeds on the circuit layout
plt.figure(figsize=(8, 8))

# Plot speeds
plt.subplot(2, 1, 1)
plt.plot(x, y, label='Circuit Layout', color='black', linewidth=2)
plt.scatter(x, y, c=speeds, cmap='viridis', label='Speed', s=100, edgecolors='w', linewidth=0.5)
plt.colorbar(label='Speed (m/s)')
plt.scatter(x[0], y[0], color='green', marker='o', s=200, label='Start Point')  # Mark the starting point
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.title(f'Car Speeds on {circuit} Circuit Layout')
plt.legend()

# 100 is the limit iteration to avoid overflow
laps_for_90_percent_wear = 100
wear_threshold = -90

while tire_wear[-1] >= wear_threshold and lap_count <= laps_for_90_percent_wear:
    # Plot tire wear
    plt.subplot(2, 1, 2)
    plt.plot(x, y, label='Circuit Layout', color='black', linewidth=2)
    plt.scatter(x, y, c=tire_wear, cmap='Reds_r', label='Tire Wear', s=100, edgecolors='w', linewidth=0.5)
    cbar = plt.colorbar(label='Tire Wear')
    cbar.ax.invert_yaxis()

    plt.scatter(x[0], y[0], color='black', marker='o', s=200, label='Start Point')  # Mark the starting point
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title(f'Tire Wear on {circuit} Circuit Layout on Lap {lap_count}')
    plt.legend()

    # Find the index where tire_wear is closest to -90
    index_tire_wear_closest_to_negative_90 = np.argmin(np.abs(tire_wear + 90))

    # Graphh
    plt.subplot(2, 1, 2)
    plt.plot(x, y, label='Circuit Layout', color='black', linewidth=2)

    # Limit the data up to the point where tire_wear is closest to -90
    plt.scatter(x[:index_tire_wear_closest_to_negative_90], y[:index_tire_wear_closest_to_negative_90],
                c=tire_wear[:index_tire_wear_closest_to_negative_90], cmap='Reds_r', label='Tire Wear', s=100, edgecolors='w', linewidth=0.5)

    cbar = plt.colorbar(label='Tire Wear %')
    cbar.ax.invert_yaxis()

    plt.scatter(x[0], y[0], color='black', marker='o', s=200, label='Start Point')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title(f'Tire Wear on {circuit} Circuit Layout on Lap {lap_count}')
    plt.legend()

    plt.tight_layout()
    plt.show()

    # Update tire wear based on the distance covered during the current lap
    distance_covered_in_lap = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2)
    tire_wear += -distance_covered_in_lap * 0.08  # Adjust as needed

    lap_count += 1

# Plot tire wear
plt.subplot(2, 1, 2)
plt.plot(x, y, label='Circuit Layout', color='black', linewidth=2)
plt.scatter(x, y, c=tire_wear, cmap='Reds_r', label='Tire Wear', s=100, edgecolors='w', linewidth=0.5)
cbar = plt.colorbar(label='Tire Wear')
cbar.ax.invert_yaxis()

plt.scatter(x[0], y[0], color='black', marker='o', s=200, label='Start Point')
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.title(f'Tire Wear on {circuit} Circuit Layout on Lap {lap_count}')
plt.legend()

# Find the index where tire_wear is closest to -90
index_tire_wear_closest_to_negative_90 = np.argmin(np.abs(tire_wear + 90))

plt.subplot(2, 1, 2)
plt.plot(x, y, label='Circuit Layout', color='black', linewidth=2)

# Limit the data up to the point where tire_wear is closest to -90
plt.scatter(x[:index_tire_wear_closest_to_negative_90], y[:index_tire_wear_closest_to_negative_90],
            c=tire_wear[:index_tire_wear_closest_to_negative_90], cmap='Reds_r', label='Tire Wear', s=100, edgecolors='w', linewidth=0.5)

cbar = plt.colorbar(label='Tire Wear %')
cbar.ax.invert_yaxis()

# Mark the point where tire_wear is closest to -90
plt.scatter(x[index_tire_wear_closest_to_negative_90], y[index_tire_wear_closest_to_negative_90],
            color='deeppink', marker='*', s=300, label='Tire Wear at 90%')

plt.scatter(x[0], y[0], color='black', marker='o', s=200, label='Start Point')
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.title(f'Tire Wear on {circuit} Circuit Layout on Lap {lap_count}')
plt.legend()

plt.tight_layout()
plt.show()

# HERE WE CALCULATE THE ERROR WITH RICHARDOS EXTRAPOLATION!!!

# Function to calculate tire wear for a given time step
def simulate_race_tire_wear(x, y, speeds, dt):
    num_steps = len(x)
    tire_wear = np.zeros(num_steps)
    lap_count = 1
    total_distance = 0.0

    for i in range(1, num_steps):
        v = speeds[i]
        rolling_resistance_force = rolling_resistance_coefficient * mass * g
        air_resistance_force = 0.5 * air_density * (v ** 2) * air_resistance_coefficient * reference_area
        net_force = v ** 2 * friction_coefficient - rolling_resistance_force - air_resistance_force

        x[i] = x[i-1] + v * np.cos(np.arctan2(y[i] - y[i-1], x[i] - x[i-1])) * dt
        y[i] = y[i-1] + v * np.sin(np.arctan2(y[i] - y[i-1], x[i] - x[i-1])) * dt
        speeds[i] += (net_force / mass) * dt

        tire_wear[i] = (tire_wear[i-1] - 0.001 * v + 0.0001 * speeds[i] * dt)

        total_distance += np.sqrt((x[i] - x[i-1])**2 + (y[i] - y[i-1])**2)

    return tire_wear[-1], total_distance

# Choose two different time steps
dt1 = 0.01
dt2 = 0.005

# Simulate the race using Euler's method with different time steps
tire_wear_euler_dt1, distance_dt1 = simulate_race_tire_wear(x.copy(), y.copy(), speeds.copy(), dt1)
tire_wear_euler_dt2, distance_dt2 = simulate_race_tire_wear(x.copy(), y.copy(), speeds.copy(), dt2)

# Estimate the error using Richardson extrapolation
estimated_tire_wear = (4 * tire_wear_euler_dt2 - tire_wear_euler_dt1) / 3
percentage_error = np.abs(estimated_tire_wear - tire_wear_euler_dt1) / np.abs(estimated_tire_wear) * 100

print(f'Tire wear with dt={dt1}: {tire_wear_euler_dt1}')
print(f'Tire wear with dt={dt2}: {tire_wear_euler_dt2}')
print(f'Estimated tire wear: {estimated_tire_wear}')
print(f'Percentage Error: {percentage_error}%')
