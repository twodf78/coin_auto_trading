#제일 높은 수익률 계산  
from re import T
import pyupbit
import numpy as np
import time
import requests
from pyupbit.quotation_api import get_tickers    

myToken = "Your Token"
def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    #iloc[0]종가는 다음날 시가
    return target_price

def get_best_ticker(k=0.5):
    ticker= pyupbit.get_tickers(fiat="KRW")
    bestc =[0,"NONE",0]
    for t in ticker:
        df = pyupbit.get_ohlcv(t,count = 7)
        time.sleep(0.05)
        df['range'] = (df['high'] - df['low']) * k
        df['target'] = df['open'] + df['range'].shift(1)
        df['ror'] = np.where(df['high'] > df['target'],
                            df['close'] / df['target'],
                            1)

        #cumprod- 누적 곱 계산 => 누적 수익률 
        df['hpr'] = df['ror'].cumprod()

        if (bestc[0] < df.iloc[-1,-1]) :
            bestc = [(df.iloc[-1,-1]), str(t),k]
    
    post_message(myToken,"#crypto", "지금 매수할 코인은 : " + str(bestc[1]) + "\n해당 코인의 수익률은 대략 : " + str(bestc[0]))
    post_message(myToken,"#crypto", "코인의 현재가는 : " + str(get_current_price(bestc[1])) + "\n해당 코인의 목표매수가는 : " +
     str(get_target_price(bestc[1],0.5)))
    return bestc
def get_best_k(coin="KRW-BTC"):
    bestK = 0.5
    interest = 0
    for k in np.arange(0.5, 1.0, 0.1):
        df = pyupbit.get_ohlcv(coin,count = 15)
        df['range'] = (df['high'] - df['low']) * k
        df['target'] = df['open'] + df['range'].shift(1)
        df['ror'] = np.where(df['high'] > df['target'],
                            df['close'] / df['target'],
                            1)

        df['hpr'] = df['ror'].cumprod()
        if (interest <= df.iloc[-1,-1]) :
            interest = df.iloc[-1,-1]
            bestK=k
    post_message(myToken,"#crypto", "지금 매수할 코인은 : " + coin + "\n해당 코인의 수익률은 대략 : " + str(interest))
    post_message(myToken,"#crypto", "코인의 현재가는 : " + str(pyupbit.get_current_price(coin)) + "\n해당 코인의 목표매수가는 : " +
     str(get_target_price(coin,k)))
    return bestK


def bestCoin():
#해당 코인의 수익률 + 제일 수익률이 높은 코인 + k값 구하는 코드
    bestc =[0,'NONE',0]
    for k in np.arange(0.5, 1.0, 0.1): #k는 0.5부터 1.0까지 0.1씩 추가한다 0.5, 0.6, 0.7, 0.8, 0.9
        ticker= get_tickers("KRW") #모든 코인종류를 불러온다
        for t in ticker:
            df = pyupbit.get_ohlcv(t,count = 15) 
            time.sleep(0.05)
            df['range'] = (df['high'] - df['low']) * k
            df['target'] = df['open'] + df['range'].shift(1)
            df['ror'] = np.where(df['high'] > df['target'],
                                df['close'] / df['target'],
                                1)

            #cumprod- 누적 곱 계산 => 누적 수익률 
            df['hpr'] = df['ror'].cumprod()
            
            if (bestc[0] < df.iloc[-1,-1]) :
                bestc = [(df.iloc[-1,-1]), str(t),k]
           
    return bestc
