import sys
from db_connection import DB_Connection
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt, QSize
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication, QMainWindow, QTableWidget, QAbstractItemView, \
    QTableWidgetItem, QHeaderView, QLabel
import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime
import time
import cx_Oracle
import os
import csv

class Check_Out_Window(QMainWindow):

    def __init__(self):
        super(Check_Out_Window, self).__init__()
        loadUi("Check_Out_Window.ui", self)
        self.startVideo('0')

    # def refreshAll(self):
    #     """
    #     Set the text of lineEdit once it's valid
    #     """
    #     self.Videocapture_ = "0"

    @pyqtSlot()
    def startVideo(self, camera_name):
        """
        :param camera_name: link of camera or usb camera
        :return:
        """
        if len(camera_name) == 1:
        	self.capture = cv2.VideoCapture(int(camera_name))
        else:
        	self.capture = cv2.VideoCapture(camera_name)
        self.timer = QTimer(self)  # Create Timer
        path = 'Images'
        if not os.path.exists(path):
            os.mkdir(path)
        # known face encoding and known face name list
        images = []
        self.class_names = []
        self.encode_list = []

        attendance_list = os.listdir(path)
        #print(attendance_list)
        for cl in attendance_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            #print(cur_img)
            images.append(cur_img)
            self.class_names.append(os.path.splitext(cl)[0])
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
            # encode = face_recognition.face_encodings(img)[0]
            self.encode_list.append(encodes_cur_frame)
            #print(self.encode_list)
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=10ms

    def face_rec_(self, frame, encode_list_known, class_names):
        """
        :param frame: frame from camera
        :param encode_list_known: known face encoding
        :param class_names: known face names
        :return:
        """
        # face recognition
        faces_cur_frame = face_recognition.face_locations(frame)
        encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        # count = 0
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            name = "unknown"
            best_match_index = np.argmin(face_dis)
            # print("s",best_match_index)
            if match[best_match_index]:
                name = class_names[best_match_index].upper()
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            self.mark_attendance(name)
        return frame

    def mark_attendance(self, name):
        """
        :param name: detected face known or unknown one
        :return:
        """
        if name != 'unknonw':
            print(name)
            self.logOut(name)

    def update_frame(self):
        ret, self.image = self.capture.read()
        # print('image: ',type(self.image))
        self.displayImage(self.image, self.encode_list, self.class_names, 1)

    def displayImage(self, image, encode_list, class_names, window=1):
        """
        :param image: frame from camera
        :param encode_list: known face encoding list
        :param class_names: known face names
        :param window: number of window
        :return:
        """
        image = cv2.resize(image, (640, 480))
        # print('image1: ', type(self.image))
        try:
            image = self.face_rec_(image, encode_list, class_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)

    def logOut(self, name):
        customer_id = int(name)
        DB = DB_Connection()
        cnt = DB.select_user(customer_id)

        if cnt[0] == "True":
            greeting = cnt[1] + '님이 퇴장 하셨습니다.'
            print(name, '님이 퇴장 하셨습니다.')
            DB.update_login_session_F(customer_id)
            df = DB.select_cart_product(customer_id)
            print('df:  ',len(df))
            if len(df) > 0:
                df1 = df.drop([0, 1, 2], axis=1)
                df1.columns = ['상품명', '단가', '수량']
                df1['금액'] = df1['단가'] * df1['수량']
                total_price = int(df1['금액'].sum())
                order_date = time.strftime("%m/%d/%Y, %H:%M:%S")
                order_date_str = '주문일시: ' + str(order_date)
                print(order_date)
                print(df1)
                # print(total_price)
                total_price_str = '합  계: ' + str(total_price) + '원'
                print(total_price_str)

                self.OrderDateLabel.setText(order_date_str)
                df1 = df1.astype(str)
                self.setupTable(df1)
                self.TotalPriceLabel.setText(total_price_str)
                DB.insert_order(customer_id, total_price)
                DB.insert_order_detail(df)
                DB.delete_cart(customer_id)
                self.GoodbyeLabel.setText('오늘도 GrabNGo를 이용해주셔서 감사합니다.')
            else:
                self.GoodbyeLabel.setText('구매하신 물품이 없습니다. 안녕히 돌아가세요.')
            self.GreetingLabel.setText(greeting)
            self.setUserImage(name)

            self.timer1 = QTimer(self)
            self.timer1.start(20000)

            self.timer1.timeout.connect(self.clearLabel)

    def setupTable(self, df1):
        self.tableWidget1.setRowCount(df1.shape[0])
        # print(df1.shape[1])
        self.tableWidget1.setColumnCount(df1.shape[1])
        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setTableWidgetData(df1)

    def setTableWidgetData(self, df1):
        self.tableWidget1.setHorizontalHeaderLabels(df1.columns)
        for col_i, (col_name, col_item) in enumerate(df1.iteritems()):
            for row_i in range(col_item.size):
                item = QTableWidgetItem(col_item[row_i])
                if col_i > 0:
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.tableWidget1.setItem(row_i, col_i, item)

        self.tableWidget1.resizeColumnsToContents()
        self.tableWidget1.resizeRowsToContents()
        # Table will fit the screen horizontally
        self.tableWidget1.horizontalHeader().setStretchLastSection(True)
        self.tableWidget1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget1.resize(self.tableWidget1)

    def setUserImage(self, name):
        imagePath = 'Images/' + name + '.jpg'
        print(imagePath)
        pixmap = QPixmap(imagePath)
        pixmap1 = pixmap.scaled(150, 150)
        self.ImageLabel.setPixmap(pixmap1)
        self.ImageLabel.resize(150, 150)

    def clearLabel(self):
        self.GreetingLabel.clear()
        self.OrderDateLabel.clear()
        self.ImageLabel.clear()
        self.tableWidget1.clear()
        self.TotalPriceLabel.clear()
        self.GoodbyeLabel.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Check_Out_Window()
    ui.show()
    sys.exit(app.exec_())