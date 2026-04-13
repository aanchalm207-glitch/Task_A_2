#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped


class NavClient(Node):

    def __init__(self):
        super().__init__('nav_client')

        # Create action client connected to Nav2's NavigateToPose server
        self._client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

    def send_goal(self, x, y):
        # Wait until Nav2 action server is up
        self.get_logger().info('Waiting for Nav2 action server...')
        self._client.wait_for_server()

        # Build the goal message
        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()

        # Target position (x, y) on the map
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        goal.pose.pose.position.z = 0.0

        # Facing forward (no rotation)
        goal.pose.pose.orientation.x = 0.0
        goal.pose.pose.orientation.y = 0.0
        goal.pose.pose.orientation.z = 0.0
        goal.pose.pose.orientation.w = 1.0

        self.get_logger().info(f'Sending goal → x={x}, y={y}')

        # Send goal and attach callbacks
        self._send_goal_future = self._client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Goal was REJECTED by Nav2!')
            rclpy.shutdown()
            return

        self.get_logger().info('Goal ACCEPTED — rover is navigating...')

        # Wait for final result
        self._result_future = goal_handle.get_result_async()
        self._result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        # Print current rover position while navigating
        pos = feedback_msg.feedback.current_pose.pose.position
        self.get_logger().info(
            f'Current position → x={pos.x:.2f}, y={pos.y:.2f}'
        )

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Goal REACHED — navigation complete!')
        rclpy.shutdown()


def main():
    rclpy.init()
    node = NavClient()

    # Wait for Nav2 to fully initialize before sending goal
    node.get_logger().info('Waiting 5 seconds for Nav2 to fully initialize...')
    import time
    time.sleep(5.0)

    # Send goal to x=3.0, y=2.0 on the map
    node.send_goal(x=3.0, y=2.0)

    rclpy.spin(node)


if __name__ == '__main__':
    main()
