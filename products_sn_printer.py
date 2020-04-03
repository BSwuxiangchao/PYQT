from PIL import Image as picImage, ImageWin, ImageDraw,ImageFont
from functools import partial
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow,QMenu,QAction,QMessageBox,QInputDialog,QLineEdit
from PyQt5.QtGui import QPainter, QPixmap,QPalette,QColor,QTextCursor
from PyQt5.QtWidgets import  QMainWindow, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt
import Ui.print_sn
import Database.Database
import time
import datetime
import os
#from elaphe.datamatrix import DataMatrix
import qrcode
import  printer_helper
from tkinter import *
import traceback
import print_label_setting
import code128_encode
import json
import win32api
import win32con

global rule_days
rule_days={"01":"1","02":"2","03":"3","04":"4","05":"5","06":"6","07":"7","08":"8","09":"9","10":"A","11":"B",
           "12":"C","13":"D","14":"E","15":"F","16":"G","17":"H","18":"J","19":"K","20":"L","21":"M","22":"N","23":"P",
            "24":"R","25":"S","26":"T","27":"V","28":"W","29":"X","30":"Y","31":"Z"
}
global rule_months
rule_months={"01":"1","02":"2","03":"3","04":"4","05":"5","06":"6","07":"7","08":"8","09":"9","10":"A","11":"B","12":"C"}
import sys


