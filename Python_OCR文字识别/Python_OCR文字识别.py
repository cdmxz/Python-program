#-*- coding:utf-8 -*-
'''
        此为桌面GUI程序，不能在浏览器使用，请下载到电脑并安装必备的库后使用海龟编辑器运行。
开源地址：https://cdmxz.github.io
已在 win10 2004 + python3.8 32bit 环境下测试过，可正常使用。
使用前请安装必备的库：PIL、windnd、requests。
'''

import ctypes
import os
import hashlib
import sys
import inspect
import winsound   # 播放wav文件
import wave
import contextlib # 获取wav文件时长
import threading  # 多线程
import datetime   # 获取当前时间
import requests   # HTTP库
import base64     # base64编码解码
import json       # 解析json数据
import tkinter.messagebox # 弹窗
import tkinter.filedialog # 选择文件对话框
import tkinter as tk      # 图形界面
import time               # 休眠
import windnd             # 文件拖动
import winreg             # 读取注册表
from urllib  import request,parse
from pathlib import Path  # 获取当前目录
from tkinter import *     # 图形界面
from tkinter.ttk import *
from PIL import ImageGrab # 读取剪切板

#  全局变量
g_playSound = winsound.PlaySound(None, winsound.SND_NODEFAULT)
g_playMusic = False
g_speechThread = threading.Thread()


'''
由于申请的是免费api并且多人共用，
可能会出现识别失败的情况，
推荐自己去百度ai开放平台（https://ai.baidu.com/）申请key。
'''


# 文字识别Key（可以去百度ai开放平台（https://ai.baidu.com/tech/ocr/general）申请key）
OCR_API_KEY = "YaOhBFsug5GySthCpUFtLkQk"
OCR_SECRET_KEY = "mqP7OOO9t0h9GvipdQe1weRld3SGQokV"

# 语音合成Key（可以去百度ai开放平台（https://ai.baidu.com/tech/speech/tts_online）申请key）
TTS_APP_ID = "19685928"
TTS_API_KEY = "qk3y9G2FQLrQsCa9v9NzzW8h"
TTS_SECRET_KEY = "qtYsvvdEGgQ6EzxVSFuYRvl8NmzVihy1"

# 翻译Key（可以去百度翻译开放平台（https://api.fanyi.baidu.com/product/11）申请key）
TRAN_APP_ID = "20200424000429104"
TRAN_KEY = "5mzyraBsLRk2yfGQMhXJ"

def IsEmpty(Str):
    " 如果字符串的值是None或""，则返回true "
    if Str == None or Str == "":
        return True
    else:
        return False


