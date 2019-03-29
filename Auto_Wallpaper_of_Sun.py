#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2019/3/29
# @Author  : 圈圈烃
# @File    : Auto_Wallpaper_of_Sun
# @Description:
#
#
from AutoWallpaperSpider import AutoWallpaperSpider
import datetime
import math


def main():
    img_url = "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0304.jpg"
    # img_url = "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171.jpg"
    auto_wallpaper = AutoWallpaperSpider(img_url=img_url, img_name="sun.jpg", img_fill=True)
    auto_wallpaper.auto_main()


if __name__ == '__main__':
    main()

