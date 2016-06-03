# -*- coding: utf-8 -*- #处理汉（双字节字符）

import matplotlib.pyplot as plt #引用matplotlib绘图，matplotlib的pyplot子库提供了和matlab类似的绘图API，方便用户快速绘制2D图表。
import numpy as np #科学计算工具
import math #数学函数库
from  statistics import mean,stdev,pstdev,variance,pvariance #引入平均数、标准差、样本总体的标准偏差、方差、样本总体的标准偏差

from prettytable import PrettyTable #python通过prettytable模块可以将输出内容如表格方式整齐的输出。
import glob #在python中，glob模块是用来查找匹配的文件的

filenames=[] #文件列表

xygroup=[] #每个文件中的x,y，列表的每个元素是一个文件中的x,y

xstagroup=[] #每个文件中x的数据处理结果，列表的每个元素是一个文件中的x的数据处理结果
ystagroup=[] #每个文件中y的数据处理结果，列表的每个元素是一个文件中的y的数据处理结果
rgroup=[] #每个文件中x,y的相关性系数，列表的每个元素是一个文件中的x,y的相关性系数

lfit=[] #每个文件中x,y的线性拟合参数，列表的每个元素是一个文件中的x,y的线性拟合参数

def getData_TextFile(fileName): #读文件函数

    dataFile = open(fileName, 'r') #读文件，read

    xy={'x':[],'y':[]} #xy是字典，用来分类描述x和y,x和y分别用来存放x和y的元素，采用列表的形式
    discardHeader = dataFile.readline() #按行读文件

    for line in dataFile:
        x,y= line.split(';') #分离x,y
        xy['x'].append(float(x)) #在xy字典的键x所对应的列表中添加x
        xy['y'].append(float(y)) #在xy字典的键y所对应的列表中添加y

    dataFile.close() #关闭文件

    return xy #返回xy字典

def satData(x,y):
    xsta={'avg':None,'stdev':None,'pstdev':None,'var':None,'pvar':None} #x的数据处理，将各个数放入字典中
    ysta={'avg':None,'stdev':None,'pstdev':None,'var':None,'pvar':None} #y的数据处理，将各个数放入字典中

    xsta['avg']=mean(x) #x平均数
    ysta['avg']=mean(y) #y平均数

    xsta['stdev']=stdev(x) #x标准差
    ysta['stdev']=stdev(y) #y标准差

    xsta['pstdev']=pstdev(x) #x样本总体的标准偏差
    ysta['pstdev']=pstdev(y) #x样本总体的标准偏差

    xsta['var']=variance(x) #x方差
    ysta['var']=variance(y) #y方差

    xsta['pvar']=pvariance(x) #x样本总体的方差
    ysta['pvar']=pvariance(y) #y样本总体的方差

    r=np.corrcoef(x,y)[0, 1] #x、y的相关性系数

    return  xsta,ysta,r #返回各数

def fitData(x,y):
    #find linear fit 线性拟合
    a,b = np.polyfit(x,y,1) #返回一次项和常数项系数
    predictedY = a*np.array(x) + b #拟合的线性函数
    return a,b,predictedY #返回拟合结果

def plotData(x,y,a,b, predictedY,fileName):
    plt.plot(x,y, 'm*',
               label= fileName) #画散点图

    plt.title(fileName)
    plt.xlabel('x') #设置X轴的文字
    plt.ylabel('y') #设置y轴的文字

    plt.plot(x,predictedY,
               label = 'Y by\nlinear fit, y = '
               + str(round(a, 6))+'*x+'+str(round(b, 6)),color="red") #画拟合曲线图

    plt.legend(loc = 'best') #添加图例，loc告诉matplotlib要将图例放在哪，“best”是不错的选择，因为它会选择最不碍事的位置。

def processing_one_TextFile(filename):

    xy=getData_TextFile(filename) #得到x,y数据

    xsta,ysta,r=satData(xy['x'],xy['y']) #得到各种数据处理后的数

    a,b,predictedY=fitData(xy['x'],xy['y']) #得到线性拟合参数

    return xy,xsta,ysta,r,a,b,predictedY

def processing_data_TextFiles(filenames):

    for i in range(len(filenames)): #分别处理文件

        xy,xsta,ysta,r,a,b,predictedY =processing_one_TextFile(filenames[i])

        xygroup.append(xy) #添加每个文件里的x,y

        xstagroup.append(xsta) #添加每个x的数据处理结果
        ystagroup.append(ysta) #添加每个y的数据处理结果

        rgroup.append(r) #添加每个文件中x、y的相关性系数

        lfit.append({'a':a,'b':b,'preY':predictedY}) #添加每个文件中x和y线性拟合参数

def processing_plot_TextFiles(filenames):

    fig=plt.figure(figsize=(12.0,8.0)) #图大小

    fig.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.95) #图间距

    figcount=len(filenames) #图总数

    figcol=2 #2列
    figrow=math.ceil(figcount/figcol) #多少行

    for i in range(figcount):
        fig.add_subplot(figrow, figcol,i+1) #分别加图、画图
        plotData(xygroup[i]['x'],xygroup[i]['y'],
                 lfit[i]['a'],lfit[i]['b'],lfit[i]['preY'],filenames[i])

    plt.show() #显示

def processing_table_TextFiles(filenames):

    table = PrettyTable(["data set",
                         "x-avg", "x-std", "x-pstd", "x-var","x-pvar",
                         "y-avg", "y-std", "y-pstd", "y-var","y-pvar",
                         "pearson_r"]) #表格第一行

    table.align= "r" # right align
    table.padding_width = 1 # One space between column edges and contents (default)

    for i in range(len(filenames)):
        table.add_row([filenames[i],
                   "%.3f" % xstagroup[i]['avg'],
                   "%.3f" % xstagroup[i]['stdev'],"%.3f" %xstagroup[i]['pstdev'],
                   "%.3f" % xstagroup[i]['var'],"%.3f" % xstagroup[i]['pvar'],
                   "%.3f" % ystagroup[i]['avg'],
                   "%.3f" % ystagroup[i]['stdev'],"%.3f" % ystagroup[i]['pstdev'],
                   "%.3f" % ystagroup[i]['var'],"%.3f" % ystagroup[i]['pvar'],
                   "%.3f" % rgroup[i]]) #绘制表格
    print(table)

if __name__ == '__main__':

    filenames=glob.glob(r'F:\python\P6\*.txt')
 
    processing_data_TextFiles(filenames)
    processing_table_TextFiles(filenames)
    processing_plot_TextFiles(filenames)