class  OCR:
    '''文字识别类'''
    def __init__(self, OCR_AK, OCR_SK,TRAN_ID,TRAN_KEY):
        self.OCR_AK = OCR_AK
        self.OCR_SK = OCR_SK
        self.TRAN_ID = TRAN_ID
        self.TRAN_KEY = TRAN_KEY
        self.ocr_Token = self.GetAccessToken()

    def GetAccessToken(self):
        "获取文字识别AccessToken"
        try:
            host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.OCR_AK + '&client_secret=' + self.OCR_SK
            r = requests.get(host).json()
            result = r.get("access_token")
            if IsEmpty(result):
                raise Exception(r.get("error_description"))
            else:
                return result
        except Exception as e:
            messagebox.showerror("OCR文字识别","获取文字识别Token失败！\n原因：" + str(e.args[0]))
            return None

    def GeneralBasic(self,filePath,lang_type,detect_dire):
        "通用文字识别\n\
    filePath    图片路径\n\
    lang_type   要识别的语言类型\n\
    detect_dire 是否检测图片朝向"

        try:
            if detect_dire == '0':
                detect_dire = 'false'
            else:
                detect_dire = 'true'
        # 如果有一项参数为空
            if IsEmpty(filePath) or IsEmpty(lang_type) or IsEmpty(detect_dire):
                raise Exception("输入参数不正确！")

            # 判断文件是否存在
            if not os.path.exists(filePath):
                raise Exception("文件不存在！")

            # 获取AccessToken
            access_token = self.ocr_Token
            if access_token == None:
                access_token = self.GetAccessToken()

            if IsEmpty(access_token):
                return ''
                #raise Exception("获取AccessToken失败！")

            # 通用文字识别
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

            # 二进制方式打开图片文件
            file = open(filePath, 'rb')
            # base64编码
            img = base64.b64encode(file.read())

            params = {"image":img,"language_type":lang_type,"detect_direction":detect_dire}
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
    
            if response:
                r = response.json()
                # 如果返回的json数据有“error_msg”
                if r.get("error_msg") != None:
                    raise Exception(r.get("error_msg"))
                word = ""
                for result in r.get("words_result"):
                    word+=result["words"] + "\n" 

                return word.rstrip('\n') # 删除掉最后面的'\n'字符

        except Exception as e:
                #print(e)
                return e  

    def AccurateBasic(self,filePath,lang_type,detect_dire):
        "通用文字识别（高精度版）\n\
    filePath    图片路径\n\
    lang_type   要识别的语言类型\n\
    detect_dire 是否检测图片朝向"

        try:
            if detect_dire == '0':
                detect_dire = 'false'
            else:
                detect_dire = 'true'
            # 如果有一项参数为空
            if IsEmpty(filePath) or IsEmpty(lang_type) or IsEmpty(detect_dire):
                raise Exception("输入参数不正确！")

            # 判断文件是否存在
            if not os.path.exists(filePath):
                raise Exception("文件不存在！")

            # 获取AccessToken
            access_token = self.ocr_Token
            if access_token == None:
                access_token = self.GetAccessToken()

            if IsEmpty(access_token):
                return ''
                #raise Exception("获取AccessToken失败！")

            # 通用文字识别（高精度版）
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

            # 二进制方式打开图片文件
            file = open(filePath, 'rb')
            # base64编码
            img = base64.b64encode(file.read())

            params = {"image":img,"language_type":lang_type,"detect_direction":detect_dire}
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                r = response.json()
                # 如果返回的json数据有“error_msg”
                if r.get("error_msg") != None:
                    raise Exception(r.get("error_msg"))
                word = ""
                for result in r.get("words_result"):
                    word+=result["words"] + "\n"

                return word.rstrip('\n') # 删除掉最后面的'\n'字符

        except Exception as e:
            #print(e)
            return e

    def Handwriting(self,filePath):
        "手写文字识别\n\
    filePath图片路径"

        try:
            # 如果有一项参数为空
            if IsEmpty(filePath):
                raise Exception("输入参数不正确！")

            # 判断文件是否存在
            if not os.path.exists(filePath):
                raise Exception("文件不存在！")

            # 获取AccessToken
            access_token = self.ocr_Token
            if access_token == None:
                access_token = self.GetAccessToken()

            if IsEmpty(access_token):
                return ''
                #raise Exception("获取AccessToken失败！")

            # 手写文字识别
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"

            # 二进制方式打开图片文件
            file = open(filePath, 'rb')
            # base64编码
            img = base64.b64encode(file.read())

            params = {"image":img}
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                r = response.json()
            # 如果返回的json数据有“error_msg”
            if r.get("error_msg") != None:
                raise Exception(r.get("error_msg"))
            word = ""
            for result in r.get("words_result"):
                word+=result["words"] + "\n"

            return word.rstrip('\n') # 删除掉最后面的'\n'字符

        except Exception as e:
                #print(e)
                return e

    # 将识别后返回的 数字信息 转换为 中文信息
    def GetIdcard_number_type(self,number):
        if number == - 1:
            return "身份证正面所有字段全为空"
        elif number == 0:
            return "身份证证号识别错误"
        elif number == 1:
            return "身份证证号和性别、出生信息一致"
        elif number == 2:
            return "身份证证号和性别、出生信息都不一致"
        elif number == 3:
            return "身份证证号和出生信息不一致"
        elif number == 4:
            return "身份证证号和性别信息不一致"
        else:
            return "未知"

    # 将返回的 英文识别状态 转换为 中文识别状态
    def En_statusToCh_status(self,EnResult):
        if EnResult == "normal":
            return "识别正常"
        elif EnResult == "reversed_side":
            return "身份证正反面颠倒"
        elif EnResult == "non_idcard":
            return "上传的图片中不包含身份证"
        elif EnResult == "blurred":
            return "身份证模糊"
        elif EnResult == "other_type_card":
            return "其他类型证照"
        elif EnResult == "over_exposure":
            return "身份证关键字段反光或过曝"
        elif EnResult == "over_dark":
            return "身份证欠曝（亮度过低）"
        else:
            return "其他未知情况"

    # 将返回的 英文识别身份证类型 转为中文识别身份证类型
    def En_typeToCh_type(self,EnType):
        if EnType == "normal":
            return "正常身份证"
        elif EnType == "copy":
            return "复印件"
        elif EnType == "temporary":
            return "临时身份证"
        elif EnType == "screen":
            return "翻拍"
        else:
            return "其他未知情况"    

    def Idcard(self,filePath,id_card_side,detect_dire):
        "身份证识别\n\
    filePath       图片路径\n\
    id_card_side   front照片面 back国徽面\n\
    detect_dire    是否检测图片朝向"

        try:
            if detect_dire == '0':
                detect_dire = 'false'
            else:
                detect_dire = 'true'

            # 如果有一项参数为空
            if IsEmpty(filePath) or IsEmpty(detect_dire):
                raise Exception("输入参数不正确！")

            # 判断文件是否存在
            if not os.path.exists(filePath):
                raise Exception("文件不存在！")

            # 获取AccessToken
            access_token = self.ocr_Token
            if access_token == None:
                access_token = self.GetAccessToken()

            if IsEmpty(access_token):
                return ''
                #raise Exception("获取AccessToken失败！")

            # 网络文字识别
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard"

            # 二进制方式打开图片文件
            file = open(filePath, 'rb')
            # base64编码
            img = base64.b64encode(file.read())

            params = {"image":img,"id_card_side":id_card_side,"detect_direction":detect_dire,"detect_risk":"true"}
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                r = response.json()
            # 如果返回的json数据有“error_msg”
            if r.get("error_msg") != None:
                raise Exception(r.get("error_msg"))


            edit,status,Type,word = "","","",""
            if r.get("edit_tool") != None:
                edit = "\n编辑软件名称：" + r.get("edit_tool")
        
            if r.get("image_status") != None:
                status = r.get("image_status")
            if r.get("risk_type") != None:
                Type = r.get("risk_type")
        

            word = "识别状态：" + self.En_statusToCh_status(status) + \
            "\n身份证类型：" + self.En_typeToCh_type(Type) + edit

        
            if id_card_side == "front": # 身份证照片面
                word +="\n身份证号码、性别、出生是否一致：" + self.GetIdcard_number_type(r.get("idcard_number_type")) + \
                "\n姓名：" + r["words_result"]["姓名"]["words"] + \
                "\n性别：" + r["words_result"]["性别"]["words"] + \
                "\n民族：" + r["words_result"]["民族"]["words"] + \
                "\n出生：" + r["words_result"]["出生"]["words"] + \
                "\n身份证号码：" + r["words_result"]["公民身份号码"]["words"] + \
                "\n住址：" + r["words_result"]["住址"]["words"]
            else:                       # 身份证国徽面
                word += "\n签发日期：" + r["words_result"]["签发日期"]["words"] + \
                "\n失效日期：" + r["words_result"]["失效日期"]["words"] + \
                "\n签发机关：" + r["words_result"]["签发机关"]["words"]

            return word.rstrip('\n') # 删除掉最后面的'\n'字符

        except Exception as e:
            #print(e)
            return e

    def Numbers(self,filePath,detect_dire):
        "数字识别\n\
    filePath图片路径\n\
    detect_dire 是否检测图片朝向"

        try:
            if detect_dire == '0':
                detect_dire = 'false'
            else:
                detect_dire = 'true'
            # 如果有一项参数为空
            if IsEmpty(filePath) or IsEmpty(detect_dire):
                raise Exception("输入参数不正确！")

            # 判断文件是否存在
            if not os.path.exists(filePath):
                raise Exception("文件不存在！")

           # 获取AccessToken
            access_token = self.ocr_Token
            if access_token == None:
                access_token = self.GetAccessToken()

            if IsEmpty(access_token):
                return ''
                #raise Exception("获取AccessToken失败！")

            # 网络文字识别
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"

            # 二进制方式打开图片文件
            file = open(filePath, 'rb')
            # base64编码
            img = base64.b64encode(file.read())

            params = {"image":img,"detect_direction":detect_dire}
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                r = response.json()
            # 如果返回的json数据有“error_msg”
            if r.get("error_msg") != None:
                raise Exception(r.get("error_msg"))

            word = ""
            for result in r.get("words_result"):
                word+=result["words"] + "\n"

            return word.rstrip('\n') # 删除掉最后面的'\n'字符

        except Exception as e:
            #print(e)
            return e
        
    # 下载表格文字识别识别后返回的表格
    def DownFile(self,url, filePath):
        try:
            r = requests.get(url)
            with open(filePath, 'wb') as f:
                f.write(r.content)

            return "已下载到当前文件夹（文件路径：" + filePath + "）"

        except Exception as e:
            return "未下载到当前文件夹"

    def TableIdent(self,filePath):
        "表格文字识别 提交（异步接口）\n\
    filePath图片路径"

        try:
            # 判断文件是否存在
            if not os.path.exists(filePath):
                raise Exception("文件不存在！")

            # 获取AccessToken
            access_token = self.ocr_Token
            if access_token == None:
                access_token = self.GetAccessToken()

            if IsEmpty(access_token):
                return ''
                #raise Exception("获取AccessToken失败！")

            # 表格文字识别 提交（异步接口）
            request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request"

            # 二进制方式打开图片文件
            file = open(filePath, 'rb')
            # base64编码
            img = base64.b64encode(file.read())

            params = {"image":img,"is_sync":"true","request_type":"excel"}
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                r = response.json()
                # 如果返回的json数据有“error_msg”
                if r.get("error_msg") != None:
                    raise Exception(r.get("error_msg"))

                url = r['result']['result_data']
                percent = r['result']['percent']
                retMsg = r['result']['ret_msg']
            
                fileName = GetFileName("\\OCR文字识别_下载的表格","xls")          

                return "识别进度：" + str(percent) + "%\n识别结果：" + retMsg + "\n是否下载：" + self.DownFile(url,fileName) + "\n下载地址：" + url
            else:
                return "识别失败！"

        except Exception as e:
                #print(e)
                return str(e.args[0]) + "\n如果识别失败请重试。"

    # 将中文表达的语言名称转为英文缩写（如：传入“中英文混合”，输出“CHN_ENG”）
    def ChToEn(self,Lang):
        if Lang == "中英文混合":
            return "CHN_ENG"
        elif Lang == "英文":
            return "ENG"
        if Lang == "葡萄牙语":
            return "POR"
        elif Lang == "法语":
            return "FRE"
        if Lang == "德语":
            return "GER"
        elif Lang == "意大利语":
            return "ITA"
        if Lang == "西班牙语":
            return "SPA"
        elif Lang == "俄语":
            return "RUS"
        if Lang == "日语":
            return "JAP"
        elif Lang == "韩语":
            return "KOR"
        else:
            return "CHN_ENG"


