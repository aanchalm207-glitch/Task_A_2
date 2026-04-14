Pre-requisites:
First, if we can reach max velocity in the target distance:
dist reqd to reach max velocity = ((max velocity)^2 - 0)/2 x max acc
this distance is equal to distance required to deaccelerate 
so if 2 x dist reqd < target distance then only trapezoid is possible 

Second, position of deacceleration:
target - distance reqd

Third, till which position to accelerate:
0 + distance reqd

If target =< 2 x reqd distance we will accelerate till target/2 then start deaccelerating after it so our velocity will not be max velocity ever but will reach a peak that is
peak velocity = sq root(2 x target/2 x max acc)

Track: 

Current position: 
Starts at 0 so after each millisecond the position will be 
new position = current position(previous call) + current velocity x 0.001

Update current position by new position

Current velocity: 
if the current position (calculated in previous call)<position till which we have to accelerate:
new velocity = max acc x 0.001 + current velocity (previous call)
updating: current velocity = min(new velocity, max velocity)
if the current position > position after which we have to deaccelerate:
new velocity = current velocity - max acc x 0.001
updating: current velocity = max(new velocity, 0)
else 
new velocity = max velocity

ACCEL: phase 0 for max acceleration
CRUISE: phase 1 for zero acceleration
DECEL: phase 2 for deacceleration
phase 3 for constant

Stop if current position >= target
There are two-three edge cases that have been also considered to prevent overshoot.

How to build and run it:
1. REQUIREMENTS
   - C++ compiler with C++11 support (e.g., g++, clang++)

2. COMPILATION
   Open a terminal in the folder containing trapezoidal_motion.cpp and run:

   g++ -o motion_profiler trapezoidal_motion.cpp -std=c++11

3. EXECUTION
   Run the program and save the output to a text file:

   ./motion_profiler > positions.txt

   (On Windows, use: motion_profiler.exe > positions.txt)

4. OUTPUT
   - The file positions.txt will contain one floating-point number per line.
   - Each number is the joint position (in the same units as your target) at
     that millisecond.
   - The program runs for a fixed number of iterations (e.g., 5000) so the
     motion completes and the output ends with repeated target values.

5. VERIFYING THE TRAPEZOIDAL SHAPE (Plotting)
   You can plot the output using Python, Excel, or any graphing tool.

   Example Python script (save as plot.py):
   import matplotlib.pyplot as plt
   import numpy as np
   positions = np.loadtxt('positions.txt')
   plt.plot(positions)
   plt.xlabel('Time (ms)')
   plt.ylabel('Position')
   plt.title('Trapezoidal Motion Profile')
   plt.show()
   Run: python plot.py

   The position curve should be S-shaped. If you compute the difference
   between consecutive positions (velocity), it should look like a trapezoid
   (or triangle for short moves).

6. PARAMETERS (modify in main() if needed)
   - target = 5.0       (final position, e.g., radians)
   - max_vel = 2.0      (maximum velocity, units/s)
   - max_accel = 4.0    (maximum acceleration, units/s²)

   The code automatically switches to a triangular profile if the target
   is too short to reach max_vel.
