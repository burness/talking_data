#-*-coding:utf-8-*-
import pandas as pd
from config import *
from tqdm import tqdm
try:
    import cPickle as pickle
except ImportError:
    import pickle


def merge(events_file, app_events_file, device_appid_file_path):
    events_pd = pd.read_csv(event_file_path)
    app_events_pd = pd.read_csv(app_event_file_path)

    device_appid_pd = app_events_pd.merge(events_pd, on='event_id', how='inner')
    device_appid_pd.to_csv(device_appid_file_path,index=None)


def get_deviceid_app_ids(device_appid_file_path, deviceid_appids_dict_file):
    device_appids = {}
    with open(device_appid_file_path,'r') as fread:
        for index,line in enumerate(fread.readlines()):
            if index == 0:
                continue
            else:
                line_list = line.split(",")
                device_id = line_list[4]
                app_id = line_list[1]
                is_installed = line_list[2]
                is_active = line_list[3]
                if not device_appids.has_key(device_id):
                    temp = []
                    temp.append(app_id+','+is_installed+','+is_active)
                    device_appids[device_id] = temp
                else:
                    temp = device_appids[device_id]
                    temp.append(app_id+','+is_installed+','+is_active)
                    device_appids[device_id] = temp
    pickle.dump(device_appids, open(deviceid_appids_dict_file, "wb"))

def get_deviceid_less_dummies_isinstall_isactive(deviceid_appids_dict_file, app_id_less_dummies_file_path,deviceid_less_dummies_file_path):
    f = open(deviceid_appids_dict_file, "r")
    deviceid_appids = pickle.load(f)
    print 'load deviceid_appids done!'
    appid_less_dummies = pickle.load(open(app_id_less_dummies_file_path,"r"))
    print 'load appid_less_dummies done!'
    with open(deviceid_less_dummies_file_path,'w') as fwrite:
        for deviceid, appids in tqdm(deviceid_appids.items()):

            dummies = [0]*50
            # dummies_isInstalled = [0]*50
            dummies_isActive = [0]*50

            for appid_isInstalled_isActive in appids:
                temp_list = appid_isInstalled_isActive.split(",")
                appid = temp_list[0]
                isInstalled = temp_list[1]
                isActive = temp_list[2]
                temp_dummies = [int(i) for i in appid_less_dummies[appid].split(",")]
                # dummies += temp_dummies
                dummies = map(lambda (a,b):a+b,zip(dummies, temp_dummies))
                # if isInstalled == '1':
                #     dummies_isInstalled = map(lambda (a,b):a+b,zip(dummies_isInstalled, temp_dummies))
                if isActive == '1':
                    dummies_isActive = map(lambda (a,b):a+b,zip(dummies_isActive, temp_dummies))
            # print deviceid
            line = deviceid+','+','.join([str(i) for i in dummies])+','+','.join([str(i) for i in dummies_isActive])+'\n'
            fwrite.write(line)





if __name__ == '__main__':
    # merge(event_file_path, app_event_file_path,device_appid_file_path)
    # get_deviceid_app_ids(device_appid_file_path,deviceid_appids_dict_file)
    # f=open(deviceid_appids_dict_file, 'rb')
    # deviceid_appids_dict = pickle.load(f)
    # print len(deviceid_appids_dict)
    get_deviceid_less_dummies_isinstall_isactive(deviceid_appids_dict_file,app_id_less_dummies_file_path,deviceid_less_dummies_file_path)