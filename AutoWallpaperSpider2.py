#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2023/8/3
# @Author  : 圈圈烃
# @File    : AutoWallpaperSpider2
# @Description:
#
#
from PIL import Image
import win32api
import win32con
import win32gui
import requests
import datetime
import os


class AutoWallpaperSpider2:
    def __init__(self, img_urls, img_name, img_fill=False):
        """
        初始化
        :param img_urls: 图片链接列表
        :param img_name: 图片名称
        :param img_fill: 图片是否需要填充
        """
        self.img_urls = img_urls
        self.img_name = img_name
        self.img_fill = img_fill
        self.wallpaper_paths = []

    def check_drive(self):
        """检测盘符, 创建保存路径"""
        # 检测盘符
        drive_list = list()
        for i in range(65, 91):
            drive_name = "%s:" % chr(i)
            if os.path.isdir(drive_name):
                drive_list.append(drive_name)
        # 创建保存路径
        self.wallpaper_dir = "%s\\Program Files\\AutoWallpaper\\" % drive_list[2]  # 第二个盘中创建路径
        try:
            os.makedirs(self.wallpaper_dir)
        except Exception as e:
            print(e)

    def download_img(self):
        """下载并合成图片"""
        # 下载图片
        for index, img_url in enumerate(self.img_urls):
            try:
                temp_path = self.wallpaper_dir + self.img_name.replace('.', '_%s.' % index)
                self.wallpaper_paths.append(temp_path)
                img_content = requests.get(img_url, timeout=20, verify=False)
                with open(temp_path, 'wb') as fw:
                    fw.write(img_content.content)
                with open(self.wallpaper_dir + "log.log", 'a') as fw:
                    fw.write("[" + datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + "] %s  图片下载成功...\n" % temp_path)
                print("[" + datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S") + "] %s  图片下载成功..." % temp_path)
            except Exception as e:
                with open(self.wallpaper_dir + "log.log", 'a') as fw:
                    fw.write("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] error: %s  \n" % e)
                os._exit(1)
        # 合成大图
        img_row = 3
        img_col = 4
        img_width = 550 * img_col
        img_height = 550 * img_row
        self.wallpaper_path = self.wallpaper_dir + self.img_name
        to_img = Image.new('RGB', (img_width, img_height))
        count = 0
        for y in range(1, img_row + 1):
            for x in range(1, img_col + 1):
                from_image = Image.open(self.wallpaper_paths[count])
                to_img.paste(from_image, ((x - 1) * 550, (y - 1) * 550))
                count += 1
        return to_img.save(self.wallpaper_path)  # 保存新图

    def fill_img(self):
        """合成图片"""
        if self.img_fill:
            img_content = Image.open(self.wallpaper_path)
            img_width, img_height = img_content.size  # 图片大小
            monitor_width, monitor_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)  # 电脑屏幕大小
            fill_img_content = Image.new(img_content.mode, (monitor_width, monitor_height), color='black')
            fill_img_content.paste(img_content,
                                   (int(monitor_width / 2 - img_width / 2), int(monitor_height / 2 - img_height / 2)))
            fill_img_content.save(self.wallpaper_path)
            with open(self.wallpaper_dir + "log.log", 'a') as fw:
                fw.write("[" + datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S") + "] %s  图片合成成功...\n" % self.wallpaper_path)
            print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] %s  图片合成成功..." % self.wallpaper_path)
        else:
            pass

    def set_desktop(self):
        """设置桌面"""
        k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "6")  # 2拉伸,0居中,6适应,10填充,0平铺
        win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.wallpaper_path, 1 + 2)

    def auto_main(self):
        """主函数"""
        self.check_drive()
        self.download_img()
        self.fill_img()
        self.set_desktop()


if __name__ == '__main__':
    # 测试例子
    url = "https://cn.bing.com/az/hprichbg/rb/HZMB_ZH-CN5238831909_1920x1080.jpg"
    auto_wallpaper = AutoWallpaperSpider2(img_urls=url, img_name="moon.jpg", img_fill=True)
    auto_wallpaper.auto_main()
