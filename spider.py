# python3
# -*- coding: utf-8 -*-
__author__ = 'allsunny'
import os,codecs,urllib
from urllib import request
from bs4 import BeautifulSoup
from urllib import error

class SpiderHTML(object):
    def __init__(self, cookie, user_agent):
        self.cookie = cookie
        self.user_agent = user_agent

    # 打开页面
    def get_url(self, url, coding='utf-8'):

        req = request.Request(url)
        req.add_header('User-Agent', self.user_agent)
        req.add_header('Cookie', self.cookie)
        with request.urlopen(req) as response:
            return BeautifulSoup(response.read().decode(coding), "lxml")


    # 保存文本内容到本地
    def save_text(self, filename, content, mode='a+'):
        self._check_path(filename)
    #    result = []
        with codecs.open(filename, encoding='utf-8', mode=mode) as f:
            f.seek(0)
            result = f.read()
            if content in result:          # 根据图片名查询图片是否已经下载
                print(content + ' is exist.')
            else:
                f.write(content + '\n')
                return True

    # 保存图片
    def save_img(self, image_url, image_name):
        data = request.urlopen(image_url).read()
        self._check_path(image_name)
        with open(image_name, 'wb') as f:
            f.write(data)

    # 创建目录
    def _check_path(self, path):
        dirname = os.path.dirname(path.strip())
        if not os.path.exists(dirname):
            os.makedirs(dirname)
