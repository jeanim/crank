# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/repo/mgear_dist/crank/crank/crankUI.ui'
#
# Created: Wed Jul 25 18:25:23 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(252, 396)
        self.gridLayout_4 = QtWidgets.QGridLayout(Form)
        self.gridLayout_4.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.search_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_lineEdit.setSizePolicy(sizePolicy)
        self.search_lineEdit.setObjectName("search_lineEdit")
        self.gridLayout_2.addWidget(self.search_lineEdit, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.createLayer_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.createLayer_pushButton.setMinimumSize(QtCore.QSize(150, 0))
        self.createLayer_pushButton.setObjectName("createLayer_pushButton")
        self.horizontalLayout.addWidget(self.createLayer_pushButton)
        self.refresh_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.refresh_pushButton.setMinimumSize(QtCore.QSize(70, 0))
        self.refresh_pushButton.setObjectName("refresh_pushButton")
        self.horizontalLayout.addWidget(self.refresh_pushButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.layers_listView = QtWidgets.QListView(self.groupBox)
        self.layers_listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.layers_listView.setProperty("showDropIndicator", False)
        self.layers_listView.setAlternatingRowColors(True)
        self.layers_listView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.layers_listView.setObjectName("layers_listView")
        self.gridLayout_2.addWidget(self.layers_listView, 2, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.postHold_spinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.postHold_spinBox.setObjectName("postHold_spinBox")
        self.gridLayout.addWidget(self.postHold_spinBox, 2, 2, 1, 1)
        self.preHold_spinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.preHold_spinBox.setObjectName("preHold_spinBox")
        self.gridLayout.addWidget(self.preHold_spinBox, 2, 1, 1, 1)
        self.easeOut_spinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.easeOut_spinBox.setMinimum(0)
        self.easeOut_spinBox.setProperty("value", 1)
        self.easeOut_spinBox.setObjectName("easeOut_spinBox")
        self.gridLayout.addWidget(self.easeOut_spinBox, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.easeIn_spinBox = QtWidgets.QSpinBox(self.groupBox_2)
        self.easeIn_spinBox.setMinimum(0)
        self.easeIn_spinBox.setProperty("value", 1)
        self.easeIn_spinBox.setObjectName("easeIn_spinBox")
        self.gridLayout.addWidget(self.easeIn_spinBox, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.addFrame_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.addFrame_pushButton.setMinimumSize(QtCore.QSize(0, 45))
        self.addFrame_pushButton.setObjectName("addFrame_pushButton")
        self.verticalLayout.addWidget(self.addFrame_pushButton)
        self.line_2 = QtWidgets.QFrame(self.groupBox_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.editFrame_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.editFrame_pushButton.setObjectName("editFrame_pushButton")
        self.verticalLayout.addWidget(self.editFrame_pushButton)
        self.line = QtWidgets.QFrame(self.groupBox_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.gridLayout_3.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.keyframe_checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.keyframe_checkBox.setChecked(True)
        self.keyframe_checkBox.setObjectName("keyframe_checkBox")
        self.gridLayout_3.addWidget(self.keyframe_checkBox, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Form", "Sculpt Layers", None, -1))
        self.createLayer_pushButton.setText(QtWidgets.QApplication.translate("Form", "Create Layer", None, -1))
        self.refresh_pushButton.setText(QtWidgets.QApplication.translate("Form", "Refresh", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("Form", "Sculpt Frames", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "Post Hold", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Ease In", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "Ease Out", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "Pre Hold", None, -1))
        self.addFrame_pushButton.setText(QtWidgets.QApplication.translate("Form", "Add Sculpt Frame", None, -1))
        self.editFrame_pushButton.setText(QtWidgets.QApplication.translate("Form", "Edit Selected Sculpt Frame", None, -1))
        self.keyframe_checkBox.setText(QtWidgets.QApplication.translate("Form", "Auto Keyframe", None, -1))

