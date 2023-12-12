# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CSVgenerator(object):
    def setupUi(self, CSVgenerator):
        CSVgenerator.setObjectName("CSVgenerator")
        CSVgenerator.resize(1400, 1000)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(CSVgenerator.sizePolicy().hasHeightForWidth())
        CSVgenerator.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        CSVgenerator.setFont(font)
        CSVgenerator.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(CSVgenerator)
        self.centralwidget.setObjectName("centralwidget")
        self.centralGrid = QtWidgets.QGridLayout(self.centralwidget)
        self.centralGrid.setObjectName("centralGrid")
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.tabs.setFont(font)
        self.tabs.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabs.setObjectName("tabs")
        self.CSV = QtWidgets.QWidget()
        self.CSV.setObjectName("CSV")
        self.csvGrid = QtWidgets.QGridLayout(self.CSV)
        self.csvGrid.setContentsMargins(10, 10, 10, 10)
        self.csvGrid.setSpacing(10)
        self.csvGrid.setObjectName("csvGrid")
        self.ifc_box = QtWidgets.QGroupBox(self.CSV)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.ifc_box.sizePolicy().hasHeightForWidth())
        self.ifc_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ifc_box.setFont(font)
        self.ifc_box.setAutoFillBackground(False)
        self.ifc_box.setTitle("")
        self.ifc_box.setAlignment(QtCore.Qt.AlignCenter)
        self.ifc_box.setFlat(False)
        self.ifc_box.setCheckable(False)
        self.ifc_box.setObjectName("ifc_box")
        self.ifcGrid = QtWidgets.QGridLayout(self.ifc_box)
        self.ifcGrid.setContentsMargins(20, 20, 20, 20)
        self.ifcGrid.setSpacing(20)
        self.ifcGrid.setObjectName("ifcGrid")
        self.vmg_order = QtWidgets.QLineEdit(self.ifc_box)
        self.vmg_order.setObjectName("vmg_order")
        self.ifcGrid.addWidget(self.vmg_order, 8, 1, 1, 2)
        self.csv_label = QtWidgets.QLabel(self.ifc_box)
        self.csv_label.setObjectName("csv_label")
        self.ifcGrid.addWidget(self.csv_label, 1, 0, 1, 1)
        self.bb_label = QtWidgets.QLabel(self.ifc_box)
        self.bb_label.setObjectName("bb_label")
        self.ifcGrid.addWidget(self.bb_label, 7, 0, 1, 1)
        self.prio_button = QtWidgets.QPushButton(self.ifc_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prio_button.sizePolicy().hasHeightForWidth())
        self.prio_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.prio_button.setFont(font)
        self.prio_button.setObjectName("prio_button")
        self.ifcGrid.addWidget(self.prio_button, 3, 2, 1, 1)
        self.ifc_button = QtWidgets.QPushButton(self.ifc_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ifc_button.sizePolicy().hasHeightForWidth())
        self.ifc_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ifc_button.setFont(font)
        self.ifc_button.setObjectName("ifc_button")
        self.ifcGrid.addWidget(self.ifc_button, 0, 2, 1, 1)
        self.ifc_label = QtWidgets.QLabel(self.ifc_box)
        self.ifc_label.setObjectName("ifc_label")
        self.ifcGrid.addWidget(self.ifc_label, 0, 0, 1, 1)
        self.vmg_label = QtWidgets.QLabel(self.ifc_box)
        self.vmg_label.setObjectName("vmg_label")
        self.ifcGrid.addWidget(self.vmg_label, 8, 0, 1, 1)
        self.bb_button = QtWidgets.QPushButton(self.ifc_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bb_button.sizePolicy().hasHeightForWidth())
        self.bb_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.bb_button.setFont(font)
        self.bb_button.setObjectName("bb_button")
        self.ifcGrid.addWidget(self.bb_button, 4, 2, 1, 1)
        self.bb_path = QtWidgets.QLineEdit(self.ifc_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bb_path.sizePolicy().hasHeightForWidth())
        self.bb_path.setSizePolicy(sizePolicy)
        self.bb_path.setReadOnly(True)
        self.bb_path.setObjectName("bb_path")
        self.ifcGrid.addWidget(self.bb_path, 4, 1, 1, 1)
        self.vh_order = QtWidgets.QLineEdit(self.ifc_box)
        self.vh_order.setObjectName("vh_order")
        self.ifcGrid.addWidget(self.vh_order, 6, 1, 1, 2)
        self.bb_order = QtWidgets.QLineEdit(self.ifc_box)
        self.bb_order.setObjectName("bb_order")
        self.ifcGrid.addWidget(self.bb_order, 7, 1, 1, 2)
        self.bb_label_2 = QtWidgets.QLabel(self.ifc_box)
        self.bb_label_2.setObjectName("bb_label_2")
        self.ifcGrid.addWidget(self.bb_label_2, 4, 0, 1, 1)
        self.csv_button = QtWidgets.QPushButton(self.ifc_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.csv_button.sizePolicy().hasHeightForWidth())
        self.csv_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.csv_button.setFont(font)
        self.csv_button.setObjectName("csv_button")
        self.ifcGrid.addWidget(self.csv_button, 1, 2, 1, 1)
        self.csv_path = QtWidgets.QLineEdit(self.ifc_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.csv_path.sizePolicy().hasHeightForWidth())
        self.csv_path.setSizePolicy(sizePolicy)
        self.csv_path.setReadOnly(True)
        self.csv_path.setObjectName("csv_path")
        self.ifcGrid.addWidget(self.csv_path, 1, 1, 1, 1)
        self.nesting_label = QtWidgets.QLabel(self.ifc_box)
        self.nesting_label.setObjectName("nesting_label")
        self.ifcGrid.addWidget(self.nesting_label, 3, 0, 1, 1)
        self.ifc_path = QtWidgets.QLineEdit(self.ifc_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ifc_path.sizePolicy().hasHeightForWidth())
        self.ifc_path.setSizePolicy(sizePolicy)
        self.ifc_path.setReadOnly(True)
        self.ifc_path.setObjectName("ifc_path")
        self.ifcGrid.addWidget(self.ifc_path, 0, 1, 1, 1)
        self.vh_label = QtWidgets.QLabel(self.ifc_box)
        self.vh_label.setObjectName("vh_label")
        self.ifcGrid.addWidget(self.vh_label, 6, 0, 1, 1)
        self.nesting_path = QtWidgets.QLineEdit(self.ifc_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nesting_path.sizePolicy().hasHeightForWidth())
        self.nesting_path.setSizePolicy(sizePolicy)
        self.nesting_path.setReadOnly(True)
        self.nesting_path.setObjectName("nesting_path")
        self.ifcGrid.addWidget(self.nesting_path, 3, 1, 1, 1)
        self.bulk_path = QtWidgets.QLineEdit(self.ifc_box)
        self.bulk_path.setObjectName("bulk_path")
        self.ifcGrid.addWidget(self.bulk_path, 5, 1, 1, 1)
        self.bulk_label = QtWidgets.QLabel(self.ifc_box)
        self.bulk_label.setObjectName("bulk_label")
        self.ifcGrid.addWidget(self.bulk_label, 5, 0, 1, 1)
        self.bulk_button = QtWidgets.QPushButton(self.ifc_box)
        self.bulk_button.setObjectName("bulk_button")
        self.ifcGrid.addWidget(self.bulk_button, 5, 2, 1, 1)
        self.csvGrid.addWidget(self.ifc_box, 0, 0, 1, 1)
        self.status_box = QtWidgets.QGroupBox(self.CSV)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.status_box.sizePolicy().hasHeightForWidth())
        self.status_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.status_box.setFont(font)
        self.status_box.setAlignment(QtCore.Qt.AlignCenter)
        self.status_box.setFlat(False)
        self.status_box.setObjectName("status_box")
        self.statusGrid = QtWidgets.QHBoxLayout(self.status_box)
        self.statusGrid.setContentsMargins(20, 20, 20, 20)
        self.statusGrid.setSpacing(30)
        self.statusGrid.setObjectName("statusGrid")
        self.status_csv = QtWidgets.QTextEdit(self.status_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_csv.sizePolicy().hasHeightForWidth())
        self.status_csv.setSizePolicy(sizePolicy)
        self.status_csv.setReadOnly(True)
        self.status_csv.setObjectName("status_csv")
        self.statusGrid.addWidget(self.status_csv)
        self.lcd = QtWidgets.QLCDNumber(self.status_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.lcd.sizePolicy().hasHeightForWidth())
        self.lcd.setSizePolicy(sizePolicy)
        self.lcd.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lcd.setDigitCount(2)
        self.lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd.setObjectName("lcd")
        self.statusGrid.addWidget(self.lcd)
        self.csvGrid.addWidget(self.status_box, 2, 0, 1, 1)
        self.progressCSV = QtWidgets.QProgressBar(self.CSV)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressCSV.sizePolicy().hasHeightForWidth())
        self.progressCSV.setSizePolicy(sizePolicy)
        self.progressCSV.setProperty("value", 0)
        self.progressCSV.setTextVisible(False)
        self.progressCSV.setInvertedAppearance(False)
        self.progressCSV.setObjectName("progressCSV")
        self.csvGrid.addWidget(self.progressCSV, 1, 0, 1, 1)
        self.generate_box = QtWidgets.QGroupBox(self.CSV)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generate_box.sizePolicy().hasHeightForWidth())
        self.generate_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.generate_box.setFont(font)
        self.generate_box.setAlignment(QtCore.Qt.AlignCenter)
        self.generate_box.setFlat(False)
        self.generate_box.setObjectName("generate_box")
        self.generateGrid = QtWidgets.QVBoxLayout(self.generate_box)
        self.generateGrid.setContentsMargins(30, 30, 30, 30)
        self.generateGrid.setSpacing(30)
        self.generateGrid.setObjectName("generateGrid")
        self.start_button = QtWidgets.QPushButton(self.generate_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")
        self.generateGrid.addWidget(self.start_button)
        self.exit_button = QtWidgets.QPushButton(self.generate_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_button.sizePolicy().hasHeightForWidth())
        self.exit_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.exit_button.setFont(font)
        self.exit_button.setObjectName("exit_button")
        self.generateGrid.addWidget(self.exit_button)
        self.csvGrid.addWidget(self.generate_box, 2, 1, 1, 1)
        self.option_box = QtWidgets.QGroupBox(self.CSV)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.option_box.sizePolicy().hasHeightForWidth())
        self.option_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.option_box.setFont(font)
        self.option_box.setAlignment(QtCore.Qt.AlignCenter)
        self.option_box.setFlat(False)
        self.option_box.setObjectName("option_box")
        self.optionGrid = QtWidgets.QVBoxLayout(self.option_box)
        self.optionGrid.setContentsMargins(30, 30, 30, 30)
        self.optionGrid.setSpacing(20)
        self.optionGrid.setObjectName("optionGrid")
        self.csvs_box = QtWidgets.QGroupBox(self.option_box)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.csvs_box.setFont(font)
        self.csvs_box.setAlignment(QtCore.Qt.AlignCenter)
        self.csvs_box.setFlat(True)
        self.csvs_box.setObjectName("csvs_box")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.csvs_box)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.erp_check = QtWidgets.QCheckBox(self.csvs_box)
        self.erp_check.setChecked(True)
        self.erp_check.setTristate(False)
        self.erp_check.setObjectName("erp_check")
        self.verticalLayout_3.addWidget(self.erp_check)
        self.vh_check = QtWidgets.QCheckBox(self.csvs_box)
        self.vh_check.setChecked(True)
        self.vh_check.setObjectName("vh_check")
        self.verticalLayout_3.addWidget(self.vh_check)
        self.bb_check = QtWidgets.QCheckBox(self.csvs_box)
        self.bb_check.setChecked(True)
        self.bb_check.setObjectName("bb_check")
        self.verticalLayout_3.addWidget(self.bb_check)
        self.vmg_check = QtWidgets.QCheckBox(self.csvs_box)
        self.vmg_check.setChecked(True)
        self.vmg_check.setObjectName("vmg_check")
        self.verticalLayout_3.addWidget(self.vmg_check)
        self.optionGrid.addWidget(self.csvs_box)
        self.erp_box = QtWidgets.QGroupBox(self.option_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.erp_box.sizePolicy().hasHeightForWidth())
        self.erp_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.erp_box.setFont(font)
        self.erp_box.setAlignment(QtCore.Qt.AlignCenter)
        self.erp_box.setFlat(True)
        self.erp_box.setObjectName("erp_box")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.erp_box)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radio_bn = QtWidgets.QRadioButton(self.erp_box)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.radio_bn.setFont(font)
        self.radio_bn.setChecked(True)
        self.radio_bn.setObjectName("radio_bn")
        self.horizontalLayout_2.addWidget(self.radio_bn)
        self.radio_mod = QtWidgets.QRadioButton(self.erp_box)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.radio_mod.setFont(font)
        self.radio_mod.setChecked(False)
        self.radio_mod.setObjectName("radio_mod")
        self.horizontalLayout_2.addWidget(self.radio_mod)
        self.optionGrid.addWidget(self.erp_box)
        self.prio_box = QtWidgets.QGroupBox(self.option_box)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.prio_box.setFont(font)
        self.prio_box.setAlignment(QtCore.Qt.AlignCenter)
        self.prio_box.setFlat(True)
        self.prio_box.setObjectName("prio_box")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.prio_box)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.radio_def = QtWidgets.QRadioButton(self.prio_box)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.radio_def.setFont(font)
        self.radio_def.setChecked(True)
        self.radio_def.setObjectName("radio_def")
        self.horizontalLayout_4.addWidget(self.radio_def)
        self.radio_ext = QtWidgets.QRadioButton(self.prio_box)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.radio_ext.setFont(font)
        self.radio_ext.setChecked(False)
        self.radio_ext.setObjectName("radio_ext")
        self.horizontalLayout_4.addWidget(self.radio_ext)
        self.optionGrid.addWidget(self.prio_box)
        self.csvGrid.addWidget(self.option_box, 0, 1, 2, 1)
        self.tabs.addTab(self.CSV, "")
        self.Quality = QtWidgets.QWidget()
        self.Quality.setObjectName("Quality")
        self.qualityGrid = QtWidgets.QGridLayout(self.Quality)
        self.qualityGrid.setContentsMargins(10, 10, 10, 10)
        self.qualityGrid.setSpacing(10)
        self.qualityGrid.setObjectName("qualityGrid")
        self.status_box2 = QtWidgets.QGroupBox(self.Quality)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.status_box2.sizePolicy().hasHeightForWidth())
        self.status_box2.setSizePolicy(sizePolicy)
        self.status_box2.setAlignment(QtCore.Qt.AlignCenter)
        self.status_box2.setFlat(False)
        self.status_box2.setObjectName("status_box2")
        self.statusGrid2 = QtWidgets.QHBoxLayout(self.status_box2)
        self.statusGrid2.setContentsMargins(20, 20, 20, 20)
        self.statusGrid2.setSpacing(30)
        self.statusGrid2.setObjectName("statusGrid2")
        self.status_qual = QtWidgets.QTextEdit(self.status_box2)
        self.status_qual.setReadOnly(True)
        self.status_qual.setObjectName("status_qual")
        self.statusGrid2.addWidget(self.status_qual)
        self.qualityGrid.addWidget(self.status_box2, 3, 0, 1, 1)
        self.generate_box2 = QtWidgets.QGroupBox(self.Quality)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generate_box2.sizePolicy().hasHeightForWidth())
        self.generate_box2.setSizePolicy(sizePolicy)
        self.generate_box2.setAlignment(QtCore.Qt.AlignCenter)
        self.generate_box2.setObjectName("generate_box2")
        self.generateGrid2 = QtWidgets.QVBoxLayout(self.generate_box2)
        self.generateGrid2.setContentsMargins(30, 30, 30, 30)
        self.generateGrid2.setSpacing(30)
        self.generateGrid2.setObjectName("generateGrid2")
        self.start_button2 = QtWidgets.QPushButton(self.generate_box2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_button2.sizePolicy().hasHeightForWidth())
        self.start_button2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.start_button2.setFont(font)
        self.start_button2.setObjectName("start_button2")
        self.generateGrid2.addWidget(self.start_button2)
        self.exit_button2 = QtWidgets.QPushButton(self.generate_box2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_button2.sizePolicy().hasHeightForWidth())
        self.exit_button2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.exit_button2.setFont(font)
        self.exit_button2.setObjectName("exit_button2")
        self.generateGrid2.addWidget(self.exit_button2)
        self.qualityGrid.addWidget(self.generate_box2, 3, 1, 1, 1)
        self.progressIFC = QtWidgets.QProgressBar(self.Quality)
        self.progressIFC.setProperty("value", 0)
        self.progressIFC.setTextVisible(False)
        self.progressIFC.setObjectName("progressIFC")
        self.qualityGrid.addWidget(self.progressIFC, 2, 0, 1, 1)
        self.qual_box = QtWidgets.QGroupBox(self.Quality)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qual_box.sizePolicy().hasHeightForWidth())
        self.qual_box.setSizePolicy(sizePolicy)
        self.qual_box.setAutoFillBackground(False)
        self.qual_box.setAlignment(QtCore.Qt.AlignCenter)
        self.qual_box.setFlat(False)
        self.qual_box.setCheckable(False)
        self.qual_box.setObjectName("qual_box")
        self.qualityBoxGrid2 = QtWidgets.QVBoxLayout(self.qual_box)
        self.qualityBoxGrid2.setContentsMargins(30, 30, 30, 30)
        self.qualityBoxGrid2.setSpacing(20)
        self.qualityBoxGrid2.setObjectName("qualityBoxGrid2")
        self.ifc_group = QtWidgets.QGroupBox(self.qual_box)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ifc_group.setFont(font)
        self.ifc_group.setAlignment(QtCore.Qt.AlignCenter)
        self.ifc_group.setFlat(True)
        self.ifc_group.setObjectName("ifc_group")
        self.ifcBoxGrid = QtWidgets.QVBoxLayout(self.ifc_group)
        self.ifcBoxGrid.setObjectName("ifcBoxGrid")
        self.ifc_path2 = QtWidgets.QLineEdit(self.ifc_group)
        self.ifc_path2.setReadOnly(True)
        self.ifc_path2.setObjectName("ifc_path2")
        self.ifcBoxGrid.addWidget(self.ifc_path2)
        self.ifc_button2 = QtWidgets.QPushButton(self.ifc_group)
        self.ifc_button2.setObjectName("ifc_button2")
        self.ifcBoxGrid.addWidget(self.ifc_button2)
        self.qualityBoxGrid2.addWidget(self.ifc_group)
        self.report_group = QtWidgets.QGroupBox(self.qual_box)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.report_group.setFont(font)
        self.report_group.setAlignment(QtCore.Qt.AlignCenter)
        self.report_group.setFlat(True)
        self.report_group.setObjectName("report_group")
        self.reportGrid = QtWidgets.QVBoxLayout(self.report_group)
        self.reportGrid.setObjectName("reportGrid")
        self.report_path = QtWidgets.QLineEdit(self.report_group)
        self.report_path.setReadOnly(True)
        self.report_path.setObjectName("report_path")
        self.reportGrid.addWidget(self.report_path)
        self.report_button = QtWidgets.QPushButton(self.report_group)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.report_button.setFont(font)
        self.report_button.setObjectName("report_button")
        self.reportGrid.addWidget(self.report_button)
        self.qualityBoxGrid2.addWidget(self.report_group)
        self.screw_check = QtWidgets.QCheckBox(self.qual_box)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.screw_check.setFont(font)
        self.screw_check.setObjectName("screw_check")
        self.qualityBoxGrid2.addWidget(self.screw_check)
        self.air_check = QtWidgets.QCheckBox(self.qual_box)
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.air_check.setFont(font)
        self.air_check.setObjectName("air_check")
        self.qualityBoxGrid2.addWidget(self.air_check)
        self.qualityGrid.addWidget(self.qual_box, 1, 1, 2, 1)
        self.preview_box = QtWidgets.QGroupBox(self.Quality)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.preview_box.sizePolicy().hasHeightForWidth())
        self.preview_box.setSizePolicy(sizePolicy)
        self.preview_box.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.preview_box.setAutoFillBackground(False)
        self.preview_box.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_box.setObjectName("preview_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.preview_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.preview_layout = QtWidgets.QHBoxLayout()
        self.preview_layout.setObjectName("preview_layout")
        self.verticalLayout.addLayout(self.preview_layout)
        self.qualityGrid.addWidget(self.preview_box, 1, 0, 1, 1)
        self.tabs.addTab(self.Quality, "")
        self.centralGrid.addWidget(self.tabs, 0, 0, 1, 1)
        CSVgenerator.setCentralWidget(self.centralwidget)
        self.csv_label.setBuddy(self.csv_path)
        self.bb_label.setBuddy(self.bb_order)
        self.ifc_label.setBuddy(self.ifc_path)
        self.vmg_label.setBuddy(self.vmg_order)
        self.bb_label_2.setBuddy(self.nesting_path)
        self.nesting_label.setBuddy(self.nesting_path)
        self.vh_label.setBuddy(self.vh_order)

        self.retranslateUi(CSVgenerator)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CSVgenerator)
        CSVgenerator.setTabOrder(self.ifc_path, self.csv_path)
        CSVgenerator.setTabOrder(self.csv_path, self.nesting_path)
        CSVgenerator.setTabOrder(self.nesting_path, self.vh_order)
        CSVgenerator.setTabOrder(self.vh_order, self.bb_order)
        CSVgenerator.setTabOrder(self.bb_order, self.vmg_order)
        CSVgenerator.setTabOrder(self.vmg_order, self.ifc_button)
        CSVgenerator.setTabOrder(self.ifc_button, self.csv_button)
        CSVgenerator.setTabOrder(self.csv_button, self.prio_button)
        CSVgenerator.setTabOrder(self.prio_button, self.start_button)
        CSVgenerator.setTabOrder(self.start_button, self.exit_button)

    def retranslateUi(self, CSVgenerator):
        _translate = QtCore.QCoreApplication.translate
        CSVgenerator.setWindowTitle(_translate("CSVgenerator", "geWOONhout"))
        self.csv_label.setText(_translate("CSVgenerator", "Waar moeten de CSVs naartoe?"))
        self.bb_label.setText(_translate("CSVgenerator", "BB ordernummer"))
        self.prio_button.setText(_translate("CSVgenerator", "Prio CSV"))
        self.ifc_button.setText(_translate("CSVgenerator", "IFC Map"))
        self.ifc_label.setText(_translate("CSVgenerator", "Waar staan de IFCs?"))
        self.vmg_label.setText(_translate("CSVgenerator", "VMG ordernummer"))
        self.bb_button.setText(_translate("CSVgenerator", "BB CSV"))
        self.bb_label_2.setText(_translate("CSVgenerator", "CSV producten voor Boerboom"))
        self.csv_button.setText(_translate("CSVgenerator", "CSV Map"))
        self.nesting_label.setText(_translate("CSVgenerator", "CSV nesting prioriteit"))
        self.vh_label.setText(_translate("CSVgenerator", "VH ordernummer"))
        self.bulk_label.setText(_translate("CSVgenerator", "Bulk producten voor Boerboom"))
        self.bulk_button.setText(_translate("CSVgenerator", "Bulk CSV"))
        self.status_box.setTitle(_translate("CSVgenerator", "Status"))
        self.generate_box.setTitle(_translate("CSVgenerator", "Genereren"))
        self.start_button.setText(_translate("CSVgenerator", "Start"))
        self.exit_button.setText(_translate("CSVgenerator", "Exit"))
        self.option_box.setTitle(_translate("CSVgenerator", "Opties"))
        self.csvs_box.setTitle(_translate("CSVgenerator", "Welke CSVs:"))
        self.erp_check.setText(_translate("CSVgenerator", "ERP"))
        self.vh_check.setText(_translate("CSVgenerator", "Van Hulst"))
        self.bb_check.setText(_translate("CSVgenerator", "Boerboom"))
        self.vmg_check.setText(_translate("CSVgenerator", "VMG"))
        self.erp_box.setTitle(_translate("CSVgenerator", "ERP CSV per:"))
        self.radio_bn.setText(_translate("CSVgenerator", "Bouwnummer"))
        self.radio_mod.setText(_translate("CSVgenerator", "Module"))
        self.prio_box.setTitle(_translate("CSVgenerator", "Prioriteit:"))
        self.radio_def.setText(_translate("CSVgenerator", "Normaal"))
        self.radio_ext.setText(_translate("CSVgenerator", "Uitgebreid"))
        self.tabs.setTabText(self.tabs.indexOf(self.CSV), _translate("CSVgenerator", "CSV Generator"))
        self.status_box2.setTitle(_translate("CSVgenerator", "Status"))
        self.generate_box2.setTitle(_translate("CSVgenerator", "Genereren"))
        self.start_button2.setText(_translate("CSVgenerator", "Start"))
        self.exit_button2.setText(_translate("CSVgenerator", "Exit"))
        self.qual_box.setTitle(_translate("CSVgenerator", "Kwaliteitscheck instellingen"))
        self.ifc_group.setTitle(_translate("CSVgenerator", "Waar staan de IFC bestanden?"))
        self.ifc_button2.setText(_translate("CSVgenerator", "IFC Map"))
        self.report_group.setTitle(_translate("CSVgenerator", "Waar moet het rapport naartoe?"))
        self.report_button.setText(_translate("CSVgenerator", "Rapport locatie"))
        self.screw_check.setText(_translate("CSVgenerator", "Controleren op schroeven?"))
        self.air_check.setText(_translate("CSVgenerator", "Controleren op luchtdichting?"))
        self.preview_box.setTitle(_translate("CSVgenerator", "Preview"))
        self.tabs.setTabText(self.tabs.indexOf(self.Quality), _translate("CSVgenerator", "Verdubbelaar"))
