# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_hkToolForm(object):
    def setupUi(self, hkToolForm):
        hkToolForm.setObjectName("hkToolForm")
        hkToolForm.resize(850, 504)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("iwhalecloud64x64.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        hkToolForm.setWindowIcon(icon)

        # 普通中文字体样式
        ch_font = QtGui.QFont()
        ch_font.setFamily("微软雅黑")
        # 普通英文字体样式
        en_font = QtGui.QFont()
        en_font.setFamily("Times New Roman")
        # 加粗的中文字体样式
        ch_bold_font = QtGui.QFont()
        ch_bold_font.setFamily("微软雅黑")
        ch_bold_font.setBold(True)
        ch_bold_font.setWeight(75)
        # 加粗的英文字体样式
        en_bold_font = QtGui.QFont()
        en_bold_font.setFamily("Times New Roman")
        en_bold_font.setBold(True)
        en_bold_font.setWeight(75)

        # 在整个软件层级添加右键菜单，
        # 显示为“关于”，点进去则显示版权信息
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(hkToolForm.showCustomMenu)
        self.contextMenu = QtWidgets.QMenu(self)
        self.rightClickMenu = self.contextMenu.addAction("关于")
        self.rightClickMenu.setObjectName("about")
        self.rightClickMenu.setFont(ch_font)
        self.rightClickMenu.triggered.connect(hkToolForm.actionHandler)

        ############################# CDP添加分区部分
        self.addDt = QtWidgets.QCheckBox(hkToolForm)
        self.addDt.setGeometry(QtCore.QRect(70, 50, 91, 16))
        self.addDt.setFont(ch_font)
        self.addDt.setObjectName("addDt")
        self.addDt.setEnabled(False)

        # 添加分区的提示
        self.dtStringIndicator = QtWidgets.QLabel(self)
        self.dtStringIndicator.setGeometry(150, 260, 600, 16)
        self.dtStringIndicator.setObjectName("dtStringIndicator")
        self.dtStringIndicator.setFont(ch_font)
        self.dtLabel = QtWidgets.QLabel(self)
        self.dtLabel.setGeometry(65, 282, 71, 16)
        self.dtLabel.setObjectName("dtLabel")
        self.dtLabel.setFont(en_font)
        # 分区字段值
        self.dtStringInput = QtWidgets.QLineEdit(self)
        self.dtStringInput.setGeometry(140, 280, 461, 20)
        self.dtStringInput.setObjectName("dtStringInput")

        ############################## 生成脚本的区域 ########################################
        self.makeScript = QtWidgets.QGroupBox(hkToolForm)
        self.makeScript.setGeometry(QtCore.QRect(180, 20, 600, 121))

        self.makeScript.setFont(ch_font)
        self.makeScript.setObjectName("makeScript")
        self.makeDDL = QtWidgets.QCheckBox(self.makeScript)
        self.makeDDL.setGeometry(QtCore.QRect(50, 30, 71, 16))
        self.makeDDL.setObjectName("makeDDL")
        self.makeCDP = QtWidgets.QCheckBox(self.makeScript)
        self.makeCDP.setGeometry(QtCore.QRect(150, 30, 71, 16))
        self.makeCDP.setObjectName("makeCDP")
        # 选择分隔符号，默认为逗号
        self.splitCharacterLabel = QtWidgets.QLabel(self.makeScript)
        self.splitCharacterLabel.setGeometry(340, 30, 60, 16)
        self.splitCharacterLabel.setObjectName("splitCharacterLabel")
        self.splitCharacterLabel.setFont(ch_font)
        self.splitCharacterComboBox = QtWidgets.QComboBox(self.makeScript)
        self.splitCharacterComboBox.setGeometry(420, 30, 80, 20)
        self.splitCharacterComboBox.addItem(",   逗号")
        self.splitCharacterComboBox.addItem(r"\t 制表符")
        self.splitCharacterComboBox.addItem("    空格")
        self.splitCharacterComboBox.addItem("||  双竖线")
        self.splitCharacterComboBox.setFont(ch_font)
        # 填充表名规则区域
        self.fillTableRuleLabel = QtWidgets.QLabel(self.makeScript)
        self.fillTableRuleLabel.setGeometry(20, 70, 300, 20)
        self.fillTableRuleLabel.setObjectName("fillTableRuleLabel")
        self.fillTableRuleLabel.setFont(ch_font)
        self.dbNamePrefix = QtWidgets.QLineEdit(self.makeScript)
        self.dbNamePrefix.setGeometry(QtCore.QRect(20, 90, 200, 20))
        self.dbNamePrefix.setInputMask("")
        self.dbNamePrefix.setObjectName("dbNamePrefix")
        self.src_tbname = QtWidgets.QLabel(self.makeScript)
        self.src_tbname.setGeometry(QtCore.QRect(250, 90, 150, 20))
        self.src_tbname.setObjectName("src_tbname")
        self.src_tbname.setFont(ch_font)
        self.dbNameSuffix = QtWidgets.QLineEdit(self.makeScript)
        self.dbNameSuffix.setGeometry(QtCore.QRect(390, 90, 191, 20))
        self.dbNameSuffix.setObjectName("dbNameSuffix")
        # 生成 DDL 时的生命周期设置区域
        self.lifecycleLabel = QtWidgets.QLabel(self)
        self.lifecycleLabel.setGeometry(65, 302, 70, 16)
        self.lifecycleLabel.setObjectName("lifecycleLabel")
        self.lifecycleLabel.setFont(ch_font)
        self.lifecycleInput = QtWidgets.QLineEdit(self)
        self.lifecycleInput.setGeometry(140, 302, 461, 20)
        self.lifecycleInput.setObjectName("lifecycleInput")

        ################### 选择数据库类型的区域
        dbRatioBtnWidth = 70
        dbRatioBtnHeight = 16
        dbRatioBtnY = 30
        dbRatioGap = 20
        dbRatioStartX = 40
        self.dbType = QtWidgets.QGroupBox(hkToolForm)
        self.dbType.setGeometry(QtCore.QRect(205, 160, 551, 80))
        self.dbType.setFont(ch_font)
        self.dbType.setObjectName("dbType")
        self.mysqlRadioBtn = QtWidgets.QRadioButton(self.dbType)
        self.mysqlRadioBtn.setGeometry(QtCore.QRect(dbRatioStartX,
                                                    dbRatioBtnY,
                                                    dbRatioBtnWidth,
                                                    dbRatioBtnHeight))
        self.mysqlRadioBtn.setObjectName("mysqlRadioBtn")
        self.oracleRadioBtn = QtWidgets.QRadioButton(self.dbType)
        self.oracleRadioBtn.setGeometry(QtCore.QRect(dbRatioStartX
                                                     + dbRatioBtnWidth*1
                                                     + dbRatioGap*1,
                                                     dbRatioBtnY,
                                                     dbRatioBtnWidth,
                                                     dbRatioBtnHeight))
        self.oracleRadioBtn.setObjectName("oracleRadioBtn")
        self.sqlserverRadioBtn = QtWidgets.QRadioButton(self.dbType)
        self.sqlserverRadioBtn.setGeometry(QtCore.QRect(dbRatioStartX
                                                        + dbRatioBtnWidth*2
                                                        + dbRatioGap*2,
                                                        dbRatioBtnY,
                                                        dbRatioBtnWidth,
                                                        dbRatioBtnHeight))
        self.sqlserverRadioBtn.setObjectName("sqlserverRadioBtn")
        self.odpsRadioBtn = QtWidgets.QRadioButton(self.dbType)
        self.odpsRadioBtn.setGeometry(QtCore.QRect(dbRatioStartX
                                                   + dbRatioBtnWidth*3
                                                   + dbRatioGap*3,
                                                   dbRatioBtnY,
                                                   dbRatioBtnWidth,
                                                   dbRatioBtnHeight))
        self.odpsRadioBtn.setObjectName("odpsRadioBtn")
        self.odpsSrcPtInput = QtWidgets.QLineEdit(hkToolForm)
        self.odpsSrcPtInput.setGeometry(580, 190, 160, 16)
        self.odpsSrcPtInput.setObjectName("odpsSrcPtInput")

        ###################### 输入输出选择区域 ########################
        self.holderLabel = QtWidgets.QLabel(hkToolForm)
        self.holderLabel.setGeometry(QtCore.QRect(70, 340, 591, 16))
        self.holderLabel.setFont(ch_bold_font)
        self.holderLabel.setText("")
        self.holderLabel.setTextFormat(QtCore.Qt.RichText)
        self.holderLabel.setObjectName("holderLabel")
        # 输入源
        self.sourceInput = QtWidgets.QLineEdit(hkToolForm)
        self.sourceInput.setGeometry(QtCore.QRect(60, 360, 500, 20))
        self.sourceInput.setObjectName("sourceInput")
        # 选择输入文件
        self.sourceFileBtn = QtWidgets.QPushButton(hkToolForm)
        self.sourceFileBtn.setGeometry(580, 360, 80, 20)
        self.sourceFileBtn.setObjectName("sourceFileBtn")
        self.sourceFileBtn.setFont(ch_bold_font)
        # 选择输入文件夹按钮
        self.sourceFolderBtn = QtWidgets.QPushButton(hkToolForm)
        self.sourceFolderBtn.setGeometry(680, 360, 80, 20)
        self.sourceFolderBtn.setObjectName("sourceFolderBtn")
        self.sourceFolderBtn.setFont(ch_bold_font)
        ############### 输出位置
        self.resultFolderLabel = QtWidgets.QLabel(hkToolForm)
        self.resultFolderLabel.setGeometry(QtCore.QRect(70, 390, 81, 16))
        self.resultFolderLabel.setFont(ch_bold_font)
        self.resultFolderLabel.setTextFormat(QtCore.Qt.RichText)
        self.resultFolderLabel.setObjectName("resultFolderLabel")
        self.resultFolderInput = QtWidgets.QLineEdit(hkToolForm)
        self.resultFolderInput.setGeometry(QtCore.QRect(60, 410, 500, 20))
        self.resultFolderInput.setObjectName("resultFolderInput")
        # 选择输出文件夹按钮
        self.resultFolderBtn = QtWidgets.QPushButton(hkToolForm)
        self.resultFolderBtn.setGeometry(580, 410, 80, 20)
        self.resultFolderBtn.setObjectName("resultFolderBtn")
        self.resultFolderBtn.setFont(ch_bold_font)

        ########################## 确定、重置、取消按钮
        self.comfirmBtn = QtWidgets.QDialogButtonBox(hkToolForm)
        self.comfirmBtn.setGeometry(QtCore.QRect(340, 450, 160, 32))
        self.comfirmBtn.setFont(en_bold_font)
        self.comfirmBtn.setOrientation(QtCore.Qt.Horizontal)
        self.comfirmBtn.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel |
                                           QtWidgets.QDialogButtonBox.Ok)
        self.comfirmBtn.setCenterButtons(False)
        self.comfirmBtn.setObjectName("comfirmBtn")
        # 单独添加一个重置按钮
        # self.resetBtn = QtWidgets.QPushButton(hkToolForm)
        # self.resetBtn.setGeometry(550, 454, 70, 23)
        # self.resetBtn.setFont(font)

        ########################### 底部提醒字符
        self.warningLabel = QtWidgets.QLabel(hkToolForm)
        self.warningLabel.setGeometry(5, 480, 850, 20)
        self.warningLabel.setObjectName("warningLabel")
        self.warningLabel.setFont(ch_bold_font)
        # 设置字体颜色为红色
        self.warningLabel.setStyleSheet("color: red")

        # 事件绑定
        self.retranslateUi(hkToolForm)
        self.comfirmBtn.accepted.connect(hkToolForm.accept)
        self.comfirmBtn.rejected.connect(hkToolForm.reject)
        # self.resetBtn.clicked.connect(hkToolForm.reset)
        self.addDt.clicked.connect(hkToolForm.cdp_add_partition)
        self.makeDDL.clicked.connect(hkToolForm.make_script)
        self.makeCDP.clicked.connect(hkToolForm.make_script)
        self.sourceFileBtn.clicked.connect(hkToolForm.choose_source_file_or_folder)
        self.sourceFolderBtn.clicked.connect(hkToolForm.choose_source_file_or_folder)
        self.sourceInput.textChanged.connect(hkToolForm.folder_input_change)
        self.resultFolderInput.textChanged.connect(hkToolForm.folder_input_change)
        self.resultFolderBtn.clicked.connect(hkToolForm.choose_result_folder)
        QtCore.QMetaObject.connectSlotsByName(hkToolForm)

    def retranslateUi(self, hkToolForm):
        _translate = QtCore.QCoreApplication.translate
        hkToolForm.setWindowTitle(
            _translate("hkToolForm",
                       "数据上云脚本生成工具v2.1{:30}".format('')))
        self.addDt.setText(_translate("hkToolForm", "cdp添加分区"))
        self.makeScript.setTitle(_translate("hkToolForm", "脚本生成"))
        self.makeDDL.setText(_translate("hkToolForm", "生成DDL"))
        self.makeCDP.setText(_translate("hkToolForm", "生成CDP"))
        self.dbNamePrefix.setPlaceholderText(_translate("hkToolForm", "表名前缀"))
        self.src_tbname.setText(_translate("hkToolForm", "+ _文件名_原表名_ +"))
        self.dbNameSuffix.setPlaceholderText(_translate("hkToolForm", "表名后缀"))
        self.dbType.setTitle(_translate("hkToolForm", "数据库类型"))
        self.mysqlRadioBtn.setText(_translate("hkToolForm", "MySQL"))
        self.oracleRadioBtn.setText(_translate("hkToolForm", "Oracle"))
        self.sqlserverRadioBtn.setText(_translate("hkToolForm", "SqlServer"))
        self.odpsRadioBtn.setText(_translate("hkTolForm", "odps"))
        self.holderLabel.setText(_translate("hkToolForm", "输入选择框"))
        self.resultFolderLabel.setText(_translate("hkToolForm", "结果文件夹"))
        self.dtStringIndicator.setText(_translate("hkToolForm", "分区表达式"))
        self.dtLabel.setText(_translate("hkTookForm", "partition:"))
        self.dtStringInput.setPlaceholderText(
            _translate("hkToolForm", "dt=${bdp.system.bizdate}"))
        self.odpsSrcPtInput.setPlaceholderText(
            _translate("hkToolForm", "源表分区，如dt=${bizdate}"))
        self.lifecycleLabel.setText(_translate("hkToolForm", "生命周期："))
        self.lifecycleInput.setPlaceholderText(_translate("hkToolForm", "15"))
        self.sourceFileBtn.setText(_translate("hkToolForm", "选择文件"))
        self.sourceFolderBtn.setText(_translate("hkToolForm", "选择文件夹"))
        self.resultFolderBtn.setText(_translate("hkToolForm", "选择文件夹"))
        self.fillTableRuleLabel.setText(
            _translate("hkToolForm", "请填充表名规则（文件名不含后缀）"))
        self.splitCharacterLabel.setText(_translate("hkToolForm", "选择分隔符"))
