#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Channing Wong
#
# @mail: channing.wong@yahoo.com
# @home: http://blog.3363.me/
# @date: Mar 3, 2012
#

import json
import sys
import time
import types
import urllib
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')


class BaiduMap:
    """
    """
    def __init__(self, keyword):
        self.keyword = keyword
        self.query = [
                ('b', '(-1599062.039999999,811604.75;24779177.96,8168020.75)'),
                ('c', '1'),
                ('from', 'webmap'),
                ('ie', 'utf-8'),
                ('l', '4'),
                ('newmap', '1'),
                ('qt', 's'),
                ('src', '0'),
                ('sug', '0'),
                ('t', time.time().__int__()),
                ('tn', 'B_NORMAL_MAP'),
                ('wd', keyword),
                ('wd2', '')
                 ]
        self.mapurl = 'http://map.baidu.com/'
        # self.file = open('%s.txt' % keyword, 'w')
        self.count = 0
        self.count_c = 0
        self.total_num = 0

        self._get_city()

    def _fetch(self, query=None, json=True):
        data = urllib.urlencode(query)
        url = self.mapurl + '?' + data
        opener = urllib.FancyURLopener()
        data = opener.open(url).read()

        if json:
            return self._tojson(data)
        else:
            return data

    def _tojson(self, data):
        try:
            js = json.loads(data, 'utf-8')
        except:
            js = None

        return js

    def _get_city(self):
        data = self._fetch(self.query)

        if type(data['content']) is not types.ListType:
            print('keyworld error.')
            sys.exit()

        self.city = data['content']

        if data.has_key('more_city'):
            for c in data['more_city']:
                self.city.extend(c['city'])

        for city in self.city:
            self.total_num += city['num']

    def _get_data(self, city, page=0):
        query = [
                ('addr', '0'),
                ('b', '(%s)' % city['geo'].split('|')[1]),
                ('c', city['code']),
                ('db', '0'),
                ('gr', '3'),
                ('ie', 'utf-8'),
                ('l', '9'),
                ('newmap', '1'),
                ('on_gel', '1'),
                ('pn', page),
                ('qt', 'con'),
                ('src', '7'),
                ('sug', '0'),
                ('t', time.time().__int__()),
                ('tn', 'B_NORMAL_MAP'),
                ('wd', self.keyword),
                ('wd2', ''),
                 ]
        data = self._fetch(query)
        return data

    def _save(self, content, city):
        for c in content:
            self.count += 1
            self.count_c += 1
            if c.has_key('tel'):
                tel = c['tel']
            else:
                tel = ''

            if c.has_key('addr'):
                addr = c['addr']
            else:
                addr = ''

            if c.has_key('indoor_pano'):
                indoor_pano = c['indoor_pano']
            else:
                indoor_pano = ''

            #_data = '%s\t%s\t%s\t%s\n' % (city['name'], c['name'], addr, tel)
            #self.file.write(_data)

            #print
	    	#print indoor_pano

            if city['name'].__len__() >= 3:
                try:
                    data_in = {
                        'sname' : c['name'],
                        'address' : addr,
                        'city' : city['name'],
                        'form' : fenlei,
                        'avatar_large' : indoor_pano,
                        'beizhu' : tel
                    }
                    d = urllib.urlencode(data_in)
                    #print d
                    req = urllib2.Request("http://ireoo.com/app/get/store.php", d)
                    response = urllib2.urlopen(req)
                    the_page = response.read()
                    #print the_page
                except Exception as e:
                    print(e)

                #the_page = ''
                print('[%s(%s) %s/%s]--(%s/%s) %s[%s/%s] %s' % (keyword, fenlei, x, list.__len__(), self.count, self.total_num, city['name'], self.count_c, city['num'], the_page))
            else:
                print('[%s(%s) %s/%s]--(%s/%s) %s[%s/%s] %s' % (keyword, fenlei, x, list.__len__(), self.count, self.total_num, city['name'], self.count_c, city['num'], "city lenght is error..."))

    def get(self, city):
        self.count_c = 0
        pages = abs(-city['num'] / 10)
        for page in range(0, pages):
            data = self._get_data(city, page)
            try:
                if data.has_key('content'):
                    self._save(data['content'], city)
            except Exception as e:
                print(e)

    def get_all(self):
        for city in self.city:
            self.get(city)

        self.file.close()



