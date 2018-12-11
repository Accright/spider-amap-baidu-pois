import json
import codecs
import os
import urllib
from urllib.parse import quote
from urllib import request
import sys
import time

class BaiDuPOI(object):
    def __init__(self, itemy, loc):
        self.itemy = itemy
        self.loc = loc

    def urls(self):
        api_key = baidu_api
        urls = []
        for pages in range(0, 20):
            url = 'http://api.map.baidu.com/place/v2/search?query=' + quote(self.itemy) + '&bounds=' + quote(self.loc) + '&page_size=20&page_num=' + str(
                pages) + '&output=json&ak=' + api_key
            urls.append(url)
        return urls

    def baidu_search(self):
        json_sel = []
        for url in self.urls():
            print("url",url)
            with request.urlopen(url) as f:
                data = f.read()
                data = data.decode('utf-8')
                data = json.loads(data)
                #print("json_obj",json_obj)
                #data = json.load(json_obj)
                #data = json_obj.read()
                #data = data.decode('utf-8')
                print("data",data['total'])
                if data['status'] != 0:
                    break
                if len(data['results'])<= 0:
                    break
                for item in data['results']:
                    jname = item["name"]
                    jlat = item["location"]["lat"]
                    jlng = item["location"]["lng"]
                    js_sel = jname + ',' + str(jlat) + ',' + str(jlng)
                    json_sel.append(js_sel)
                    print("item",item)
        return json_sel


class LocaDiv(object):
    def __init__(self, loc_all):
        self.loc_all = loc_all

    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[0])
        lat_ne = float(self.loc_all.split(',')[2])
        print("loc_all",self.loc_all,"lat_sw",lat_sw,"lat_ne",lat_ne,">>>",int((lat_ne - lat_sw + 0.0001) / 0.1))
        lat_list = []
        for i in range(0, int((lat_ne - lat_sw + 0.0001) / 0.1)):  # 0.1为网格大小，可更改
            lat_list.append(lat_sw + 0.1 * i)  # 0.05
        lat_list.append(lat_ne)
        return lat_list

    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[1])
        lng_ne = float(self.loc_all.split(',')[3])
        lng_list = []
        for i in range(0, int((lng_ne - lng_sw + 0.0001) / 0.1)):  # 0.1为网格大小，可更改
            lng_list.append(lng_sw + 0.1 * i)  # 0.1为网格大小，可更改
        lng_list.append(lng_ne)
        return lng_list

    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i in range(0, len(l1)):
            a = str(l1[i])
            for i2 in range(0, len(l2)):
                b = str(l2[i2])
                ab = a + ',' + b
                ab_list.append(ab)
        return ab_list

    def ls_row(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ls_com_v = self.ls_com()
        ls = []
        for n in range(0, len(l1) - 1):
            for i in range(0 + len(l1) * n, len(l2) + (len(l2)) * n - 1):
                a = ls_com_v[i]
                b = ls_com_v[i + len(l2) + 1]
                ab = a + ',' + b
                ls.append(ab)
        return ls


if __name__ == '__main__':
    # ak
    baidu_api ="vkie9s9hRY9xlbMxDuXtXBPajHPhNBuU"   # 这里填入你的百度API的ak
    print( "开始爬取数据，请稍等...")
    start_time = time.time()
    loc = LocaDiv('26.200572, 106.128061, 27.33595, 107.282491')
    # 贵阳市坐标 左下点坐标：106.128061, 26.200572 右上角坐标：107.282491 27.33595
    # demo 坐标 ：29.8255, 115.367400, 30.2194, 115.8287
    locs_to_use = loc.ls_row()

    for loc_to_use in locs_to_use:
        par = BaiDuPOI(u'购物', loc_to_use)  # 请修改爬取的类别
        a = par.baidu_search()
        print("a is >>>",a)
        doc = open('zhengfujigou.csv', 'w+')
        #doc.write(codecs.BOM_UTF8)
        for ax in a:
            doc.write(ax)
            doc.write('\n')
        doc.close()
    end_time = time.time()
    print ("购物爬取完毕，用时%.2f秒" % (end_time - start_time))