#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2023/8/3
# @Author  : 圈圈烃
# @File    : Auto_Wallpaper_of_Earth2
# @Description: 向日葵8号卫星图片下载 http://himawari8.nict.go.jp/ 多图拼接高清版本
#
#
from AutoWallpaperSpider2 import AutoWallpaperSpider2
import datetime


def main():
    # today = datetime.datetime.now().strftime("%Y/%m/%d/%H%M%S")  # 获取当前系统时间
    utc_today = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)  # 获取GMT时间并减去30分钟
    delat_utc_today = utc_today.strftime("%Y/%m/%d/%H%M")  # 时间格式化
    # 分钟向下取整
    delat_utc_today_list = list(delat_utc_today)
    delat_utc_today_list[-1] = "0"
    delat_utc_today = "".join(delat_utc_today_list)
    # 生成链接 格式为：https://himawari8.nict.go.jp/img/D531106/4d/550/2023/08/03/020000_0_0.png, 其中4d表示图片为4*4，2d为2*2,左上角图片为0_0
    img_urls = []
    for x in range(4):
        for y in range(4):
            base_url = 'https://himawari8.nict.go.jp/img/D531106/4d/550/%s00_%s_%s.png' % (delat_utc_today, y, x)
            # base_url = 'https://himawari8.nict.go.jp/img/D531106/4d/550/2023/08/03/023000_%s_%s.png' % (y, x)
            print(base_url)
            img_urls.append(base_url)
    auto_wallpaper = AutoWallpaperSpider2(img_urls=img_urls, img_name="earth2.jpg", img_fill=False)
    auto_wallpaper.auto_main()


if __name__ == '__main__':
    main()
