# -*- coding:utf-8 -*-

import sys
import traceback
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox
import hkForm
import function_kit


class HkODPSTool(QWidget, hkForm.Ui_hkToolForm):

    def __init__(self):
        super(HkODPSTool, self).__init__()
        self.form_isvalid = True
        self.setupUi(self)

    def showCustomMenu(self, pos):
        # 显示右键菜单

        self.contextMenu.move(self.pos() + pos)
        self.contextMenu.show()

    def actionHandler(self):
        # 当点击右键菜单中的“关于”时的动作

        about_str = ('由 Xian Jiarong 开发完成\n'
                     '工号：0027011795\n\n'
                     '完成时间：2019年1月12日\n'
                     '更新时间：2019年4月15日\n'
                     '版本号：1.1.0\n\n'
                     '浩鲸云计算科技股份有限公司\n\n'
                     '本程序使用 PyQt5 开发，遵守 LGPL 协议\n')

        QMessageBox.about(self,
                          "关于软件",
                          about_str)

    def cdp_add_partition(self):
        '''
        CDP添加分区复选框点击事件
        :return:
        '''

        if self.addDt.isChecked():
            # 同时把生成脚本的各个选项禁用
            self.makeDDL.setEnabled(False)
            self.makeCDP.setEnabled(False)
            self.dbNamePrefix.setEnabled(False)
            self.dbNameSuffix.setEnabled(False)
            self.lifecycleInput.setEnabled(False)
            self.dbType.setEnabled(False)
            self.splitCharacterComboBox.setEnabled(False)
            self.holderLabel.setText(
                "选择从 ODPS 中导出的 CDP 文件夹位置。如 C:/cdp_export，大小写不区分")
        else:
            self.makeDDL.setEnabled(True)
            self.makeCDP.setEnabled(True)
            self.dbNamePrefix.setEnabled(True)
            self.dbNameSuffix.setEnabled(True)
            self.lifecycleInput.setEnabled(True)
            self.dbType.setEnabled(True)
            self.splitCharacterComboBox.setEnabled(True)
            self.holderLabel.setText("输入选择框")

    def make_script(self):
        '''
        生成脚本内 DDL 和 CDP 两个复选框的点击事件，使用同一事件
        这里仅用于控制 placeholder 显示的文本
        :return:
        '''

        if self.makeDDL.isChecked() or self.makeCDP.isChecked():
            # 同时把添加分区相关的选项框、输入框禁用
            self.addDt.setEnabled(False)
            msg = "选择数据库元数据的 CSV 文件或文件夹。"
            msg += "CSV文件内容必须是经过规范化后的，且不含多余行"
            self.holderLabel.setText(msg)
        else:
            self.addDt.setEnabled(True)
            self.holderLabel.setText("输入选择框")

        if self.makeDDL.isChecked() and self.makeCDP.isChecked():
            # 同时生成 DDL 和 CDP 时，DDL 的分区字段需要从分区表达式中截取
            msg = "同时生成DDL和CDP，请输入分区表达式，DDL的分区字段将从分区表达式中截取。"
            msg += "即等号（=）前的字符"
            self.dtStringIndicator.setText(msg)
        elif self.makeDDL.isChecked() and not self.makeCDP.isChecked():
            # 只生成 DDL
            msg = "请输入分区字段"
            self.dtStringIndicator.setText(msg)
            self.dtStringInput.setPlaceholderText("dt")
        else:
            # 恢复原状
            msg = "分区表达式"
            self.dtStringIndicator.setText(msg)
            self.dtStringInput.setPlaceholderText("dt=${bdp.system.bizdate}")

        if self.makeCDP.isChecked():
            # 只要生成 CDP 脚本的框被选中，则都要恢复原状
            self.dtStringInput.setPlaceholderText("dt=${bdp.system.bizdate}")

    def show_warning(self, text):
        '''
        在程序底部显示警告信息
        :param text: 需要显示的文件
        :return: 无返回值
        '''
        self.warningLabel.setText(str(text))

    def show_error(self, e):
        '''
        执行出错时候显示错误，包括弹窗显示和终端显示
        :param e: 执行出现的异常对象
        :return: 无返回
        '''
        traceback.print_exc()
        QMessageBox.warning(self,
                            "Error!",
                            "执行遇到错误：\n\n{}".format(e),
                            QMessageBox.Ok,
                            QMessageBox.Ok)
        return

    def choose_source_file_or_folder(self):
        '''
        选择输入源，可以是文件或者文件夹（代码中会先做判断是点击了哪个按钮）
        :return:
        '''

        # 先判断点击的是哪个按钮
        sender = self.sender()
        sourceBtn = sender.objectName()

        if sourceBtn == "sourceFileBtn":
            # 选择文件作为输入源
            fname = QFileDialog.getOpenFileName(self, '选择文件', '/home')
            if fname[0]:
                # 文件有效，处理文件。这里获取到的文件名是全路径的
                source = fname[0]
            else:
                source = ""
        elif sourceBtn == "sourceFolderBtn":
            # 选择文件夹作为输入源
            folder = QFileDialog.getExistingDirectory(self, '选择文件夹', '/home')
            if folder:
                source = folder
            else:
                source = ""

        if source == "":
            source = self.sourceInput.text()

        self.sourceInput.setText(source)

    def choose_result_folder(self):
        '''
        选择结果文件夹
        :return:
        '''

        result_folder = QFileDialog.getExistingDirectory(self,
                                                         '选择保存位置',
                                                         '/home')
        if result_folder:
            self.resultFolderInput.setText(result_folder)

    def accept(self):
        """
        用户点击了确定按钮时的操作
        :return:
        """

        # 先判断输入输出的位置值是否存在
        if not self.form_isvalid:
            return

        # 获取公共的配置信息 #################
        # 包括：分区字段、输入文件或文件夹、输出位置
        # ------ 分区表达式
        partition = self.dtStringInput.text().strip()
        if not partition:
            partition = self.dtStringInput.placeholderText()
        # ------ 输入输出位置
        source_location = self.sourceInput.text().strip()
        target_location = self.resultFolderInput.text().strip()
        # 输入输出不能是相同的位置
        if source_location == target_location:
            self.show_warning("输入输出位置不能相同！！！")
            return

        # 检查是勾选了添加分区还是生成脚本
        if self.addDt.isChecked():
            # 添加分区，返回值是被添加了分区的文件个数
            try:
                result_value = function_kit.addDt(partition,
                                                  source_location,
                                                  target_location)
            except Exception as e:
                self.show_error(e)
                return

        else:
            # 生成 DDL 和 CDP
            # 获取字段分隔符
            split_combo_index = self.splitCharacterComboBox.currentIndex()
            if split_combo_index == 1:
                split_character = '\t'
            elif split_combo_index == 2:
                split_character = ' '
            elif split_combo_index == 3:
                split_character = '||'
            else:
                split_character = ','
            # ------ 要先获取表名前后缀
            tbname_prefix = self.dbNamePrefix.text().strip()
            tbname_suffix = self.dbNameSuffix.text().strip()
            # ------ 数据库类型
            db_type = ''
            if self.mysqlRadioBtn.isChecked():
                db_type = self.mysqlRadioBtn.text().lower()
            elif self.oracleRadioBtn.isChecked():
                db_type = self.oracleRadioBtn.text().lower()
            elif self.sqlserverRadioBtn.isChecked():
                db_type = self.sqlserverRadioBtn.text().lower()
            elif self.odpsRadioBtn.isChecked():
                db_type = self.odpsRadioBtn.text().lower()

            # ------ 表生命周期
            lifecycle = self.lifecycleInput.text().strip()
            if not lifecycle:
                lifecycle = self.lifecycleInput.placeholderText()

            if self.makeDDL.isChecked():
                try:
                    result_value = function_kit.makeDDL(db_type,
                                                        partition,
                                                        tbname_prefix,
                                                        tbname_suffix,
                                                        source_location,
                                                        target_location,
                                                        lifecycle,
                                                        split_character)
                except Exception as e:
                    self.show_error(e)
                    return
            if self.makeCDP.isChecked():
                try:
                    result_value = function_kit.makeCDP(db_type,
                                                        partition,
                                                        tbname_prefix,
                                                        tbname_suffix,
                                                        source_location,
                                                        target_location,
                                                        split_character)
                except Exception as e:
                    self.show_error(e)
                    return

        self.show_warning(result_value)

    def folder_input_change(self, value):
        '''检查输入输出两个框的（文件或目录）值是否存在，
        如果不存在，则在提醒栏显示警告
        :param value: 文本框的值，事件自动传送过来的
        :return: 布尔值 True 或 False
        '''

        sender = self.sender()
        if sender.objectName() == 'sourceInput':
            prefix = "输入"
        elif sender.objectName() == 'resultFolderInput':
            prefix = "输出"
        value = value.strip()
        if not function_kit.check_if_exists(value):
            self.show_warning(prefix + "的文件夹位置不存在，请检查！")
            self.form_isvalid = False
        else:
            self.form_isvalid = True
            self.show_warning("")

        return self.form_isvalid

    def reject(self):
        '''
        用户点击了取消按钮时的动作
        :return:
        '''

        self.close()

    def reset(self):
        # 重置事件

        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    hk_form = HkODPSTool()
    hk_form.show()
    sys.exit(app.exec_())
