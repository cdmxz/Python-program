#-*- coding:utf-8 -*-
'''
        此为桌面GUI程序，不能在浏览器使用，请下载到电脑并安装必备的库后使用海归编辑器运行。
开源地址：https://cdmxz.github.io
已在 python3.8 32bit 测试过，可正常使用 
使用前请安装必备的库：PIL、windnd、requests
'''

import ctypes
import os
import hashlib
import sys
import inspect
import winsound  # 播放wav文件
import wave
import contextlib# 获取wav文件时长
import threading # 多线程
import datetime  # 获取当前时间
import requests  # HTTP库
import base64    # base64编码解码
import json      # 解析json数据
import tkinter.messagebox # 弹窗
import tkinter.filedialog # 选择文件对话框
import tkinter as tk # 图形界面
import time      # 休眠
import windnd    # 文件拖动
from urllib  import request,parse
from pathlib import Path # 获取当前目录
from tkinter import *    # 图形界面
from tkinter.ttk import *
from PIL import ImageGrab # 读取剪切板
playSound = winsound.PlaySound(None, winsound.SND_NODEFAULT)
playMusic = False

'''
由于申请的是免费api并且多人共用，
可能会出现识别失败的情况，
推荐自己去百度ai开放平台（https://ai.baidu.com/）申请api。
'''
# 文字识别Key（可以去百度ai开放平台（https://ai.baidu.com/tech/ocr/general）申请api）
OCR_API_KEY = "YaOhBFsug5GySthCpUFtLkQk"
OCR_SECRET_KEY = "mqP7OOO9t0h9GvipdQe1weRld3SGQokV"

# 语音合成Key（可以去百度ai开放平台（https://ai.baidu.com/tech/speech/tts_online）申请api）
TTS_APP_ID = "19685928"
TTS_API_KEY = "qk3y9G2FQLrQsCa9v9NzzW8h"
TTS_SECRET_KEY = "qtYsvvdEGgQ6EzxVSFuYRvl8NmzVihy1"


# 翻译Key（可以去百度翻译开放平台（https://api.fanyi.baidu.com/product/11）申请api）
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
    def __init__(self, OCR_AK, OCR_SK,TTS_ID,TTS_AK,TTS_SK,TRAN_ID,TRAN_KEY):
        self.OCR_AK = OCR_AK
        self.OCR_SK = OCR_SK
        self.TTS_ID = TTS_ID
        self.TTS_AK = TTS_AK
        self.TTS_SK = TTS_SK
        self.TRAN_ID = TRAN_ID
        self.TRAN_KEY = TRAN_KEY
        self.ocr_Token = self.GetAccessToken()


    def GetAccessToken(self):
        "获取文字识别AccessToken"
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.OCR_AK + '&client_secret=' + self.OCR_SK
        r = requests.get(host).json()
        result = r.get("access_token")
        if IsEmpty(result):
            messagebox.showerror("OCR文字识别","获取文字识别Token失败！\n原因：" + r.get("error_description"))
            return None
        else:
            return result

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
            
                # 获取当前时间，用作音频文件的文件名
                curr_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d_%H_%M_%S')
                # 下载表格时所存放的目录
                fileDir = os.path.abspath('.') + '\\OCR文字识别_下载的表格'
                if not os.path.exists(fileDir):
                    os.mkdir(fileDir) # 目录不存在则创建
                fileName = fileDir + '\\' + curr_time + '.xls'
        
                return "识别进度：" + str(percent) + "%\n识别结果：" + retMsg + "\n是否下载：" + self.DownFile(url,fileName) + "\n下载地址：" + url
            else:
                return "识别失败！"

        except Exception as e:
                #print(e)
                return e.args[0] + "\n如果识别失败请重试。"




# 获取Wav文件时间长度
def GetWavLength(WavPath):
        "获取wav文件时长\n\
    filePath  wav路径\n"
        with contextlib.closing(wave.open(WavPath,'r')) as f:
            return f.getnframes() / float(f.getframerate())

