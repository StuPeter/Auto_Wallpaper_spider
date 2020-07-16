#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/9/26
# @Author  : 圈圈烃
# @File    : Auto_Wallpaper_of_Earth
# @Description: 向日葵8号卫星图片下载 http://himawari8.nict.go.jp/
#
#
from AutoWallpaperSpider import AutoWallpaperSpider
import datetime
import time


def main():
    while True:
        try:
            # today = datetime.datetime.now().strftime("%Y/%m/%d/%H%M%S")  # 获取当前系统时间
            utc_today = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)  # 获取GMT时间并减去30分钟
            delat_utc_today = utc_today.strftime("%Y/%m/%d/%H%M")  # 时间格式化
            # 分钟向下取整
            delat_utc_today_list = list(delat_utc_today)
            delat_utc_today_list[-1] = "0"
            delat_utc_today = "".join(delat_utc_today_list)
            # 整合为链接 格式为：http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/2018/09/25/065000_0_0.png
            img_url = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/" + delat_utc_today + "00_0_0.png"
            auto_wallpaper = AutoWallpaperSpider(img_url=img_url, img_name="earth.jpg", img_fill=True)
            auto_wallpaper.auto_main()
        except:
            pass
        time.sleep(60)


if __name__ == '__main__':
    main()
