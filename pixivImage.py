# -*- coding: utf-8 -*-
__author__ = 'allsunny'
# !python3

from spider import SpiderHTML
import urllib
import os
import re
import http
import threading
import queue
from urllib import request
from urllib import parse
from urllib import error

'''
使用了第三方类库 BeautifulSoup4
需要目录下的spider.py文件
运行环境：python3.4,windows10
功能：下载P站固定标签下的收藏超过一定数量的图片
    标签(keyword)和收藏数目(bookmark_count)可自行修改
'''

# 使用前要修改cookie
ROOT_URL = 'http://www.pixiv.net'
START_URL = 'http://www.pixiv.net/search.php?order=date_d&s_mode=s_tag_full'

STORE_PATH = 'E:\\P站'
COOKIE = '# 使用前要修改cookie'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'


class PixivImage(SpiderHTML, threading.Thread):
    def __init__(self, keyword, dir_name, bookmark_count, start_page=1, end_page=1000):
        SpiderHTML.__init__(self, COOKIE, USER_AGENT)
        threading.Thread.__init__(self)
        self.root_url = ROOT_URL
        self.start_url = START_URL
        self.start_page = start_page
        self.end_page = end_page
        self.keyword = urllib.parse.quote(keyword)  # 将搜索关键词汉字转换为%xx
        self.dir_name = dir_name
        self.bookmark_count = bookmark_count
        self.start_url += (u'&word=' + self.keyword + u'&p=')

    def run(self):
        for page in range(self.start_page, self.end_page + 1):
            page_url = self.get_page_url(page)
            image_item_list = self.get_image_list(page_url)
            self.get_image(image_item_list)

    def get_page_url(self, page):
        page_url = self.start_url + str(page)
        print('Opening ', page_url)
        return page_url

    def get_image_list(self, page_url):
        content = self.get_url(page_url)
        image_item_list = content.find_all(class_='image-item')
        return image_item_list

    def get_image(self, image_item_list):
        for image_item in image_item_list:
            image = image_item.find(class_='bookmark-count _ui-tooltip')
            if image is None:
                continue

            img_bookmark_count = int(image.get_text())  # 收藏数目
            if img_bookmark_count < self.bookmark_count:
                continue
            else:
                imageID = image_item.a['href']
                self.ID = imageID.split('illust_id=')[1]  # 取出图片ID作为图片名字
                img_page_url = self.root_url + imageID  # 包含原始图片的页面
                self.save_image(img_page_url)

    def save_image(self, img_page_url):
        content = self.get_url(img_page_url)
        original_image_item = content.find(class_='original-image')
        if original_image_item is None:
            return
        else:
            print('Downloading', img_page_url)
            original_image_url = original_image_item['data-src']
            filename = original_image_item['alt']
            extension = os.path.splitext(original_image_url)[1]  # 扩展名

            req = request.Request(original_image_url)
            referer = original_image_url
            req.add_header('Referer', referer)  # 没有这个header会出现403 error
            self.remove_illegal_chars(filename)
            filename = filename + '_id' + self.ID
            path_name = os.path.join(STORE_PATH, self.dir_name, filename + extension)
            txt_name = os.path.join(STORE_PATH, 'ImageName.txt')
            if self.save_text(txt_name, filename):
                try:
                    self.save_img(req, path_name)  # 捕获图片异常，流程不中断
                except OSError:
                    pass
                except urllib.error.HTTPError as e:
                    pass
                # except urllib.error.URLError:
                #     pass
                except http.client.IncompleteRead:
                    pass


    @staticmethod
    def remove_illegal_chars(filename):  # 处理文件名中不合法字符  \ / ? : * " > < |
        pattern = r'[\\/\?:\*"><\|]*'
        return re.sub(pattern, "#", filename)


class Main(SpiderHTML):
    def __init__(self):
        SpiderHTML.__init__(self,COOKIE, USER_AGENT)
        keyword = u'JK'
        dir_name = keyword
        bookmark_count = 1000  # 收藏数目
        keyword = urllib.parse.quote(keyword)
        url = START_URL + str(u'&word=' + keyword)
        print(url)
        content = self.get_url(url)

        count_badge_text = content.find(class_='count-badge')
        count_badge = int(count_badge_text.getText().split('件')[0])
        print(count_badge)

        if count_badge < 4000:
            page = 10
        elif count_badge < 6000:
            page = 15
        elif count_badge < 8000:
            page = 20
        elif count_badge < 10000:
            page = 25
        elif count_badge < 12000:
            page = 30
        elif count_badge < 14000:
            page = 35
        elif count_badge < 16000:
            page = 40
        elif count_badge < 18000:
            page = 45
        else:
            page = 50

        page = 1

        # 开启20个线程
        for i in range(1, 21):
            _get_img_url = PixivImage(keyword, dir_name, bookmark_count, (i-1)*page+1, i*page)
            _get_img_url.start()

    #    _get_img_url.join()

if __name__ == '__main__':
    Main()
    print('all over')