# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import  QMainWindow, QMessageBox
import os
import json
import mysql.connector
import configparser
from threading import Thread
import time
import uuid
import  wmi
import hashlib
import hashlib
import pymysql
from copy import deepcopy
import win32api
import win32con

global g_MacID
g_MacID=""
global g_StationID
g_StationID=-1

def GetCfgByDB(strmacid, model_name,strstationid,default_cfg_dic=None,bautocopy=True):
    jsoncfg = {}
    md5id = hashlib.md5((strmacid + '_' + model_name).encode("utf-8")).hexdigest().upper()
    cnx = pymysql.connect(user="orbdatamgr", password="orbbec20180724", host="db.orbbecdata.com",
                                  database="mft_params",
                                  port=3306, charset='utf8', use_unicode=True)
    cursor = cnx.cursor()
    sqlStr = "SELECT data FROM `product_label_cfg` WHERE `ID`='{0}' ".format(md5id)
    cursor.execute(sqlStr)
    results = cursor.fetchall()
    if len(results) > 0:
        for ret in results:
            jsoncfg = json.loads((ret[0]))
    else:
        win32api.MessageBox(0, "请选择标签尺寸并确保有本地默认配置", "提示", win32con.MB_SERVICE_NOTIFICATION)
        jsoncfg = -1
    cursor.close()
    cnx.close()
    return jsoncfg
def SaveCfgToDB(strmacid,model_name,stationid,jcfgvalue):
    md5id = hashlib.md5((strmacid + '_' + model_name).encode("utf-8")).hexdigest().upper()
    cnx = pymysql.connect(user="orbdatamgr", password="orbbec20180724", host="db.orbbecdata.com", database="mft_params", port=3306, charset='utf8', use_unicode=True)
    cursor = cnx.cursor()
    jdmupvalue = json.dumps(jcfgvalue, ensure_ascii=False)
    #sqlStr = "INSERT INTO product_sn_cfg(`ID`, `MACID`,`CFGNAME`,`DATA`,`TIME`,`STATIONID`) VALUES('{0}','{1}','{2}', (JSON_EXTRACT('{3}','$')),now(),'66') on duplicate key update TIME=now(), daDATA =  (JSON_EXTRACT('{4}','$'));"
    sqlStr = "INSERT INTO product_label_cfg(`ID`, `MACID`,`CFGNAME`,`DATA`,`TIME`,`STATIONID`) VALUES('{0}','{1}','{2}',(JSON_EXTRACT('{3}','$')),now(),'{4}') on duplicate key update TIME=now(), DATA =(JSON_EXTRACT('{5}','$'));".format(
        md5id,strmacid,model_name,jdmupvalue,stationid,jdmupvalue )
    cursor.execute(sqlStr)
    cnx.commit()
    cursor.close()
    cnx.close()
def CheckSaveTable(strSaveDB,strSaveTable,strSrcTable):
    cnx = pymysql.connect(user="orbdatamgr", password="orbbec20180724", host="db.orbbecdata.com",
                                  database=strSaveDB, port=3306, charset='utf8', use_unicode=True)
    cursor = cnx.cursor()
    sqlStr = "SELECT count(1) FROM information_schema.TABLES WHERE TABLE_NAME = '{0}' AND TABLE_SCHEMA='{1}';".format(
        strSaveTable,strSaveDB)
    cursor.execute(sqlStr)
    results = cursor.fetchall()
    bExistTable = False
    if len(results) > 0:
        for ret in results:
            bExistTable = ret[0] == 1

    if not bExistTable:
        sqlStr = "CREATE TABLE `{0}`.`{1}` LIKE `{2}`.`{3}`;".format(
            strSaveDB,strSaveTable,strSaveDB,strSrcTable)
        cursor.execute(sqlStr)
    cursor.close()
    cnx.close()

