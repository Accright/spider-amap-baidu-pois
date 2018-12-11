from urllib.parse import quote
from urllib import request
import json
import xlwt

amap_web_key = 'vkie9s9hRY9xlbMxDuXtXBPajHPhNBuU'
poi_search_url = "http://api.map.baidu.com/place/v2/search"

# TODO 需要爬取的POI所属的城市名，以及分类名. (中文名或者代码都可以，代码详见高德地图的POI分类编码表)
cityname = "济南"
keywords = "公司企业"
tag = "公司企业"


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords,tag):
    i = 1
    poilist = []
    while i < 20:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i,tag)
        #print(result)
        result = json.loads(result)  # 将字符串转换为json
        print("status",result['status'])
        if result['status'] != 0:
            break
        hand(poilist, result)
        i = i + 1
    return poilist


# 数据写入excel
def write_to_excel(poilist, cityname, classfield):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)

    # 第一行(列标题)
    sheet.write(0, 0, 'uid')
    sheet.write(0, 1, 'name')
    #sheet.write(0, 2, 'location')
    sheet.write(0, 3, 'province')
    sheet.write(0, 4, 'city')
    sheet.write(0, 5, 'area')
    sheet.write(0, 6, 'address')
    sheet.write(0, 7, 'street_id')
    sheet.write(0, 8, 'telephone')
    sheet.write(0, 9, 'detail_info')

    for i in range(len(poilist)):
        # 每一行写入
        sheet.write(i + 1, 0, poilist[i]['uid'])
        sheet.write(i + 1, 1, poilist[i]['name'])
        #sheet.write(i + 1, 2, poilist[i]['location'])
        sheet.write(i + 1, 3, poilist[i]['province'])
        sheet.write(i + 1, 4, poilist[i]['city'])
        sheet.write(i + 1, 5, poilist[i]['area'])
        sheet.write(i + 1, 6, poilist[i]['address'])
        sheet.write(i + 1, 7, poilist[i].get('street_id','未知街道id'))
        sheet.write(i + 1, 8, poilist[i].get('telephone','未知电话'))
        sheet.write(i + 1, 9, poilist[i]['detail_info'].get('tag','未知标签'))

    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'' + cityname + "_" + classfield + '.xls')


# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['results']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(cityname, keywords, page,tag):
    req_url = poi_search_url + "?ak=" + amap_web_key + '&query='+quote(keywords)+ '&region=' + quote(cityname) + '&city_limit=true' + '&page_size=25' + '&page_num=' + str(
        page) + '&output=json&scope=2'#+'&tag=' + quote(tag)
    print("req_url is",req_url)
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data


# 获取城市分类数据

pois = getpois(cityname, keywords,tag)

# 将数据写入excel
write_to_excel(pois, cityname, keywords)
print('写入成功')