def Speech(Text,Vol,Per,Spd):
        "文字转语音 （只支持中英文和数字）\n\
    Text 要合成的文本内容\n\
    Vol  音量大小\n\
    Per  发音人\n\
    Spd  语速快慢"

        try:
            # 全局变量
            global playMusic,playSound

            #如果Text为空
            if IsEmpty(Text):
                return

            # 获取ttsAccessToken
            tts_access_token = ocr.Get_tts_AccessToken()
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
            # 将返回的header信息取出并生成一个字典
            headers = dict((name.lower(), value) for name, value in f.headers.items())
            # 如果返回的header含有“Content-Type: audio/wav”，则成功
            if "audio/wav" == headers['content-type']:
                with open(musicName, 'wb') as of:
                        of.write(result)
                # 播放wav文件
                playSound = winsound.PlaySound(musicName, winsound.SND_ASYNC)
                playMusic = True
                sec = float(GetWavLength(musicName))
                # 休眠
                time.sleep(sec)
                playMusic = False
            else:
                err = json.loads(result)
                if err.get("err_detail") != None:
                    raise Exception("语音合成失败！\n原因：" + err.get("err_detail"))
                else:
                    raise Exception("语音合成失败！")

        except Exception as e:
            playMusic = False
            messagebox.showerror("文字转语音失败", e.args[0])


# 将中文表达的语言名称转为英文缩写（如：传入“中英文混合”，输出“CHN_ENG”）
def ChToEn(Lang):
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

# 将发音人名称转为数字
def InformantToNumber(informant):
    if informant == "度小宇":
        return 1
    elif informant == "度小美":
        return 0
    elif informant == "度逍遥":
        return 3
    elif informant == "度丫丫":
        return 4

# 语音合成
def Command_Speech():
    "语音合成"
    global playMusic,playSound,newThread

    # 如果要合成语音的内容为空
    if IsEmpty(Text2_showResult.get('0.0', 'end').rstrip('\n')):
        Text2_showResult.insert(INSERT,"请点击“识别”按钮识别图片文字，或在此处输入要合成语音的文字后，点击“语音合成”按钮。\n\
使用说明：\n1、语速滑动条可调节语音合成发音语速。\n2、音量滑动条可调节语音合成发音音量。\n3、“语音合成”按钮左边的下拉列表可选择语音合成发音人。") # 向Text控件插入提示内容
        #return

    if not playMusic:
        # 创建一个新线程
        newThread = threading.Thread(target=Speech, args=(Text2_showResult.get('0.0', 'end').rstrip('\n'),Slider2.get(),InformantToNumber(ComboBox3_informant.get()),Slider1.get()))
        newThread.start()
    else:
        # 终止线程
        winsound.PlaySound(playSound, winsound.SND_PURGE)
        playMusic = False
        newThread.join(0)


# 识别图片
def Command_StartOCR():
    "识别图片"

    if IsEmpty(Entry1_showPath_Var.get()):
            messagebox.showinfo("图片识别","请先选择文件！") # 弹出提示
            #Command_SelectImage() # 调用“选择图片文件”函数
            return   
    if not os.path.exists(Entry1_showPath_Var.get()):
            messagebox.showinfo("图片识别","路径无效！") # 弹出提示
            return

    global playMusic,playSound,newThread

    # 如果文字转语音正在播放，则关闭
    if playMusic:
        # 终止线程
        winsound.PlaySound(playSound, winsound.SND_PURGE)
        playMusic = False
        newThread.join(0)

    if RadioVar.get() == 1:  # 通用文字识别
        re = ocr.GeneralBasic(Entry1_showPath_Var.get(),ChToEn(ComboBox1_lang.get()),CheckBox1Var.get())
    elif RadioVar.get() == 2:# 通用文字识别（高精度版）
        re = ocr.AccurateBasic(Entry1_showPath_Var.get(),ChToEn(ComboBox1_lang.get()),CheckBox1Var.get())
    elif RadioVar.get() == 3:# 手写文字识别
        re = ocr.Handwriting(Entry1_showPath_Var.get())
    elif RadioVar.get() == 4:# 身份证识别
        if ComboBox2.get() == "照片面": # 获取身份证照片面或国徽面
            f = "front"
        else:
            f = "back"
        re = ocr.Idcard(Entry1_showPath_Var.get(),f,CheckBox1Var.get())  
    elif RadioVar.get() == 5:# 数字识别
        re = ocr.Numbers(Entry1_showPath_Var.get(),CheckBox1Var.get())
    elif RadioVar.get() == 6:# 表格文字识别
        re = ocr.TableIdent(Entry1_showPath_Var.get())

    if IsEmpty(re):
        return

    # 将识别的内容显示到text控件
    if Text2_showResult.get('0.0', 'end') != "":     # 如果Text控件不为空
        Text2_showResult.delete('0.0',tkinter.END)   # 清空Text控件
    Text2_showResult.insert(INSERT,re)   # 向Text控件插入内容


