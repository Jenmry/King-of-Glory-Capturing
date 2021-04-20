#!usr/bin/python
# -*- coding = utf-8 -*-
import re
import os
import time
import requests


class King(object):

    def __init__(self):
        self.names = []
        self.ids = []
        self.skin_name = []
        self.skin_number = []
        self.url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'
        self.js = 'https://pvp.qq.com/web201605/js/herolist.json'
        self.detail_url = 'https://pvp.qq.com/web201605/herodetail/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
        }

    def get_info(self):
        response = requests.session().get(url=self.js, headers=self.headers)
        lists = response.json()
        for i, index in enumerate(lists, 0):
            self.names.append(index['cname'])
            self.ids.append(index['ename'])
            response2 = requests.session().get(url=self.detail_url + '{}.shtml'.format(self.ids[i]), headers=self.headers)
            index_re = re.findall(r'<ul class="pic-pf-list pic-pf-list3" data-imgname="(.*?)">', response2.content.decode('gbk'))
            self.skin_number.append(len(index_re[0].split('|')))
            mode = []
            for k in range(self.skin_number[i]):
                test = index_re[0].split('|')[k].split('&')[0]
                mode.append(test)
            self.skin_name.append(mode)
        self.get_pic()
        return len(self.names)

    def get_pic(self):
        path = os.path.exists('D:/Pycharm/King_of_Pic/King')
        if not path:
            os.makedirs('D:/Pycharm/King_of_Pic/King')
        for i in range(len(self.names)):
            for j in range(self.skin_number[i]):
                new_url = self.url + '{}/{}-bigskin-{}.jpg'.format(self.ids[i], self.ids[i], j + 1)
                resp = requests.session().get(new_url, headers=self.headers)
                path = os.path.exists('D:/Pycharm/King_of_Pic/King/' + self.names[i])
                if not path:
                    os.makedirs('D:/Pycharm/King_of_Pic/King/' + self.names[i])
                with open(
                        'D:/Pycharm/King_of_Pic/King/' + self.names[i] + '/' + self.skin_name[i][j] + '.jpg', 'wb') as f:
                    print(self.skin_name[i][j] + 'downloading......')
                    f.write(resp.content)
                    f.close()


if __name__ == '__main__':
    beginTime = time.strftime('%H:%M:%S', time.localtime(time.time())).split(':')
    print('开始时间：' + time.strftime('%H:%M:%S', time.localtime(time.time())))
    beginTime1 = int(beginTime[0]) * 3600 + int(beginTime[1]) * 60 + int(beginTime[2])
    glory = King()
    number = glory.get_info()
    beginTimes = time.strftime('%H:%M:%S', time.localtime(time.time())).split(':')
    print('结束时间：' + time.strftime('%H:%M:%S', time.localtime(time.time())))
    beginTimes1 = int(beginTimes[0]) * 3600 + int(beginTimes[1]) * 60 + int(beginTimes[2])
    print('共保存{}'.format(number))
    print('所有图片下载保存用时：' + str(beginTimes1 - beginTime1) + '秒')
