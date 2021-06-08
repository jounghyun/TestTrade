import time
import pyupbit
import numpy as np

access = ""
secret = ""

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

while True:
    try:
        df = pyupbit.get_ohlcv("KRW-BTC", interval="minute60", count=100)

        df['ashiopen'] = df['open']
        df['ashiclose'] = (df['high'] + df['low'] + df['open'] + df['close']) * 0.25

        for i in range(1,100):
            df.iloc[i,6] = (df.iloc[i-1,6] + df.iloc[i-1,7]) * 0.5

        df['bong'] = df['ashiclose'] - df['ashiopen']
        df['norbong'] = df['close'] - df['open']

        print ('ash(h-2) : {0}, ash(h-1) : {1} , ash_cur : {2}, nor(h-2) : {3}, nor(h-1) : {4}, nor_cur : {5}'.format(df.iloc[97,8], df.iloc[98,8], df.iloc[99,8], df.iloc[97,9], df.iloc[98,9], df.iloc[99,9]))

        if df.iloc[97,8] > 0 and df.iloc[98,8] > 0 and df.iloc[97,9] > 0 and df.iloc[98,9] > 0:
            krw = get_balance("KRW")
            print("balance : {0} won".format(krw))
            if krw > 5000:
                print("buy : {0}".format(krw*0.9995))
                upbit.buy_market_order("KRW-BTC", krw*0.9995) 
        else:
            btc = get_balance("BTC")
            print("sell : {0}".format(btc*0.9995))
            
            if btc > 0.00008:
                print("sell : {0}".format(btc*0.9995))
                upbit.sell_market_order("KRW-BTC", btc*0.9995)

        time.sleep(500)
    except Exception as e:
        print(e)
        time.sleep(500)

#df.to_excel("dd.xlsx")