if __name__ == '__main__':
    if sys.argv.__len__() > 1:
        keyword = sys.argv[1]
        fenlei = sys.argv[2]
    else:
        keyword = '贸易'
        fenlei = 54

    #baidumap = BaiduMap(keyword)
    #print('_' * 20)
    #print('CITY: %s' % baidumap.city.__len__())
    #print('DATA: %s' % baidumap.total_num)
    #baidumap.get_all()

    list = [
        
        {'name':'食品', 'id':40},
        {'name':'医药器械服务', 'id':46},
        {'name':'医疗器械服务', 'id':46},
        {'name':'生物制品', 'id':45},
        {'name':'中药', 'id':44},
        {'name':'化学制药', 'id':44},
        {'name':'西药', 'id':44},
        {'name':'造纸', 'id':43},
        {'name':'包装', 'id':43},
        {'name':'印刷', 'id':43},
        {'name':'试听器材', 'id':38},
        {'name':'电力', 'id':47},
        {'name':'燃气', 'id':47},
        {'name':'公路', 'id':48},
        {'name':'铁路', 'id':48},
        {'name':'机场', 'id':48},
        {'name':'港口', 'id':48},
        {'name':'运输', 'id':48},
        {'name':'计算机应用', 'id':56},
        {'name':'通信服务', 'id':55},
        {'name':'通讯设备', 'id':34},
        {'name':'计算机设备', 'id':35},
        {'name':'银行', 'id':53},
        {'name':'保险', 'id':53},
        {'name':'证券', 'id':53},
        {'name':'建筑装饰', 'id':50},
        {'name':'房地产开发', 'id':49},
        {'name':'家用轻工', 'id':37},
        {'name':'建筑材料', 'id':23},
        {'name':'钢铁', 'id':22},
        {'name':'化工新材料', 'id':21},
        {'name':'化工合成材料', 'id':20},
        {'name':'化学制品', 'id':19},
        {'name':'基础化学', 'id':18},
        {'name':'采掘服务', 'id':17},
        {'name':'石油', 'id':3},
        {'name':'煤炭', 'id':3},
        {'name':'矿业', 'id':3},
        {'name':'开采', 'id':3},
        {'name':'通用机械', 'id':24},
        {'name':'专用设备', 'id':24},
        {'name':'交运设备服务', 'id':33},
        {'name':'汽车零部件', 'id':31},
        {'name':'汽车整车', 'id':30},
        {'name':'光学', 'id':28},
        {'name':'光电子', 'id':28},
        {'name':'半导体', 'id':27},
        {'name':'元件', 'id':27},
        {'name':'电气设备', 'id':26},
        {'name':'农产品加工', 'id':2},
        {'name':'种植业', 'id':1},
        {'name':'林木业', 'id':1},
        {'name':'养殖业', 'id':1},
	{'name':'零售', 'id':54},
        {'name':'贸易', 'id':54},
        {'name':'传媒', 'id':54},
        {'name':'酒类制造', 'id':39},
        {'name':'饮料制造', 'id':39},
        {'name':'酒类', 'id':39},
        {'name':'饮料', 'id':39},
        {'name':'酒店', 'id':52},
        {'name':'餐饮', 'id':52},
        {'name':'景点', 'id':51},
        {'name':'旅游', 'id':51},
        {'name':'白色家电', 'id':36},
        {'name':'家电', 'id':36},
        {'name':'金属制品', 'id':25},
        {'name':'纺织制造', 'id':41},
        {'name':'食品加工', 'id':40},
        {'name':'食品制造', 'id':40}

    ]

    #print(list)
    x = 0

    for l in list:
        try:
            print(l)
            keyword = l['name']
            fenlei = l['id']
            baidumap = BaiduMap(keyword)
            print('_' * 20)
            print('CITY: %s' % baidumap.city.__len__())
            print('DATA: %s' % baidumap.total_num)
            baidumap.get_all()
            x += 1
        except Exception as e:
            print(e)