class TTS:
    '''语音合成类'''
    def __init__(self,TTS_ID,TTS_AK,TTS_SK):
        self.TTS_ID = TTS_ID
        self.TTS_AK = TTS_AK
        self.TTS_SK = TTS_SK

    def Get_tts_AccessToken(self):
            "获取语音合成AccessToken"
            host = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + \
            self.TTS_AK + '&client_secret=' + self.TTS_SK
            r = requests.get(host).json()
            result = r.get("access_token")
            if IsEmpty(result):
                messagebox.showerror("OCR文字识别","获取语音合成Token失败！\n原因：" + r.get("error_description"))
                return None
            else:
                return result

    def PlayMusic(self,musicName):
        # 全局变量
        global g_playMusic,g_playSound

        try:
            # 播放wav文件
            g_playSound = winsound.PlaySound(musicName, winsound.SND_ASYNC)
            g_playMusic = True
            sec = float(self.GetWavLength(musicName))
            # 休眠
            time.sleep(sec)
            g_playMusic = False

        except Exception as e:
            g_playMusic = False
            messagebox.showerror("播放音频文件失败",e.args[0])


    def Speech(self,Text,Vol,Per,Spd,control=None):
            "文字转语音 （只支持中英文和数字）\n\
        Text 要合成的文本内容\n\
        Vol  音量大小\n\
        Per  发音人\n\
        Spd  语速快慢"

            try:
                if control != None:
                    # 设置按钮“gui.button4_Speech（语音合成）”状态为禁用
                    control["state"] = "disabled"

                #如果Text为空
                if IsEmpty(Text):
                    return

                # 获取ttsAccessToken
                tts_access_token = self.Get_tts_AccessToken()
                if IsEmpty(tts_access_token):
                    return
                    #raise Exception("获取AccessToken失败！")

                # 获取当前时间，用作音频文件的文件名
                curr_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d_%H_%M_%S')
                # 下载表格时所存放的目录
                fileDir = os.path.abspath('.') + '\\OCR文字识别_合成的音频文件'
                if not os.path.exists(fileDir):
                    os.mkdir(fileDir) # 目录不存在则创建
                musicName = fileDir + '\\' + curr_time + '.wav' 

                # 将需要合成的文字做2次urlencode编码
                tex = parse.quote_plus(Text)
                params = {'tok':tts_access_token,'tex':tex,'per':Per,'spd':Spd,'pit':5,'vol':Vol,'aue':6,'cuid':"test",'lan':'zh','ctp':1}  
                # 将参数进行urlencode编码
                data = parse.urlencode(params)
                req = request.Request("http://tsn.baidu.com/text2audio", data.encode('utf-8'))
                # 发送post请求
                f = request.urlopen(req)
                result = f.read()

                if control != None:
                    # 设置按钮“gui.button4_Speech（语音合成）”状态为启用
                    control["state"] = "normal"
                
                # 将返回的header信息取出并生成一个字典
                headers = dict((name.lower(), value) for name, value in f.headers.items())
                # 如果返回的header含有“Content-Type: audio/wav”，则成功
                if "audio/wav" == headers['content-type']:
                    with open(musicName, 'wb') as of:
                            of.write(result)
                    # 播放下载的音频文件
                    self.PlayMusic(musicName)
                else:
                    err = json.loads(result)
                    if err.get("err_detail") != None:
                        raise Exception("语音合成失败！\n原因：" + err.get("err_detail"))
                    else:
                        raise Exception("语音合成失败！")

            except Exception as e:
                if control != None:
                    control["state"] = "normal"
                messagebox.showerror("语音合成失败", e.args[0])

    # 将发音人名称转为数字
    def InformantToNumber(self,informant):
        if informant == "度小宇":
            return 1
        elif informant == "度小美":
            return 0
        elif informant == "度逍遥":
            return 3
        elif informant == "度丫丫":
            return 4

    # 获取Wav文件时间长度
    def GetWavLength(self,WavPath):
            "获取wav文件时长\n\
        filePath  wav路径\n"
            with contextlib.closing(wave.open(WavPath,'r')) as f:
                return f.getnframes() / float(f.getframerate())


