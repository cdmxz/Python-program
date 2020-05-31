#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys
import datetime
import requests
import base64
import json
import tkinter.messagebox
import tkinter.filedialog
import tkinter as tk

from pygame import mixer 
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
from aip import AipSpeech

fileName = ""
playMp3 = False
mixer.init()

def IsEmpty(str):
    " 如果字符串的值是None或""，则返回true "

    if str == None or str == "":
        return True
    else:
        return False


def GetAccessToken():
    "获取AccessToken"

    API_KEY = "ABHVET3G06m8RAmvE7lHCpkn"
    SECRET_KEY = "3vv0bG0P9MkAI0SRgabEgS3Hac8vHQPC"
   
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + API_KEY + '&client_secret=' + SECRET_KEY

    r = requests.get(host).json()
    result = r.get("access_token")
    if IsEmpty(result):
        raise Exception(r.get("error_description"))
    else:
        return result



def GeneralBasic(filePath,lang_type,detect_dire):
    "通用文字识别\n\
filePath    图片路径\n\
lang_type   要识别的语言类型\n\
detect_dire 是否检测图片朝向"

    try:
    # 如果有一项参数为空
        if IsEmpty(filePath) or IsEmpty(lang_type) or IsEmpty(detect_dire):
            raise Exception("输入参数不正确！")

        # 判断文件是否存在
        if not os.path.exists(filePath):
            raise Exception("文件不存在！")

        # 获取AccessToken
        access_token = GetAccessToken()
        if IsEmpty(access_token):
            raise Exception("获取AccessToken失败！")

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
            print(e)
            return e
    

def AccurateBasic(filePath,lang_type,detect_dire):
    "通用文字识别（高精度版）\n\
filePath    图片路径\n\
lang_type   要识别的语言类型\n\
detect_dire 是否检测图片朝向"

    try:
        # 如果有一项参数为空
        if IsEmpty(filePath) or IsEmpty(lang_type) or IsEmpty(detect_dire):
            raise Exception("输入参数不正确！")

        # 判断文件是否存在
        if not os.path.exists(filePath):
            raise Exception("文件不存在！")

        # 获取AccessToken
        access_token = GetAccessToken()
        if IsEmpty(access_token):
            raise Exception("获取AccessToken失败！")

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
        print(e)
        return e



def Handwriting(filePath):
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
        access_token = GetAccessToken()
        if IsEmpty(access_token):
            raise Exception("获取AccessToken失败！")

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
            print(e)
            return e



# 将识别后返回的 数字信息 转换为 中文信息
def GetIdcard_number_type(number):
    if number == -1:
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
def En_statusToCh_status(EnResult):
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
def En_typeToCh_type(EnType):
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


def Idcard(filePath,id_card_side,detect_dire):
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
        access_token = GetAccessToken()
        if IsEmpty(access_token):
            raise Exception("获取AccessToken失败！")

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


        edit,status,type,word = "","","",""
        #edit,status,type,re,name,gender,nation,birth,number,address,word =
        #"","","","","","","","","","",""
        if r.get("edit_tool") != None:
            edit = "\n编辑软件名称：" + r.get("edit_tool")
        
        if r.get("image_status") != None:
            status = r.get("image_status")
        if r.get("risk_type") != None:
            type = r.get("risk_type")
        

        word = "识别状态：" + En_statusToCh_status(status) + \
        "\n身份证类型：" + En_typeToCh_type(type) + edit

        if id_card_side == "front":
            word +="\n身份证号码、性别、出生是否一致：" + GetIdcard_number_type(r.get("idcard_number_type")) + \
            "\n姓名：" + r["words_result"]["姓名"]["words"] + \
            "\n性别：" + r["words_result"]["性别"]["words"] + \
            "\n民族：" + r["words_result"]["民族"]["words"] + \
            "\n出生：" + r["words_result"]["出生"]["words"] + \
            "\n身份证号码：" + r["words_result"]["公民身份号码"]["words"] + \
            "\n住址：" + r["words_result"]["住址"]["words"]
        else:
            word+="\n签发日期：" + r["words_result"]["签发日期"]["words"] + \
            "\n失效日期：" + r["words_result"]["失效日期"]["words"] + \
            "\n签发机关：" + r["words_result"]["签发机关"]["words"]

        return word.rstrip('\n') # 删除掉最后面的'\n'字符

    except Exception as e:
        print(e)
        return e



def Numbers(filePath,detect_dire):
    "数字识别\n\
filePath图片路径\n\
detect_dire 是否检测图片朝向"

    try:
        # 如果有一项参数为空
        if IsEmpty(filePath) or IsEmpty(detect_dire):
            raise Exception("输入参数不正确！")

        # 判断文件是否存在
        if not os.path.exists(filePath):
            raise Exception("文件不存在！")

        # 获取AccessToken
        access_token = GetAccessToken()
        if IsEmpty(access_token):
            raise Exception("获取AccessToken失败！")

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
        print(e)
        return e
        


