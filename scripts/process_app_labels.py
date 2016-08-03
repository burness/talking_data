#-*-coding:utf-8-*-
from config import *
try:
    import cPickle as pickle
except ImportError:
    import pickle



def get_appid_labels(file, app_labels_dict_file):
    app_labels = {}
    with open(file, 'r') as fread:
        for index,line in enumerate(fread.readlines()):
            if index == 0:
                continue
            else:
                line_list = line.split(",")
                app_id = line_list[0]
                app_label = line_list[1]
                if not app_labels.has_key(app_id):
                    temp = []
                    temp.append(app_label)
                    app_labels[app_id]=temp
                else:
                    temp = app_labels[app_id]
                    temp.append(app_label)
                    app_labels[app_id] = temp
    pickle.dump(app_labels, open(app_labels_dict_file, "wb"))

def get_labels_cate(file,labels_line_num_dict_file):
    labels_line_num = {}
    with open(file, "r") as fread:
        for index, line in enumerate(fread.readlines()):
            print index
            if index == 0:
                continue
            else:
                label_id = line.split(",")[0]
                labels_line_num[label_id] = index
    pickle.dump(labels_line_num, open(labels_line_num_dict_file, "wb"))


def gen_appid_dummies(labels_line_num_dict_file,app_labels_dict_file,app_id_dummies_file_path):
    f_labels_line_num = open(labels_line_num_dict_file,'rb')
    labels_line_num = pickle.load(f_labels_line_num)
    f_appid_labels = open(app_labels_dict_file,'rb')
    appid_labels = pickle.load(f_appid_labels)

    with open(app_id_dummies_file_path, 'w') as fwrite:
        for appid, labels in appid_labels.items():
            a = [0]*930
            # print a
            label_strip_int = [labels_line_num[i.strip()] for i in labels]
            # print label_strip_int
            for i in label_strip_int:
                a[int(i)-1] = 1
            a_str = ','.join([str(i) for i in a])
            line = appid+','+a_str+'\n'
            fwrite.write(line)

def app_id_dummies_to_less_dummies(app_id_dummies_file_path, app_id_less_dummies_file_path):
    a = [0]*930
    c = [489, 359, 712, 713, 629, 639, 638, 771, 635, 636, 714, 727, 646, 717, 728, 730, 650, 716, 774, 787, 729, 695, 722, 719, 490, 232, 720, 701, 715, 676, 791, 700, 696, 705, 790, 776, 788, 243, 877, 681, 266, 648, 640, 707, 726, 778, 99, 12, 724, 692]
    index_c = {}
    for index, i in enumerate(c):
        index_c[i] = index
    # print index_c
    appid_less_dummies = {}

    with open(app_id_dummies_file_path,'r') as fread:
        # with open(app_id_less_dummies_file_path, 'w') as fwrite:
        for index, line in enumerate(fread.readlines()):
            aa = [0]*51
            line_list =  line.split(",")[1:]
            for index, i in enumerate(line_list):
                if i == "1":
                    if index_c.has_key(index):
                        aa[index_c[index]]=1
                    else:
                        aa[50] +=1
            aa_str = ','.join([str(i) for i in aa])
            appid_less_dummies[line.split(",")[0]] = aa_str
    pickle.dump(appid_less_dummies, open(app_id_less_dummies_file_path, "wb"))




if __name__ == '__main__':
    # get_labels_cate(label_categories_file_path,labels_line_num_dict_file)
    # gen_appid_dummies(labels_line_num_dict_file,app_labels_dict_file,app_id_dummies_file_path)
    app_id_dummies_to_less_dummies(app_id_dummies_file_path,app_id_less_dummies_file_path)
