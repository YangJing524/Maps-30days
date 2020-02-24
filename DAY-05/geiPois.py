import numpy as np
import requests
import math
import time


def gcj2wgs(loc):
    lon = float(loc.split(',')[0])
    lat = float(loc.split(',')[1])
    a = 6378245.0
    ee = 0.00669342162296594323
    PI = 3.14159265358979324
    # convert way
    x = lon - 105.0
    y = lat - 35.0
    # longtitude
    dLon = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    dLon += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    dLon += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
    dLon += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0
    # lattitude
    dLat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    dLat += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    dLat += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
    dLat += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI)
    wgsLon = lon - dLon
    wgsLat = lat - dLat
    return wgsLon, wgsLat


def getGaodePois(keyword,city_param):

    arr1 = ['610101', '610102', '610103', '610104', '610111','610112','610113','610114', '610115','610116','610101','610117', '610118']
    arr2 = ['610201', '610202', '610203', '610204']
    arr3 = ['610301', '610302', '610303', '610304']
    arr4 = ['610401', '610402', '610403', '610404']
    arr5 = ['610501', '610502', '610503']
    arr6 = ['610601', '610602', '610603', '610621', '610622']
    arr7 = ['610701', '610702', '610703']
    arr8 = ['610801', '610802', '610803']
    arr9 = ['610901', '610902']
    arr10 = ['611001', '611002']

    if city_param == '西安':
        arr = arr1
    elif city_param.encode('utf-8') == '铜川'.encode('utf-8'):
        arr = arr2
    elif city_param == "宝鸡":
        arr=arr3
    elif city_param == "咸阳":
        arr=arr4
    elif city_param == "渭南":
        arr=arr5
    elif city_param=="延安":
        arr=arr6
    elif city_param=="汉中":
        arr=arr7
    elif city_param=="榆林":
        arr=arr8
    elif city_param=="安康":
        arr=arr9
    elif city_param=="商洛":
        arr=arr10
    global arr

    url1 = "https://restapi.amap.com/v3/place/text?keywords="+keyword+"&city="
    url2 = "&output=JSON&offset=45&key=b01803a8d6382fc3dbeaf2d7fcf319df&extensions=all&page="
    x = []
    # x.append(['name','type','address','adname','long','lat'])
    num = 0
    for i in range(0, len(arr)):
        city = arr[i]
        for page in range(1, 46):
            if page == 45:
                pass
            thisUrl = url1 + city + url2 + str(page)
            data = requests.get(thisUrl)
            s = data.json()
            aa = s["pois"]
            if len(aa) == 0:
                break
            for k in range(0, len(aa)):
                s1 = aa[k]["name"]
                s2 = aa[k]["type"]
                s3 = aa[k]["address"]
                s4 = aa[k]["adname"]
                long,lat = gcj2wgs(aa[k]["location"])
                x.append([s1, s2, s3, s4, float(long), float(lat)])
                num += 1
                arcpy.AddMessage("Crawl " + str(num) + " pieces of data")
            time.sleep(1)


    # c = pd.DataFrame(x)
    # try:
    #     c.to_excel(keyword+r'.xlsx', index = False,columns=x[0])
    # except:
    #     c.to_csv(keyword+'.csv', encoding='utf-8-sig',index = False,columns=x[0])

    arr=np.array(x)

    struct_array = np.core.records.fromarrays(arr.transpose(), np.dtype(
        [('name', 'U50'), ('type', 'U50'), ('address', 'U150'), ('adname', 'U50'), ('long', '<f8'), ('lat', '<f8')]))

    np.save('%s'%poi,struct_array)
