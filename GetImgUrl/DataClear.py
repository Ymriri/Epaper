# -*- coding: utf-8 -*-
"""
@since      :2024/3/18 23:32
@Author    :Ymri

"""

import pandas as pd
import requests


class DataClear(object):
    def __init__(self, file_path: str):
        self.file_path = file_path
        # 读取 csv 文件
        self.data = pd.read_csv(self.file_path)
        # 二十四节气
        self.weather_24 = [
            "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
            "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
        ]

    @staticmethod
    def img_url_clear_down(cover: str, new_file_name: str):
        """
        下载文件并保存
        :param cover: 封面Url
        :param new_file_name: 图片的新文件名
        :return:
        """
        if cover is None:
            return None

        img_url = cover.replace("mmbiz.qpic.cn", "mmbiz.qlogo.cn").replace("/0?wx_fmt=jpeg",
                                                                           "/640?wx_fmt=jpeg&wxfrom=5&wx_lazy=1&wx_co=1")
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
        }
        new_file_name = new_file_name
        response = requests.get(img_url, headers=header)
        if response.status_code == 200:
            with open(new_file_name, 'wb+') as f:
                f.write(response.content)
        else:
            print("图片下载失败：" + new_file_name)

    def title_img_connect(self):
        """
        下载所有的图片
        :return:
        """
        for index, row in self.data.iterrows():
            title = row["title"]
            # 默认是标题
            img_file_name = "../Img/" + row["title"] + ".jpeg"
            # 如果包括24节气
            sub_title = title.split("：")
            weacher24 = self.check_weather24(sub_title[0])
            if weacher24:
                # 24节气
                img_file_name = "../Img/weather24/" + title + ".jpeg"
            # 包括月份开头
            elif "月：" in title:
                # 独立月份开始
                img_file_name = "../Img/month/" + title + ".jpeg"
                self.img_url_clear_down(row["cover"], img_file_name)
            # 特殊节假日就不管了
            else:
                # 其他归为通用
                pass
            # 统一处理


    def check_weather24(self, title: str):
        for i in self.weather_24:
            if i in title:
                return i
        return None


if __name__ == "__main__":
    dataClear = DataClear(file_path="为你读诗_0.csv")
    dataClear.title_img_connect()
