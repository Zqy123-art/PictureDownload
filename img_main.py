import os
import re
import sys
import sipbuild
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from img_download import Ui_MainWindow
from PyQt5.QtCore import QCoreApplication

class MyMainForm(QMainWindow, Ui_MainWindow):
    num = 0
    numPicture = 0
    file = ''

    def __init__(self, parent=None):

        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        #获取内容
        QMessageBox.warning(self, "提示", "测试版")
        QMessageBox.warning(self, "提示", "使用查询的时候请不要点击下载，使用下载的时候请不要点击查询！下载的图片均以jpg形式进行保存，这可能会导致一些图片无法正常显示")
        #判断是否联网
        try:
            html = requests.get("http://www.baidu.com")
        except:
            QMessageBox.warning(self, "警告", "使用之前请先联网！")
            os._exit(0)




        #添加点击事件
        self.pushButton.clicked.connect(lambda:self.Find())
        self.pushButton_3.clicked.connect(lambda: self.find_dir())
        self.pushButton_2.clicked.connect(lambda: self.dowmloadPicture())
    #查找图片
    def Find(self):
        self.textEdit.setText("")
        #获取关键字
        t = 0  # 翻一页
        i = 1
        s = 0  # 图片数量

        keyword = self.lineEdit.text()

        if keyword!='':
            self.textEdit.setText("正在检测图片总数，请稍等.....")
            QMessageBox.warning(self, "提示", "检测图片总数最大不超过1020，时间有点长，请中途不要中断此程序！")
            url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + '&pn='

            # 设置最大页数100页
            while t < 1000:
                Url = url + str(t)
                try:
                    Result = requests.get(Url, timeout=7)
                except BaseException:

                    t = t + 60
                    continue
                else:
                    result = Result.text
                    pic_url = re.findall('"objURL":"(.*?)",', result, re.S)  # 先利用正则表达式找到图片url
                    # pic_url所有图像集合
                    s += len(pic_url)
                    if len(pic_url) == 0:
                        # 没有图像就返回
                        break
                    else:
                        t = t +60
            self.textEdit.setText("经过检测"+keyword+"类图片共有"+str(s)+"张")




        else:
            QMessageBox.warning(self, "警告", "请输入搜索关键字")

    def down_img(self, html, keyword):

        pic_url = re.findall('"objURL":"(.*?)",', html, re.S)

        if len(pic_url) == 0:
            self.textEdit_2.append('...未找到图片...')
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            QMessageBox.warning(self, "提示", "下载结束！！！")
            return
        for each in pic_url:

            try:
                if each is not None:
                    pic = requests.get(each, timeout=7)  # url

                else:
                    continue
            except BaseException:
                self.textEdit_2.append('错误,第' + str(self.num + 1) + '图片无法下载,图片链接:'+each)
                continue
            else:
                # r''不转义
                string = self.file + r'\\' + keyword + '_' + str(self.num) + '.jpg'
                fp = open(string, 'wb')
                fp.write(pic.content)
                fp.close()
                self.num += 1
            if self.num >= int(self.img_num):
                self.lineEdit.setText("")
                self.lineEdit_2.setText("")
                self.lineEdit_3.setText("")

                return 1

    #下载图片
    def dowmloadPicture(self):
        self.num = 0

        self.textEdit_2.setText("")

        keyword = self.lineEdit.text()
        self.file = self.lineEdit_3.text()
        self.img_num = self.lineEdit_2.text()
        if keyword== '':
            QMessageBox.warning(self, "警告", "请输入搜索关键字")
            return
        if self.img_num == '':
            QMessageBox.warning(self, "警告", "请输入数量")
            return
        if self.file == '':
            QMessageBox.warning(self, "警告", "请选择文件")
            return
        if int(self.img_num)>200:
            QMessageBox.warning(self, "警告", "最大下载数量不得超过200")
            self.lineEdit_2.setText("")
            return
        t = 0

        self.textEdit_2.append("开始下载图片，请中途不要中断此程序，时间也许会很长,请等待...")
        QMessageBox.warning(self, "提示", "时间有点长，请中途不要中断此程序！")

        while t < int(self.img_num):
            url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + '&pn='
            try:
                url = url + str(t)
                result = requests.get(url, timeout=10)

            except :
                self.textEdit_2.append("下载错误,此网站"+url+"不可到达")
                t = t + 60
            else:
                html = result.text
                l = self.down_img(html, keyword)
                if l==1:
                    QMessageBox.warning(self, "提示", "下载结束！！！")
                    return
                t = t + 60
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        QMessageBox.warning(self, "提示", "下载结束！！！")




    def find_dir(self):
        directory1 = QFileDialog.getExistingDirectory(self)
        directory1 = directory1.replace("/",r"\\")
        self.lineEdit_3.setText(directory1)







if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()


        #程序运行，sys.exit方法确保程序完整退出。

    sys.exit(app.exec_())

