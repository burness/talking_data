#-*-coding:utf-8-*-

# process the time to the local time according to lat and lng



import requests
import time
from config import *
import pickle
# lat = ""
# lon = ""
#
# url = "http://api.geonames.org/timezoneJSON?formatted=true&lat={}&lng {}&username=burness".format(lat,lon)
#
# r = requests.get(url) ## Make a request
# r.json()['timezoneId'] ## return the timezone



def get_timezone_lat_lng(lat, lng):
    url = "http://api.geonames.org/timezoneJSON?formatted=true&lat={}&lng={}&username=burness".format(lat,lng)
    r = requests.get(url) ## Make a request
    # print r.json()
    try:
        result = r.json()['timezoneId']
    except:
        print r.json()
        result = 'error'
    return result ## return the timezone


def get_lat_lng(events_file_path):
    lat_lng_list = []
    with open(events_file_path, 'r') as fread:
        # with open(lat_lng_file_path, 'w') as fwrite:
        for index, line in enumerate(fread.readlines()):
            if index ==0:
                continue
            else:
                line_list = line.strip().split(",")
                lat = line_list[3]
                lng = line_list[4]
                lat_lng_list.append((lat,lng))
    # print len(lat_lng_list)
    return list(set(lat_lng_list))




if __name__ == '__main__':
    lat_lng_list = get_lat_lng(events_file_path=event_file_path)
    # print len(lat_lng_list)
    # print [i for i in lat_lng_list][:2]
    lat_lng_dict = {}
    index = 0
    for lng,lat in lat_lng_list[:20000]:
        index+=1
        if index % 100 ==0:
            print 'get the lat %d th'%index
        timezone = get_timezone_lat_lng(lat,lng)
        time.sleep(0.5)
        key = lat+','+lng
        lat_lng_dict[key] = timezone
        # print timezone
    f = open('lat_lng_dict_0_20000.dict','wb')
    pickle.dump(lat_lng_dict, f)