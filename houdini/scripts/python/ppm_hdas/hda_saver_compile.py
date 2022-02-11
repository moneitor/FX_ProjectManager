# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hda_saver.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_HDA_Manager_UI(object):
    def setupUi(self, HDA_Manager_UI):
        if not HDA_Manager_UI.objectName():
            HDA_Manager_UI.setObjectName(u"HDA_Manager_UI")
        HDA_Manager_UI.resize(447, 378)
        self.gridLayout = QGridLayout(HDA_Manager_UI)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label = QLabel(HDA_Manager_UI)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.ln_name = QLineEdit(HDA_Manager_UI)
        self.ln_name.setObjectName(u"ln_name")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ln_name)

        self.label_2 = QLabel(HDA_Manager_UI)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.spn_version = QSpinBox(HDA_Manager_UI)
        self.spn_version.setObjectName(u"spn_version")
        self.spn_version.setMinimum(1)
        self.spn_version.setValue(1)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.spn_version)

        self.label_3 = QLabel(HDA_Manager_UI)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_3)

        self.ln_description = QPlainTextEdit(HDA_Manager_UI)
        self.ln_description.setObjectName(u"ln_description")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.ln_description)

        self.label_4 = QLabel(HDA_Manager_UI)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_4)

        self.lbl_path = QLabel(HDA_Manager_UI)
        self.lbl_path.setObjectName(u"lbl_path")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.lbl_path)

        self.lbl_inputs = QLabel(HDA_Manager_UI)
        self.lbl_inputs.setObjectName(u"lbl_inputs")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lbl_inputs)

        self.spn_inputs = QSpinBox(HDA_Manager_UI)
        self.spn_inputs.setObjectName(u"spn_inputs")
        self.spn_inputs.setMaximum(4)
        self.spn_inputs.setValue(1)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.spn_inputs)

        self.label_5 = QLabel(HDA_Manager_UI)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.cb_global = QComboBox(HDA_Manager_UI)
        self.cb_global.addItem("")
        self.cb_global.addItem("")
        self.cb_global.setObjectName(u"cb_global")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cb_global)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_save = QPushButton(HDA_Manager_UI)
        self.btn_save.setObjectName(u"btn_save")

        self.horizontalLayout_2.addWidget(self.btn_save)

        self.btn_cancel = QPushButton(HDA_Manager_UI)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.horizontalLayout_2.addWidget(self.btn_cancel)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)


        self.retranslateUi(HDA_Manager_UI)

        QMetaObject.connectSlotsByName(HDA_Manager_UI)
    # setupUi

    def retranslateUi(self, HDA_Manager_UI):
        HDA_Manager_UI.setWindowTitle(QCoreApplication.translate("HDA_Manager_UI", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("HDA_Manager_UI", u"HDA name:", None))
        self.label_2.setText(QCoreApplication.translate("HDA_Manager_UI", u"Version:", None))
        self.label_3.setText(QCoreApplication.translate("HDA_Manager_UI", u"Description:", None))
        self.label_4.setText(QCoreApplication.translate("HDA_Manager_UI", u"Path to HDA:", None))
        self.lbl_path.setText(QCoreApplication.translate("HDA_Manager_UI", u"...", None))
        self.lbl_inputs.setText(QCoreApplication.translate("HDA_Manager_UI", u"Number of Inputs:", None))
        self.label_5.setText(QCoreApplication.translate("HDA_Manager_UI", u"Save to:", None))
        self.cb_global.setItemText(0, QCoreApplication.translate("HDA_Manager_UI", u"Globally", None))
        self.cb_global.setItemText(1, QCoreApplication.translate("HDA_Manager_UI", u"Project", None))

        self.btn_save.setText(QCoreApplication.translate("HDA_Manager_UI", u"Save ", None))
        self.btn_cancel.setText(QCoreApplication.translate("HDA_Manager_UI", u"Cancel", None))
    # retranslateUi

