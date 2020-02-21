import requests
import math



def geocodeGaode(address):
    key='b01803a8d6382fc3dbeaf2d7fcf319df'
    city = '西安市'
    base_url = "https://restapi.amap.com/v3/place/text?keywords={}&city={}&offset=20&page=1&key={}&extensions=base".format(address,city,key)
    response = requests.get(base_url)
    try:
        answer = response.json()
        locat = answer['pois'][0]['location']
        # latitude=locat.split(',')[1]
        # longitude = locat.split(',')[0]
        # # tel=answer['pois'][0]['tel']
        # # time.sleep(1)s
        # return longitude, latitude

        return gcj2wgs(locat)
    except:
        print(response.status_code)
        return '', ''

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
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI);
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI);
    wgsLon = lon - dLon
    wgsLat = lat - dLat
    return wgsLon, wgsLat

