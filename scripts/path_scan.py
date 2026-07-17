import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time


class PathScanner(Node):
    def __init__(self):
        super().__init__('path_scanner')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def send_cmd(self, linear_x, angular_z, duration):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z

        start = time.time()
        while time.time() - start < duration:
            self.pub.publish(msg)
            time.sleep(0.1)

        self.stop()

    def stop(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.pub.publish(msg)
        time.sleep(1.0)


def main():
    rclpy.init()
    node = PathScanner()

    # Simple tunnel scan path
    node.send_cmd(0.25, 0.0, 10.0)   # move forward 10 sec
    node.send_cmd(0.0, 0.4, 4.0)     # turn left 4 sec
    node.send_cmd(0.25, 0.0, 8.0)    # move forward 8 sec
    node.send_cmd(0.0, -0.4, 4.0)    # turn right 4 sec
    node.send_cmd(0.25, 0.0, 10.0)   # move forward 10 sec
    node.stop()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
