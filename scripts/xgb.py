import pandas as pd
from config import *
import numpy as np
import time
from sklearn.cross_validation import train_test_split
import xgboost as xgb
from sklearn.metrics import log_loss
import datetime


def map_column(table, f):
    labels = sorted(table[f].unique())
    mappings = dict()
    for i in range(len(labels)):
        mappings[labels[i]] = i
    table = table.replace({f: mappings})
    return table

def run_xgb(train, test, features, target, random_state=0):
    eta = 0.07
    max_depth = 6
    subsample = 0.7
    colsample_bytree = 0.7
    start_time = time.time()

    print('XGBoost params. ETA: {}, MAX_DEPTH: {}, SUBSAMPLE: {}, COLSAMPLE_BY_TREE: {}'.format(eta, max_depth, subsample, colsample_bytree))
    params = {
        "objective": "multi:softprob",
        "num_class": 12,
        "booster" : "gbtree",
        "eval_metric": "mlogloss",
        "eta": eta,
        "max_depth": max_depth,
        "subsample": subsample,
        "colsample_bytree": colsample_bytree,
        "silent": 1,
        "seed": random_state,
    }
    num_boost_round = 500
    early_stopping_rounds = 50
    test_size = 0.3

    X_train, X_valid = train_test_split(train, test_size=test_size, random_state=random_state)
    print('Length train:', len(X_train.index))
    print('Length valid:', len(X_valid.index))
    y_train = X_train[target]
    y_valid = X_valid[target]
    dtrain = xgb.DMatrix(X_train[features], y_train)
    dvalid = xgb.DMatrix(X_valid[features], y_valid)

    watchlist = [(dtrain, 'train'), (dvalid, 'eval')]
    gbm = xgb.train(params, dtrain, num_boost_round, evals=watchlist, early_stopping_rounds=early_stopping_rounds, verbose_eval=True)

    print("Validating...")
    check = gbm.predict(xgb.DMatrix(X_valid[features]), ntree_limit=gbm.best_iteration)
    score = log_loss(y_valid.tolist(), check)

    print("Predict test set...")
    test_prediction = gbm.predict(xgb.DMatrix(test[features]), ntree_limit=gbm.best_iteration)

    print('Training time: {} minutes'.format(round((time.time() - start_time)/60, 2)))
    return test_prediction.tolist(), score


def read_train_test():
    print "reading deviceid less_dummies isactive data"
    # add table headers
    deviceid_less_dummies = pd.read_csv(deviceid_less_dummies_file_path,header=None)
    # print deviceid_less_dummies.count()
    deviceid_headers = ['device_id']+['event_'+str(i) for i in range(50)]+['is_active_'+str(i) for i in range(50)]
    deviceid_less_dummies.columns = deviceid_headers
    deviceid_less_dummies['device_id'] = deviceid_less_dummies['device_id'].astype(np.str)
    # add phone brand
    pbd = pd.read_csv(phone_brand_device_model_file_path, dtype={'device_id': np.str})
    pbd.drop_duplicates('device_id', keep='first', inplace=True)
    pbd = map_column(pbd, 'phone_brand')
    pbd = map_column(pbd, 'device_model')
    deviceid_less_dummies = deviceid_less_dummies.merge(pbd, on='device_id', how='inner')

    # print deviceid_less_dummies.head(5)
    # print deviceid_less_dummies.dtypes

    print "reading train data"
    gender_age_train = pd.read_csv(gender_age_train_file_path, dtype={'device_id': np.str})
    # print gender_age_train.count()
    gender_age_train = map_column(gender_age_train, 'group')
    gender_age_train = gender_age_train.drop(['age'], axis=1)
    gender_age_train = gender_age_train.drop(['gender'], axis=1)
    # print gender_age_train =
    train = deviceid_less_dummies.merge(gender_age_train, on='device_id', how='inner')

    print "reading test data"
    test_deviceid = pd.read_csv(gender_age_test_file_path, dtype={'device_id': np.str})
    test = deviceid_less_dummies.merge(test_deviceid, on='device_id', how='inner')

    features = list(test.columns.values)
    features.remove('device_id')
    return train, test, features

def create_submission(score, test, prediction):
    # Make Submission
    now = datetime.datetime.now()
    sub_file = 'submission2_' + str(score) + '_' + str(now.strftime("%Y-%m-%d-%H-%M")) + '.csv'
    print('Writing submission: ', sub_file)
    f = open(sub_file, 'w')
    f.write('device_id,F23-,F24-26,F27-28,F29-32,F33-42,F43+,M22-,M23-26,M27-28,M29-31,M32-38,M39+\n')
    total = 0
    test_val = test['device_id'].values
    for i in range(len(test_val)):
        str1 = str(test_val[i])
        for j in range(12):
            str1 += ',' + str(prediction[i][j])
        str1 += '\n'
        total += 1
        f.write(str1)
    f.close()


if __name__ == '__main__':
    train, test, features = read_train_test()
    test_prediction,score = run_xgb(train, test, features,'group')
    create_submission(score, test, test_prediction)
    # print score
    # print test_prediction