# 选择图片路径
def Command_SelectImage():
        "选择图片文件"

        # 打开文件对话框
        fileName = tkinter.filedialog.askopenfilename(filetypes=[("jpg、png、bmp、webp、jpeg、tiff、pnm","*.jpg;*.png;*.bmp;*.webp;*.jpeg;*.tiff;*.pnm")])
        #print(fileName)
    
        if fileName == "": # 如果未选择文件
            return 
        # 否则将选择的图片路径显示到Text_showResult控件
        if Entry1_showPath_Var.get() != "":
            Entry1_showPath.delete('0',tkinter.END)
        Entry1_showPath.insert(INSERT,fileName)
        pass


# 翻译
def Translate(Text,From,To,Salt):
    "翻译"
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
        messagebox.showerror("OCR文字识别","翻译失败！")
        return ''     

# 根据触发的此事件的快捷键 选择翻译时的源语言和目标语言
def Translate_event(event):
    # From 源语言，To 目标语言
    From,To = '',''
    replace = False # 是否替换掉翻译源内容
    salt = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M%S')
    # 先保存当前选择的选项
    RadioButton_Var = RadioVar.get()
    # 设置当前识别选项为：通用文字识别（高精度版）
    RadioVar.set(2)

    # 如果为鼠标事件，则通过判断是鼠标左键还是右键触发此事件，来选择翻译源语言和目标语言
    # 再判断Text控件是否为空 - （如果为空）判断图片路径不为空并且路有效 - 先识别图片文字再翻译
    if event.type == '4':
        # 鼠标左键（英译中）
        if event.num == 1:
           From = "en"
           to = "zh"
        # 鼠标右键（中译英）
        elif event.num == 3:
            From = "zh"
            to = "en"
        else:
            return
        replace = False
        if IsEmpty(Text2_showResult.get('0.0', 'end').rstrip('\n')): # 如果Text控件为空
            if (not IsEmpty(Entry1_showPath_Var.get())) and os.path.exists(Entry1_showPath_Var.get()): # 如果图片路径不为空并且路径有效
                    Command_StartOCR()                      # 先文字识别再翻译
            else:# 如果Text控件为空和图片路径为空或路径无效
                Text2_showResult.insert(INSERT,"请点击“识别”按钮识别图片中的文字，或在此处输入要翻译的文字后，点击“翻译”按钮（鼠标左键单击按钮英译中，鼠标右键单击按钮中译英，\
CTRL+SHIFT+E识别剪切板中的图片并英译中，CTRL+SHIFT+C识别剪切板中的图片并中译英）。") # 向Text控件插入提示内容
                From = "zh"
                to = "en"
                #return
    else: # 如果为键盘事件，则通过判断按下的快捷键，来选择翻译源语言和目标语言，
          # 然后保存剪切板的图片 - 先识别图片文字再翻译
        if event.keysym == 'C':# 快捷键CTRL+SHIFT+C（中译英）
           From = "zh"
           to = "en"
        elif event.keysym == 'E': # 快捷键CTRL+SHIFT+E（英译中）
           From = "en"
           to = "zh" 
        #replace = True # 替换掉翻译源内容

        # 将剪切板中的图片保存到本地
        fileName = SaveClipboardPicture()
        if IsEmpty(fileName):
            #Text2_showResult.insert(INSERT,"保存剪切版中的图片失败！") # 向Text控件插入提示内容
            return 
        Command_StartOCR()# 文字识别

    # 恢复原来的文字识别选项
    RadioVar.set(RadioButton_Var)
    # 调用百度api翻译文字
    result = Translate(Text2_showResult.get('0.0', 'end').rstrip('\n'),From,to,salt)   
    if replace: # 是否替换原内容
        Text2_showResult.delete('0.0',tkinter.END)
        Text2_showResult.insert(INSERT, result)
    else:
        Text2_showResult.insert(END,'\n' + result)# 追加到末尾


# 撤销
def Undo(editor, event=None):
    # 如果还剩一个字符，则返回
    if len(editor.get('0.0', 'end').rstrip('\n')) <= 1: 
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
    SaveClipboardPicture()


