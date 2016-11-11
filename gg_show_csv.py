# ！usr/bin/python
# coding=utf-8
# -*- coding:cp936 -*-
import pandas as pd
import time
import os

prepath = '/home/lin/ggprice/'
file_ar = os.listdir(prepath)  # list all files

df_file = pd.DataFrame(file_ar, columns=['filename'])
df_file['newfile'] = df_file['filename'].apply(lambda x: x.split('.')[0])
df_file['date'] = df_file['newfile'].\
    apply(lambda x: int(x.split(' ')[0].replace('-', '')+x.split(' ')[1].replace(':', '')))

file_target = prepath+df_file.ix[df_file.date == df_file['date'].max()]['filename'].values[0]  # find newest file

while True:
    df = pd.read_csv(file_target, names=['date', 'EURUSD', 'EURJPY', 'EURAUD', 'USDJPY'])
    df = df[-1:]
    df['EURUSD'] = df['EURUSD'].apply(lambda x: float(x.split(':')[1]))
    df['EURJPY'] = df['EURJPY'].apply(lambda x: float(x.split(':')[1]))
    df['EURAUD'] = df['EURAUD'].apply(lambda x: float(x.split(':')[1]))
    df['USDJPY'] = df['USDJPY'].apply(lambda x: float(x.split(':')[1]))
    df['date'] = df['date'].apply(lambda x: x.split('.')[0] + '.' + x.split('.')[1][0:3])

    print(df)
    time.sleep(0.5)
