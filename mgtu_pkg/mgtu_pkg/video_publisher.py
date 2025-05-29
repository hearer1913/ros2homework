#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class VideoPublisher(Node):
    def __init__(self):
        super().__init__("video_publisher")

        # Получаем путь к видео из переменной окружения V_SRC
        self.declare_parameter('file_name', '/mgtu_ws/test.mp4')
        self.vf = self.get_parameter('file_name').value

        
        self.get_logger().info(f'Загрузка видео из: {self.vf}')

        self.publisher_ = self.create_publisher(Image, "/image_raw", 10)
        self.cap = cv2.VideoCapture(self.vf)
        self.bridge = CvBridge()
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            height, width, channels = frame.shape
            msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            msg.height = height
            msg.width = width
            self.publisher_.publish(msg)
        else:
            self.get_logger().info("Конец видео. Перезапуск.")
            self.cap = cv2.VideoCapture(self.vf)

def main(args=None):
    rclpy.init(args=args)
    node = VideoPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()



if __name__ == '__main__':
    main()
