from urllib.parse import quote
from urllib import request
import json
import xlwt
import gzip
import time

amap_web_key = '5eb46ea6fa37410047f8d994309b9437'
poi_search_url = "http://restapi.amap.com/v3/place/text"
#poi_boundary_url = "https://ditu.amap.com/detail/get/detail"
#poi_boundary_url = "https://restapi.amap.com/v3/place/detail"
poi_boundary_url = "https://www.amap.com/detail/get/detail"
user_headers = {
    "Accept": "*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,en-US;q=0.8,zh;q=0.7,zh-TW;q=0.5,zh-HK;q=0.3,en;q=0.2",
    "amapuuid":"916f893f-cec2-426b-803c-5b5ec4561dd2",
    "Cache-Control": "no-cache",
    "Connection":"keep-alive",
    "Cookie":"guid=e76c-fe6d-b172-d3e4; cna=VFmCFHwPaDUCATo4YBwMxvGd; UM_distinctid=1677d609703160-047d521484d454-3f674706-100200-1677d609705294; _uab_collina=154399674306109011360082; CNZZDATA1255827602=951263052-1544000258-https%253A%252F%252Fwww.amap.com%252F%7C1544000258; passport_login=MjkyODAxODUsYW1hcDFzQU90bzlBLDF0a3h6Mndva3p4dnJ4c2lqczlubHI0bDFtbThmejh2LDE1NDQwMDE2NjIsWlRRNE1tRXdNemMzT0RBd09EWTROVGxpT0dZd05tSTBORGM1WW1VeU5qZz0%3D; dev_help=Sy9s5VNrXHb8CavXjjS0ezk1YjEyNWJiMzkwNGY4ODg0ZTg3OWJiY2YxNGMwZWE4NmM3ZmVjNzY5N2IyODQ3YzA2ZjFiNmIyM2NiMzgzZjn7jjyPrV7hgsxyMuxywFmBy0p7Nkv4koka5RtGOyAl5il7%2Ffwc8ZPgjCfeqrPlEhOgWzBAarKyva28URsrNbdbStwZpe8JB8CBx2CwaTS%2FRo0FZ1nIYcze1qNvBmXRrjE%3D; CNZZDATA1255626299=25125204-1543995015-https%253A%252F%252Fwww.baidu.com%252F%7C1544161437; x5sec=7b22617365727665723b32223a226165326562643965636165396334636532616339333135646231313132626135434f367a742b4146454d615337656a397759485159773d3d227d; isg=BFdXSFZix6Mo6UMlHPID1STr5sur1K1zumu2wqmORiaN2EYasG6xTzi-PhjjMAN2",
    "Host":"www.amap.com",
    "Pragma": "no-cache",
    #"If-None-Match":"W/\"382b-0w87OtvHSz1K1c/FUTJxullFxqU\""
    "Referer":"https://www.amap.com/",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    "x-csrf-token":"null",
    "X-Requested-With":"XMLHttpRequest"
}


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords,types):
    i = 1
    poilist = []
    while i < 100:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords,types, i)
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
    sheet.write(0, 12, 'boundary')
    for i in range(len(poilist)):
        # 根据poi的id获取边界数据
        bounstr = ''
        bounlist = getBounById(poilist[i]['id'])
        if (len(bounlist) > 1):
            bounstr = str(bounlist)
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
        sheet.write(i + 1, 12, bounstr)
    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'' + cityname + '_'+ classfield+'-1.xls')


# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(cityname, keywords,types, page):
    #req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
    #    keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
    #    page) + '&output=json'
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&types=' + quote(
        types) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=10' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    print("data is",data)
    return data


# 根据id获取边界数据
def getBounById(id):
    time.sleep(1)#避免被识别为爬虫
    get_request = request.Request(poi_boundary_url+"?id="+id, headers= user_headers)
    #access_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    req_url = poi_boundary_url + "?key="+amap_web_key+"&id=" + id
    with request.urlopen(get_request) as f:
        data = f.read()
        data = gzip.decompress(data).decode("utf-8")
        #print("real data is",ret)
        #data = data.decode('utf-8')
        dataList = []
        datajson = json.loads(data)  # 将字符串转换为json
        print("datajson",datajson)
        datajson = datajson['data']
        datajson = datajson['spec']
        if len(datajson) == 1:
            return dataList
        if datajson.get('mining_shape') != None:
            datajson = datajson['mining_shape']
            shape = datajson['shape']
            dataArr = shape.split(';')

            for i in dataArr:
                innerList = []
                f1 = float(i.split(',')[0])
                innerList.append(float(i.split(',')[0]))
                innerList.append(float(i.split(',')[1]))
                dataList.append(innerList)
        return dataList


# 获取城市分类数据
cityname = "370102"#"济南"
classfiled = "浪潮科技园"
typeparam = "100100"#"120100"
pois = getpois(cityname, classfiled,typeparam)

# 将数据写入excel
write_to_excel(pois, cityname, classfiled)
print('写入成功')

# 根据获取到的poi数据的id获取边界数据
# dataList = getBounById('B02F4027LY')
# print(type(dataList))

# print(str(dataList))
'''
  返回的边界数据格式--方便高德地图前端展示
  [[113.559199, 22.239364], [113.559693, 22.238274], [113.55677, 22.237162], 
  [113.557008, 22.236653], [113.555582, 22.236117], [113.555747, 22.235742], 
  [113.555163, 22.235538], [113.555027, 22.235831], [113.554934, 22.235875], 
  [113.554088, 22.235522], [113.553919, 22.235885], [113.553905, 22.235961], 
  [113.556167, 22.236835], [113.55561, 22.238172], [113.55494, 22.237933], 
  [113.554607, 22.238652], [113.554593, 22.238697], [113.554597, 22.238765], 
  [113.554614, 22.238834], [113.554646, 22.238885], [113.558612, 22.240406], 
  [113.558799, 22.240258], [113.559199, 22.239364]] 
'''