class ControlTip:
    '''在控件中显示提示类'''
    def __init__(self,widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self,tip_text):
        "在控件中显示提示"
        if self.tip_window or not tip_text:
            return
        # 获取控件的大小
        x, y, _cx, cy = self.widget.bbox("insert")       
        # 获取控件相对于屏幕左上角的x坐标
        x = x + self.widget.winfo_rootx() + 25          
        # 获取控件相对于屏幕左上角的y坐标
        y = y + cy + self.widget.winfo_rooty() + 25     
        # 创建一个提示窗口
        self.tip_window = tw = tk.Toplevel(self.widget) 
        tw.wm_overrideredirect(True) 
        # 设置提示窗口要显示的位置
        tw.wm_geometry("+%d+%d" % (x, y))                
        # 在控件下方放置一个label控件
        label = tk.Label(tw, text=tip_text, justify=tk.LEFT,background="#FFFFFF", relief=tk.SOLID,borderwidth=1,font=("微软雅黑", "9"))
        label.pack(ipadx=1)
 
    def hide_tip(self):
        "在控件中隐藏提示"
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

def create_Tip(widget, text):
    "在控件中显示或隐藏提示"
    tip = ControlTip(widget)
    def enter(event):
        tip.show_tip(text)
    def leave(event):
        tip.hide_tip()
    # 绑定事件
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


