import base64
from tkinter import messagebox
import requests
from util import *


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

        except:
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
