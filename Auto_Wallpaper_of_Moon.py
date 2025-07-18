# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Date    : 2018/10/6
# @Author  : 圈圈烃
# @File    : Auto_Wallpaper_of_Moon
# @Description: NASA月相图片下载 https://svs.gsfc.nasa.gov/
#
#
from AutoWallpaperSpider import AutoWallpaperSpider
import datetime
import math


def main():
    time_diff = datetime.datetime.utcnow() - datetime.datetime(2024, 1, 1, 0)  # 获取GMT时间并减2018-01-01,0时
    time_diff_hours = math.floor(time_diff.days * 24 + time_diff.seconds / 3600) + 1
    # 整合为链接 格式为：https://svs.gsfc.nasa.gov/vis/a000000/a004600/a004604/frames/730x730_1x1_30p/moon.0001.jpg 2018年1月1日0时UT
    # img_url = "https://svs.gsfc.nasa.gov/vis/a000000/a004600/a004604/frames/730x730_1x1_30p/moon." + str(time_diff_hours) + ".jpg"    # 2018年
    # img_url = "https://svs.gsfc.nasa.gov/vis/a000000/a004400/a004442/frames/730x730_1x1_30p/moon." + str(time_diff_hours) + ".jpg"      # 2019年
    # img_url = "https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004768/frames/730x730_1x1_30p/moon." + str(time_diff_hours) + ".jpg"      # 2020年
    # img_url = "https://svs.gsfc.nasa.gov/vis/a000000/a004800/a004874/frames/730x730_1x1_30p/moon." + str(time_diff_hours) + ".jpg"      # 2021年
    # img_url = "https://svs.gsfc.nasa.gov/vis/a000000/a004900/a004955/frames/730x730_1x1_30p/moon." + str(time_diff_hours) + ".jpg"      # 2022年
    # img_url = "https://svs.gsfc.nasa.gov/vis/a000000/a005100/a005187/frames/730x730_1x1_30p/moon." + str(time_diff_hours) + ".jpg"      # 2024年
    img_url = "https://svs.gsfc.nasa.gov/vis/a000000/a005400/a005415/frames/730x730_1x1_30p/moon." + str(time_diff_hours) + ".jpg"      # 2025年
    print(img_url)
    auto_wallpaper = AutoWallpaperSpider(img_url=img_url, img_name="moon.jpg", img_fill=True)
    auto_wallpaper.auto_main()


if __name__ == '__main__':
    main()



