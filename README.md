# pixivImage
Crawl images from http://www.pixiv.net/

使用了第三方类库 BeautifulSoup4
需要目录下的spider.py文件
运行环境：python3.4,windows10
功能：下载P站固定标签下的收藏超过一定数量的图片，标签(keyword)和收藏数目(bookmark_count)可自行修改

Second commit:
增加功能，在父文件夹下建立txt文件，保存图片名字，下载图片前查询是否已经下载。
增加多线程。
规范命名
