import datetime
import os


def IsEmpty(Str):
    " 如果字符串的值是None或""，则返回true "
    if Str == None or Str == "":
        return True
    else:
        return False

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