class GUI:
    """界面设计类"""
    def __init__(self,root):
        self.root = root

    def create_window(self):
         # 窗口标题
        self.root.title('OCR文字识别  最后修改时间：2020-07-25')
        # 获取屏幕宽度
        self.screenW = self.root.winfo_screenwidth()
        # 获取屏幕高度
        self.screenH = self.root.winfo_screenheight()
        # 窗口宽度和高度
        self.windowW,self.windowH = 650 ,400
        # 设置窗口显示居中
        self.root.geometry('%dx%d+%d+%d' % (self.windowW, self.windowH,((self.screenW - self.windowW) / 2),((self.screenH - self.windowH) / 2)))

        # 设置窗口的宽高为固定（不能改变大小）
        self.root.resizable(0,0)
        self.top = self.root.winfo_toplevel()
        self.style = Style()

        # 右键菜单
        self.menubar = Menu(self.root, tearoff=False)

        # 发音语速滑动条
        self.Slider1 = Scale(self.top, orient='horizontal', from_=0, to=15)
        self.Slider1.place(relx=0.472, rely=0.210, relwidth=0.118, relheight=0.098)
        self.Slider1.set(5)
        create_Tip(self.Slider1,"设置语音合成发音语速")

        # 音量滑动条
        self.Slider2 = Scale(self.top, orient='horizontal', from_=0, to=15)
        self.Slider2.place(relx=0.660, rely=0.212, relwidth=0.118, relheight=0.098)
        self.Slider2.set(7)
        create_Tip(self.Slider2,"设置语音合成发音音量")

        # 识别文字时是否检测图片朝向
        self.CheckBox1Var = StringVar(value='1')
        self.style.configure('Check1.TCheckbutton',font=('微软雅黑',10))
        self.CheckBox1 = Checkbutton(self.top, text='检测图片朝向', variable=self.CheckBox1Var, style='Check1.TCheckbutton')
        self.CheckBox1.place(relx=0.246, rely=0.215, relwidth=0.17, relheight=0.074)

        # 选择要识别的图片中的语言
        self.ComboBox1_lang_List = ['中英文混合','英文','葡萄牙语','法语','德语','意大利语','西班牙语','俄语','日语','韩语']
        self.ComboBox1_lang = Combobox(self.top, state='readonly', values=self.ComboBox1_lang_List, font=('微软雅黑',10))
        self.ComboBox1_lang.place(relx=0.013, rely=0.215, relwidth=0.12, relheight=0.08)
        self.ComboBox1_lang.set(self.ComboBox1_lang_List[0])
        create_Tip(self.ComboBox1_lang,"选择要识别的图片中的语言")

        # 选择身份证正反面
        self.ComboBox2List = ['照片面','国徽面']
        self.ComboBox2 = Combobox(self.top, state='readonly',values=self.ComboBox2List, font=('微软雅黑',10))
        self.ComboBox2.place(relx=0.14, rely=0.215, relwidth=0.10, relheight=0.08) 
        self.ComboBox2.set(self.ComboBox2List[0])
        create_Tip(self.ComboBox2,"身份证识别时选择照片面或国徽面")

        # 发音人
        self.ComboBox3_informant_List = ['度小宇','度小美','度逍遥','度丫丫']
        self.ComboBox3_informant = Combobox(self.top, state='readonly', values=self.ComboBox3_informant_List, font=('微软雅黑',10))
        self.ComboBox3_informant.place(relx=0.785, rely=0.215, relwidth=0.1, relheight=0.08)
        self.ComboBox3_informant.set(self.ComboBox3_informant_List[0])
        create_Tip(self.ComboBox3_informant,"选择语音合成发音人")

        # 默认选中第一个单选框
        self.RadioVar = IntVar()   
        self.RadioVar.set(1)

        # 通用文字识别单选按钮
        self.style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
        self.RadioButton1 = Radiobutton(self.top, text='通用文字识别', variable=self.RadioVar, value=1, style='Option1.TRadiobutton')
        self.RadioButton1.place(relx=0.010, rely=0.120, relwidth=0.157, relheight=0.074)

        # 通用文字识别（高精度版）单选按钮
        self.style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
        self.RadioButton2 = Radiobutton(self.top, text='通用文字识别（高精度版）',variable=self.RadioVar, value=2, style='Option1.TRadiobutton')
        self.RadioButton2.place(relx=0.167, rely=0.120, relwidth=0.273, relheight=0.074)

        # 手写文字识别单选按钮
        self.style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
        self.RadioButton3 = Radiobutton(self.top, text='手写文字识别',variable=self.RadioVar, value=3, style='Option1.TRadiobutton')
        self.RadioButton3.place(relx=0.432, rely=0.120, relwidth=0.157, relheight=0.074)

        # 身份证识别单选按钮
        self.style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
        self.RadioButton4 = Radiobutton(self.top, text='身份证识别',variable=self.RadioVar, value=4, style='Option1.TRadiobutton')
        self.RadioButton4.place(relx=0.59, rely=0.120, relwidth=0.157, relheight=0.074)

        # 数字识别单选按钮
        self.style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
        self.RadioButton5 = Radiobutton(self.top, text='数字识别',variable=self.RadioVar, value=5, style='Option1.TRadiobutton')
        self.RadioButton5.place(relx=0.73, rely=0.120, relwidth=0.131, relheight=0.074)

        # 表格识别单选按钮
        self.style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
        self.RadioButton5 = Radiobutton(self.top, text='表格文字识别',variable=self.RadioVar, value=6, style='Option1.TRadiobutton')
        self.RadioButton5.place(relx=0.847, rely=0.120, relwidth=0.157, relheight=0.074)

        # 选择按钮
        self.style.configure('Command1.TButton',font=('微软雅黑',9))
        self.Button2_SelectImage = Button(self.top, text='选择', command=Command_SelectImage, style='Command1.TButton')
        self.Button2_SelectImage.place(relx=0.7, rely=0.021, relwidth=0.07, relheight=0.08)
        create_Tip(self.Button2_SelectImage,"选择图片路径")

        # 识别按钮
        self.style.configure('Command1.TButton',font=('微软雅黑',9))
        self.Button1_Start = Button(self.top, text='识别', command=Command_OCR, style='Command1.TButton')
        self.Button1_Start.place(relx=0.783, rely=0.021, relwidth=0.07, relheight=0.08)
        self.Button1_Start.bind_all("<Control-Shift-V>",lambda x:PastePictureAndOCR(x))
        create_Tip(self.Button1_Start,"识别图片中的文字")

        # 翻译按钮
        self.style.configure('Command1.TButton',font=('微软雅黑',9))
        self.Button5_Translate = Button(self.top, text='翻译', style='Command1.TButton')
        self.Button5_Translate.place(relx=0.855, rely=0.021, relwidth=0.07, relheight=0.08)
        # 绑定鼠标右键事件
        self.Button5_Translate.bind("<Button-3>", lambda x: Translate_event(x))
        self.Button5_Translate.bind_all("<Control-Shift-C>", lambda x:Translate_event(x))
        # 绑定鼠标左键事件
        self.Button5_Translate.bind("<Button-1>", lambda x: Translate_event(x))
        self.Button5_Translate.bind_all("<Control-Shift-E>", lambda x:Translate_event(x))
        create_Tip(self.Button5_Translate,"鼠标左键为英译中\n鼠标右键为中译英\nCTRL+SHIFT+E 识别粘贴剪切板的图片，再英译中\nCTRL+SHIFT+C 识别粘贴剪切板的图片，再中译英")

        # 截图按钮
        self.style.configure('Command1.TButton',font=('微软雅黑',9))
        self.Button6_Screen = Button(self.top, text='截图', style='Command1.TButton')
        self.Button6_Screen.place(relx=0.927, rely=0.021, relwidth=0.07, relheight=0.08)
        # 绑定鼠标右键事件
        self.Button6_Screen.bind("<Button-3>", lambda x: Screen(x))
        # 绑定鼠标左键事件
        self.Button6_Screen.bind("<Button-1>", lambda x: Screen(x))
        # 绑定快捷键事件
        self.Button6_Screen.bind_all("<Control-Shift-P>", lambda x:Screen(x))
        self.Button6_Screen.bind_all("<Control-Shift-O>", lambda x:Screen(x))
        create_Tip(self.Button6_Screen,"鼠标左键 截图并识别\n鼠标右键 截图并英译中\nCTRL+SHIFT+P 截图，再中译英\nCTRL+SHIFT+O 截图，再英译中")

        # 语音合成按钮
        self.style.configure('Command1.TButton',font=('微软雅黑',9))
        self.button4_Speech = Button(self.top, text='语音合成', command=Command_Speech,style='Command1.TButton')
        self.button4_Speech.place(relx=0.89, rely=0.215, relwidth=0.105, relheight=0.082)
        create_Tip(self.button4_Speech,"将文字合成为语音\n单击可发音\n再单击停止发音")

        # 显示图片的路径
        self.Entry1_showPath_Var = StringVar(value='请点击“选择”按钮、拖动图片到此、粘贴剪切板图片获取图片路径')
        self.Entry1_showPath = Entry(self.top, text='请点击“选择”按钮、拖动图片到此、粘贴剪切板图片获取图片路径', textvariable=self.Entry1_showPath_Var, font=('微软雅黑',9))
        self.Entry1_showPath.place(relx=0.115, rely=0.024, relwidth=0.585, relheight=0.074)
        # 绑定鼠标右键事件
        self.Entry1_showPath.bind("<Button-3>", lambda x: Entry1_MouseRightKey(x, self.Entry1_showPath)) 
        self.Entry1_showPath.bind("<Control-v>",lambda x: SaveClipImage())

        # 显示识别后的结果
        self.Text1_showResult = Text(self.top, font=('微软雅黑',10), undo = True)
        self.Text1_showResult.place(relx=0, rely=0.32, relwidth=0.985, relheight=0.683)
        # 绑定鼠标右键事件
        self.Text1_showResult.bind("<Button-3>", lambda x: Text_MouseRightKey(x, self.Text1_showResult)) 
        self.Text1_showResult.bind("<Control-v>", lambda x: SaveClipImage())

        # text控件滚动条
        self.Slider3_scroll = tkinter.Scrollbar()
        self.Slider3_scroll.place(relx=0.985, rely=0.357, relwidth=0.10, relheight=0.683)
        # 关联到Text1_showResult控件
        self.Slider3_scroll.config(command=self.Text1_showResult.yview)
        self.Text1_showResult.config(yscrollcommand=self.Slider3_scroll.set)

        self.style.configure('Label1.TLabel',anchor='w', font=('微软雅黑',9))
        self.Label1 = Label(self.top, text='语速：', style='Label1.TLabel')
        self.Label1.place(relx=0.408, rely=0.250, relwidth=0.066, relheight=0.051)

        self.style.configure('Label1.TLabel',anchor='w', font=('微软雅黑',9))
        self.Label2 = Label(self.top, text='音量：', style='Label1.TLabel')
        self.Label2.place(relx=0.595, rely=0.250, relwidth=0.066, relheight=0.051)

        self.style.configure('Label1.TLabel',anchor='w', font=('微软雅黑',9))
        self.Label3 = Label(self.top, text='图片路径：', style='Label1.TLabel')
        self.Label3.place(relx=0.010, rely=0.026, relwidth=0.105, relheight=0.07)


