# video_publisher.py

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class VideoPublisher(Node):
    vf = "/mgtu_ws/test.mp4"
    wf = "/mgtu_ws/test.mp4"

    def __init__(self):
        super().__init__("video_publisher")
        self.publisher_ = self.create_publisher(Image, "/camera/rgb/image_raw", 10)
        self.cap = cv2.VideoCapture(self.vf)
        self.bridge = CvBridge()
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            # Публикация кадра в сообщении ROS 2
            msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            self.publisher_.publish(msg)
            self.get_logger().info("Publishing video frame")
        else:
            self.get_logger().info("End of video")
            self.cap = cv2.VideoCapture(self.vf)

def main(args=None):
    rclpy.init(args=args)
    video_publisher = VideoPublisher()
    rclpy.spin(video_publisher)
    video_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()