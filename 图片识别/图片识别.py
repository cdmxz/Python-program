# -*- coding:utf-8 -*-
'''
说明：
开源地址：https://fuhohua.gitee.io
已在 win10 2004 + python3.7.8 32bit 环境下测试过，可正常使用。
使用前请安装库：wx和requests
终端输入pip命令安装：pip install wxpython requests
'''
# author：傅宏华
# datetime：2021/05/01


import wx
import os
import requests
import base64

# 百度图片识别Key（可以去百度ai开放平台（https://cloud.baidu.com/product/imagerecognition）申请）
Api_Key = ""
Sercet_Key = ""


class CaptureFrame(wx.Frame):
    '''截图类'''

    def __init__(self, frame):
        wx.Frame.__init__(self, frame, -1, pos=(0, 0),
                          size=wx.GetDisplaySize(), style=wx.NO_BORDER | wx.STAY_ON_TOP)
        self.firstPoint = wx.Point(0, 0)  # 起始坐标（矩形左上角坐标）
        self.lastPoint = wx.Point(0, 0)  # 结束坐标（矩形右下角坐标）
        self.pressLeftKey = False  # 是否按下鼠标左键
        self.frame = frame  # 父窗体
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.PaintEvent)  # 绑定窗体重绘事件
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseLeftDownEvent)  # 绑定鼠标左键按下事件
        self.Bind(wx.EVT_RIGHT_DOWN, self.MouseRightDownEvent)  # 绑定鼠标右键按下事件
        self.Bind(wx.EVT_KEY_DOWN, self.KeyDownEvent)  # 绑定键盘按下事件
        self.Bind(wx.EVT_LEFT_UP, self.MouseLeftUpEvent)  # 绑定鼠标左键松开事件
        self.Bind(wx.EVT_MOTION, self.MouseMoveEvent)  # 绑定鼠标移动事件
        self.Bind(wx.EVT_SHOW, self.MouseMoveEvent)  # 绑定鼠标移动事件

    def Start(self):
        '''开始截图'''
        self.fullScreenImg = self.CopyScreen()  # 拷贝屏幕图像
        self.Show()

    def CopyScreen(self):
        '''拷贝屏幕'''
        size = wx.GetDisplaySize()  # 获取屏幕分表率
        bmp = wx.Bitmap(size.x, size.y)  # 创建一个和屏幕一样大的位图
        # 拷贝桌面内容到图片
        dc = wx.ScreenDC()
        memdc = wx.MemoryDC()
        memdc.SelectObject(bmp)
        memdc.Blit(0, 0, size.x, size.y, dc, 0, 0)
        memdc.SelectObject(wx.NullBitmap)
        return bmp

    def PaintEvent(self, event):
        '''窗体重绘事件'''
        dc = wx.GCDC(wx.BufferedPaintDC(self))
        self.PaintUpdate(dc)

    def PaintUpdate(self, dc):
        '''在屏幕上绘制鼠标拖动的矩形'''
        rect = self.GetClientRect()
        color = wx.Colour(0, 0, 0, 100)
        # 设置绘制截图区域时矩形的点
        minX = min(self.firstPoint.x, self.lastPoint.x)
        minY = min(self.firstPoint.y, self.lastPoint.y)
        maxX = max(self.firstPoint.x, self.lastPoint.x)
        maxY = max(self.firstPoint.y, self.lastPoint.y)
        # 画出整个屏幕的截图
        dc.DrawBitmap(self.fullScreenImg, 0, 0)
        # 画出阴影部分（截取的部分不需要画）
        dc.SetPen(wx.Pen(color))
        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangle(0, 0, maxX, minY)
        dc.DrawRectangle(maxX, 0, rect.width - maxX, maxY)
        dc.DrawRectangle(minX, maxY, rect.width - minX, rect.height - maxY)
        dc.DrawRectangle(0, minY, minX, rect.height - minY)
        if(self.pressLeftKey == True):
            # 绘制鼠标选定的边框
            dc.SetPen(wx.Pen(wx.Colour(30, 144, 255)))
            dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
            dc.DrawRectangle(minX, minY, maxX - minX, maxY - minY)
            # 绘制边框上的点
            dc.SetBrush(wx.Brush(wx.Colour(30, 144, 255)))
            dc.DrawRectangleList([
                (minX - 2, minY - 2, 5, 5),
                (maxX / 2 + minX / 2 - 2, minY - 2, 5, 5),
                (maxX - 2, minY - 2, 5, 5),
                (maxX - 2, maxY / 2 + minY / 2 - 2, 5, 5),
                (maxX - 2, maxY - 2, 5, 5),
                (maxX / 2 + minX / 2 - 2, maxY - 2, 5, 5),
                (minX - 2, maxY - 2, 5, 5),
                (minX - 2, maxY / 2 + minY / 2 - 2, 5, 5)
            ])
            color = wx.Colour(0, 0, 0, 180)
            dc.SetPen(wx.Pen(color))
            dc.SetBrush(wx.Brush(color, wx.SOLID))
            w, h = 140, 49
            # 显示坐标文字
            s = f'按鼠标右键或ESC键退出\n矩形大小：{str(maxX - minX)}*{str(maxY - minY)}\n鼠标坐标：{str(self.lastPoint.x)}, {str(self.lastPoint.y)}'
            dc.DrawRectangle(minX, minY-h-5 if minY - 5 > h else minY+5, w, h)
            dc.SetTextForeground(wx.Colour(255, 255, 255))
            dc.DrawText(s, minX+5, (minY-h-5 if minY-5 > h else minY + 5)+5)

    def MouseLeftDownEvent(self, event):
        '''鼠标左键按下事件'''
        self.pressLeftKey = True
        self.firstPoint = event.GetPosition()
        self.lastPoint = event.GetPosition()

    def MouseLeftUpEvent(self, event):
        '''鼠标左键松开事件'''
        if(not self.pressLeftKey):
            return
        self.lastPoint = event.GetPosition()  # 获取当前鼠标坐标，也就是矩形右下角坐标
        if(self.firstPoint.x == self.lastPoint.x) and (self.firstPoint.y == self.lastPoint.y):
            wx.MessageBox(u"选择的区域不正确！", u"错误", wx.OK | wx.ICON_ERROR, self)
        else:
            # 获取选择的矩形大小和坐标
            self.selectedRect = wx.Rect(
                min(self.firstPoint.x, self.lastPoint.x),
                min(self.firstPoint.y, self.lastPoint.y),
                abs(self.firstPoint.x - self.lastPoint.x),
                abs(self.firstPoint.y - self.lastPoint.y)
            )
            # 在截取的全屏图像上，拷贝选择的矩形区域
            self.captureBmp = self.fullScreenImg.GetSubBitmap(
                self.selectedRect)
        # 关闭截图
        self.CloseCapture()
        ShowPicture(self.captureBmp)

    def MouseMoveEvent(self, event):
        '''鼠标移动事件'''
        if(self.pressLeftKey):
            self.lastPoint = event.GetPosition()  # 保存矩形右下角的坐标
            self.NewUpdate()  # 重绘矩形

    def NewUpdate(self):
        '''重绘矩形'''
        self.RefreshRect(self.GetClientRect(), True)
        self.Update()

    def MouseRightDownEvent(self, event):
        '''鼠标右键按下事件'''
        self.CloseCapture()  # 取消截图

    def KeyDownEvent(self, event):
        '''键盘按下事件'''
        if event.GetKeyCode() == 27:  # 如果按下esc键
            self.CloseCapture()  # 则关闭截图

    def CloseCapture(self):
        '''关闭截图'''
        self.Close()
        self.frame.Show()