# 鼠标右键菜单栏
def Text2_MouseRightKey(event, editor):
    menubar.delete(0,tkinter.END)
    menubar.add_command(label='剪切',command=lambda:Cut(editor))
    menubar.add_command(label='复制',command=lambda:Copy(editor))
    menubar.add_command(label='粘贴',command=lambda:Paste(editor))
    menubar.add_command(label='撤销',command=lambda:Undo(editor))
    menubar.add_command(label='恢复',command=lambda:Redo(editor))
    menubar.post(event.x_root,event.y_root)

# 鼠标右键菜单栏
def Text1_MouseRightKey(event, editor):
    menubar.delete(0,tkinter.END)
    menubar.add_command(label='剪切',command=lambda:Cut(editor))
    menubar.add_command(label='复制',command=lambda:Copy(editor))
    menubar.add_command(label='粘贴',command=lambda:Paste(editor))
    menubar.post(event.x_root,event.y_root)


# 保存剪切板的图片
def SaveClipboardPicture():
    im = ImageGrab.grabclipboard()
    # 如果im=None则说明剪切板没有图片
    if im == None:
        return None
    # 获取当前时间，用于保存文件时当作文件名
    curr_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d_%H_%M_%S')
    # 下载表格时所存放的目录
    fileDir = os.path.abspath('.') + '\\OCR文字识别_保存的剪切板图片'
    if not os.path.exists(fileDir):
        os.mkdir(fileDir) # 目录不存在则创建
    pictureName = fileDir + '\\' + curr_time + '.png'
    # 保存剪切板的图片
    im.save(pictureName, 'PNG')
    print(pictureName)
    # 将保存的图片路径显示到Entry1_showPath
    if Entry1_showPath_Var.get() != "":
        Entry1_showPath.delete('0', tkinter.END)
    Entry1_showPath.insert(INSERT, pictureName)
    return pictureName

# 拖动文件
def DragFile(files):
    # 将选择的图片路径显示到Text_showResult控件
    if Entry1_showPath_Var.get() != "":
        Entry1_showPath.delete('0',tkinter.END)
    Entry1_showPath.insert(INSERT,files[0].decode('gbk'))


# 第一次使用时显示欢迎窗口
def Welcome():
    try:
        readingTipsPath = os.getenv('temp') + '\\readingTips.txt' 
        if os.path.exists(readingTipsPath):
            return 
        result = messagebox.askokcancel("欢迎使用OCR文字识别","本软件是文字识别软件，可从图片中提取文字并转为语音或翻译。\n\
    注意：语音合成功能和翻译功能只支持英文、中文、数字。\n\
    \t\t\t  是否查看完整版的使用教程？") 
        if result:
            os.system("start https://shimo.im/docs/e485cac745624f42/")

        # 创建一个文件，用来标识已阅读第一次使用提示
        with open(readingTipsPath, 'w') as file:
            file.write("OCR文字识别_已阅读提示")
    except Exception as e:
        print(e)




