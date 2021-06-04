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

        print ('before1 : {0}, before : {1} , final : {2}'.format(df.iloc[97,8], df.iloc[98,8], df.iloc[99,8]))

        if df.iloc[97,8] > 0 and df.iloc[98,8] > 0 :
            krw = get_balance("KRW")
            print("balance : {0} won".format(krw))
            if krw > 5000:
                print("buy : {0}".format(krw*0.9995))
                upbit.buy_market_order("KRW-BTC", krw*0.9995) 
        else:
            btc = get_balance("KRW-BTC")
            #if btc > 0.00008:
            print("sell : {0}".format(btc*0.9995))
            upbit.sell_market_order("KRW-BTC", btc*0.9995)

        time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(5)

#df.to_excel("dd.xlsx")
