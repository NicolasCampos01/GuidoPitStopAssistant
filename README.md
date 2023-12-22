# GuidoPitStopAssistant
 Euler and Leapfrog Method Simulation for Tire Wear on a F1 Racing Circuit
#Introduction
This code simulates tire wear during a race on a given racing circuit using Euler's method and Leapfrog. The simulation is based on the telemetry data obtained from a FastF1 session for the 2021 season. The primary goal is to analyze the tire wear at different points on the circuit and estimate the error in the simulation using Richardson extrapolation.

#Dependencies
fastf1: This library is used for extracting lap telemetry data from the FastF1 database.
numpy: A powerful library for numerical operations in Python.
matplotlib.pyplot: A library for creating visualizations in Python.
#Input
The user is prompted to enter the name of the racing circuit.
Telemetry Data Extraction
The FastF1 library is used to extract telemetry data for the quickest lap during a qualifying session for the specified circuit in the 2021 season.
The lap telemetry includes speed, position (X, Y), and time data.
#Physical Constants and Parameters
Mass of the car: 900 kg
Gravitational acceleration: 9.81 m/s^2
Reference area: 2.0 m^2
Air density: 1.225 kg/m^3
Rolling resistance coefficient: 0.01
Friction coefficient: 0.9
Air resistance coefficient: 0.7
#Simulation
Resistive forces (rolling resistance and air resistance) are calculated based on the current speed.
The simulation uses Euler's method to update the car's position and speed over time.
Tire wear is simulated, considering work done against resistive forces.
Accumulative wear is calculated throughout the race.
#Visualization
The car speeds are plotted on the circuit layout, with the color indicating speed.
Tire wear is visualized on the circuit layout for each lap, highlighting wear at 90% completion.
The final visualization includes the point where tire wear is closest to -90% and the optimal pit stop markers.
#Richardson Extrapolation
Two different time steps (dt1 and dt2) are chosen for the Euler simulation.
Richardson extrapolation is used to estimate tire wear with a smaller time step (dt2) and compare it with the result from a larger time step (dt1).
The percentage error is calculated to assess the accuracy of the simulation.
#Output
The estimated tire wear, actual tire wear for different time steps, and the percentage error are printed at the end of the simulation.
