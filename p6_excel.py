# -*- coding: utf-8 -*- #处理汉（双字节字符）

import matplotlib.pyplot as plt #引用matplotlib绘图，matplotlib的pyplot子库提供了和matlab类似的绘图API，方便用户快速绘制2D图表。
import numpy as np #科学计算工具
import math #数学函数库
from  statistics import mean,stdev,variance #引入平均数、标准差、方差
import xlrd #python语言中读取Excel的扩展工具
excel = xlrd.open_workbook('F:\Python\P6\p6.xlsx')  #打开EXCEL文件
sheet = excel.sheets()[0]  #打开表格

def r(x, y): 
   r=np.corrcoef(x,y)[0, 1] #计算皮尔逊相关系数
   return r

for i in range(0,4):       
    avg_x= mean(sheet.col_values(2*i)) #计算x的平均值、标准差、方差
    stdev_x= stdev(sheet.col_values(2*i)) 
    var_x= variance(sheet.col_values(2*i))
    print('x',i+1,'平均值:',avg_x,'标准差:',stdev_x,'方差:',var_x)

    avg_y= mean(sheet.col_values(2*i+1)) #计算y的平均值、标准差、方差
    stdev_y= stdev(sheet.col_values(2*i+1)) 
    var_y= variance(sheet.col_values(2*i+1))
    print('y',i+1,'平均值:',avg_y,'标准差:',stdev_y,'方差:',var_y)

    xgxs= r(sheet.col_values(2*i),sheet.col_values(2*i+1)) #计算x和y的相关系数
    print('x',i+1,'和y',i+1,'的相关系数：',xgxs)

plt.figure(figsize=(12.0,8.0)) #图大小
plt.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.95) #图间距
for i in range(0,4):
    ax=plt.subplot(221+i) #分别作图
    plt.sca(ax) #把ax设为当前的坐标轴
    plt.xlabel('x')     #设置X轴的文字
    plt.ylabel('y')     #设置y轴的文字
    plt.title('图'+str(i+1)) #设置图的标题
    plt.plot(sheet.col_values(2*i), sheet.col_values(2*i+1),'mo',label='图'+str(i+1))   #浣滄暎鐐瑰浘 
    x = np.array(sheet.col_values(2*i))          #pylab.array将列表转换为数组类型
    y = np.array(sheet.col_values(2*i+1))
    a,b = np.polyfit(x, y, 1) #返回一次项和常数项系数
    predict_y = a*np.array(x)+b #拟合的线性函数
    plt.plot(x,predict_y,
               label = 'Y by\nlinear fit, y = '
               + str(round(a, 6))+'*x+'+str(round(b, 6)),color="red") #作出拟合曲线
    plt.legend(loc = 'best') #添加图例，loc告诉matplotlib要将图例放在哪，“best”是不错的选择，因为它会选择最不碍事的位置。
    
plt.show()   #绘制图像