def Speech(Text,Vol,Per,Spd):
    "文字转语音 （只支持中英文和数字）\n\
Text 要合成的文本内容\n\
Vol  音量大小\n\
Per  发音人\n\
Spd  语速快慢"

    try:
        # 全局变量
        global playMp3

        #如果文字为空
        if IsEmpty(Text):
            return  

        tts_APP_ID = "19685928"
        tts_API_KEY = "qk3y9G2FQLrQsCa9v9NzzW8h"
        tts_SECRET_KEY = "qtYsvvdEGgQ6EzxVSFuYRvl8NmzVihy1"
    
        # 获取当前时间，用作音频文件的文件名
        curr_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d_%H_%M_%S')
        # 语音合成
        client = AipSpeech(tts_APP_ID, tts_API_KEY, tts_SECRET_KEY)
        result = client.synthesis(Text, 'zh', 1, { 'vol': Vol,'per':Per,'spd':Spd })
        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            mp3Name = os.path.abspath('..') + '\\' + curr_time + '.mp3' 
            with open(mp3Name, 'wb') as f: 
                f.write(result)
        # 播放Mp3文件
        mixer.music.load(mp3Name)
        mixer.music.play()
        playMp3 = True

    except Exception as e:
        mixer.music.stop()
        playMp3 = False
        tkinter.messagebox.showerror("语音播放","Error:\n"+e)


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
    if informant == "女声":
        return 0
    elif informant == "男声":
        return 1
    elif informant == "度逍遥":
        return 3
    elif informant == "度丫丫":
        return 4


def Command_Play():
    global playMp3 # 全局变量

    if not playMp3:
        Speech(Text2_showResult.get('0.0', 'end').rstrip('\n'),Slider2.get(),InformantToNumber(ComboBox3_informant.get()),Slider1.get())
        playMp3 = True
    else:
        mixer.music.stop()
        playMp3 = False



def Command_Start():
    "开始识别"

    if Text1_showPath_Var.get() == "请先选择路径" or IsEmpty(Text1_showPath_Var.get()):
        tkinter.messagebox.showinfo("图片识别","请先选择文件！") # 弹出提示
        Command_SelectImage() # 调用“选择图片文件”函数
        return   

    if RadioVar.get() == 1: # 通用文字识别
        re = GeneralBasic(Text1_showPath_Var.get(),ChToEn(ComboBox1_lang.get()),CheckBox1Var.get())
    elif RadioVar.get() == 2:
        re = AccurateBasic(Text1_showPath_Var.get(),ChToEn(ComboBox1_lang.get()),CheckBox1Var.get())
    elif RadioVar.get() == 3:
        re = Handwriting(Text1_showPath_Var.get())
    elif RadioVar.get() == 4:  
        if ComboBox2.get() == "照片面": # 获取身份证照片面或国徽面
            f = "front"
        else:
            f = "back"
        re = Idcard(Text1_showPath_Var.get(),f,CheckBox1Var.get())  
    elif RadioVar.get() == 5:
        re = Numbers(Text1_showPath_Var.get(),CheckBox1Var.get())

    if IsEmpty(re):
        return

    # 将识别的内容显示到text控件
    if Text2_showResult.get('0.0', 'end') != "":            # 如果Text控件不为空
        Text2_showResult.delete('0.0',tkinter.END)   # 清空Text控件
    Text2_showResult.insert(INSERT,re)               # 向Text控件插入内容
def Command_SelectImage():
        "选择图片文件"

        fileName = tkinter.filedialog.askopenfilename(filetypes=[("jpg、png、bmp、webp、jpeg、tiff、pnm","*.jpg;*.png;*.bmp;*.webp;*.jpeg;*.tiff;*.pnm")])
        #print(fileName)
       
        if fileName == "": # 如果未选择文件
            return 
        # 否则将选择的图片路径显示到Text_showResult控件
        if Text1_showPath_Var.get() != "":
            Text1_showPath.delete('0',tkinter.END)
        Text1_showPath.insert(INSERT,fileName)
        pass



############################ 以下为界面设计代码 ###################################
window = tk.Tk()

# 窗口标题
window.title('OCR文字识别')
# 窗口高宽
window.geometry('618x336')

# 设置窗口的宽高为固定（不能改变大小）
window.resizable(0,0)

top = window.winfo_toplevel()
style = Style()

# Slider

# 音量滑动条
Slider2 = Scale(top, orient='horizontal', from_=0, to=15)
Slider2.place(relx=0.673, rely=0.238, relwidth=0.105, relheight=0.098)
Slider2.set(7)

# 发音语速滑动条
Slider1 = Scale(top, orient='horizontal', from_=0, to=9)
Slider1.place(relx=0.479, rely=0.238, relwidth=0.118, relheight=0.098)
Slider1.set(5)

# ComboBox

# 识别文字时是否检测图片朝向
CheckBox1Var = StringVar(value='1')
style.configure('Check1.TCheckbutton',font=('微软雅黑',10))
CheckBox1 = Checkbutton(top, text='检测图片朝向', variable=CheckBox1Var, style='Check1.TCheckbutton')
CheckBox1.place(relx=0.246, rely=0.238, relwidth=0.17, relheight=0.074)

