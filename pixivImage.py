__author__ = 'allsunny'
# !python3
# -*- coding: utf-8 -*-
from spider import SpiderHTML
import urllib, os, re
from urllib import request

'''
使用了第三方类库 BeautifulSoup4
需要目录下的spider.py文件
运行环境：python3.4,windows10
功能：下载P站固定标签下的收藏超过一定数量的图片
    标签(keyword)和收藏数目(bookmarkCount)可自行修改
'''

# 使用前要修改cookie
rootURL = 'http://www.pixiv.net'
startURL = 'http://www.pixiv.net/search.php?order=date_d'

store_path = 'E:\\P站'
cookie = 'p_ab_id=7; login_ever=yes; _ga=GA1.2.1980361329.1457164315; __utmt=1; visit_ever=yes; PHPSESSID=8309039_2a2e277d91b025f3a1f360387213750d; device_token=b409b8016b75b0fc4fc96edbe938c9dc; module_orders_mypage=%5B%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; __utma=235335808.1980361329.1457164315.1457314990.1457318723.5; __utmb=235335808.28.10.1457318723; __utmc=235335808; __utmz=235335808.1457314990.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=8309039=1'
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'

class pixivImage(SpiderHTML):
    def __init__(self, cookie, userAgent, keyword, dirName, bookmarkCount, startPage=1):
        SpiderHTML.__init__(self, cookie, userAgent)
        self.rootURL = rootURL
        self.startURL = startURL
        self.page = startPage
        self.keyword = urllib.parse.quote(keyword)  # 将搜索关键词汉字转换为%xx
        self.dirName = dirName
        self.bookmarkCount = bookmarkCount
        self.startURL += (u'&word=' + self.keyword + u'&p=')

    def start(self):
        while(True):
            pageURL = self.getPage()
            imageItemList = self.getImageList(pageURL)
            self.getImage(imageItemList)

    def getPage(self):
        pageURL = self.startURL + str(self.page)
        print('Opening ', pageURL)
        self.page += 1
        return pageURL

    def getImageList(self, pageURL):
        content = self.getUrl(pageURL)
        imageItemList = content.find_all(class_='image-item')
        return imageItemList

    def getImage(self, imageItemList):
        for imageItem in imageItemList:
            image = imageItem.find(class_='bookmark-count _ui-tooltip')
            if image is None:
                continue

            bookmarkCount = int(image.get_text())    #收藏数目
            if(bookmarkCount < self.bookmarkCount):
                continue
            else:
                imageId = imageItem.a['href']
                self.ID = imageId.split('illust_id=')[1]  # 取出图片ID作为图片名字
                imgPageURL = self.rootURL + imageId  # 包含原始图片的页面
                self.saveImage(imgPageURL)

    def saveImage(self, imgPageURL):
        content = self.getUrl(imgPageURL)
        originalImageItem = content.find(class_='original-image')
        if originalImageItem is None:
            return
        else:
            print('Downloading', imgPageURL)
            originalImageUrl = originalImageItem['data-src']
            filename = originalImageItem['alt']
            extension = os.path.splitext(originalImageUrl)[1]  # 扩展名

            req = request.Request(originalImageUrl)
            referer = originalImageUrl
            req.add_header('Referer', referer)  # 没有这个header会出现403 error
            self.removeIllegalChars(filename)
            path_name = os.path.join(store_path, self.dirName, filename + '_id' + self.ID + extension)
            try:
                self.saveImg(req, path_name)  # 捕获图片异常，流程不中断
            except OSError:
                pass


    def removeIllegalChars(self, filename):  # 处理文件名中不合法字符  \ / ? : * " > < |
            pattern = r'[\\/\?:\*"><\|]*'
            return re.sub(pattern, "#", filename)




if __name__ == '__main__':
    keyword = u'百合'
    dirName = keyword
    bookmarkCount = 1000   # 赞同数量
    startPage = 1
    spider = pixivImage(cookie, userAgent, keyword, dirName, bookmarkCount, startPage)
    spider.start()