class SelectionArea:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def empty(self):
        return self.start_x is None or self.end_x is None

    def setStart(self, x, y):
        # 开始的坐标
        self.start_x = x
        self.start_y = y

    def setEnd(self, x, y):
        # 结束的坐标
        self.end_x = x
        self.end_y = y

    def box(self):
        "计算要绘制的矩形的坐标"
        lt_x = min(self.start_x, self.end_x)
        lt_y = min(self.start_y, self.end_y)
        rb_x = max(self.start_x, self.end_x)
        rb_y = max(self.start_y, self.end_y)
        return lt_x, lt_y, rb_x, rb_y

    def center(self):
        center_x = (self.start_x + self.end_x) / 2
        center_y = (self.start_y + self.end_y) / 2
        return center_x, center_y

    def setStartPoint(self, x, y):
        # 清空画布
        self.canvas.delete('area', 'lt_txt', 'rb_txt')
        # 记录开始的坐标
        self.setStart(x, y)
        # 显示坐标文字
        self.canvas.create_text(x, y - 10, text=f'鼠标右键或ESC键退出\n松开鼠标左键保存\n起点坐标：{x}, {y}',font=("微软雅黑","12","bold"), fill='red', tag='lt_txt')

    def updateEndPoint(self, x, y):
        "绘制矩形"
        self.setEnd(x, y)
        # 清空画布
        self.canvas.delete('area', 'rb_txt')
        box_area = self.box()
        # 绘制选择的区域
        self.canvas.create_rectangle(*box_area, fill='black', outline='red', width=2, tags="area")
        self.canvas.create_text(x, y + 10, text=f'当前坐标：{x}, {y}',font=("微软雅黑","12","bold"), fill='red', tag='rb_txt')

class ScreenShot:
    """截图类"""
    def __init__(self,savePath):
        self.win = tk.Tk()
        # 图片保存路径
        self.savePath = savePath

        # 获取屏幕宽度、高度、缩放比例
        self.width = self.win.winfo_screenwidth()
        self.height = self.win.winfo_screenheight()
        self.screenScaling = self.getScreenScaling()

        # 窗体设置无边框、在Windows系统任务栏上消失
        self.win.overrideredirect(True)
        self.win.attributes('-alpha', 0.6)# 透明度

        # 当前是否正在选择矩形区域
        self.is_selecting = False

    def create(self):
        # 绑定按快捷键 鼠标右键和ESC键退出
        self.win.bind('<Escape>', self.exit)               # ESC键按下
        self.win.bind('<Button-3>', self.exit)             # 鼠标右键按下
        self.win.bind('<Button-1>', self.startSelect)      # 鼠标左键按下
        self.win.bind('<ButtonRelease-1>', self.selectDone)# 鼠标左键松开
        self.win.bind('<Motion>', self.changeSelectionArea)# 鼠标移动

        # 创建一块画布
        self.canvas = tk.Canvas(self.win, width=self.width,height=self.height)
        self.canvas.pack()
        self.area = SelectionArea(self.canvas)
        self.win.mainloop()

    def clear(self):
        # 清空画布
        self.canvas.delete('area', 'lt_txt', 'rb_txt')
        # 设置窗口的透明度
        self.win.attributes('-alpha', 0)

    def startSelect(self, event):
        "开始截图"
        self.is_selecting = True
        # 记录鼠标左键第一次按下时的位置
        self.area.setStartPoint(event.x, event.y)

    def changeSelectionArea(self, event):
        "鼠标移动时"
        if self.is_selecting:# 如果正在选择矩形区域
            self.area.updateEndPoint(event.x, event.y)# 刷新当前鼠标坐标

    def selectDone(self, event):
        "选择矩形区域完成"
        self.is_selecting = False
        self.saveScreenShot(event)

    def saveScreenShot(self, event):
        "保存图片"

        # 先捕获选区的区域的内容
        if self.area.empty():
            return None
    
        # 获得选取的矩形大小
        box_area = [x * self.screenScaling for x in self.area.box()]
        self.clear()

        # 截图并保存
        img = ImageGrab.grab(box_area)
        img.save(self.savePath,'png',quality=95, subsampling=0)
        # 关闭当前窗口，释放资源
        self.win.quit()
        self.win.destroy()

    def exit(self, event):
         # 关闭当前窗口，释放资源
        self.clear()
        self.win.quit()
        self.win.destroy()

    def getScreenScaling(self):
        "获取屏幕缩放比"
        # 通过注册表HKEY_CURRENT_USER\Control
        # Panel\Desktop\WindowMetrics\AppliedDPI获取缩放比
        hkey = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,r"Control Panel\Desktop\WindowMetrics",0,winreg.KEY_READ)
        val = winreg.QueryValueEx(hkey,'AppliedDPI')
        winreg.CloseKey(hkey)
        return round(val[0] / 96.0, 2)


def GetFileName(dirName,ext):
    "返回以当前时间为文件名的路径\n\
    dirName 文件夹名称\n\
    ext     文件扩展名"

    # 获取当前时间，用于保存文件时当作文件名
    curr_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d_%H_%M_%S')
    fileDir = os.path.abspath('.') + '\\' + dirName
    if not os.path.exists(fileDir):
        os.mkdir(fileDir) # 目录不存在则创建

    return fileDir + '\\' + curr_time + '.' + ext


# 翻译
def Translate(Text,From,To,Salt):
    "翻译"
    if IsEmpty(Text):
        return

    appid = TRAN_APP_ID + Text + Salt + TRAN_KEY
    # 获取md5编码
    m = hashlib.md5()
    m.update(appid.encode(encoding='utf-8'))
    sign = m.hexdigest()

    url = "https://fanyi-api.baidu.com/api/trans/vip/translate?q=" + parse.quote(Text) + "&from=" + From + "&to=" + To + "&appid=" + TRAN_APP_ID + \
          "&salt=" + Salt + "&sign=" + sign
    try:
        req = request.Request(url, url.encode('utf-8'))
        f = request.urlopen(req)
        result = json.load(f)
        
        if result.get("error_msg") != None:
            raise Exception(result.get("error_msg"))

        word = ""
        for r in result['trans_result']:
            word += r['dst'] + '\n'  
        return word.rstrip('\n')
    except Exception as e:
        messagebox.showerror("OCR文字识别","翻译失败！\n原因：" + str(e.args[0]))
        return ''     

