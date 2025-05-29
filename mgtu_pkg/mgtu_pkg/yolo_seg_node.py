#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2
import os
from ultralytics import YOLO

class YoloSegNode(Node):
    def __init__(self):
        super().__init__('yolo_seg_node')

        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(
            Image,
            '/segmentation_image',
            10
        )

        self.bridge = CvBridge()
        self.get_logger().info('Загрузка YOLOv8 сегментационной модели...')
        self.model = YOLO('yolo11s-seg.pt')
        self.get_logger().info('Модель загружена!')

        # Путь для сохранения видео из переменной окружения
        self.declare_parameter('file_name_dst', '/mgtu_ws/v_dst.mp4')
        self.v_dst = self.get_parameter('file_name_dst').value


        self.video_writer = None

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        height, width = cv_image.shape[:2]

        if self.video_writer is None:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(self.v_dst, fourcc, 10.0, (width, height))
            if not self.video_writer.isOpened():
                self.get_logger().error(f'Ошибка записи в файл: {self.v_dst}')
                return

        results = self.model(cv_image)[0]

        if results.masks is not None:
            masks = results.masks.data.cpu().numpy()
            boxes = results.boxes.xyxy.cpu().numpy()
            class_ids = results.boxes.cls.cpu().numpy().astype(int)
            class_names = results.names

            overlay = cv_image.copy()

            for i in range(masks.shape[0]):
                mask_resized = cv2.resize(masks[i], (width, height), interpolation=cv2.INTER_NEAREST)
                mask_uint8 = (mask_resized * 255).astype(np.uint8)
                contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(overlay, contours, -1, (0, 255, 0), 2)

                x1, y1, x2, y2 = boxes[i].astype(int)
                label = class_names[class_ids[i]]
                cv2.putText(overlay, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            result_image = overlay
        else:
            result_image = cv_image

        out_msg = self.bridge.cv2_to_imgmsg(result_image, encoding='bgr8')
        self.publisher.publish(out_msg)

        self.video_writer.write(result_image)

    def destroy_node(self):
        if self.video_writer is not None:
            self.video_writer.release()
            self.get_logger().info(f'Видео сохранено: {self.v_dst}')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = YoloSegNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()




