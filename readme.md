# 彩色电子日历
复刻少数派电子日历：https://sspai.com/post/82704

材料：
* 微雪彩色墨水屏5.6寸(F)600*448分辨率
* 微雪官方esp32+墨水屏驱动
* 3D打印外壳

进度:
* [x] 基础界面设计、图片生成
* [ ] 爬虫批量生成图片
* [ ] esp32定时获取图片
* [ ] 服务端管理系统
* [ ] 3D打印外壳
### 基础界面设计

爬取数据自动生成Img,然后esp32通过http请求获取图片，~~目前不确定处理算法是在python还是esp32~~

首先把左下角话和图片全部合成，天气和日历再拼接，原版的艺术画有裸体，改成手动检查和过滤（工作量++）
代码见ImgCreate.py

效果图如下

![效果图](./out/test_0.png)


### 爬虫
* 从[一言](https://developer.hitokoto.cn/sentence/demo.html)获得句子（为了最佳显示效果，限制句子长度） 
* 封面图，从原本[艺术油画](http://en.most-famous-paintings.com/MostFamousPaintings.nsf/ListOfTop1000MostPopularPainting?OpenForm) 切换爬取到公众号：**为你读诗**每日的推送封面



### 后台服务管理

用go写咯，目前还没开始