############################ 以下为界面设计代码 ###################################
if __name__ == "__main__":    
    window = tk.Tk()
    
    windnd.hook_dropfiles(window,func=DragFile)
    # 窗口标题
    window.title('OCR文字识别  by：南雄市黄坑中学-傅宏华  最后修改时间：2020-06-14 11:50')
    # 调用api设置成由应用程序自己缩放
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # 调用api获得当前的缩放因子
    scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    #设置缩放因子
    window.tk.call('tk', 'scaling', scaleFactor / 75)

    # 获取屏幕宽度
    screenW = window.winfo_screenwidth()
    # 获取屏幕高度
    screenH = window.winfo_screenheight()
    # 窗口宽度和高度
    windowW,windowH = 618 ,350
    # 设置窗口显示居中
    window.geometry('%dx%d+%d+%d' % (windowW, windowH,((screenW - windowW) / 2),((screenH - windowH) / 2)))

    # 设置窗口的宽高为固定（不能改变大小）
    window.resizable(0,0)
    # 避免messagebox弹窗时显示一个新的窗口
    #window.withdraw()
    top = window.winfo_toplevel()
    style = Style()


    # 右键菜单
    menubar = Menu(window, tearoff=False)

    # 发音语速滑动条
    Slider1 = Scale(top, orient='horizontal', from_=0, to=15)
    Slider1.place(relx=0.472, rely=0.210, relwidth=0.118, relheight=0.098)
    #Slider1.place(relx=0.479, rely=0.238, relwidth=0.118, relheight=0.098)
    Slider1.set(5)

    # 音量滑动条
    Slider2 = Scale(top, orient='horizontal', from_=0, to=15)
    Slider2.place(relx=0.660, rely=0.212, relwidth=0.118, relheight=0.098)
    Slider2.set(7)
    # ComboBox

    # 识别文字时是否检测图片朝向
    CheckBox1Var = StringVar(value='1')
    style.configure('Check1.TCheckbutton',font=('微软雅黑',10))
    CheckBox1 = Checkbutton(top, text='检测图片朝向', variable=CheckBox1Var, style='Check1.TCheckbutton')
    CheckBox1.place(relx=0.246, rely=0.215, relwidth=0.17, relheight=0.074)

    # 选择要识别的图片中的语言
    ComboBox1_lang_List = ['中英文混合','英文','葡萄牙语','法语','德语','意大利语','西班牙语','俄语','日语','韩语']
    ComboBox1_lang = Combobox(top, state='readonly', values=ComboBox1_lang_List, font=('微软雅黑',10))
    ComboBox1_lang.place(relx=0.013, rely=0.215, relwidth=0.12, relheight=0.08) # relx=0.013, rely=0.238, relwidth=0.105（0.209）, relheight=0.08
    ComboBox1_lang.set(ComboBox1_lang_List[0])

    # 选择身份证正反面
    ComboBox2List = ['照片面','国徽面']
    ComboBox2 = Combobox(top, state='readonly',values=ComboBox2List, font=('微软雅黑',10))
    ComboBox2.place(relx=0.14, rely=0.215, relwidth=0.10, relheight=0.08) # relx=0.129, rely=0.238, relwidth=0.105, relheight=0.08
    ComboBox2.set(ComboBox2List[0])

    # 发音人
    ComboBox3_informant_List = ['度小宇','度小美','度逍遥','度丫丫']
    ComboBox3_informant = Combobox(top, state='readonly', values=ComboBox3_informant_List, font=('微软雅黑',10))
    ComboBox3_informant.place(relx=0.785, rely=0.215, relwidth=0.1, relheight=0.08)
    ComboBox3_informant.set(ComboBox3_informant_List[0])

    # RadioButton

    # 默认选中第一个单选框
    RadioVar = IntVar()   
    RadioVar.set(1)

    # 通用文字识别单选按钮
    style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
    RadioButton1 = Radiobutton(top, text='通用文字识别', variable=RadioVar, value=1, style='Option1.TRadiobutton')
    RadioButton1.place(relx=0.010, rely=0.120, relwidth=0.157, relheight=0.074)

    # 通用文字识别（高精度版）单选按钮
    style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
    RadioButton2 = Radiobutton(top, text='通用文字识别（高精度版）',variable=RadioVar, value=2, style='Option1.TRadiobutton')
    RadioButton2.place(relx=0.167, rely=0.120, relwidth=0.273, relheight=0.074)
    #RadioButton2.place(relx=0.167, rely=0.143, relwidth=0.273,
    #relheight=0.074)

    # 手写文字识别单选按钮
    style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
    RadioButton3 = Radiobutton(top, text='手写文字识别',variable=RadioVar, value=3, style='Option1.TRadiobutton')
    RadioButton3.place(relx=0.432, rely=0.120, relwidth=0.157, relheight=0.074)

    # 身份证识别单选按钮
    style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
    RadioButton4 = Radiobutton(top, text='身份证识别',variable=RadioVar, value=4, style='Option1.TRadiobutton')
    RadioButton4.place(relx=0.59, rely=0.120, relwidth=0.157, relheight=0.074)

    # 数字识别单选按钮
    style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
    RadioButton5 = Radiobutton(top, text='数字识别',variable=RadioVar, value=5, style='Option1.TRadiobutton')
    RadioButton5.place(relx=0.73, rely=0.120, relwidth=0.131, relheight=0.074)

    # 表格识别单选按钮
    style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
    RadioButton5 = Radiobutton(top, text='表格文字识别',variable=RadioVar, value=6, style='Option1.TRadiobutton')
    RadioButton5.place(relx=0.847, rely=0.120, relwidth=0.157, relheight=0.074)

    # Button

    # 识别按钮
    style.configure('Command1.TButton',font=('微软雅黑',9))
    Button1_Start = Button(top, text='识别', command=Command_StartOCR, style='Command1.TButton')
    Button1_Start.place(relx=0.85, rely=0.021, relwidth=0.07, relheight=0.08)

    # 选择按钮
    style.configure('Command1.TButton',font=('微软雅黑',9))
    Button2_SelectImage = Button(top, text='选择', command=Command_SelectImage, style='Command1.TButton')
    Button2_SelectImage.place(relx=0.766, rely=0.021, relwidth=0.07, relheight=0.08)

    # 语音合成
    style.configure('Command1.TButton',font=('微软雅黑',9))
    button4_StopPlay = Button(top, text='语音合成', command=Command_Speech, style='Command1.TButton')
    button4_StopPlay.place(relx=0.89, rely=0.215, relwidth=0.105, relheight=0.082)

    # 翻译按钮
    style.configure('Command1.TButton',font=('微软雅黑',9))
    Button5_Translate = Button(top, text='翻译', style='Command1.TButton')
    Button5_Translate.place(relx=0.925, rely=0.021, relwidth=0.07, relheight=0.08)
    # 绑定鼠标右键事件
    Button5_Translate.bind("<Button-3>", lambda x: Translate_event(x))
    Button5_Translate.bind_all("<Control-Shift-C>", lambda x:Translate_event(x))
    # 绑定鼠标左键事件
    Button5_Translate.bind("<Button-1>", lambda x: Translate_event(x))
    Button5_Translate.bind_all("<Control-Shift-E>", lambda x:Translate_event(x))

    # 显示图片的路径
    Entry1_showPath_Var = StringVar(value='请通过点击“选择”按钮、拖动图片到此处、粘贴剪切板图片获取图片路径')
    Entry1_showPath = Entry(top, text='请通过点击“选择”按钮、拖动图片到此处、粘贴剪切板图片获取图片路径', textvariable=Entry1_showPath_Var, font=('微软雅黑',9))
    Entry1_showPath.place(relx=0.115, rely=0.024, relwidth=0.650, relheight=0.074)
    # 绑定鼠标右键事件
    Entry1_showPath.bind("<Button-3>", lambda x: Text1_MouseRightKey(x, Entry1_showPath)) 
    Entry1_showPath.bind("<Control-v>",lambda x: SaveClipboardPicture())

    # 显示识别结果
    Text2_showResult = Text(top, font=('微软雅黑',10), undo = True)
    Text2_showResult.place(relx=0, rely=0.32, relwidth=0.985, relheight=0.683)
    # 绑定鼠标右键事件
    Text2_showResult.bind("<Button-3>", lambda x: Text2_MouseRightKey(x, Text2_showResult)) 
    Text2_showResult.bind("<Control-v>", lambda x: SaveClipboardPicture())

    # text控件滚动条
    Slider3_scroll = tkinter.Scrollbar()
    Slider3_scroll.place(relx=0.985, rely=0.357, relwidth=0.10, relheight=0.683)
    # 关联到Text2_showResult控件
    Slider3_scroll.config(command=Text2_showResult.yview)
    Text2_showResult.config(yscrollcommand=Slider3_scroll.set)

    # label
    style.configure('Label1.TLabel',anchor='w', font=('微软雅黑',9))
    Label1 = Label(top, text='语速：', style='Label1.TLabel')
    Label1.place(relx=0.408, rely=0.250, relwidth=0.066, relheight=0.051)

    style.configure('Label1.TLabel',anchor='w', font=('微软雅黑',9))
    Label2 = Label(top, text='音量：', style='Label1.TLabel')
    Label2.place(relx=0.595, rely=0.250, relwidth=0.066, relheight=0.051)
    #Label2.place(relx=0.608, rely=0.262, relwidth=0.066, relheight=0.051)

    style.configure('Label1.TLabel',anchor='w', font=('微软雅黑',9))
    Label3 = Label(top, text='图片路径：', style='Label1.TLabel')
    Label3.place(relx=0.010, rely=0.026, relwidth=0.105, relheight=0.07)


    # 实例化类
    ocr = OCR(OCR_API_KEY,OCR_SECRET_KEY,TTS_APP_ID,TTS_API_KEY,TTS_SECRET_KEY,TRAN_APP_ID,TRAN_KEY)
    # 创建一个线程，用于调用语音合成
    newThread = threading.Thread(target=Speech)
    Welcome()
    # 显示窗口
    window.mainloop()