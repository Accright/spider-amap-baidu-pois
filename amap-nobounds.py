from urllib.parse import quote
from urllib import request
import json
import xlwt

amap_web_key = '5eb46ea6fa37410047f8d994309b9437'
poi_search_url = "http://restapi.amap.com/v3/place/text"

# TODO 需要爬取的POI所属的城市名，以及分类名. (中文名或者代码都可以，代码详见高德地图的POI分类编码表)
cityname = "370102"
classfiled = "100100"


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i)
        print(result)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
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
    sheet.write(0, 0, 'id')
    sheet.write(0, 1, 'related_id')
    sheet.write(0, 2, 'name')
    sheet.write(0, 3, 'location')
    sheet.write(0, 4, 'pname')
    sheet.write(0, 5, 'pcode')
    sheet.write(0, 6, 'cityname')
    sheet.write(0, 7, 'citycode')
    sheet.write(0, 8, 'adname')
    sheet.write(0, 9, 'adcode')
    sheet.write(0, 10, 'address')
    sheet.write(0, 11, 'type')
    sheet.write(0, 12, 'typecode')
    sheet.write(0, 13, 'gridcode')
    sheet.write(0, 14, 'entr_location')
    sheet.write(0, 15, 'timestamp')
    sheet.write(0, 16, 'tel')
    sheet.write(0, 17, 'postcode')
    sheet.write(0, 18, 'tag')
    sheet.write(1, 19, 'shopid')
    sheet.write(1, 20, 'shopinfo')

    for i in range(len(poilist)):
        # 每一行写入
        sheet.write(i + 1, 0, poilist[i]['id'])
        sheet.write(i + 1, 1, poilist[i]['parent'])
        sheet.write(i + 1, 2, poilist[i]['name'])
        sheet.write(i + 1, 3, poilist[i]['location'])
        sheet.write(i + 1, 4, poilist[i]['pname'])
        sheet.write(i + 1, 5, poilist[i]['pcode'])
        sheet.write(i + 1, 6, poilist[i]['cityname'])
        sheet.write(i + 1, 7, poilist[i]['citycode'])
        sheet.write(i + 1, 8, poilist[i]['adname'])
        sheet.write(i + 1, 9, poilist[i]['adcode'])
        sheet.write(i + 1, 10, poilist[i]['address'])
        sheet.write(i + 1, 11, poilist[i]['type'])
        sheet.write(i + 1, 12, poilist[i]['typecode'])
        sheet.write(i + 1, 13, poilist[i]['gridcode'])
        sheet.write(i + 1, 14, poilist[i]['entr_location'])
        sheet.write(i + 1, 15, poilist[i]['timestamp'])
        sheet.write(i + 1, 16, poilist[i]['tel'])
        sheet.write(i + 1, 17, poilist[i]['postcode'])
        sheet.write(i + 1, 18, poilist[i]['tag'])
        sheet.write(i + 1, 19, poilist[i]['shopid'])
        sheet.write(i + 1, 20, poilist[i]['shopinfo'])

    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'' + cityname + "_" + classfield + '.xls')


# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&types=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data


# 获取城市分类数据

pois = getpois(cityname, classfiled)

# 将数据写入excel
write_to_excel(pois, cityname, classfiled)
print('写入成功')