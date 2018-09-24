import pandas as pd
from pandas.io.common import urlencode
import os
import requests
import io
import argparse
import plot_data
import sys
import time

# Open the file with Api key
with open(os.getcwd()+'/'+'apikey') as file:
    API_KEY = file.read().splitlines()
    API_KEY = ''.join(API_KEY)
API_URL = 'https://www.alphavantage.co/query?'


# Get exchange rate of any crypto-/currency to any crypto-/currency at the time of request
def get_exchange_rate(from_which, to_which):
    ex_rate_dict = dict()
    ex_rate_dict['function'] = 'CURRENCY_EXCHANGE_RATE'
    ex_rate_dict['from_currency'] = from_which
    ex_rate_dict['to_currency'] = to_which
    ex_rate_dict['apikey'] = API_KEY
    return ex_rate_dict


# Get currency exchange intraday time series - realtime updated
def get_exchange_intraday(from_which, to_which, interv, datatype='csv'):
    ex_intraday_dict = dict()
    ex_intraday_dict['function'] = 'FX_INTRADAY'
    ex_intraday_dict['from_symbol'] = from_which
    ex_intraday_dict['to_symbol'] = to_which
    ex_intraday_dict['interval'] = str(interv)+'min'
    ex_intraday_dict['apikey'] = API_KEY
    ex_intraday_dict['datatype'] = datatype
    return ex_intraday_dict


# Encode dictionaries to match needed url to download data, download data, process it depending on the option
# and return dataframe
def download_data(paramdict):
    if paramdict is not None:
        sess = requests.session()
        url = API_URL + urlencode(paramdict)
        # print(url)
        r = sess.get(url)
        if paramdict['function'] == 'CURRENCY_EXCHANGE_RATE':
            data = r.json()
            df = pd.DataFrame.from_dict(data)
            return df
        elif paramdict['function'] == 'FX_INTRADAY':
            data = r.content
            df = pd.read_csv(io.BytesIO(data))
            return df
        else:
            sys.exit("Wrong option!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get and plot stock data')
    parser.add_argument('-o', '--option', help='Decide whether you want FX INTRADAY with time interval or just'
                                               'EXCHANGE RATE(with crypto)', required=True, dest='o')
    parser.add_argument('-f', '--from', help='Which (crypto)currency do you want to get exchange from', required=True,
                        dest='f')
    parser.add_argument('-t', '--to', help='To which currency you want exchange to', required=True, dest='t')
    parser.add_argument('-i', '--interval', help='(Only for intraday) specify time interval for intraday exchange',
                        default=1, type=int, dest='i')
    parser.add_argument('-p', '--plot', help='Plot types - linear or candle (Intraday only)', type=str, dest='p')
    args = parser.parse_args()
    if args.o == 'XR'.lower() or args.o == 'EXR'.lower() or args.o == 'EXCHANGE RATE'.lower():
        while True:
            intradict = get_exchange_rate(args.f, args.t)
            dframe = download_data(intradict)
            plot_data.show_exchange_rate(dframe)
            print("It will keep refreshing every three seconds")
            print('\n')
            time.sleep(3)
    elif args.o == 'FX INTRADAY'.lower() or args.o == 'FXI'.lower() or args.o == 'FI'.lower():
        intradict = get_exchange_intraday(args.f, args.t, args.i)
        dframe = download_data(intradict)
        columns = ['Timestamp', 'Open', 'High', 'Low', 'Close']
        dframe.columns = columns
        dframe['Timestamp'] = pd.to_datetime(dframe['Timestamp'])
        if args.p == 'linear':
            plot_data.plot_time_open(dframe)
        elif args.p == 'candle':
            plot_data.plot_candlestick(dframe, intradict)
        else:
            sys.exit("Wrong plot type")


# TODO
# manage interval 1-5-15-30-60 to not allow different
# split into more files
# kick out the while True
# clean the code?
