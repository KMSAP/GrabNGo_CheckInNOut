import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate,Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication,QMainWindow
import cv2
import numpy as np
import os
import numpy as np
from Face_Recognition import pre_trained_facenet
import cv2
from mtcnn.mtcnn import MTCNN
import xlrd
import tensorflow.compat.v1 as tf
import time

# Load a single image and display
frame = cv2.imread('/home/bit/PycharmProjects/GrabNGOCheckIn&Out/Webcam-based-Face-Recognition-using-Deep-Learning-/Face_Recognition/images/3.jpg')
detector = MTCNN()

sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))
pre_trained_facenet.load_model('/home/bit/PycharmProjects/GrabNGOCheckIn&Out/model/20170512-110547.pb')
images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
embedding_size = embeddings.get_shape()[1]

# Detect face
faces_detected = 0
start = time.time()
result = detector.detect_faces(frame)
print(result)
faces_detected += len(result)
print(
    f'Frames per second: {(time.time() - start)},',
    f'faces detected: {faces_detected}\r'
)
bounding_box = result[0]['box']
keypoints = result[0]['keypoints']
image = cv2.rectangle(frame,
              (bounding_box[0], bounding_box[1]),
              (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
              (0, 155, 255),
              2)
cv2.circle(frame, (keypoints['left_eye']), 2, (0, 155, 255), 2)
cv2.circle(frame, (keypoints['right_eye']), 2, (0, 155, 255), 2)
cv2.circle(frame, (keypoints['nose']), 2, (0, 155, 255), 2)
cv2.circle(frame, (keypoints['mouth_left']), 2, (0, 155, 255), 2)
cv2.circle(frame, (keypoints['mouth_right']), 2, (0, 155, 255), 2)
cropped = frame[bounding_box[1]:bounding_box[1] + bounding_box[3],
          bounding_box[0]:bounding_box[0] + bounding_box[2]]
# print(cropped)
print(cropped)
print(cropped.shape)
print(type(cropped))
# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow('image',image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# Visualize
# fig, axes = plt.subplots(1, len(faces))
# for face, ax in zip(faces, axes):
#     ax.imshow(face.permute(1, 2, 0).int().numpy())
#     ax.axis('off')
# fig.show()