# 选择要识别的图片中的语言
ComboBox1_lang_List = ['中英文混合','英文','葡萄牙语','法语','德语','意大利语','西班牙语','俄语','日语','韩语']
ComboBox1_lang = Combobox(top, state='readonly', values=ComboBox1_lang_List, font=('微软雅黑',10))
ComboBox1_lang.place(relx=0.013, rely=0.238, relwidth=0.12, relheight=0.08) # relx=0.013, rely=0.238, relwidth=0.105（0.209）, relheight=0.08
ComboBox1_lang.set(ComboBox1_lang_List[0])

 # 选择身份证正反面
ComboBox2List = ['照片面','国徽面']
ComboBox2 = Combobox(top, state='readonly',values=ComboBox2List, font=('微软雅黑',10))
ComboBox2.place(relx=0.14, rely=0.238, relwidth=0.10, relheight=0.08) # relx=0.129, rely=0.238, relwidth=0.105, relheight=0.08
ComboBox2.set(ComboBox2List[0])

# 发音人
ComboBox3_informant_List = ['女声','男声','度逍遥','度丫丫']
ComboBox3_informant = Combobox(top, state='readonly', values=ComboBox3_informant_List, font=('微软雅黑',10))
ComboBox3_informant.place(relx=0.79, rely=0.238, relwidth=0.105, relheight=0.08)
ComboBox3_informant.set(ComboBox3_informant_List[1])

# RadioButton

# 默认选中第一个单选框
RadioVar = IntVar()   
RadioVar.set(1)

# 通用文字识别单选按钮
style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
RadioButton1 = Radiobutton(top, text='通用文字识别', variable=RadioVar, value=1, style='Option1.TRadiobutton')
RadioButton1.place(relx=0.013, rely=0.143, relwidth=0.157, relheight=0.074)

# 通用文字识别（高精度版）单选按钮
style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
RadioButton2 = Radiobutton(top, text='通用文字识别（高精度版）',variable=RadioVar, value=2, style='Option1.TRadiobutton')
RadioButton2.place(relx=0.194, rely=0.143, relwidth=0.273, relheight=0.074)

# 手写文字识别单选按钮
style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
RadioButton3 = Radiobutton(top, text='手写文字识别',variable=RadioVar, value=3, style='Option1.TRadiobutton')
RadioButton3.place(relx=0.492, rely=0.143, relwidth=0.157, relheight=0.074)

# 身份证识别单选按钮
style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
RadioButton4 = Radiobutton(top, text='身份证识别',variable=RadioVar, value=4, style='Option1.TRadiobutton')
RadioButton4.place(relx=0.673, rely=0.143, relwidth=0.157, relheight=0.074)

# 数字识别单选按钮
style.configure('Option1.TRadiobutton',font=('微软雅黑',9))
RadioButton5 = Radiobutton(top, text='数字识别',variable=RadioVar, value=5, style='Option1.TRadiobutton')
RadioButton5.place(relx=0.854, rely=0.143, relwidth=0.131, relheight=0.074)

# Button

# 开始识别按钮
style.configure('Command1.TButton',font=('微软雅黑',9))
Button1_Start = Button(top, text='开始识别', command=Command_Start, style='Command1.TButton')
Button1_Start.place(relx=0.88, rely=0.024, relwidth=0.105, relheight=0.08)

# 选择图片按钮
style.configure('Command1.TButton',font=('微软雅黑',9))
Button2_SelectImage = Button(top, text='选择图片', command=Command_SelectImage, style='Command1.TButton')
Button2_SelectImage.place(relx=0.764, rely=0.024, relwidth=0.105, relheight=0.08)

# 文字转语音
style.configure('Command1.TButton',font=('微软雅黑',10))
button4_StopPlay = Button(top, text='播放', command=Command_Play, style='Command1.TButton')
button4_StopPlay.place(relx=0.906, rely=0.238, relwidth=0.079, relheight=0.082)

# Text

# 显示图片的路径
Text1_showPath_Var = StringVar(value='请先选择路径')
Text1_showPath = Entry(top, text='请先选择路径', textvariable=Text1_showPath_Var, font=('微软雅黑',9))
Text1_showPath.place(relx=0.129, rely=0.024, relwidth=0.623, relheight=0.074)

# 显示识别结果
Text2_showResult = Text(top, font=('微软雅黑',10))
Text2_showResult.place(relx=0., rely=0.357, relwidth=0.998, relheight=0.646)

# label
style.configure('Label1.TLabel',anchor='w', font=('微软雅黑',9))
Label1 = Label(top, text='语速：', style='Label1.TLabel')
Label1.place(relx=0.414, rely=0.262, relwidth=0.066, relheight=0.051)

style.configure('Label1.TLabel',anchor='w', font=('微软雅黑',9))
Label2 = Label(top, text='音量：', style='Label1.TLabel')
Label2.place(relx=0.608, rely=0.262, relwidth=0.066, relheight=0.051)

style.configure('Label1.TLabel',anchor='w', font=('微软雅黑',9))
Label3 = Label(top, text='图片路径：', style='Label1.TLabel')
Label3.place(relx=0.013, rely=0.024, relwidth=0.105, relheight=0.051)


# 显示窗口
mainloop()
