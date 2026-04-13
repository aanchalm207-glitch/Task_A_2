# rover_nav2 — Nav2 Costmap Tuner for URC Rover

## Overview
This package configures a Nav2 stack for a URC rover with a custom
1.0m x 0.8m footprint, ensuring a minimum 0.5m clearance from all
obstacles using the inflation layer.

as there is

## Package Structure
- `config/nav2_params.yaml` — Custom Nav2 parameters
- `launch/nav2_rover.launch.py` — Launch file
- `rover_nav2/nav_client.py` — NavigateToPose action client
- `rover_nav2/fake_scan.py` — Fake laser scan publisher for testing
- `rover_nav2/activate_nav2.py` — Node activation script
- `maps/` — Blank test map

## How to Build
```bash
cd ~/ros2_ws
colcon build --packages-select rover_nav2
source ~/ros2_ws/install/setup.bash
```

## How to Run

### Terminal 1 — Fake Robot:
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_fake_node turtlebot3_fake_node.launch.py
```

### Terminal 2 — Nav2 Stack:
```bash
ros2 launch rover_nav2 nav2_rover.launch.py
```

### Terminal 3 — Activate Nodes:
```bash
python3 ~/ros2_ws/src/rover_nav2/rover_nav2/activate_nav2.py
ros2 lifecycle set /behavior_server configure
ros2 lifecycle set /behavior_server activate
```

### Terminal 4 — Fake Laser Scan:
```bash
python3 ~/ros2_ws/src/rover_nav2/rover_nav2/fake_scan.py
```

### Terminal 3 — Set Initial Pose:
```bash
ros2 topic pub --once /initialpose geometry_msgs/msg/PoseWithCovarianceStamped \
"{header: {frame_id: 'map'}, pose: {pose: {position: {x: 0.0, y: 0.0, z: 0.0}, \
orientation: {w: 1.0}}, covariance: [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, \
0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, \
0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853]}}"
```

### Terminal 3 — Activate planner and Send Goal:
```bash
ros2 lifecycle set /planner_server activate
ros2 run rover_nav2 nav_client
```

## Algorithm & Architecture

### Robot Footprint (1.0m x 0.8m)
The rover footprint is defined as a rectangle with corners: [[0.5, 0.4], [0.5, -0.4], [-0.5, -0.4], [-0.5, 0.4]]
This represents a 1.0m (length) x 0.8m (width) rover.

### inflation_radius vs cost_scaling_factor

**inflation_radius: 0.85m**
Defines the distance from each obstacle out to which costs are
applied in the costmap. Set to 0.85m to guarantee the required
0.5m clearance from the rover footprint edge:
- Robot half-diagonal = √(0.5² + 0.4²) ≈ 0.64m
- Required clearance from obstacle = 0.5m
- inflation_radius = 0.5 + 0.35 (buffer) = 0.85m

**cost_scaling_factor: 3.5**
Controls the exponential decay rate of the cost as distance from
the obstacle increases. Higher value = steeper drop-off = planner
strongly prefers paths far from obstacles.

Formula: cost = 253 × e^(-cost_scaling_factor × (distance - inscribed_radius))

A value of 3.5 creates a steep enough gradient that the planner
avoids getting within 0.5m of obstacles while still finding
efficient paths.

### Action Client
The Python action client sends a NavigateToPose goal to the
bt_navigator action server and prints feedback (current position)
until the goal is reached.