def ShowPicture(bmp):
    '''显示图片到主界面'''
    image = bmp.ConvertToImage().Rescale(285, 125).ConvertToBitmap()  # 文件转为图像流
    app.frame.staticBitmap.SetBitmap(wx.Bitmap(image))  # 显示到主界面
    file = "temp.bmp"
    if os.path.exists(file):
        os.remove(file)
    # 先将文件流保存到文件，再识别
    bmp.SaveFile(file, wx.BITMAP_TYPE_BMP)
    ShowText(ident.Ident(file))
    os.remove(file)


def ShowImageFile(file):
    '''显示图片到主界面'''
    image = wx.Image(file, wx.BITMAP_TYPE_ANY).Rescale(
        285, 125).ConvertToBitmap()  # 文件转为图像流
    app.frame.staticBitmap.SetBitmap(wx.Bitmap(image))  # 显示到主界面
    ShowText(ident.Ident(file))  # 图片识别


def ShowText(text):
    '''显示文本到主界面'''
    app.frame.textctrl.Clear()
    app.frame.textctrl.AppendText(text)


class Frame(wx.Frame):
    '''主界面'''

    def __init__(self):
        wx.Frame.__init__(self, None, title=u'图片识别 by:黄坑中学-傅宏华', size=(
            426, 539), name='frame', style=541072384)
        self.window = wx.Panel(self)
        self.Centre()
        self.staticBitmap = wx.StaticBitmap(self.window, -1, size=(287, 126), pos=(
            14, 12), name='staticBitmap', style=33554432)
        self.button_capture = wx.Button(self.window, size=(91, 41), pos=(
            305, 97), label=u'截图', name='button')
        self.button_capture.Bind(wx.EVT_BUTTON, self.button_capture_click)
        self.button_openFile = wx.Button(self.window, size=(91, 41), pos=(
            305, 11), label=u'打开', name='button')
        self.button_openFile.Bind(wx.EVT_BUTTON, self.button_openFile_click)
        self.textctrl = wx.TextCtrl(self.window, size=(385, 326), pos=(
            14, 150), value='', name='text', style=1073741872)

        # 拖拽图片文件
        self.fileDrop = FileDrop(self.staticBitmap)
        self.staticBitmap.SetDropTarget(self.fileDrop)
        # 打开文件对话框，选择的图片类型
        self.wildcard = u"图片文件（*.jpg、*.png、*.bmp、*.webp、*.jpeg、*.tiff）|*.jpg;*.png;*.bmp;*.webp;*.jpeg;*.tiff;"

    def button_capture_click(self, event):
        '''截图'''
        f = CaptureFrame(self)
        self.Hide()  # 隐藏主窗体
        wx.MilliSleep(500)  # 延时500毫秒，等待窗体隐藏
        f.Start()

    def button_openFile_click(self, event):
        dlg = wx.FileDialog(self, message=u'打开图片', defaultDir='',
                            defaultFile='', wildcard=self.wildcard, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            file = dlg.GetPath()
            ShowImageFile(file)
        dlg.Destroy()


class FileDrop(wx.FileDropTarget):
    '''文件拖拽'''

    def __init__(self, staticBitmap):
        wx.FileDropTarget.__init__(self)
        self.staticBitmap = staticBitmap

    def OnDropFiles(self, x, y, filePath):  # 文件被拖入图片框
        # try:
        ShowImageFile(filePath[0])
        # except:
        #     wx.MessageBox(u"此图片格式不受支持！", u"错误", wx.OK | wx.ICON_ERROR)
        return True


class IdentPicture:
    '''图片识别类'''

    def __init__(self, ak, sk):
        self.OCR_AK = ak
        self.OCR_SK = sk

    def GetAccessToken(self):
        '''获取文字识别AccessToken'''
        try:
            host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + \
                self.OCR_AK + '&client_secret=' + self.OCR_SK
            r = requests.get(host).json()
            result = r.get("access_token")
            if self.IsEmpty(result):
                raise Exception(r.get("error_description"))
            else:
                return result
        except Exception as e:
            wx.MessageBox(u"获取图片识别Token失败！\n原因：" +
                          str(e.args[0]), u"错误", wx.OK | wx.ICON_ERROR)
            return None

    def Ident(self, file):
        try:
            request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
            # 二进制方式打开图片文件
            f = open(file, 'rb')
            img = base64.b64encode(f.read())
            params = {"image": img}
            access_token = self.GetAccessToken()
            if(access_token == None):
                return
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                # print(response.json())
                return self.ParseJson(response.json())
        except Exception as e:
            wx.MessageBox(u"图片识别失败！\n原因：" +
                          str(e.args[0]), u"错误", wx.OK | wx.ICON_ERROR)
            return None

    def ParseJson(self, js):
        if int(js.get("result_num")) == 0:
            return "未获取到数据"
        word = ""
        for result in js.get("result"):
            word += u"图片信息："+result["root"]+u"\n关键字：" + \
                result["keyword"]+u"\n相似度："+str(result["score"])+u"\n\n"
            if "baike_info" in result.keys() and "description" in result["baike_info"]:
                word = word.rstrip('\n') + \
                    "\n百度百科："+result["baike_info"]["description"] + "\n\n"
        return word.rstrip('\n')

    def IsEmpty(self, Str):
        " 如果字符串的值是None或""，则返回true "
        if Str == None or Str == "":
            return True
        else:
            return False


class myApp(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True


if __name__ == '__main__':
    app = myApp()
    # 实例化图片识别类
    ident = IdentPicture(Api_Key, Sercet_Key)
    app.MainLoop()
