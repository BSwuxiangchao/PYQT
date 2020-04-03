

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from copy import deepcopy
import Database.Database as DBproduct

import os
import json


import Ui.LabelConfigWnd
import printer_helper


class PrintLabelSetting(QMainWindow, Ui.LabelConfigWnd.Ui_MainWindow):
    def __init__(self, parent,product_name="",model_name="",strmacid="",strstationid=""):
        super(PrintLabelSetting, self).__init__()
        print("access in setting dialog")
        self.setupUi(self)
        self.parent = parent
        self.first_cfg_path = './Config/12.0x5.5_default_cfg.json'
        self.second_cfg_path = './Config/18.0x40_default_cfg.json'
        self.third_cfg_path = './Config/37.8x16.8_default_cfg.json'
        self.product_name =product_name
        self.model_name = model_name
        self.strstationid = strstationid
        self.strmacid = strmacid
        self.beChangeDefaultCfg = 0

        #当前标签尺寸
        self.label_size_cur_str = ''

        # 打印机信息
        self.printer_name_list = []
        self.index_of_cur_printer = 0
        self.printer_name_cur_str = ''


        self.o_printer = printer_helper.printer_helper()
        self.loadDBProductConfig()
        # 绑定按键事件
        self.setConnection()
        self.updateUI()

    def setConnection(self):
        self.btn_save_config.clicked.connect(self.saveConfigSetting)
        self.btn_quit_config.clicked.connect(self.quitConfigSetting)
        self.ckb_change_default.stateChanged.connect(self.changeDefaultCfg)

    def updateUI(self):
        self._updatePrinterList()
        self._updateLabelSizeList()

    def changeDefaultCfg(self,state):
        self.beChangeDefaultCfg = int(self.ckb_change_default.isChecked())

    def _updateLabelSizeList(self):
        list_labelSize = ["12.0 * 5.5(mm)", "37.8 * 16.8(mm)", "18.0 * 40.0(mm)"]
        self.lsv_labelsize_model = QStandardItemModel()

        cur_item = QStandardItem()
        for index, labelsize_name in enumerate(list_labelSize):
            name = labelsize_name
            self.printer_name_list.append(name)
            # 添加到list view
            item = QStandardItem(name)
            self.lsv_labelsize_model.appendRow(item)
            if item.text() == self.label_size_cur_str:
                cur_item = item
                self.index_of_cur_printer = index

        self.lsv_label_size.setModel(self.lsv_labelsize_model)
        self.lsv_label_size.clicked.connect(self.eventOfLabelSizeSelected)
        self.lsv_label_size.setCurrentIndex(self.lsv_labelsize_model.indexFromItem(cur_item))
    # 尺寸列表选中事件
    def eventOfLabelSizeSelected(self, index):
        selectedIndex = index.row()
        self._updateCurSizeDefaultInfo(selectedIndex)

    def _updateCurSizeDefaultInfo(self,int_index):
        self.labelsize_cur_str = self.lsv_labelsize_model.item(int_index).text()
        print('cur_labelSize = ',self.labelsize_cur_str)
        # 标签
        self.led_label_model.setText(str(self.product_name))
        if self.labelsize_cur_str == "12.0 * 5.5(mm)":
            self.led_label_width.setText("12.0")
            self.led_label_height.setText(str("5.5"))
            config_js = self.first_cfg_path
        elif self.labelsize_cur_str == "37.8 * 16.8(mm)":
            self.led_label_width.setText(str("37.8"))
            self.led_label_height.setText(str("16.8"))
            config_js = self.third_cfg_path
        elif self.labelsize_cur_str == "18.0 * 40.0(mm)":
            self.led_label_width.setText(str("18.0 "))
            self.led_label_height.setText(str("40.0"))
            config_js = self.second_cfg_path
        else:
            pass
        if not os.path.exists(config_js):
            QMessageBox.warning(None, 'Error', '不存在默认配置'+format('%s' % config_js))
            exit(0)
        fp = open(config_js, 'r', encoding='utf_8_sig')
        print("ok")
        data_of_default_cfg_js_dic = json.load(fp)
        fp.close()
        self.loadCurProductConfig(data_of_default_cfg_js_dic)
        self.btn_save_config.setEnabled(1)

    def loadCurProductConfig(self,select_product_cfg_js_dic):
        self.data_of_select_product_cfg_js_dic = select_product_cfg_js_dic
        # 数据库
        self.db_ip_str = self.data_of_select_product_cfg_js_dic['database']['host']
        self.db_user_str = self.data_of_select_product_cfg_js_dic['database']['user']
        self.db_pw_str = self.data_of_select_product_cfg_js_dic['database']['pw']
        self.db_port_str = self.data_of_select_product_cfg_js_dic['database']['port']
        self.db_db_res_str = self.data_of_select_product_cfg_js_dic['database']['db_reslt']
        self.db_tb_res_str = self.data_of_select_product_cfg_js_dic['database']['tb_reslt']
        self.db_db_param_str = self.data_of_select_product_cfg_js_dic['database']['db_param']
        self.db_tb_param_str = self.data_of_select_product_cfg_js_dic['database']['tb_param']
        # 标签
        self.label_width = self.data_of_select_product_cfg_js_dic['label']['width']
        self.label_height = self.data_of_select_product_cfg_js_dic['label']['height']

        self.label_has_bar_code = bool(self.data_of_select_product_cfg_js_dic['label']['has_bar_code'])
        self.label_bar_code_size = self.data_of_select_product_cfg_js_dic['label']['bar_code_size']
        self.label_bar_code_x_offset = self.data_of_select_product_cfg_js_dic['label']['bar_x_offset']
        self.label_bar_code_y_offset = self.data_of_select_product_cfg_js_dic['label']['bar_y_offset']

        self.label_has_qr_code = bool(self.data_of_select_product_cfg_js_dic['label']['has_qr_code'])
        self.label_qr_code_size = self.data_of_select_product_cfg_js_dic['label']['qr_code_size']
        self.label_qr_code_x_offset = self.data_of_select_product_cfg_js_dic['label']['qr_x_offset']
        self.label_qr_code_y_offset = self.data_of_select_product_cfg_js_dic['label']['qr_y_offset']

        self.label_has_hr_code = bool(self.data_of_select_product_cfg_js_dic['label']['has_hr'])
        self.label_hr_size = self.data_of_select_product_cfg_js_dic['label']['hr_size']
        self.label_hr_x_offset = self.data_of_select_product_cfg_js_dic['label']['hr_x_offset']
        self.label_hr_y_offset = self.data_of_select_product_cfg_js_dic['label']['hr_y_offset']
        # 打印机
        self.product_printer = self.data_of_select_product_cfg_js_dic['printer_name']
        self.add_label_width = self.data_of_select_product_cfg_js_dic['label_add']['width']
        self.add_label_height = self.data_of_select_product_cfg_js_dic['label_add']['height']
        self.add_label_x_offset = self.data_of_select_product_cfg_js_dic['label_add']['x_offset']
        self.add_label_y_offset = self.data_of_select_product_cfg_js_dic['label_add']['y_offset']
        self.add_label_left_margin = self.data_of_select_product_cfg_js_dic['label_add']['left_margin']
        self.add_label_right_margin = self.data_of_select_product_cfg_js_dic['label_add']['right_margin']
        self._updateCurProductInfo()

    def loadDBProductConfig(self):
        tempselect_product_cfg_js_dic = DBproduct.GetCfgByDB(self.strmacid,self.model_name,self.strstationid)
        if tempselect_product_cfg_js_dic == -1:
            self.btn_save_config.setEnabled(0)
            self.btn_quit_config.setEnabled(0)
        else:
            self.loadCurProductConfig(tempselect_product_cfg_js_dic)

    def _updatePrinterList(self):
        tup_printers =self.o_printer.get_printers()

        list_printers = list(tup_printers)
        self.lsv_printer_model = QStandardItemModel()

        cur_item = QStandardItem()
        for index, printer_name in enumerate(list_printers):
            name = printer_name[2]
            self.printer_name_list.append(name)
            # 添加到list view
            item = QStandardItem(name)
            self.lsv_printer_model.appendRow(item)
            if item.text() == self.printer_name_cur_str:
                cur_item = item
                self.index_of_cur_printer = index

        self.lsv_printer_names.setModel(self.lsv_printer_model)
        self.lsv_printer_names.clicked.connect(self.eventOfPrinterSelected)
        self.lsv_printer_names.setCurrentIndex(self.lsv_printer_model.indexFromItem(cur_item))

    # 打印机列表选中事件
    def eventOfPrinterSelected(self, index):
        selectedIndex = index.row()
        self._updateCurPrinterInfo(selectedIndex)

    def _updateCurPrinterInfo(self, int_index):
        self.printer_name_cur_str = self.lsv_printer_model.item(int_index).text()
        print('cur_printer name = ', self.printer_name_cur_str)

        # 更新打印机信息UI
        self.led_printer_name.setText(self.printer_name_cur_str)
        self.o_printer.open_printer(self.printer_name_cur_str)
        # _宽高
        printer_area = self.o_printer.get_printable_area()
        self.led_printer_width.setText(str(int(self.o_printer.pixel_to_mm(printer_area[0], 0) + 0.5)))
        self.led_printer_height.setText(str(int(self.o_printer.pixel_to_mm(printer_area[1], 1) + 0.5)))
        # _ppi
        printer_ppi = self.o_printer.get_ppi()
        self.led_printer_x_ppi.setText(str(printer_ppi[0]))
        self.led_printer_y_ppi.setText(str(printer_ppi[1]))
        # _边缘
        printer_margin = self.o_printer.get_margin()
        self.led_printer_left_margin.setText(str(int(self.o_printer.pixel_to_mm(printer_margin[0], 0) + 0.5)))
        self.led_printer_right_margin.setText(str(int(self.o_printer.pixel_to_mm(printer_margin[1], 0) + 0.5)))
        print(self.printer_name_cur_str, printer_area, printer_ppi, printer_margin)


    def _updateCurProductInfo(self):
        # 数据库
        self.led_db_ip.setText(self.db_ip_str)
        self.led_db_user.setText(self.db_user_str)
        self.led_db_pw.setText(self.db_pw_str)
        self.led_db_port.setText(str(self.db_port_str))
        self.led_db_chk_name.setText(self.db_db_res_str)
        self.led_db_chk_table.setText(self.db_tb_res_str)
        self.led_db_rec_name.setText(self.db_db_param_str)
        self.led_db_rec_table.setText(self.db_tb_param_str)
        # 打印机

        self.led_printer_name.setText(self.product_printer)

        self.led_add_label_width.setText(str(self.add_label_width))
        self.led_add_label_height.setText(str(self.add_label_height))
        self.led_add_label_x_offset.setText(str(self.add_label_x_offset))
        self.led_add_label_y_offset.setText(str(self.add_label_y_offset))
        self.led_add_label_left_margin.setText(str(self.add_label_left_margin))
        self.led_add_label_right_margin.setText(str(self.add_label_right_margin))

        #标签
        self.led_label_model.setText(str(self.product_name))
        self.led_label_width.setText(str(self.label_width))
        self.led_label_height.setText(str(self.label_height))
        # 条形码
        self.ckb_use_barcode.setChecked(self.label_has_bar_code)
        self.led_label_barcode_size.setText(str(self.label_bar_code_size))
        self.led_label_barcode_x_offset.setText(str(self.label_bar_code_x_offset))
        self.led_label_barcode_y_offset.setText(str(self.label_bar_code_y_offset))
        # QR码
        self.ckb_use_qrcode.setChecked(self.label_has_qr_code)
        self.led_label_qrcode_size.setText(str(self.label_qr_code_size))
        self.led_label_qrcode_x_offset.setText(str(self.label_qr_code_x_offset))
        self.led_label_qrcode_y_offset.setText(str(self.label_qr_code_y_offset))
        # 文字
        self.ckb_use_hr.setChecked(self.label_has_hr_code)
        self.led_label_hr_size.setText(str(self.label_hr_size))
        self.led_label_hr_x_offset.setText(str(self.label_hr_x_offset))
        self.led_label_hr_y_offset.setText(str(self.label_hr_y_offset))

    def saveConfigSetting(self):
        product_cfg_buf_dic = deepcopy(self.data_of_select_product_cfg_js_dic)
        # 数据库
        product_cfg_buf_dic['database']['host'] = self.led_db_ip.text()
        product_cfg_buf_dic['database']['user'] = self.led_db_user.text()
        product_cfg_buf_dic['database']['pw'] = self.led_db_pw.text()
        product_cfg_buf_dic['database']['port'] = int(self.led_db_port.text())
        product_cfg_buf_dic['database']['db_reslt'] = self.led_db_chk_name.text()
        product_cfg_buf_dic['database']['tb_reslt'] = self.led_db_chk_table.text()
        product_cfg_buf_dic['database']['db_param'] = self.led_db_rec_name.text()
        product_cfg_buf_dic['database']['tb_param'] = self.led_db_rec_table.text()
        # 附加标签
        product_cfg_buf_dic['label_add']['height'] = float(self.led_add_label_height.text())
        product_cfg_buf_dic['label_add']['width'] = float(self.led_add_label_width.text())
        product_cfg_buf_dic['label_add']['x_offset'] = float(self.led_add_label_x_offset.text())
        product_cfg_buf_dic['label_add']['y_offset'] = float(self.led_add_label_y_offset.text())
        product_cfg_buf_dic['label_add']['left_margin'] = float(self.led_add_label_left_margin.text())
        product_cfg_buf_dic['label_add']['right_margin'] = float(self.led_add_label_right_margin.text())
        # 标签
        product_cfg_buf_dic['label']['width'] = float(self.led_label_width.text())
        product_cfg_buf_dic['label']['height'] = float(self.led_label_height.text())

        product_cfg_buf_dic['label']['has_bar_code'] = int(self.ckb_use_barcode.isChecked())
        product_cfg_buf_dic['label']['bar_code_size'] = float(self.led_label_barcode_size.text())
        product_cfg_buf_dic['label']['bar_x_offset'] = float(self.led_label_barcode_x_offset.text())
        product_cfg_buf_dic['label']['bar_y_offset'] = float(self.led_label_barcode_y_offset.text())

        product_cfg_buf_dic['label']['has_qr_code'] = int(self.ckb_use_qrcode.isChecked())
        product_cfg_buf_dic['label']['qr_code_size'] = float(self.led_label_qrcode_size.text())
        product_cfg_buf_dic['label']['qr_x_offset'] = float(self.led_label_qrcode_x_offset.text())
        product_cfg_buf_dic['label']['qr_y_offset'] = float(self.led_label_qrcode_y_offset.text())

        product_cfg_buf_dic['label']['has_hr'] = int(self.ckb_use_hr.isChecked())
        product_cfg_buf_dic['label']['hr_size'] = float(self.led_label_hr_size.text())
        product_cfg_buf_dic['label']['hr_x_offset'] = float(self.led_label_hr_x_offset.text())
        product_cfg_buf_dic['label']['hr_y_offset'] = float(self.led_label_hr_y_offset.text())
        # 保存打印机名
        if self.printer_name_cur_str == '':
            product_cfg_buf_dic['printer_name'] = self.led_printer_name.text()
        else:
            product_cfg_buf_dic['printer_name'] = self.printer_name_cur_str
        tempStr = ''
        if self.beChangeDefaultCfg:
            if float(product_cfg_buf_dic['label']['width']) == 12.0 and float(product_cfg_buf_dic['label']['height']) ==5.5:
                fp = open(self.first_cfg_path, 'w')
                json.dump(product_cfg_buf_dic, fp, indent=4)
                fp.close()
                tempStr = "\n并保存默认配置为:" +format('%s' % self.first_cfg_path)
            elif float(product_cfg_buf_dic['label']['width']) == 37.8 and float(product_cfg_buf_dic['label']['height']) ==16.8:
                fp = open(self.third_cfg_path, 'w')
                json.dump(product_cfg_buf_dic, fp, indent=4)
                fp.close()
                tempStr = "\n并保存默认配置为:" +format('%s' % self.third_cfg_path)
            elif float(product_cfg_buf_dic['label']['width']) == 18.0 and float(product_cfg_buf_dic['label']['height']) == 40.0:
                fp = open(self.second_cfg_path, 'w')
                json.dump(product_cfg_buf_dic, fp, indent=4)
                fp.close()
                tempStr = "\n并保存默认配置为:"+format('%s'%self.second_cfg_path)
            else:
                pass
        try:
            DBproduct.SaveCfgToDB(self.strmacid, self.model_name, self.strstationid, product_cfg_buf_dic)
            QMessageBox.warning(None, 'PASS', '已存入当前配置到'+format('%s.' % self.db_db_param_str)+format('%s中' % self.db_tb_param_str)+tempStr)
            self.btn_quit_config.setEnabled(1)
        except Exception:
            QMessageBox.warning(None, 'Error', '未存入当前产品配置')
            return

    def quitConfigSetting(self):
        #self.destroy()
        self.parent.loadConfig(self.model_name)
        self.close()
        print("quit printe seting dialog")