# 根据触发的此事件的快捷键 选择翻译时的源语言和目标语言
def Translate_event(event):
    # From 源语言，To 目标语言
    From,To = '',''
    salt = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M%S')

    # 如果为鼠标事件，则通过判断是鼠标左键还是右键触发此事件，来选择翻译源语言和目标语言
    # 再判断Text控件是否为空 - （如果为空）判断图片路径不为空并且路有效 - 先识别图片文字再翻译
    if event.type == '4':
        if event.num == 1: # 鼠标左键（英译中）
           From,to = "en","zh"
        elif event.num == 3:# 鼠标右键（中译英）
            From ,to = "zh","en"
        else:
            return
        if IsEmpty(gui.Text1_showResult.get('0.0', 'end').rstrip('\n')): # 如果Text控件为空
            if (not IsEmpty(gui.Entry1_showPath_Var.get())) and os.path.exists(gui.Entry1_showPath_Var.get()): # 如果图片路径不为空并且路径有效
                    Command_OCR() # 先文字识别再翻译
            else:                 # 如果Text控件为空和图片路径为空或路径无效
                gui.Text1_showResult.insert(INSERT,"请点击“识别”按钮识别图片中的文字，\
                或在此处输入要翻译的文字后，点击“翻译”按钮（鼠标左键单击按钮英译中，鼠标右键单击按钮中译英，\
                CTRL+SHIFT+E识别剪切板中的图片并英译中，CTRL+SHIFT+C识别剪切板中的图片并中译英）。") # 向Text控件插入提示内容

                From,to = "zh","en"

    else: # 如果为键盘事件，则通过判断按下的快捷键，来选择翻译源语言和目标语言，
          # 然后保存剪切板的图片 - 先识别图片文字再翻译
        if event.keysym == 'C':# 快捷键CTRL+SHIFT+C（中译英）
            From,to = "zh","en"

        elif event.keysym == 'E': # 快捷键CTRL+SHIFT+E（英译中）
            From,to = "en","zh"

        
        fileName = SaveClipImage()# 将剪切板中的图片保存到本地
        if IsEmpty(fileName):     # 如果文件名为空
            return 

        Command_OCR()             # 调用文字识别

    # 调用百度api翻译文字
    result = Translate(gui.Text1_showResult.get('0.0', 'end').rstrip('\n'),From,to,salt)   
    if not IsEmpty(result):
        gui.Text1_showResult.insert(END,'\n' + result)# 追加到末尾


# 截图
def Screen(event):
    pictureName = GetFileName("OCR文字识别_保存的图片","png")
    salt = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M%S')
    try:
        # 截图
        sc = ScreenShot(pictureName)
        sc.create()
    except Exception as e:
        print(e.args[0])
        sc.win.quit() 
        sc.win.destroy()
        messagebox.showerror("OCR文字识别","截图失败！")
        return

    # 如果文件不存在，则视为用户取消截图
    if not os.path.exists(pictureName):
        return

    # 将保存的图片路径显示到Entry1_showPath
    if gui.Entry1_showPath_Var.get() != "":
        gui.Entry1_showPath.delete('0', tkinter.END)
    gui.Entry1_showPath.insert(INSERT, pictureName)
     # 文字识别
    Command_OCR()

    # 如果为鼠标事件，则通过判断是鼠标左键还是右键触发此事件，来选择翻译源语言和目标语言
    if event.type == '4':  
        if event.num == 1: # 鼠标左键（文字识别，上面语句已完成文字识别，所以直接返回）
          return
        elif event.num == 3:# 鼠标右键（英译中）
            From,to = "en","zh"
        else:
            return
    else: # 如果为键盘事件，则通过判断按下的快捷键，来选择翻译源语言和目标语言
        if event.keysym == 'P':   # 快捷键CTRL+SHIFT+P（中译英）
           From,to = "zh","en"
        elif event.keysym == 'O': # 快捷键CTRL+SHIFT+O（英译中）
            From,to = "en","zh" 

    result = Translate(gui.Text1_showResult.get('0.0', 'end').rstrip('\n'),From,to,salt)   
    if not IsEmpty(result):
        gui.Text1_showResult.insert(END,'\n' + result)# 追加到末尾


# 创建一个新线程，用于语音合成
def CreateThread(text):
    global g_speechThread

    g_speechThread = threading.Thread(target=tts.Speech, args=(text.rstrip('\n'),gui.Slider2.get(),tts.InformantToNumber(gui.ComboBox3_informant.get()),gui.Slider1.get(),gui.button4_Speech))
    # 父线程退出时，子线程也退出
    g_speechThread.daemon = True
    g_speechThread.start()


# 语音合成
def Command_Speech():
    "语音合成"
    global g_playMusic,g_playSound,g_speechThread

    # 如果要合成语音的内容为空
    if IsEmpty(gui.Text1_showResult.get('0.0', 'end').rstrip('\n')):
        gui.Text1_showResult.insert(INSERT,"请点击“识别”按钮识别图片文字，或在此处输入要合成语音的文字后，点击“语音合成”按钮。\n\
使用说明：\n1、语速滑动条可调节语音合成发音语速。\n2、音量滑动条可调节语音合成发音音量。\n3、“语音合成”按钮左边的下拉列表可选择语音合成发音人。\n4、单击“语音合成”按钮可停止发音。") # 向Text控件插入提示内容
        #return

    winsound.PlaySound(g_playSound, winsound.SND_PURGE)
    if not g_playMusic:
        CreateThread(gui.Text1_showResult.get('0.0', tkinter.END))
    else:
        # 终止线程
        winsound.PlaySound(g_playSound, winsound.SND_PURGE)
        g_speechThread.join(0)
        g_playMusic = False


def PastePictureAndOCR(event):
    "粘贴剪切板图片并识别文字"
    if event.type == '2':
        if event.keysym == 'V':# 快捷键CTRL+SHIFT+V
            fileName = SaveClipImage()# 将剪切板中的图片保存到本地
            if not IsEmpty(fileName):     # 如果文件名不为空
                Command_OCR()             # 调用文字识别



# 识别图片中的文字
def Command_OCR():
    "识别图片"

    # 如果文件不存在
    if IsEmpty(gui.Entry1_showPath_Var.get()):
            messagebox.showinfo("图片识别","请先选择文件！") # 弹出提示
            Command_SelectImage() # 调用“选择图片文件”函数
            return   
    # 如果文件不存在
    if not os.path.exists(gui.Entry1_showPath_Var.get()):
            messagebox.showinfo("图片识别","路径无效！") # 弹出提示
            return

    global g_playMusic,g_playSound,g_speechThread

    # 如果文字转语音正在播放，则关闭
    if g_playMusic:
        # 终止线程
        winsound.PlaySound(g_playSound, winsound.SND_PURGE)
        g_playMusic = False
        g_speechThread.join(0)

    if gui.RadioVar.get() == 1:  # 通用文字识别
        re = ocr.GeneralBasic(gui.Entry1_showPath_Var.get(),ocr.ChToEn(gui.ComboBox1_lang.get()),gui.CheckBox1Var.get())
    elif gui.RadioVar.get() == 2:# 通用文字识别（高精度版）
        re = ocr.AccurateBasic(gui.Entry1_showPath_Var.get(),ocr.ChToEn(gui.ComboBox1_lang.get()),gui.CheckBox1Var.get())
    elif gui.RadioVar.get() == 3:# 手写文字识别
        re = ocr.Handwriting(gui.Entry1_showPath_Var.get())
    elif gui.RadioVar.get() == 4:# 身份证识别
        f = "front" if gui.ComboBox2.get() == "照片面" else "back" # 获取身份证照片面或国徽面
        re = ocr.Idcard(gui.Entry1_showPath_Var.get(),f,gui.CheckBox1Var.get())  
    elif gui.RadioVar.get() == 5:# 数字识别
        re = ocr.Numbers(gui.Entry1_showPath_Var.get(),gui.CheckBox1Var.get())
    elif gui.RadioVar.get() == 6:# 表格文字识别
        re = ocr.TableIdent(gui.Entry1_showPath_Var.get())

    # 如果返回的结果为空
    if IsEmpty(re):
        return

    # 将识别的内容显示到text控件
    if gui.Text1_showResult.get('0.0', 'end') != "":     # 如果Text控件不为空
        gui.Text1_showResult.delete('0.0',tkinter.END)   # 清空Text控件
    gui.Text1_showResult.insert(INSERT,re)   # 向Text控件插入内容


