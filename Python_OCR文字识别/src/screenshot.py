from PIL import ImageGrab # 读取剪切板
import winreg             # 读取注册表
import tkinter as tk      # 图形界面

class SelectionArea:
    """截图类的辅助类"""
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