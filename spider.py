# python3
# -*- coding: utf-8 -*-
__author__ = 'allsunny'
import os, codecs
from urllib import request
from bs4 import BeautifulSoup

class SpiderHTML(object):
    def __init__(self, cookie, userAgent):
        self.cookie = cookie
        self.userAgent = userAgent

    # 打开页面
    def getUrl(self, url, coding='utf-8'):
        req = request.Request(url)
        req.add_header('User-Agent', self.userAgent)
        req.add_header('Cookie', self.cookie)
        with request.urlopen(req) as response:
            return BeautifulSoup(response.read().decode(coding), "html.parser")

    # 保存文本内容到本地
    def saveText(self, filename, content, mode='w'):
        self._checkPath(filename)
        with codecs.open(filename, encoding='utf-8', mode=mode) as f:
            f.write(content)


    # 保存图片
    def saveImg(self, imgUrl, imgName):
        data = request.urlopen(imgUrl).read()
        self._checkPath(imgName)
        with open(imgName, 'wb') as f:
            f.write(data)

    # 创建目录
    def _checkPath(self, path):
        dirname = os.path.dirname(path.strip())
        if not os.path.exists(dirname):
            os.makedirs(dirname)