# -*- coding: utf-8 -*-
import csv
import datetime
import random
import time

import pandas as pd
import requests

print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))


def GetTargetUrls(Cookie, token, fakeid, account_name, sleep_time=3, start_page=0, post_count=0):
    # 目标url
    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

    # 使用Cookie，跳过登陆操作
    headers = {
        "Cookie": Cookie,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5763.195 Safari/537.36",
    }

    # 构造请求头
    data = {
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": "0",
        "count": "5",
        "query": "",
        "fakeid": fakeid,  # 填写目标公众号的fakeid(公众号唯一标识)
        "type": "9",
    }

    content_list = []
    mistake = 0

    data["begin"] = 1 * 5
    content_json = requests.get(url, headers=headers, params=data).json()
    time.sleep(2 + random.random() * 2)
    # 获得总条目数量，每爬取一个条目，进行计数，条目够大后break
    content_json_pages = content_json['app_msg_cnt']  # 一共有多少次推送

    print('正在处理公众号：{}\n推送数量：{}'.format(account_name, content_json_pages))
    post_count = post_count
    item_count = 0
    # post_count += start_page

    f0 = open('temp_{}.csv'.format(account_name), 'w+', encoding='utf-8', newline='')
    temp_writer = csv.writer(f0)
    # 每天只有第一条没有广告，其他几条可能存在广告，这里只选第一条
    temp_map = {}
    # ret_ = []
    i = int(404) # 下次开始的地方
    # 404
    while i < 500:
        try:
            i += start_page
            # if i == 696:
            #     break
            data["begin"] = i * 5
            time.sleep(sleep_time + random.random() * 10)  # 我不信睡十秒钟还被限制访问 2022.22.15睡200+秒
            # 使用get方法进行提交
            content_json = requests.get(url, headers=headers, params=data).json()
            if len(str(content_json)) > 150:
                print(str(content_json)[:150])
            else:
                print(content_json)
            # 返回了一个json，里面是每一页的数据
            # print(content_json)
            for item in content_json["app_msg_list"]:
                # 提取每页文章的标题及对应的url 填入DF
                items = []
                items.append(item["title"])
                temp_date = change_time(item['update_time'])
                if temp_date in temp_map:
                    continue
                temp_map[temp_date] = 1
                # 描述
                items.append(item['digest'])
                # 封面图
                items.append(item['cover'])
                items.append(item["link"])
                items.append(temp_date)
                content_list.append(items)
                url0 = item["link"]
                url_lis = url0.split('&')
                post_index0 = int(url_lis[2][4:])
                item_count += 1
                if post_index0 == 1:
                    post_count += 1
                print(items)
                temp_writer.writerow([item["title"], item['digest'],item['cover'],item["link"], temp_date])
            print('已经爬取{}页，{}条，{}次推送，剩余推送{}次'.format(i + 1, item_count, post_count,
                                                                   content_json_pages - post_count))

            if post_count >= content_json_pages:
                print('正常完成公众号，跳出循环')
                break

            if content_json_pages - post_count <= 1:
                print('正常完成公众号，跳出循环')
                break
            # if len(content_json["app_msg_list"]) == 0:
            #   print('url返回msg_list为空，可能已经完成')
            # break
            i = i + 1

        except Exception as e:
            """
            可能有风控
            """
            print(e)
            print("程序出错，数据正在保存")
            print("出错信息如下：")
            content_json = requests.get(url, headers=headers, params=data).json()
            print(content_json)
            name = ['title', 'digest', 'cover', 'link', 'date']
            test = pd.DataFrame(columns=name, data=content_list)
            test.to_csv("{}.csv".format(account_name), mode='w', encoding='utf-8')
            print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
            print("保存成功")
            print("本次进行到：{}".format(i))
            mistake = 1
            break

    if mistake == 0:
        print("程序运行未出错")
        name = ['title', 'digest', 'cover', 'link', 'date']
        test = pd.DataFrame(columns=name, data=content_list)
        test.to_csv("{}.csv".format(account_name), mode='w+', encoding='utf-8')
        print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
        print("保存成功")


def change_time(date):
    dt = datetime.datetime.fromtimestamp(date)
    return dt.strftime('%Y-%m-%d')


if __name__ == '__main__':
    """
    这两个参数需要自己从公众号里面寻找，一个在请求的cookie里面，一个在请求的playload里面
    Cookie和Token每次登录都不同
    fakeId 倒是相同
    """
    Cookie = 'appmsglist_action_3942669769=card; RK=Zq9pn73saS; ptcz=bd7d699ca054d4d1a3ca4a476ab766a675c6b2d8a4607e0fca49c9cc4be7ba46; pgv_pvid=4738048034; pac_uid=1_1448265203; iip=0; ua_id=hnupH2nZ9VFbQB9DAAAAAPmI8DdGsy2g4fGVOM-7IH4=; wxuin=94673875678644; mm_lang=zh_CN; eas_sid=V1c6F9r5U476L4m7B4p3c4k9i3; qq_domain_video_guid_verify=66bf25f4066ba83b; o_cookie=1448265203; _qimei_q36=; amp_6e403e=5ym2yuS7Z0uVcW9k6oQNgm...1hf4l4l3n.1hf4l4l3n.0.0.0; _qimei_fingerprint=93328461860c044dc8aea742604afbf9; _qimei_h38=2aadf3e28fa05bfa3ad543430200000f217a0f; _clck=3942669769|1|fkd|0; uuid=f5b9d234fdac41de3802f23069c9f356; rand_info=CAESIDqV6+ukKWbVKuLltxmdufaySpKy1FSVIDrg5xpSEMZ0; slave_bizuin=3942669769; data_bizuin=3942669769; bizuin=3942669769; data_ticket=0jWfb3SpV6gTm4Yr4gEC1lr5MFubt1tFSx300MES6AajTiyfzgPIi61rzQvDeyhG; slave_sid=OG4yUmdwUDZ3b1h0Z2dtSTlaZXhrVG9jNnJGWEN5SU5uSnhXWjJUaUpmejRRVW9Gdk9IY3NNR3hKV0lISkl5TW1ZbVoydWRlRzJvdG5WRHNvZW1Qa2ZOcGE0OEc5Mm5XYU5GajhOZGVCSW1ZNldrU0hnWE40ZzZ3ZmN3QnBwelJ2OHJybkJPdlNiWm1hSWZQ; slave_user=gh_ddcb3ad05899; xid=c9669552039ff62a6cb330876884bbb5; _clsk=fmgiuq|1711355253465|2|1|mp.weixin.qq.com/weheat-agent/payload/record'
    token = '1100927603'  #
    fakeid = 'MjM5NjU5NDkzMg=='
    account_name = '为你读诗'
    # 存在爬虫限制，
    sleep_time = 10
    start_page = 0
    GetTargetUrls(Cookie, token, fakeid, account_name, sleep_time=sleep_time, start_page=0)
