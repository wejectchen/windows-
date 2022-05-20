# -*- coding: utf-8 -*-

import datetime
import json
import os
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

time = 60
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
endTime = (datetime.datetime.now() + datetime.timedelta(seconds=time)).strftime("%Y-%m-%d %H:%M:%S")
data = {
    'startTime': now,
    'endTime': endTime,
    'cmd': ''
}

message = {
    200: '计划成功',
    201: '你已取消操作',
    300: '你已设置了关机计划',
    301: f'设置计划关机成功，你的计算机将于{endTime}关机',
    400: '尚无正在运行的计划，无法取消'
}


def readLog():
    with open('./data.json', 'r') as log:
        return json.load(log)


def writeLog(_data):
    with open('./data.json', 'w') as log:
        json.dump(_data, log)
        log.close()


def action_shutdown(_time):
    res = os.popen(f'shutdown -s -t {_time}')
    if len(res.read()) != 0:
        return 300
    data['startTime'] = now
    data['endTime'] = (datetime.datetime.now() + datetime.timedelta(seconds=_time)).strftime("%Y-%m-%d %H:%M:%S")
    data['cmd'] = f'shutdown -s -t {_time}'
    writeLog(data)
    return 301


def action_cancel():
    if readLog()['cmd'] == '':
        return 400
    os.popen('shutdown -a')
    data['startTime'] = ''
    data['endTime'] = ''
    data['cmd'] = ''
    writeLog(data)
    return 201


class Ui_MainWindow(object):
    def __init__(self):
        self.input_config = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(380, 160)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 确认按钮
        self.comfirm_btn = QtWidgets.QPushButton(self.centralwidget)
        self.comfirm_btn.setGeometry(QtCore.QRect(270, 50, 75, 23))
        self.comfirm_btn.setCheckable(False)
        self.comfirm_btn.setObjectName("comfirm_btn")
        self.comfirm_btn.clicked.connect(lambda: self.action())

        # 取消按钮
        self.cancel_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_btn.setGeometry(QtCore.QRect(270, 80, 75, 23))
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(lambda: self.cancel())

        # 输入框
        self.input_config = QtWidgets.QWidget(self.centralwidget)
        self.input_config.setGeometry(QtCore.QRect(20, 20, 231, 91))
        self.input_config.setObjectName("input_config")
        self.label_shutdown = QtWidgets.QLabel(self.input_config)
        self.label_shutdown.setGeometry(QtCore.QRect(20, 30, 54, 31))
        self.label_shutdown.setObjectName("label_shutdown")
        self.shutdown_time = QtWidgets.QSpinBox(self.input_config)
        self.shutdown_time.setGeometry(QtCore.QRect(80, 30, 91, 31))
        self.shutdown_time.setMaximum(99999999)
        self.shutdown_time.setObjectName("shutdown_time")
        self.shutdown_time.setValue(30)
        self.label_sec = QtWidgets.QLabel(self.input_config)
        self.label_sec.setGeometry(QtCore.QRect(190, 31, 54, 31))
        self.label_sec.setObjectName("label_sec")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def cancel(self):
        res = action_cancel()
        QMessageBox.information(None, '提示', message[res])

    def action(self):
        _time = self.shutdown_time.value() * 60
        res = action_shutdown(_time)
        global endTime, message
        endTime = (datetime.datetime.now() + datetime.timedelta(seconds=_time)).strftime("%Y-%m-%d %H:%M:%S")
        message[301] = f'设置计划关机成功，你的计算机将于{endTime}关机'
        QMessageBox.information(None, '提示', message[res])

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "windows关机定时器"))
        self.comfirm_btn.setText(_translate("MainWindow", "确定"))
        self.cancel_btn.setText(_translate("MainWindow", "取消计划"))
        self.label_shutdown.setText(_translate("MainWindow", "关机时间："))
        self.label_sec.setText(_translate("MainWindow", "分钟"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