class LocalDatabase():
    def __init__(self,configFile):
        if not os.path.exists(configFile):
            QMessageBox(configFile + '路径不存在')
            return
        self.configFile =configFile

        # 载入配置
        self.loadConfig()


    def loadConfig(self):
        fp = open(self.configFile, 'r', encoding='utf_8_sig')
        self.data_of_selected_product_cfg_js_dic = json.load(fp)
        fp.close()
        # 数据库
        self.db_ip_str = self.data_of_selected_product_cfg_js_dic['database']['host']
        self.db_user_str = self.data_of_selected_product_cfg_js_dic['database']['user']
        self.db_pw_str = self.data_of_selected_product_cfg_js_dic['database']['pw']
        self.db_port_str = self.data_of_selected_product_cfg_js_dic['database']['port']
        self.db_param_str = self.data_of_selected_product_cfg_js_dic['database']['db_param']
        self.tb_param_str = self.data_of_selected_product_cfg_js_dic['database']['tb_param']
        self.db_result_str = self.data_of_selected_product_cfg_js_dic['database']['db_reslt']
        self.tb_result_str = self.data_of_selected_product_cfg_js_dic['database']['tb_reslt']




    def getAllProducts(self):
        print('access in database 1')
        JsonAllProduct = {}
        sqlStr = "SELECT model_name,product_name,short_sn,parent FROM `model` ;"
        cnx = mysql.connector.connect(user=self.db_user_str, password=self.db_pw_str,
                                                  host=self.db_ip_str,
                                                  database=self.db_param_str,
                                                  port=self.db_port_str)
        cursor = cnx.cursor()

        cursor.execute(sqlStr)
        results = cursor.fetchall()
        for ret in results:
            if not ret[3] in JsonAllProduct:
                JsonAllProduct[ret[3]] = []
            JsonTemp = {}
            JsonTemp["model_name"] = ret[0]
            JsonTemp["short_sn"] = ret[2]
            JsonTemp["product_name"] = ret[1]
            JsonTemp["parent"] = ret[3]
            JsonAllProduct[ret[3]].append(JsonTemp)
        cnx.close()
        cursor.close()
        return JsonAllProduct

    def GetShortSNByDB(self,model_name):
        StrShortSN = ""
        StrPid = ""
        StrVid = ""
        strID = ""
        cnx = mysql.connector.connect(user=self.db_user_str, password=self.db_pw_str, host=self.db_ip_str,
                                      database=self.db_param_str,
                                      port=self.db_port_str)
        cursor = cnx.cursor()
        sqlStr = "SELECT short_sn,vid,pid,id FROM `mft_params`.`model` WHERE model_name='{0}' ;".format(model_name)
        cursor.execute(sqlStr)
        results = cursor.fetchall()
        for ret in results:
            StrShortSN = ret[0]
            StrVid = ret[1]
            StrPid = ret[2]
            strID = ret[3]
        cursor.close()
        cnx.close()
        return StrShortSN, StrVid, StrPid,strID

    def GetMACID(self):
        global g_MacID
        if len(g_MacID) > 0:
            return g_MacID
        encrypt_str = ""
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        w = wmi.WMI()
        cpus = w.Win32_Processor()
        for u in cpus:
            encrypt_str = encrypt_str + u.ProcessorId.strip()
        encrypt_str += mac
        g_MacID = hashlib.md5(encrypt_str.encode("utf-8")).hexdigest().upper()
        return g_MacID

    def GetStationID(self):
        global g_StationID
        if g_StationID > -1:
           return g_StationID
        cnx =  mysql.connector.connect(user=self.db_user_str, password=self.db_pw_str, host=self.db_ip_str,
                                      database=self.db_param_str,
                                      port=self.db_port_str)
        cursor = cnx.cursor()
        strSQL = "SELECT ID FROM `station_info` WHERE `MACID`='{0}' AND `APPNAME`='pre_printer' ".format(
            self.GetMACID())
        cursor.execute(strSQL)
        results = cursor.fetchall()
        for ret in results:
            g_StationID = ret[0]
        if g_StationID == -1:
            strSQL2 = "INSERT INTO `mft_params`.`station_info` (`MACID`, `APPNAME`) VALUES ('{0}', 'pre_printer');".format(
                self.GetMACID())
            cursor.execute(strSQL2)
            cnx.commit()
            cursor.execute(strSQL)
            results = cursor.fetchall()
            for ret in results:
                g_StationID = ret[0]
        cursor.close()
        cnx.close()
        return g_StationID


    def conect2mft_database(self):
        self.cnx_result = mysql.connector.connect(user=self.db_user_str, password=self.db_pw_str,
                                                  host=self.db_ip_str,
                                                  database=self.db_result_str,
                                                  port=self.db_port_str)
        self.cursor_result = self.cnx_result.cursor()

    def getMaterialId(self,material_num):
        sqlStr = "INSERT INTO pmaterial_info(material_num) select '{0}'from DUAL " \
                 "where not EXISTS(select material_num from pmaterial_info where material_num='{1}');" \
            .format(material_num, material_num)
        self.cursor_result.execute(sqlStr)
        self.cnx_result.commit()
        sqlStr = "select id from pmaterial_info where material_num = '{0}';".format(material_num)
        self.cursor_result.execute(sqlStr)
        results = self.cursor_result.fetchall()
        for res in results:
            material_id = res[0]
        return material_id

    def saveSNtoDB(self,model_id,SN,material_id):
        sqlStr = "INSERT INTO products_sn (MODEL_ID,SN,generate_time,material_id)" \
                 " VALUES ('{0}','{1}',now(),'{2}') on duplicate key update SN ='{3}'"\
            .format(model_id,SN,material_id,SN)
        self.cursor_result.execute(sqlStr)


    def getMaxSN(self,model_id):
        try:
            sqlStr = "SELECT MAX(SN) FROM products_sn WHERE MODEL_ID = '{0}' and TO_DAYS(NOW()) -TO_DAYS(generate_time) =0 ".format(model_id)
            self.cursor_result.execute(sqlStr)
            results = self.cursor_result.fetchall()
        except Exception:
            QMessageBox.warning(None, 'getMaxSN Error',  'sql execute fail')
            return
        for res in results:
             maxsn = res[0]
        if res[0]:
            return maxsn
        else:
            return 0

    def close2mft_database(self):
        self.cnx_result.commit()
        self.cursor_result.close()
        self.cnx_result.close()