# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_browser_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dlg_AssetCreation(object):
    def setupUi(self, Dlg_AssetCreation):
        if not Dlg_AssetCreation.objectName():
            Dlg_AssetCreation.setObjectName(u"Dlg_AssetCreation")
        Dlg_AssetCreation.resize(1020, 486)
        self.layoutWidget = QWidget(Dlg_AssetCreation)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(46, 0, 901, 451))
        self.lyt_main = QHBoxLayout(self.layoutWidget)
        self.lyt_main.setObjectName(u"lyt_main")
        self.lyt_main.setContentsMargins(0, 0, 0, 0)
        self.lyt_left = QVBoxLayout()
        self.lyt_left.setObjectName(u"lyt_left")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.bnt_search = QPushButton(self.layoutWidget)
        self.bnt_search.setObjectName(u"bnt_search")

        self.horizontalLayout_3.addWidget(self.bnt_search)


        self.lyt_left.addLayout(self.horizontalLayout_3)

        self.lst_description = QListWidget(self.layoutWidget)
        self.lst_description.setObjectName(u"lst_description")

        self.lyt_left.addWidget(self.lst_description)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lbl_addTo = QLabel(self.layoutWidget)
        self.lbl_addTo.setObjectName(u"lbl_addTo")
        self.lbl_addTo.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.lbl_addTo)

        self.cmb_addTo = QComboBox(self.layoutWidget)
        self.cmb_addTo.addItem("")
        self.cmb_addTo.addItem("")
        self.cmb_addTo.setObjectName(u"cmb_addTo")

        self.horizontalLayout.addWidget(self.cmb_addTo)


        self.lyt_left.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lbl_project = QLabel(self.layoutWidget)
        self.lbl_project.setObjectName(u"lbl_project")
        self.lbl_project.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.lbl_project)

        self.cmb_project = QComboBox(self.layoutWidget)
        self.cmb_project.addItem("")
        self.cmb_project.addItem("")
        self.cmb_project.addItem("")
        self.cmb_project.setObjectName(u"cmb_project")

        self.horizontalLayout_2.addWidget(self.cmb_project)


        self.lyt_left.addLayout(self.horizontalLayout_2)

        self.btn_addAsset = QPushButton(self.layoutWidget)
        self.btn_addAsset.setObjectName(u"btn_addAsset")

        self.lyt_left.addWidget(self.btn_addAsset)

        self.btn_removeAsset = QPushButton(self.layoutWidget)
        self.btn_removeAsset.setObjectName(u"btn_removeAsset")

        self.lyt_left.addWidget(self.btn_removeAsset)

        self.btn_editAsset = QPushButton(self.layoutWidget)
        self.btn_editAsset.setObjectName(u"btn_editAsset")

        self.lyt_left.addWidget(self.btn_editAsset)


        self.lyt_main.addLayout(self.lyt_left)

        self.tbl_assets = QTableWidget(self.layoutWidget)
        if (self.tbl_assets.columnCount() < 5):
            self.tbl_assets.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignTrailing|Qt.AlignVCenter);
        self.tbl_assets.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_assets.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_assets.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_assets.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tbl_assets.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tbl_assets.setObjectName(u"tbl_assets")

        self.lyt_main.addWidget(self.tbl_assets)


        self.retranslateUi(Dlg_AssetCreation)

        QMetaObject.connectSlotsByName(Dlg_AssetCreation)
    # setupUi

    def retranslateUi(self, Dlg_AssetCreation):
        Dlg_AssetCreation.setWindowTitle(QCoreApplication.translate("Dlg_AssetCreation", u"Asset Creation", None))
        self.label.setText(QCoreApplication.translate("Dlg_AssetCreation", u"Search Folder", None))
        self.bnt_search.setText(QCoreApplication.translate("Dlg_AssetCreation", u"...", None))
        self.lbl_addTo.setText(QCoreApplication.translate("Dlg_AssetCreation", u"Add To:", None))
        self.cmb_addTo.setItemText(0, QCoreApplication.translate("Dlg_AssetCreation", u"Global", None))
        self.cmb_addTo.setItemText(1, QCoreApplication.translate("Dlg_AssetCreation", u"Project", None))

        self.lbl_project.setText(QCoreApplication.translate("Dlg_AssetCreation", u"Project name", None))
        self.cmb_project.setItemText(0, QCoreApplication.translate("Dlg_AssetCreation", u"Project 1", None))
        self.cmb_project.setItemText(1, QCoreApplication.translate("Dlg_AssetCreation", u"Project 2", None))
        self.cmb_project.setItemText(2, QCoreApplication.translate("Dlg_AssetCreation", u"Project 3", None))

        self.btn_addAsset.setText(QCoreApplication.translate("Dlg_AssetCreation", u"Create Asset", None))
        self.btn_removeAsset.setText(QCoreApplication.translate("Dlg_AssetCreation", u"Remove Asset", None))
        self.btn_editAsset.setText(QCoreApplication.translate("Dlg_AssetCreation", u"Edit Asset Info", None))
        ___qtablewidgetitem = self.tbl_assets.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dlg_AssetCreation", u"ID", None));
        ___qtablewidgetitem1 = self.tbl_assets.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dlg_AssetCreation", u"Name", None));
        ___qtablewidgetitem2 = self.tbl_assets.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dlg_AssetCreation", u"Project", None));
        ___qtablewidgetitem3 = self.tbl_assets.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dlg_AssetCreation", u"Type", None));
        ___qtablewidgetitem4 = self.tbl_assets.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dlg_AssetCreation", u"Description", None));
    # retranslateUi

