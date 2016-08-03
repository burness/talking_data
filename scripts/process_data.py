#-*-coding:utf-8-*-
import pandas as pd
from config import *


# app_label_pd = pd.read_csv(app_labels_file_path)
# print app_label_pd['app_id'].nunique()
#
# events_pd = pd.read_csv(event_file_path)
# print events_pd['device_id'].nunique()
#
#
# device_appid_pd = pd.read_csv(device_appid_file_path)
# print device_appid_pd['device_id'].nunique()
#
# gender_age_train_pd = pd.read_csv(gender_age_train_file_path)
# print gender_age_train_pd['device_id'].nunique()
#
# gender_age_test_pd = pd.read_csv(gender_age_test_file_path)
# print gender_age_test_pd['device_id'].nunique()
#
#
# # merge the gender_age_train and events
# train_data = events_pd.merge(gender_age_train_pd, on='device_id', how='inner')
# print train_data['device_id'].nunique()

app_events_pd = pd.read_csv(app_event_file_path)
print app_events_pd.count()
print app_events_pd[app_events_pd.is_active==1].count()