# 选择图片路径
def Command_SelectImage():
        "选择图片文件"

        # 打开文件对话框
        fileName = tkinter.filedialog.askopenfilename(filetypes=[("jpg、png、bmp、webp、jpeg、tiff、pnm","*.jpg;*.png;*.bmp;*.webp;*.jpeg;*.tiff;*.pnm")])
        if fileName == "" or fileName == None: # 如果未选择文件
            return 
        # 否则将选择的图片路径显示到Text_showResult控件
        if gui.Entry1_showPath_Var.get() != "":
            gui.Entry1_showPath.delete('0',tkinter.END)
        gui.Entry1_showPath.insert(INSERT,fileName)


# 撤销
def Undo(editor, event=None):
    # 如果还剩一个字符，则返回
    if len(editor.get('0.0', tkinter.END).rstrip('\n')) <= 1: 
        return
    editor.edit_undo()

# 恢复撤销
def Redo(editor, event=None):
    try:
        editor.edit_redo()
    except:
        pass

# 剪切
def Cut(editor, event=None):
    editor.event_generate("<<Cut>>")

# 复制
def Copy(editor, event=None):
    editor.event_generate("<<Copy>>")

# 粘贴
def Paste(editor, event=None):
    editor.event_generate('<<Paste>>')
    SaveClipImage()

  
# 朗读选择的内容
def SpeechSelectCont(editor, event=None):
    try:
        selectText = gui.Text1_showResult.selection_get()
        global g_playMusic,g_playSound,g_speechThread

        # 如果线程在运行则终止线程
        if  g_playMusic:
            winsound.PlaySound(g_playSound, winsound.SND_PURGE)
            g_playMusic = False
            g_speechThread.join(0)
        # 文字转语音
        CreateThread(selectText)
    except:
        pass


# 鼠标右键菜单栏
def Text_MouseRightKey(event, editor):
    gui.menubar.delete('0',tkinter.END)
    gui.menubar.add_command(label='剪切',command=lambda:Cut(editor))
    gui.menubar.add_command(label='复制',command=lambda:Copy(editor))
    gui.menubar.add_command(label='粘贴',command=lambda:Paste(editor))
    gui.menubar.add_command(label='撤销',command=lambda:Undo(editor))
    gui.menubar.add_command(label='恢复',command=lambda:Redo(editor))
    gui.menubar.add_command(label='朗读选择项',command=lambda:SpeechSelectCont(editor))
    gui.menubar.post(event.x_root,event.y_root)

# 鼠标右键菜单栏
def Entry1_MouseRightKey(event, editor):
    gui.menubar.delete(0,tkinter.END)
    gui.menubar.add_command(label='剪切',command=lambda:Cut(editor))
    gui.menubar.add_command(label='复制',command=lambda:Copy(editor))
    gui.menubar.add_command(label='粘贴',command=lambda:Paste(editor))
    gui.menubar.post(event.x_root,event.y_root)


# 保存剪切板的图片
def SaveClipImage():
    im = ImageGrab.grabclipboard()
    # 如果im=None则说明剪切板没有图片
    if im == None:
        return None
    
    pictureName = GetFileName("OCR文字识别_保存的图片","png")
    # 保存剪切板的图片
    im.save(pictureName, 'png',quality=100)
    print(pictureName)
    # 将保存的图片路径显示到Entry1_showPath
    if gui.Entry1_showPath_Var.get() != "":
        gui.Entry1_showPath.delete('0', tkinter.END)
    gui.Entry1_showPath.insert(INSERT, pictureName)
    return pictureName


# 拖动文件
def DragFile(files):
    # 将选择的图片路径显示到Text_showResult控件
    if gui.Entry1_showPath_Var.get() != "":
        gui.Entry1_showPath.delete('0',tkinter.END)
    gui.Entry1_showPath.insert(INSERT,files[0].decode('ANSI'))# 使用ansi是为了避免本地化问题，导致乱码


# 第一次使用时显示欢迎窗口
def WelcomeWindow(path):
    try:
        result = messagebox.askokcancel("欢迎使用OCR文字识别","本软件是文字识别软件，可从图片中提取文字并转为语音或翻译。\n\
    注意：语音合成功能和翻译功能只支持英文、中文、数字。\n\
    \t\t\t  是否查看完整版的使用教程？") 
        if result:# 如果用户点击了“确定”的按钮
            os.system("start https://shimo.im/docs/e485cac745624f42/")

        # 创建一个文件，用来标识已阅读第一次使用提示
        with open(path, 'w') as file:
            file.write("OCR文字识别_已阅读提示")
    except Exception as e:
        print(e)


if __name__ == "__main__":    
    window = tk.Tk()
    gui = GUI(window)
    gui.create_window()

    # 拖动文件
    windnd.hook_dropfiles(window,func=DragFile)
    # 调用api设置成由应用程序自己缩放
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # 调用api获得当前的缩放因子
    scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    #设置缩放因子
    window.tk.call('tk', 'scaling', scaleFactor / 75)


    # 实例化文字识别类
    ocr = OCR(OCR_API_KEY,OCR_SECRET_KEY,TRAN_APP_ID,TRAN_KEY)
    # 实例化语音合成类
    tts = TTS(TTS_APP_ID,TTS_API_KEY,TTS_SECRET_KEY)


    # 根据用户磁盘中是否存在“OCR文字识别_已阅读提示.txt”来显示欢迎窗口
    tipFilePath = os.getenv('temp') + '\\OCR文字识别_已阅读提示.txt' 
    if not os.path.exists(tipFilePath): 
        WelcomeWindow(tipFilePath)

    # 显示窗口
    window.mainloop()
