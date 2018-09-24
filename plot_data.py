import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance


# linear plot timestamp/open
def plot_time_open(dframe):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(1, figsize=(20, 10))
    fig.autofmt_xdate()
    plt.plot(dframe['Timestamp'], dframe['Open'])

    xfmt = mdates.DateFormatter('%d-%m-%y %H:%M')
    ax.xaxis.set_major_formatter(xfmt)

    plt.show()


# just print dataframe with
def show_exchange_rate(dframe):
    return print(dframe)


# Candlestick plot of data
def plot_candlestick(dframe, intradict):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(1, figsize=(20, 10))
    dframe['Timestamp'] = dframe['Timestamp'].apply(lambda d: mdates.date2num(d.to_pydatetime()))
    fig.autofmt_xdate()
    xfmt = mdates.DateFormatter('%d-%m-%y %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    # width=0.02 for 60min , 0.0005 for 1m 0.015 for 30m, 0.008 for 15m, 0.003 for 5m
    if intradict['interval'] == '1min':
        mpl_finance.candlestick_ohlc(ax, dframe.values, width=0.0005, colorup='g')
    elif intradict['interval'] == '5min':
        mpl_finance.candlestick_ohlc(ax, dframe.values, width=0.003, colorup='g')
    elif intradict['interval'] == '15min':
        mpl_finance.candlestick_ohlc(ax, dframe.values, width=0.008, colorup='g')
    elif intradict['interval'] == '30min':
        mpl_finance.candlestick_ohlc(ax, dframe.values, width=0.015, colorup='g')
    else:
        mpl_finance.candlestick_ohlc(ax, dframe.values, width=0.02, colorup='g')
    plt.show()
