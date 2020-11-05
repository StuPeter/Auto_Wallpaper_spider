# Python 定时获取卫星图像做为桌面背景
---
## 简介
这两天看新闻的时候，突然发现最近有个台风产生，并且在不断的增强中。幸运的是从中央气象台预报的路径来看，不会登陆我国。也正是通过这则新闻，我发现了一个不错的卫星云图网站。

[向日葵-8号实时网页](http://himawari8.nict.go.jp/)

简单的介绍一下，向日葵-8号是日本气象厅的一颗气象卫星，于2014年10月7日发射。设计寿命15年以上，主要用于检测暴雨云团、台风动向和火山活动等防灾领域。

因为是日本的网站，所以访问的速度可能会比较慢。网页截图如下：

![](https://i.imgur.com/3W46xV1.png)

下面我将简单的介绍一下如何将这个网站上定时更新的卫星云图爬取下来，设置为自己的电脑桌面。这样每时每刻你都可以关注到西太平洋上空的动态了。哈哈哈哈~

## Python实现思路

### 1. 获取卫星云图
由于这个是日本的网站，所以访问的速度可能会有点慢。但是只要能够正常访问就都不是问题。
首先对这个网站进行分析，打开firebug看看先：

![](https://i.imgur.com/nBHf2hn.png)


从图中，我们可以看到只要获取图片的链接，用get方法就能够直接下载到本地了。因此要获取这个网站的图片是非常的简单的，如果会一点python爬虫知识，很容易就能够将这张图片爬取下来。选择就是具体的分析一下图片的链接是这么组成的呢？

[http://himawari8-dl.nict.go.jp/himawari8/img/D531106/thumbnail/550/2018/09/26/063000_0_0.png](http://himawari8-dl.nict.go.jp/himawari8/img/D531106/thumbnail/550/2018/09/26/063000_0_0.png)

为了便于理解，我把它拆分为以下几条：

链接段     | 意思（我猜的）
-------- | -----
 http://himawari8-dl.nict.go.jp/ | 网站域名
himawari8/  | 卫星名字：向日葵8号
img/  | 图片
D531106/  | 布吉岛
thumbnail/  | 布吉岛
550/  | 卫星图像像素
2018/09/26/ | 卫星图像日期
063000_0_0 | 卫星图像时间（GMT：格林威治标准时间）
.png | 图像格式（GMT：格林威治标准时间）

好了，通过上面的分析，我们其实只要修改**卫星图像日期**和**卫星图像时间**就可以获取你想要的时间段的卫星图像图片了。但是要注意的是，你不可能获取未来的图片。

接下来贴上程序：
	
	#!/usr/bin/env python  
	# _*_ coding:utf-8 _*_  
	#  
	# @Version : 1.0  
	# @Time    : 2018/9/25
	# @Author  : 圈圈烃
	# @File    : NICT_download
	# @Description: http://himawari8.nict.go.jp/ 向日葵8号卫星实时图片下载
	#
	#
	from PIL import Image
	import requests
	import re
	import datetime
	
	
	def download_img(url, img_save_path):
	    img = requests.get(url)
	    with open(img_save_path, "wb") as fwi:
	        fwi.write(img.content)
	        print(img_save_path + "图片下载成功")

	
	def fill_img(img, img_save_path):
	    width, height = 1920, 1080      # 电脑屏幕大小
	    new_img = Image.new(img.mode, (width, height), color='black')
	    new_img.paste(img, (int(width/2 - 250), int(height/2 - 250)))
	    new_img.save(img_save_path)
	    print(img_save_path + "图片合成成功")
	
	
	def dl_main():
	    # 获取当前系统时间
	    utc_today = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)  # 获取GMT时间并减去30分钟
	    delat_utc_today = utc_today.strftime("%Y/%m/%d/%H%M")  # 时间格式化
	    # 分钟向下取整
	    delat_utc_today_list = list(delat_utc_today)
	    delat_utc_today_list[-1] = "0"
	    delat_utc_today = "".join(delat_utc_today_list)
	    # 整合为链接 格式为：http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/2018/09/25/065000_0_0.png
	    img_url = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/" + delat_utc_today + "00_0_0.png"
	    name = delat_utc_today.replace("/", "_") + "00_0_0.png"  # 获取图片名字
	    # 图片保存路径
	    img_save_path = "Download_Picture/" + name
	    new_img_save_path = "Wallpaper/new_" + name
	    # 下载图片
	    download_img(img_url, img_save_path)
	    # 合成图片
	    img = Image.open(img_save_path)
	    fill_img(img, new_img_save_path)
	    return new_img_save_path
	
	
	if __name__ == '__main__':
	    dl_main()

在上面的程序中，有个 **fill_img(img, img_save_path)** 函数，由于我们获取的卫星图像的大小为550*550，直接作为背景不好看，所以在这里对这个图片进行填充，填充背景为黑色。至于最后图片的大小可以根据自己显示器的屏幕大小来修改。 

### 2. 设置桌面背景

成功获取图片之后就是将获取的图片设置为左面的壁纸了，我的系统是win10，亲测可用。

	#!/usr/bin/env python  
	# _*_ coding:utf-8 _*_  
	#  
	# @Version : 1.0  
	# @Time    : 2018/9/25
	# @Author  : 圈圈烃
	# @File    : Auto_Wallpaper
	# @Description: 自动设置桌面壁纸
	#
	#
	import win32api, win32con, win32gui
	import NICT_Download
	
	
	def set_desktop_windows(imagepath):
	    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
	    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")  # 2拉伸适应桌面，0桌面居中
	    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
	    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imagepath, 1 + 2)
	
	
	if __name__ == '__main__':
	    print("正在下载图片")
	    try:
	        new_img_save_path = NICT_Download.dl_main()
	    except Exception as e:
	        print(e)
	    # 这里的路径必须为绝对路径
	    wallpaper_path = "D:\\Users\\Administrator\\Documents\\Python Files\\Auto_Background\\" + new_img_save_path
	    set_desktop_windows(wallpaper_path)

效果图为：

![](https://i.imgur.com/QJiT8cs.png)

### 3. 开启定时更新

为了实现能够定时更新桌面的卫星图像，我们需要设置定时任务。通过分析可知，[向日葵-8号实时网页](http://himawari8.nict.go.jp/)每隔10分钟会更新图片，所以我们也设置为10分钟更新一次。

1. 打开 win10 的计划任务程序
2. 创建任务![](https://i.imgur.com/dHSCRr1.png)
3. 填写任务名称![](https://i.imgur.com/gjq3tMm.png)
4. 新建触发器，如图设置![](https://i.imgur.com/zfjg9u9.png)
5. 新建操作，如图设置，这里注意一点：不要用python.exe 打开py文件，使用pythonw.exe 打开pyw文件。这样就不会出现哪个黑色的cmd窗口。![](https://i.imgur.com/CyvkUdN.png)
6. 接下来就是一直“确定”。
7. 完成设置![](https://i.imgur.com/mMeo8XU.png)


## 最后

实现效果：
![](https://i.imgur.com/2UZxXWT.gif)

希望对大家有所帮助！：-）

## 补充

项目打包命令：
 `pyinstaller Auto_Wallpaper_of_Earth.py -w -i "F:\Users\QQT\Documents\Python Projects\Auto_Wallpaper_spider\icon\earth.ico" --version-file version_file_earth.txt -F`