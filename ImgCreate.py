# -*- coding: utf-8 -*-
"""
@since      :2024/3/15 20:09
@Author    :Ymri

"""
# 导入json解析
import json

from PIL import Image, ImageDraw, ImageFont


class ImgCreate(object):

    def __init__(self, mode: str = "Portrait", head_img_path: str = "640_1.jpeg",
                 description_text: str = "An introduction to oil painting", text: str = "Hello, World!",
                 date: json = None):
        """
        根据配置自动生成图片
        """
        self.mode = mode
        self.head_img_path = date['img']
        if not date:
            Exception("Please input date!")
        # the json abut date、weather、day、holiday
        self.date = date
        self.text = text
        self.description_text = description_text
        if self.mode == "Portrait":
            # ouptut img size
            # 竖屏
            self.EINK_WIDTH = 448
            self.EINK_HEIGHT = 600
        else:
            # 横屏
            self.EINK_WIDTH = 600
            self.EINK_HEIGHT = 448
        # domain_color about the line and the Day
        self.domain_color = (0, 0, 0)
        # The size of the icon in the upper right corner
        self.svg_size = 40
        # The size of the font
        self.text_font_size = 20
        # The size of the day
        self.day_font_size = 100
        self.output_path = "./out"
        # connect Img from the path
        self.input_path = "./inputImg"
        # Golden section line
        self.split_value = 0.618
        self.load()

    def load(self):
        # Load the image
        image = Image.open(self.input_path + "/" + self.head_img_path)
        image = image.resize((int(self.EINK_WIDTH), int(self.EINK_HEIGHT * 0.55)))
        self.image = image
        # 默认主题是黑色 中间横向
        self.midd = self.EINK_WIDTH * 0.5
        # 域初始化
        self.domain_color = self.get_dominant_color(image)
        # return image

    def dithering(self):
        """
        change img to 7-colored img
        :return:
        """
        # Create a pallette with the 7 colors supported by the panel
        pal_image = Image.new("P", (1, 1))
        # 调色板 算法处理7color 如果有色差在这里校准
        pal_image.putpalette(
            (0, 0, 0, 255, 255, 255, 0, 255, 0, 0, 0, 255, 255, 0, 0, 255, 255, 0, 255, 128, 0) + (
                0, 0, 0) * 249)
        # Convert the soruce image to the 7 colors, dithering if needed
        image_7color = self.image.convert("RGB").quantize(palette=pal_image)
        image_7color.save(self.output_path + "/7color.png")
        self.pImg = image_7color
        return image_7color

    @staticmethod
    def buffImg(image):
        image_temp = image
        buf_7color = bytearray(image_temp.tobytes('raw'))
        # PIL does not support 4 bit color, so pack the 4 bits of color
        # into a single byte to transfer to the panel
        buf = [0x00] * int(image_temp.width * image_temp.height / 2)
        idx = 0
        for i in range(0, len(buf_7color), 2):
            buf[idx] = (buf_7color[i] << 4) + buf_7color[i + 1]
            idx += 1
        return buf

    @staticmethod
    def change_mod(file_path="下雨 (1).png"):
        """
        Icon background set to white
        :param file_path:
        :return:
        """
        imagePtah = file_path
        img = Image.open(imagePtah)
        if img.mode != 'RGBA':
            image = img.convert('RGBA')
        width = img.width
        height = img.height
        image = Image.new('RGB', size=(width, height), color=(255, 255, 255))
        image.paste(img, (0, 0), mask=img)
        return image

    def get_dominant_color(self, pil_img):
        """
        获得主题色
        调整图片大小，然后获取中心点的颜色，起到类似主题颜色的作用
        调整的时候会自动插值
        :return:
        """
        img = pil_img.copy()
        img = img.convert("RGBA")
        img = img.resize((5, 5), resample=0)
        dominant_color = img.getpixel((2, 2))
        self.domain_color = dominant_color
        return dominant_color

    def draw_img_add(self, img, mode: str = 'text', text: str = "06", size=100, fillDomain: bool = False,
                     position=None):
        """
        在图片上绘制文字
        :param mode: 绘制模式
        :param str:
        :param img: 绘制的图片
        :param text: 文字
        :param size: 字体大小 默认100
        :param fillDomain: 是否使用主题色
        :param position: 绘制的位置
        :return:
        """
        # 开始的位置
        if not position:
            position = (0, self.EINK_WIDTH * self.split_value)
        if not img:
            Exception("Please init the img!")
            exit(-1)
        draw = ImageDraw.Draw(img)
        # 默认是微软雅黑，有需要去github下载其他字体
        font_path = "font.ttf"
        font_size = size
        font = ImageFont.truetype(font_path, size=font_size)
        if mode == "text":
            if fillDomain:
                draw.text(position, text, font=font, fill=self.domain_color)
            else:
                # 默认黑色
                draw.text(position, text, font=font, fill=(0, 0, 0))
        elif mode == 'line':
            # 画横线 画一半 宽度就应人而异
            # 模式切换暂时省略
            draw.line(
                (5, int(self.EINK_HEIGHT * self.split_value), self.EINK_WIDTH * 0.48, int(self.EINK_HEIGHT * 0.618)),
                fill=self.domain_color, width=2)

        return img

    def connection(self, WHITE_COLOR=(255, 255, 255), DisplayMode="Portrait"):
        """
         连接图片，默认背景为白色
        :param WHITE_COLOR:
        :param DisplayMode:
        :return:
        """
        img_concat = Image.new('RGB', (self.EINK_WIDTH, self.EINK_HEIGHT), WHITE_COLOR)
        img_1 = self.image
        #
        weather_1 = self.change_mod(file_path=self.input_path + "/" + self.date['weather'][0])
        weather_1 = weather_1.resize((self.svg_size, self.svg_size), resample=0)
        weather_2 = self.change_mod(file_path=self.input_path + "/" + self.date['weather'][1])
        weather_2 = weather_2.resize((self.svg_size, self.svg_size), resample=0)
        weather_3 = self.change_mod(file_path=self.input_path + "/" + self.date['weather'][2])
        weather_3 = weather_3.resize((self.svg_size, self.svg_size), resample=0)
        weather_4 = None
        if len(self.date['weather']) > 3:
            """
            节假日 特殊时间提醒
            """
            weather_4 = self.change_mod(file_path=self.input_path + "/" + self.date['weather'][3])
            weather_4 = weather_4.resize((self.svg_size, self.svg_size), resample=0)
        # 新月1.png
        if DisplayMode == "Portrait":
            # load head_img
            img_concat.paste(img_1, (0, 0))
            # draw the img description
            self.draw_img_add(img_concat, mode='text', text=self.description_text, size=15,
                              position=(5, int(self.EINK_HEIGHT * 0.618 - 30)))
            # draw line
            self.draw_img_add(img_concat, mode='line', fillDomain=True)
            # 加载天气 20 作为界限
            img_concat.paste(weather_1, (int(self.midd + 40), int(self.EINK_HEIGHT * 0.618 - 20)))
            img_concat.paste(weather_2, (int(self.midd + 90), int(self.EINK_HEIGHT * 0.618 - 20)))
            if weather_4:
                img_concat.paste(weather_4, (int(self.midd + 140), int(self.EINK_HEIGHT * 0.618 - 20)))
            img_concat.paste(weather_3, (int(self.EINK_WIDTH - 50), int(self.EINK_HEIGHT * 0.618 - 20)))
            # draw month
            self.draw_img_add(img_concat, mode='text', text=self.date["month"] + "|", size=20,
                              position=(self.midd + 50, int(self.EINK_HEIGHT * 0.618 + 100)))
            # draw day
            self.draw_img_add(img_concat, mode='text', text=self.date["day"], size=self.day_font_size,
                              position=(self.midd + 80, int(self.EINK_HEIGHT * 0.618 + 20)), fillDomain=True)
            # week and holiday
            self.draw_img_add(img_concat, mode='text', text=self.date["week"], size=20,
                              position=(self.midd + 50, int(self.EINK_HEIGHT * 0.618 + 150)))

            self.draw_img_add(img_concat, mode='text',
                              text="日历©Ymri  " + str(self.date['dayCount']) + "/" + str(self.date['yearCount']),
                              size=20,
                              position=(int((self.EINK_WIDTH - 20 * 10) / 2), int(self.EINK_HEIGHT - 35)))
            # 节气
            # self.draw_img_add(img_concat, mode='text', text="春风", size=20,
            #                   position=(self.midd + 30, int(self.EINK_HEIGHT * 0.618 - 20)))
            # # 星期

            # 节气和节假日一起出现
            # self.draw_img_add(img_concat, mode='text', text="星期日 谷雨 母亲节", size=20,
            #                   position=(self.midd + 40, int(self.EINK_HEIGHT * 0.618 + 150)))

            # 阴历

            self.draw_img_add(img_concat, mode='text', text=self.text, size=20,
                              position=(10, int(self.EINK_HEIGHT * 0.618 + 100)))

        elif DisplayMode == "Landscape":
            img_concat.paste(img_date, (0, 0))
            img_concat.paste(img_todo, (0, img_date.height))
            img_concat.paste(img_info, (0, img_date.height + img_todo.height))
            img_concat.paste(img_photo, (img_date.width, 0))
        self.image = img_concat
        self.image.save(self.output_path + "/test_0.png")
        buffs = self.buffImg(self.dithering())
        if len(buffs) == self.EINK_HEIGHT * self.EINK_WIDTH / 2:
            print("Success")


if __name__ == "__main__":
    date = {
        "img": "test.jpeg",
        "weather": ["下雨.png", "太阳.png", "新月1.png", "烟花.png"],
        "month": "03",
        "day": "15",
        "week": "星期日 初六",
        "dayCount": 100,
        "yearCount": 366
    }
    imgCreate = ImgCreate(date=date)
    # 拼接生成图像
    imgCreate.connection()

