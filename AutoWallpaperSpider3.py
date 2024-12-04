#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2024/12/4
# @Author  : 圈圈烃
# @File    : AutoWallpaperSpider3
# @Description:
#
#
import os
import time
import datetime
import requests
from typing import List, Union
from PIL import Image
import win32api
import win32con
import win32gui


class AutoWallpaperSpider:
    """
    A class to download, merge, and set desktop wallpapers with enhanced error handling and flexibility.
    """

    def __init__(self,
                 img_urls: Union[str, List[str]],
                 img_name: str = "wallpaper.jpg",
                 img_fill: bool = False,
                 grid_rows: int = 4,
                 grid_cols: int = 4,
                 tile_size: int = 550):
        """
        Initialize the AutoWallpaperSpider.

        :param img_urls: Single image URL or list of image URLs
        :param img_name: Name of the final wallpaper file
        :param img_fill: Whether to fill the entire desktop background
        :param grid_rows: Number of rows in the grid merge
        :param grid_cols: Number of columns in the grid merge
        :param tile_size: Size of each tile in the merged image
        """
        # Ensure img_urls is a list
        self.img_urls = [img_urls] if isinstance(img_urls, str) else img_urls

        self.img_name = img_name
        self.img_fill = img_fill
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.tile_size = tile_size

        self.wallpaper_paths = []
        self.wallpaper_dir = self._create_wallpaper_directory()
        self.wallpaper_path = ""

    def _create_wallpaper_directory(self) -> str:
        """
        Create and return the wallpaper directory on the most suitable drive.

        :return: Path to the wallpaper directory
        """
        # Find available drives
        drives = [f"{chr(i)}:" for i in range(65, 91) if os.path.isdir(f"{chr(i)}:")]

        # Prefer the third drive if available, otherwise use the first
        target_drive = drives[2] if len(drives) > 2 else drives[0]

        wallpaper_dir = f"{target_drive}\\Program Files\\AutoWallpaper\\"

        try:
            os.makedirs(wallpaper_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory: {e}")
            raise

        return wallpaper_dir

    def _log(self, message: str):
        """
        Log messages to a log file and print to console.

        :param message: Message to log
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"

        print(log_message)

        try:
            with open(os.path.join(self.wallpaper_dir, "log.log"), 'a') as log_file:
                log_file.write(log_message + "\n")
        except IOError as e:
            print(f"Failed to write to log file: {e}")

    def download_images(self):
        """
        Download images with retry mechanism and logging.
        """
        for index, img_url in enumerate(self.img_urls):
            max_attempts = 3
            for attempt in range(1, max_attempts + 1):
                try:
                    temp_path = os.path.join(
                        self.wallpaper_dir,
                        self.img_name.replace('.', f'_{index}.')
                    )

                    response = requests.get(img_url, timeout=20, verify=False)
                    response.raise_for_status()  # Raise an error for bad status codes

                    with open(temp_path, 'wb') as file:
                        file.write(response.content)

                    self.wallpaper_paths.append(temp_path)
                    self._log(f"{temp_path} image downloaded successfully")
                    break

                except requests.RequestException as e:
                    if attempt == max_attempts:
                        self._log(f"Failed to download {img_url} after {max_attempts} attempts: {e}")
                        raise

                    self._log(f"Download attempt {attempt}/{max_attempts} failed: {e}")
                    time.sleep(2)  # Wait before retrying

    def merge_images(self):
        """
        Merge multiple images into a grid.
        """
        img_width = self.tile_size * self.grid_cols
        img_height = self.tile_size * self.grid_rows

        self.wallpaper_path = os.path.join(self.wallpaper_dir, self.img_name)

        merged_img = Image.new('RGB', (img_width, img_height))

        for index, img_path in enumerate(self.wallpaper_paths):
            with Image.open(img_path) as from_image:
                x = (index % self.grid_cols) * self.tile_size
                y = (index // self.grid_cols) * self.tile_size
                merged_img.paste(from_image, (x, y))

        merged_img.save(self.wallpaper_path)
        self._log(f"{self.wallpaper_path} images merged successfully")

    def fill_image(self):
        """
        Fill the image to match desktop resolution if required.
        """
        if not self.img_fill:
            return

        with Image.open(self.wallpaper_path) as img_content:
            img_width, img_height = img_content.size
            monitor_width = win32api.GetSystemMetrics(0)
            monitor_height = win32api.GetSystemMetrics(1)

            fill_img = Image.new(img_content.mode, (monitor_width, monitor_height), color='black')
            paste_x = (monitor_width - img_width) // 2
            paste_y = (monitor_height - img_height) // 2

            fill_img.paste(img_content, (paste_x, paste_y))
            fill_img.save(self.wallpaper_path)

        self._log(f"{self.wallpaper_path} image filled successfully")

    def set_desktop_wallpaper(self):
        """
        Set the merged/filled image as desktop wallpaper.
        """
        try:
            # Open registry key
            key = win32api.RegOpenKeyEx(
                win32con.HKEY_CURRENT_USER,
                r"Control Panel\Desktop",
                0,
                win32con.KEY_SET_VALUE
            )

            # Set wallpaper style
            # 6: Fit, 2: Stretch, 0: Center, 10: Fill, 0: Tile
            win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "6")
            win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")

            # Change wallpaper
            win32gui.SystemParametersInfo(
                win32con.SPI_SETDESKWALLPAPER,
                self.wallpaper_path,
                1 + 2  # Update and broadcast
            )
            self._log(f"{self.wallpaper_path}  setting desktop successfully")
        except Exception as e:
            self._log(f"Error setting desktop wallpaper: {e}")

    def run(self):
        """
        Execute the entire wallpaper setting process.
        """
        try:
            self.download_images()
            self.merge_images()
            self.fill_image()
            self.set_desktop_wallpaper()
        except Exception as e:
            self._log(f"Wallpaper process failed: {e}")
            raise


if __name__ == '__main__':
    # Example usage
    bing_url = "https://cn.bing.com/az/hprichbg/rb/HZMB_ZH-CN5238831909_1920x1080.jpg"

    auto_wallpaper = AutoWallpaperSpider(
        img_urls=bing_url,
        img_name="moon.jpg",
        img_fill=False,
        grid_rows=4,
        grid_cols=4,
        tile_size=550
    )

    auto_wallpaper.run()
