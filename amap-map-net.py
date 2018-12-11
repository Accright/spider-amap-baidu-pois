import json
import codecs
import os
import urllib
from urllib.parse import quote
from urllib import request
import sys
import time
import re

class BaiDuPOI(object):
    def __init__(self, itemy, loc):
        self.itemy = itemy
        self.loc = loc

    def urls(self):
        api_key = amap_api
        urls = []
        for pages in range(1, 100):
            #url = 'http://api.map.baidu.com/place/v2/search?query=' + quote(self.itemy) + '&bounds=' + quote(self.loc) + '&page_size=20&page_num=' + str(
                #pages) + '&output=json&ak=' + api_key
            url = "http://restapi.amap.com/v3/place/polygon?key=" + api_key + '&extensions=base&types=' + quote(
                    self.itemy) + '&polygon=' + quote(self.loc) + '&offset=20' + '&page=' + str(
                    pages) + '&output=json'
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
                print("data",data)
                if data['status'] != '1':
                    break
                if len(data['pois'])<= 0:
                    break
                for item in data['pois']:
                    jid = item["id"]
                    jrelated = item['parent']
                    jname = item['name']
                    jtype = item['type']
                    jlocation = item["location"]
                    jprov = item["pname"]
                    jcity = item["cityname"]
                    js_sel = jid+","+str(jrelated) + ','+jname + ','+jtype + ','+str(jlocation) + ','+jprov + ','+jcity
                    if jcity == '贵阳市':
                        bMap = Bmap(jname,'')#获取百度的地址数据
                        bMapAddr = bMap.get_addr()
                        js_sel += ","+bMapAddr
                        json_sel.append(js_sel)#追加到贵阳市的表格数据
                    #print("json_sel",json_sel)
                    #print("item",item)
        return json_sel


class LocaDiv(object):
    def __init__(self, loc_all):
        self.loc_all = loc_all

    def lat_all(self):
        lat_nw = float(self.loc_all.split(',')[1])
        lat_se = float(self.loc_all.split(',')[3])
        #print("loc_all",self.loc_all,"lat_sw",lat_nw,"lat_ne",lat_se,">>>",int((lat_nw - lat_se + 0.0001) / 0.1))
        #分块大小
        print("纬度分块大小及多少",int((lat_nw - lat_se + 0.0001) / 0.1))
        lat_list = []
        for i in range(0, int((lat_nw - lat_se + 0.0001) / 0.1)):  # 0.1为网格大小，可更改
            lat_list.append(round(lat_se + 0.1 * i,6))  # 0.05
        lat_list.append(lat_nw)
        #lat_list.reverse()
        return lat_list

    def lng_all(self):
        lng_nw = float(self.loc_all.split(',')[0])
        lng_se = float(self.loc_all.split(',')[2])
        lng_list = []
        #print("loc_all",self.loc_all,"lng_se",lng_se,"lng_nw",lng_nw,">>>",int((lng_se - lng_nw + 0.0001) / 0.1))
        print("经度分块大小及多少",int((lng_se - lng_nw + 0.0001) / 0.1))
        for i in range(0, int((lng_se - lng_nw + 0.0001) / 0.1)):  # 0.1为网格大小，可更改
            lng_list.append(round(lng_nw + 0.1 * i,6))  # 0.1为网格大小，可更改
        lng_list.append(lng_se)
        return lng_list

    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        print("lng_all",l2)
        print("lat_all",l1)
        ab_list = []
        for i in range(0, len(l1)):
            a = str(l1[i])
            for i2 in range(0, len(l2)):
                b = str(l2[i2])
                ab = b + ',' + a
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


class Bmap(object):
    def __init__(self,wd,ak):
        self.wd = wd
        self.url = "https://api.map.baidu.com/?qt=s&c=146&wd="+quote(wd)+""\
                   "&rn=10&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk9406" \
                   "&ak=8QiGVpCMtmzYxWSeYCMhzQvmjH8laVql"
                   #"&ak="+quote(ak)

    def get_addr(self):
        global addr
        global uid
        global poiboundary
        with request.urlopen(self.url) as f:
            data = f.read()
            data = data.decode('utf-8')
            #result = json.loads(self.loads_jsonp(data))
            result = self.loads_jsonp(data)
            print("result is",result,"url is",self.url)
            if result.get("content") != None and len(result['content']) > 0:
                print("result content", result['content'][0].get("acc_flag"))
                if result['content'][0].get("acc_flag") != None:
                    addr = result['content'][0]['address_norm']
                    uid = result['content'][0]['uid']
                    if result['content'][0].get("ext") != None and result['content'][0].get("ext").get("detail_info") != None \
                        and result['content'][0].get("ext").get("detail_info").get("guoke_geo") != None \
                        and result['content'][0].get("ext").get("detail_info").get("guoke_geo").get("geo") != None:
                        poiboundary = result['content'][0].get("ext").get("detail_info").get("guoke_geo").get("geo")
                    else:
                        poiboundary = ""
                else:
                    addr = ""
                    uid = ""
                    poiboundary = ""
            return addr+","+uid+","+poiboundary

    def loads_jsonp(self, _jsonp):
        """
        解析jsonp数据格式为json
        :return:
        """
        try:
            return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
        except:
            raise ValueError('Invalid Input')


if __name__ == '__main__':
    # ak
    baidu_api ="vkie9s9hRY9xlbMxDuXtXBPajHPhNBuU"   # 这里填入你的百度API的ak
    amap_api = "5eb46ea6fa37410047f8d994309b9437"
    print( "开始爬取数据，请稍等...")
    start_time = time.time()
    loc = LocaDiv('106.126088, 27.289100, 107.266844, 26.169422')
    # 贵阳市坐标 左上点坐标：106.12608804006908, 27.289100635458635 右下角坐标：107.26684404805242 26.16942282420166
    # demo 坐标 ：29.8255, 115.367400, 30.2194, 115.8287
    # 公司企业分类 170000
    locs_to_use = loc.ls_row()
    print("locs_to_use",locs_to_use)
    for loc_to_use in locs_to_use:
        par = BaiDuPOI(u'010000|020000|030000|040000|050000|060000|070000|080000|090000|100000'
                       u'|110000|120000|130000|140000|150000|160000|170000|180000|190108|190109|200000',
                       loc_to_use)  # 请修改爬取的类别
        a = par.baidu_search()
        #print("a is >>>",a)
        doc = open('demo_sql_amap_bmap.csv', 'w+')
        #doc.write(codecs.BOM_UTF8)
        for ax in a:
            doc.write(ax)
            doc.write('\n')
        doc.close()
    end_time = time.time()
    print ("购物爬取完毕，用时%.2f秒" % (end_time - start_time))