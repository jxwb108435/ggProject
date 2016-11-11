# coding=utf-8
# -*- coding:cp936 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import DateFormatter, AutoDateLocator
import os

prepath = '/home/lin/ggprice/'
file_ar = os.listdir(prepath)  # list all files

df_file = pd.DataFrame(file_ar, columns=['filename'])
df_file['newfile'] = df_file['filename'].apply(lambda x: x.split('.')[0])
df_file['date'] = df_file['newfile']. \
    apply(lambda x: int(x.split(' ')[0].replace('-', '') + x.split(' ')[1].replace(':', '')))

df_file = df_file.sort_values(by='date')
df_file.index = range(len(df_file))

file_target = prepath + df_file['filename'][-1:].values[0]  # find newest file


def live_data(_file_target):
    df = pd.read_csv(_file_target, names=['date', 'EURUSD', 'EURJPY', 'EURAUD', 'USDJPY']).dropna()
    df = df[-3500:]

    df['EURUSD'] = df['EURUSD'].apply(lambda x: float(x.split(':')[1]))
    df['EURJPY'] = df['EURJPY'].apply(lambda x: float(x.split(':')[1]))
    df['EURAUD'] = df['EURAUD'].apply(lambda x: float(x.split(':')[1]))
    df['USDJPY'] = df['USDJPY'].apply(lambda x: float(x.split(':')[1]))
    df['date'] = df['date'].apply(lambda x: x.split('.')[0] + '.' + x.split('.')[1][0:3])

    df.index = pd.DatetimeIndex(df['date'])  # index as DatetimeIndex
    df = df.resample('1S').mean()  # resample 1S

    df['sma5_eurusd'] = df['EURUSD'].rolling(5).mean()
    df['sma20_eurusd'] = df['EURUSD'].rolling(20).mean()
    df['sma60_eurusd'] = df['EURUSD'].rolling(60).mean()
    df['sma180_eurusd'] = df['EURUSD'].rolling(180).mean()

    # _, df['bbup'], df['bbdown'] = bollinger(df['EURUSD'], period=240, d=2.5)

    df = df.ix[-601:]  # keep 10 minutes price

    return df['EURUSD'].index, df['EURUSD'].values,\
           df['sma5_eurusd'].values, df['sma20_eurusd'].values, df['sma60_eurusd'].values, df['sma180_eurusd'].values


'''
start = time.time()
live_data(file_target)
print(time.time() - start)
'''

fig = plt.figure(figsize=(20, 10), facecolor=(0.15, 0.18, 0.22))

price_color = (0.14, 0.56, 0.78)
bg_color = (0.12, 0.13, 0.16)


def animate(_):
    fig.clf()
    fig.subplots_adjust(bottom=0.2, hspace=0)

    '''EURUSD_main_win'''
    ax0 = plt.subplot2grid((6, 4), (1, 0), rowspan=5, colspan=4, axisbg=bg_color)
    ax0.grid(True)

    # data
    date, price_float, sma5, sma20, sma60, sma180 = live_data(file_target)

    # live price line
    ax0.plot(date, price_float, color=price_color, linewidth=1.5)  # live price line

    # sma
    ax0.plot(date, sma5, color='w', linewidth=0.7, alpha=0.5)  # sma5 line
    ax0.plot(date, sma20, color='w', linewidth=1, alpha=1)  # sma20 line
    ax0.plot(date, sma60, color='y', linewidth=1, alpha=0.8)  # sma60 line
    ax0.plot(date, sma180, color='r', linewidth=1.25, alpha=1)  # sma180 line

    # bb
    # ax0.plot(date, bbup, color='blue', linewidth=1, alpha=0.7)  # bb line
    # ax0.plot(date, bbdown, color='blue', linewidth=1, alpha=0.7)  # bb line

    ax0.axhline(price_float[-1:], color=price_color)  # newest live price level line
    ax0.ticklabel_format(axis='y', useOffset=False)  # Y not use offset

    # live price text
    y_location = (price_float[-1:] - ax0.get_ylim()[0]) / (ax0.get_ylim()[1] - ax0.get_ylim()[0])
    ax0.text(1.03, y_location, price_float[-1:][0], color=price_color, ha='center', transform=ax0.transAxes)  # right
    ax0.text(-0.03, y_location, price_float[-1:][0], color=price_color, ha='center', transform=ax0.transAxes)  # left

    # X set
    ax0.xaxis.set_major_locator(AutoDateLocator())
    ax0.xaxis.set_major_formatter(DateFormatter('%y-%m-%d %H:  %M:%S'))
    ax0.set_xlabel('Date', color='w', fontsize=12)  # X label set
    plt.setp(ax0.get_xticklabels(), rotation=35, ha='right', color='w', fontsize=9)

    '''EURUSD_rsi_win'''
    '''
    ax1 = plt.subplot2grid((6, 4), (0, 0), rowspan=1, colspan=4, axisbg=bg_color, sharex=ax0)
    ax1.set_ylim(0, 100)
    ax1.axhline(80, color='w', linewidth=0.7, alpha=0.6)
    ax1.axhline(20, color='w', linewidth=0.7, alpha=0.6)
    ax1.plot(date, rsiline, color=(0.14, 0.56, 0.78), linewidth=1.5)'''


while True:
    ani = animation.FuncAnimation(fig, animate, interval=1)
    plt.show()