class SnPrinter(QMainWindow, Ui.print_sn.Ui_MainWindow):
    def __init__(self):
        super(SnPrinter, self).__init__()
        self.setupUi(self)
        self.m_dbconfig=  './Config/12.0x5.5_default_cfg.json'
        self.orbbec_logo = 'orbbec.png'
        self.bigImagePath =''
        self.strProductSN =""
        self.strDisplaySN=""
        self.StrShortSN=''
        self.StrVid=''
        self.StrPid=''

        self.printer = printer_helper.printer_helper()

        self.iniUT()
        self.initGraphicsView(self.orbbec_logo)
        self.mydata = Database.Database.LocalDatabase(self.m_dbconfig)
        self.popMeu()

        self.setupConnection()

    # 绑定主窗口按键
    def setupConnection(self):
            self.btn_start.clicked.connect(self.startProductLabelPrint)
            self.btn_test_printer.clicked.connect(self.testPrint)
            self.slider_pre_view.valueChanged.connect(self.changePreViewScale)
            self.checkBox_preScan.stateChanged.connect(self.prescanLabel)
            self.btn_reprint.clicked.connect(self.reprint)

    def iniUT(self):
        self.btn_reprint.setEnabled(0)
        self.btn_start.setEnabled(0)
        self.btn_test_printer.setEnabled(0)

        for i in range(1,10):
            self.comboBox_Lines.addItem(str(i))
        self.comboBox_Lines.setCurrentText("3")


    #从数据库加载产品标签打印配置
    def loadConfig(self,model_name):
        self.data_of_product_cfg_js_dic = Database.Database.GetCfgByDB(self.strMACID,model_name,self.strStationID)
        # 标签
        self.label_width = self.data_of_product_cfg_js_dic['label']['width']
        self.label_height = self.data_of_product_cfg_js_dic['label']['height']

        self.label_has_bar_code = bool(self.data_of_product_cfg_js_dic['label']['has_bar_code'])
        self.label_bar_code_size = self.data_of_product_cfg_js_dic['label']['bar_code_size']
        self.label_bar_code_x_offset = self.data_of_product_cfg_js_dic['label']['bar_x_offset']
        self.label_bar_code_y_offset = self.data_of_product_cfg_js_dic['label']['bar_y_offset']

        self.label_has_qr_code = bool(self.data_of_product_cfg_js_dic['label']['has_qr_code'])
        self.label_qr_code_size = self.data_of_product_cfg_js_dic['label']['qr_code_size']
        self.label_qr_code_x_offset = self.data_of_product_cfg_js_dic['label']['qr_x_offset']
        self.label_qr_code_y_offset = self.data_of_product_cfg_js_dic['label']['qr_y_offset']

        self.label_has_hr_code = bool(self.data_of_product_cfg_js_dic['label']['has_hr'])
        self.label_hr_size = self.data_of_product_cfg_js_dic['label']['hr_size']
        self.label_hr_x_offset = self.data_of_product_cfg_js_dic['label']['hr_x_offset']
        self.label_hr_y_offset = self.data_of_product_cfg_js_dic['label']['hr_y_offset']
        # 打印机
        #self.printer_name_cur_str = "打印驱动（光机电区"
        self.printer_name_cur_str = self.data_of_product_cfg_js_dic['printer_name']
        self.add_label_width = self.data_of_product_cfg_js_dic['label_add']['width']
        self.add_label_height = self.data_of_product_cfg_js_dic['label_add']['height']
        self.add_label_x_offset = self.data_of_product_cfg_js_dic['label_add']['x_offset']
        self.add_label_y_offset = self.data_of_product_cfg_js_dic['label_add']['y_offset']
        self.add_label_left_margin = self.data_of_product_cfg_js_dic['label_add']['left_margin']
        self.add_label_right_margin = self.data_of_product_cfg_js_dic['label_add']['right_margin']

        cfgvalues = json.dumps(self.data_of_product_cfg_js_dic,ensure_ascii=False)
        print(cfgvalues)

    def initGraphicsView(self, img):
        self.pixel_map = QPixmap(img)
        self.grap_scene = QGraphicsScene(self)
        self.pixel_item = QGraphicsPixmapItem(self.pixel_map)
        self.pixel_item.setScale(self.slider_pre_view.value() / (self.slider_pre_view.maximum()*2 / 3))

        self.grap_scene.addItem(self.pixel_item)
        self.gph_view_label.setScene(self.grap_scene)

    def changePreViewScale(self):
        self.pixel_item.setScale(self.slider_pre_view.value() / (self.slider_pre_view.maximum() * 2 / 3))

    def prescanLabel(self,state):
        folder = os.path.exists(self.bigImagePath)
        if folder and state:
            self.initGraphicsView(self.bigImagePath)
            self.printLog("产品标签预览成功..........")
        else:
            if not folder:
                QMessageBox.warning(None,"TIPS","预览图片不存在")
            self.initGraphicsView(self.orbbec_logo)

    def popMeu(self):
        JsonAllProudct = self.mydata.getAllProducts()
        for k in sorted(JsonAllProudct.keys()):
            v = JsonAllProudct[k]
            m_action = QAction(self.m_menu)
            subsubmenu = QMenu()
            self.m_menu.addAction(m_action)
            parentname = k
            for pitem in v:
                m_subAdd = QAction(subsubmenu)
                m_subAdd.setText(pitem["product_name"])
                subsubmenu.addAction(m_subAdd)
                m_subAdd.triggered.connect(
                    partial(self.show_seting_dialog, pitem["product_name"], pitem["model_name"]))
                m_subAdd.triggered.connect(
                    partial(self.triggeredOpenConfigWnd,pitem["product_name"], pitem["model_name"]))
                if k == pitem["model_name"]:
                    parentname = pitem["product_name"]
            m_action.setText(parentname)
            m_action.setMenu(subsubmenu)

    def show_seting_dialog(self,product_name,model_name):
        self.strMACID = self.mydata.GetMACID()
        self.strStationID = self.mydata.GetStationID()
        print("MACID:", self.strMACID)
        print("StationID:", self.strStationID)
        self.configwnd = print_label_setting.PrintLabelSetting(self, product_name,model_name,self.strMACID,self.strStationID)
        self.configwnd.setWindowModality(Qt.ApplicationModal)
        self.configwnd.setWindowFlags(self.configwnd.windowFlags() & ~Qt.WindowCloseButtonHint & ~Qt.WindowMaximizeButtonHint & ~Qt.WindowMinimizeButtonHint)
        self.configwnd.show()

    def triggeredOpenConfigWnd(self,product_name,model_name):
        #if self.configwnd.exec():
        self.ted_log.clear()
        self.btn_start.setEnabled(1)
        self.btn_test_printer.setEnabled(1)
        self.initGraphicsView(self.orbbec_logo)
        self.product_name = product_name
        self.label_products.setText(product_name)
        self.StrShortSN, self.StrVid, self.StrPid, self.strID = self.mydata.GetShortSNByDB(model_name)
        print("ProductID:",self.strID)
        if self.StrShortSN == '':
            QMessageBox.warning(None, 'Error', '产品主版本号为空，请检查数据库')
            return
        self.label_label.setText("主版本号:")
        self.label_sortSN.setText(self.StrShortSN)

        self.curLabelPath = '.\\Code\\' + format('%s\\' % self.product_name)
        self.bigImagePath = self.curLabelPath + format('%s' % self.product_name) + 'currentImag.png'

    def getMainSN(self):
        date_year= time.strftime('%Y', time.localtime())
        date_month= time.strftime('%m', time.localtime())
        date_day= time.strftime('%d', time.localtime())
        strLines = self.comboBox_Lines.currentText()
        strProductSN =self.StrShortSN+rule_days[date_day]+rule_months[date_month]+str(int(date_year)%10)+strLines
        strDisplaySN =self.StrShortSN+rule_days[date_day]+rule_months[date_month]+'\n'+str(int(date_year)%10)+strLines
        return strProductSN,strDisplaySN

    def generate_print_img(self,tempProductSN,tempDisplaySN,tempIndex,tempStartIndex):
        # faw
        _WIDTH = self.add_label_width
        _HEIGHT = self.add_label_height
        _XOFFSET = self.add_label_x_offset
        _YOFFSET = self.add_label_y_offset
        _LMARGIN = self.add_label_left_margin
        _RMARGIN = self.add_label_right_margin

        _LABELWIDTH = self.label_width
        _LABELHIGHT = self.label_height

        _HAS_BAR = self.label_has_bar_code
        _BARSIZE = self.label_bar_code_size
        _BARXOFFSET = self.label_bar_code_x_offset
        _BARYOFFSET = self.label_bar_code_y_offset

        _HAS_QR = self.label_has_qr_code
        _QRSIZE = self.label_qr_code_size
        _QRXOFFSET = self.label_qr_code_x_offset
        _QRYOFFSET = self.label_qr_code_y_offset

        _HAS_HR = self.label_has_qr_code
        _HRSIZE = self.label_hr_size
        _HRXOFFSET = self.label_hr_x_offset
        _HRYOFFSET = self.label_hr_y_offset

        tempQRPath = self.curLabelPath
        tempQRPath += format('curProductLabel.png')

        tempImg = picImage.new('RGB', (
        self.printer.mm_to_pixel(float(_LABELWIDTH), 0), self.printer.mm_to_pixel(float(_LABELHIGHT), 1)),
                               (255, 255, 255))
        tempImgDraw = ImageDraw.Draw(tempImg)
        if (int(_HAS_BAR) == 1):
            font_hr_text = ImageFont.truetype('./font/code128.ttf', int(_BARSIZE))
            barcode = code128_encode.code128_encode()
            encode = barcode.encode(tempProductSN)
            tempImgDraw.text((self.printer.mm_to_pixel(float(_HRXOFFSET), 0),
                              self.printer.mm_to_pixel(float(_HRYOFFSET), 1)),
                             encode, font=font_hr_text, fill=256)
        if (int(_HAS_QR) == 1):
            qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(tempProductSN)
            qr.make(fit=True)
            qr_img = qr.make_image()
            qr_img.save(self.curLabelPath + '/qr_temp_no_src.png', 'PNG')
            imgdm = picImage.open(self.curLabelPath + '/qr_temp_no_src.png')
            imgdm = imgdm.resize((int(_QRSIZE), int(_QRSIZE)))
        if (int(_HAS_HR) == 1):
            tempImg.paste(imgdm,(self.printer.mm_to_pixel(float(_QRXOFFSET), 0), self.printer.mm_to_pixel(float(_QRYOFFSET), 1)))
            font_hr_text = ImageFont.truetype('./font/arial.ttf', int(_HRSIZE))
            tempImgDraw.text((self.printer.mm_to_pixel(float(_HRXOFFSET), 0),
                              self.printer.mm_to_pixel(float(_HRYOFFSET), 1)),
                             tempDisplaySN,font=font_hr_text, fill=256)
        tempImg.save(tempQRPath)

        try:
            self.printer.do_printer(tempQRPath, self.add_label_x_offset, self.add_label_x_offset,
                                    self.add_label_width, self.add_label_height)
        except Exception:
            #QMessageBox.warning(None, 'Error', '打印失败，请点击“接着打印"')
            self.printLog("标签打印失败............")
            print(traceback.format_exc())
            return -1

        temp_WIDTH = 1
        gap = 0.5
        self.todayImg.paste(tempImg,
                            (self.printer.mm_to_pixel(float(1 + (tempIndex) % temp_WIDTH * (_LABELWIDTH)), 0),
                             self.printer.mm_to_pixel(float(3 + (tempIndex) // temp_WIDTH * (_LABELHIGHT + gap)), 1)))
        self.img.paste(tempImg, (
        self.printer.mm_to_pixel(float(1 + (tempIndex - tempStartIndex) % temp_WIDTH * (_LABELWIDTH)), 0),
        self.printer.mm_to_pixel(float(1 + (tempIndex - tempStartIndex) // temp_WIDTH * (_LABELHIGHT + gap)), 1)))
        return 0

    def startProductLabelPrint(self):
        if self.StrShortSN=='':
            QMessageBox.warning(None, 'Error',  '请选择产品')
            return
        self.printer.open_printer(self.printer_name_cur_str)
        #self.printer.open_printer("打印驱动（光机电区）")
        self.ted_log.clear()
        self.strProductSN, self.strDisplaySN = self.getMainSN()

        strOutput = self.lineEdit_output.text()
        Material_number =''
        Material_number =self.lineEdit_materialNum.text()
        if strOutput =='':
            QMessageBox.warning(None, 'Error', '请输入产量')
            self.lineEdit_output.clear()
            return
        if not strOutput.isdigit():
            QMessageBox.warning(None, 'Error', '只能输入正整数')
            self.lineEdit_output.clear()
            return
        if int(strOutput) not in range(1,100001):
            QMessageBox.warning(None, 'Error',  '输入产量有误，区间（0，10000）')
            self.lineEdit_output.clear()
            return
        if int(strOutput) >= 1000:
            QMessageBox.warning(None, 'wait.....', '过程时间有点长，请稍等')
        self.printLog("产品标签准备打印..........")
        self.pgb_print_progress.setMaximum(int(strOutput))
        #打印机
        self._WIDTH = self.add_label_width
        self._HIGHT = self.add_label_height
        folder = os.path.exists(self.curLabelPath)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(self.curLabelPath)
        self.todaybg_path = self.curLabelPath + datetime.datetime.now().strftime('%Y%m%d') + 'ProductImag.png'
        font_hr_text = ImageFont.truetype('./font/arial.ttf', int(50))
        self.mydata.conect2mft_database()
        maxSN = self.mydata.getMaxSN(self.strID)
        if maxSN == 0:
            self.first_startIndex =int(maxSN)
        else:
            maxSN = maxSN[-4:]
            self.first_startIndex = int(maxSN)+1
        self.first_endIndex = self.first_startIndex +int(strOutput)
        self.strOutput = strOutput
        print("maxSN:", maxSN)

        if (self.todaybg_path == 'NULL' or len(self.todaybg_path) == 0 or not os.path.exists(self.todaybg_path)):
            self.todayImg = picImage.new('RGB', (self.printer.mm_to_pixel(float(self._WIDTH), 0),
                                                 self.printer.mm_to_pixel(float(self._HIGHT*int(strOutput)*3), 1)),(144,144,144))
            self.todayImgDraw = ImageDraw.Draw(self.todayImg)
            self.todayImgDraw.text((self.printer.mm_to_pixel(float(0), 0),
                                    self.printer.mm_to_pixel(float(0), 1)),
                                   self.product_name, font=font_hr_text, fill=256)
        else:
            self.todayImg = picImage.open(self.todaybg_path)

        self.img = picImage.new('RGB', (
        self.printer.mm_to_pixel(float(self._WIDTH), 0), self.printer.mm_to_pixel(float(self._HIGHT*int(strOutput)), 1)),
                                (144,144,144))


        self.material_id = self.mydata.getMaterialId(Material_number)
        #生成的SN存入数据库
        already_generateSN_nums =0
        for i in range(self.first_startIndex, self.first_endIndex):
            tempProductSN = self.strProductSN
            tempProductSN += format('%04d' % i)
            try:
                self.mydata.saveSNtoDB(self.strID, tempProductSN,self.material_id)
                already_generateSN_nums = already_generateSN_nums + 1
            except Exception:
                QMessageBox.warning(None, 'Warming', "已生成" + format(' %d 个SN,' % already_generateSN_nums) + format('还剩 %d 个未生成' %(int(strOutput)-already_generateSN_nums)))
                break
        self.mydata.close2mft_database()
        if already_generateSN_nums < 1:
            QMessageBox.warning(None,"ERROR","请确保能正常进入数据库")
            return
        if already_generateSN_nums <int(strOutput):
            self.printLog("已生成" + format(' %d 个SN,' % already_generateSN_nums) + format(
                '还剩 %d 个未生成' % (int(strOutput) - already_generateSN_nums)))
        if already_generateSN_nums == int(strOutput):
            self.printLog("SN生成完毕.................")
            print("SN生成完毕.................")
        self.already_generateSN_nums = already_generateSN_nums
        #打印SN
        self.second_endIndex = self.first_startIndex + already_generateSN_nums
        already_print_nums = 0
        for j in range(self.first_startIndex,self.second_endIndex):
            tempProductSN = self.strProductSN
            tempProductSN += format('%04d' % j)
            tempDisplaySN = self.strDisplaySN
            tempDisplaySN += format('%04d' % j)
            print(tempDisplaySN)
            if self.generate_print_img(tempProductSN,tempDisplaySN,j,self.first_startIndex) < 0:
                break
            already_print_nums = already_print_nums + 1
            self.pgb_print_progress.setValue(already_print_nums)

        self.already_print_nums = already_print_nums

        self.img.save(self.bigImagePath, 'PNG')
        self.todayImg.save(self.todaybg_path,'PNG')
        if already_print_nums == int(strOutput):
            self.printLog(format('%d 个'%int(already_print_nums))+"产品标签已打印完毕...........")
        else:
            QMessageBox.warning(None,"Warning","未打印完毕，请点击“接着打印")
            self.printLog("还有"+format('%d 个产品标签未打印'%(int(strOutput) - int(already_print_nums))))
            self.btn_reprint.setEnabled(1)

        self.prescanLabel(1)
        self.btn_start.setEnabled(0)

    def reprint(self):
        if self.already_generateSN_nums == int(self.strOutput):
            self.printLog("产品SN已生成完毕..........")
        else:
            self.mydata.conect2mft_database()
            already_generateSN_nums = self.already_generateSN_nums
            count_reGenerateSN_nums = 0
            for i in range(self.first_startIndex + self.already_generateSN_nums , self.first_endIndex):
                tempProductSN = self.strProductSN
                tempProductSN += format('%04d' % i)
                try:
                    self.mydata.saveSNtoDB(self.strID, tempProductSN, self.material_id)
                    self.already_generateSN_nums = self.already_generateSN_nums + 1
                    count_reGenerateSN_nums = count_reGenerateSN_nums + 1
                except Exception:
                    QMessageBox.warning(None, 'Warming', "已生成" + format(' %d 个SN,' % self.already_generateSN_nums) + format(
                    '还剩 %d 个未生成' % (int(self.strOutput) - self.already_generateSN_nums)))
                    self.printLog("已生成" + format(' %d 个SN,' % self.already_generateSN_nums) + format(
                    '还剩 %d 个未生成' % (int(self.strOutput) - self.already_generateSN_nums)))
                    break
            self.mydata.close2mft_database()
            if already_generateSN_nums == self.already_generateSN_nums:
                QMessageBox.warning(None, "ERROR", "请确保能正常进入数据库")
                return
            if self.already_generateSN_nums <int(self.strOutput):
                print("已生成" + format(' %d 个SN,' % self.already_generateSN_nums) + format(
                    '还剩 %d 个未生成' % (int(self.strOutput) - self.already_generateSN_nums)))
            if self.already_generateSN_nums == int(self.strOutput):
                self.printLog("SN生成完毕.................")
        if self.already_print_nums == int(self.strOutput):
            self.printLog("产品SN已打印完毕..........")
        else:
            self.todayImg = picImage.open(self.todaybg_path)
            self.img = picImage.open(self.bigImagePath)
            startIndex = self.first_startIndex+self.already_print_nums
            if self.already_generateSN_nums == int(self.strOutput):
                endIndex = self.second_endIndex
            else:
                endIndex = self.second_endIndex + count_reGenerateSN_nums
            for j in range(startIndex,endIndex):
                tempProductSN = self.strProductSN
                tempProductSN += format('%04d' % j)
                tempDisplaySN = self.strDisplaySN
                tempDisplaySN += format('%04d' % j)
                print(tempDisplaySN)
                if self.generate_print_img(tempProductSN, tempDisplaySN, j, self.first_startIndex) < 0:
                    break
                self.already_print_nums = self.already_print_nums + 1
                self.pgb_print_progress.setValue(self.already_print_nums)
            self.img.save(self.bigImagePath, 'PNG')
            self.todayImg.save(self.todaybg_path, 'PNG')
            if self.already_print_nums == int(self.strOutput):
                self.printLog(format(' %d 个' % int(self.already_print_nums)) + "产品标签已打印完毕...........")
                self.btn_reprint.setEnabled(FALSE)

            else:
                QMessageBox.warning(None, "Warning", "未打印完毕，请点击“接着打印")
                self.printLog("还有 " + format('%d 个产品标签未打印' % (int(self.strOutput) - int(self.already_print_nums))))
            self.prescanLabel(1)

    def print_testimg(self,tempProductSN,tempDisplaySN):
        # faw
        _WIDTH = self.add_label_width
        _HEIGHT = self.add_label_height
        _XOFFSET = self.add_label_x_offset
        _YOFFSET = self.add_label_y_offset
        _LMARGIN = self.add_label_left_margin
        _RMARGIN = self.add_label_right_margin

        _LABELWIDTH = self.label_width
        _LABELHIGHT = self.label_height

        _HAS_BAR = self.label_has_bar_code
        _BARSIZE = self.label_bar_code_size
        _BARXOFFSET = self.label_bar_code_x_offset
        _BARYOFFSET = self.label_bar_code_y_offset

        _HAS_QR = self.label_has_qr_code
        _QRSIZE = self.label_qr_code_size
        _QRXOFFSET = self.label_qr_code_x_offset
        _QRYOFFSET = self.label_qr_code_y_offset

        _HAS_HR = self.label_has_qr_code
        _HRSIZE = self.label_hr_size
        _HRXOFFSET = self.label_hr_x_offset
        _HRYOFFSET = self.label_hr_y_offset

        tempQRPath = self.curLabelPath
        tempQRPath += format('curProductLabel.png')

        tempImg = picImage.new('RGB', (
            self.printer.mm_to_pixel(float(_LABELWIDTH), 0), self.printer.mm_to_pixel(float(_LABELHIGHT), 1)),
                               (255, 255, 255))
        tempImgDraw = ImageDraw.Draw(tempImg)
        if (int(_HAS_BAR) == 1):
            font_hr_text = ImageFont.truetype('./font/code128.ttf', int(_BARSIZE))
            barcode = code128_encode.code128_encode()
            encode = barcode.encode(tempProductSN)
            tempImgDraw.text((self.printer.mm_to_pixel(float(_HRXOFFSET), 0),
                              self.printer.mm_to_pixel(float(_HRYOFFSET), 1)),
                             encode, font=font_hr_text, fill=256)
        if (int(_HAS_QR) == 1):
            qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(tempProductSN)
            qr.make(fit=True)
            qr_img = qr.make_image()
            qr_img.save(self.curLabelPath + '/qr_temp_no_src.png', 'PNG')
            imgdm = picImage.open(self.curLabelPath + '/qr_temp_no_src.png')
            imgdm = imgdm.resize((int(_QRSIZE), int(_QRSIZE)))
        if (int(_HAS_HR) == 1):
            tempImg.paste(imgdm, (
                self.printer.mm_to_pixel(float(_QRXOFFSET), 0), self.printer.mm_to_pixel(float(_QRYOFFSET), 1)))
            font_hr_text = ImageFont.truetype('./font/arial.ttf', int(_HRSIZE))
            tempImgDraw.text((self.printer.mm_to_pixel(float(_HRXOFFSET), 0),
                              self.printer.mm_to_pixel(float(_HRYOFFSET), 1)),
                             tempDisplaySN, font=font_hr_text, fill=256)
        tempImg.save(tempQRPath)
        testMsg = picImage.new('RGB', (
            self.printer.mm_to_pixel(float(self.add_label_width), 0),
            self.printer.mm_to_pixel(float(self.add_label_height * 1), 1)),
                                (144, 144, 144))
        testMsg.paste(tempImg, (self.printer.mm_to_pixel(float(1), 0),
            self.printer.mm_to_pixel(float(1), 1)))
        testMsg.save(self.bigImagePath)
        self.initGraphicsView(self.bigImagePath)

        try:
            self.printer.do_printer(tempQRPath, self.add_label_x_offset, self.add_label_x_offset,
                                    self.add_label_width, self.add_label_height)
        except Exception:
            # QMessageBox.warning(None, 'Error', '打印失败，请点击“接着打印"')
            self.printLog("标签打印失败............")
            print(traceback.format_exc())
            return -1

    def testPrint(self):
        opN, okPressed = QInputDialog.getText(self, "权限管理", "请输入权限密码:", QLineEdit.Password, "")
        if not okPressed :
            QMessageBox.warning(None, 'Error', '取消打印测试')
            self.printLog("取消打印测试..........")
            return
        if opN != '5':
            QMessageBox.warning(None, 'Error', '权限密码错误')
            self.printLog("权限密码错误..........")
            return
        if self.StrShortSN == '':
            QMessageBox.warning(None, 'Error', '请选择产品')
            return
        self.printer.open_printer(self.printer_name_cur_str)
        self.ted_log.clear()
        strProductSN, strDisplaySN = self.getMainSN()
        self.printLog("产品标签打印测试开始..........")
        folder = os.path.exists(self.curLabelPath)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(self.curLabelPath)
        j = 1
        strDisplaySN += format('%04d' % j)
        strProductSN += format('%04d' % j)
        print(strDisplaySN)
        self.print_testimg(strProductSN,strDisplaySN)
        win32api.MessageBox(0,"标签打印测试结束", "提示", win32con.MB_SERVICE_NOTIFICATION)
        self.printLog("产品标签打印测试结束..........")

    def printLog(self, log):
        strLog = self.ted_log.toPlainText() + log+'\n'
        self.ted_log.setPlainText(strLog)

import sys

if __name__ == '__main__':

    app = QApplication(sys.argv)

    print(sys.getdefaultencoding())
    mainWindow = SnPrinter()
    mainWindow.show()
    sys.exit(app.exec())