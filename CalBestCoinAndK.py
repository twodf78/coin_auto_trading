"""
코인 및 k값 자동 선정하는 함수들을 
담고 있는 모듈
"""
from re import T
import pyupbit
import numpy as np
import time
import requests
from setting import *

#수익률이 제일 좋은 코인을 선정하는 함수
def get_best_ticker(k=0.7):
    #현재는 원화만 고려
    ticker= pyupbit.get_tickers(fiat="KRW")
    #수익률이 제일 좋은 코인을 담는 변수
    bestC = "KRW-BTC"
    #해당 수익률을 계속 담을 변수
    interest = 0
    for t in ticker:
        df = pyupbit.get_ohlcv(t,count = 7)
        time.sleep(0.08)
        # 범위값 == 전날 고가와 저가의 차이 * k 값
        df['range'] = (df['high'] - df['low']) * k
        # 매수목표가 == 당일 시가 + 범위 값
        # shift(1)을 한 이유는 범위는 전날의 범위고, 시가는 오늘의 시가이기 때문
        df['target'] = df['open'] + df['range'].shift(1)
        #당일 수익률. 
        # 매수가 진행되면(당일 고가 > 당일 타겟), 수익률 == (종가/목표가) == (매도가/ 매수가)
        # 매수가 진행이 안 되면, 수익률 == 1
        df['ror'] = np.where(df['high'] > df['target'],
                            df['close'] / df['target'],
                            1)

        ##cumprod- 누적 곱 계산 => 누적 수익률 
        df['hpr'] = df['ror'].cumprod()

        #df.iloc[-1,-1] == 해당 데이터프레임의 마지막 행 마지막 열,
        #즉 오늘(*마지막 행)의 누적 수익률(*마지막 열)
        if (interest < df.iloc[-1,-1]) :
            #누적 수익률이 더 큰 값이 나올 때마다 초기화
            bestC = t
            interest = df.iloc[-1,-1]
    
    post_message(myToken,"#crypto", "지금 매수할 코인은 : " + bestC + "\n해당 코인의 수익률은 대략 : " + str(interest)
    +"\nk값은 : " + str(k))
    post_message(myToken,"#crypto", "코인의 현재가는 : " + str(pyupbit.get_current_price(bestC)) + "\n해당 코인의 목표매수가는 : " +
     str(get_target_price(bestC,k)))
    return bestC

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
    post_message(myToken,"#crypto", "지금 매수할 코인은 : " + coin + "\n해당 코인의 수익률은 대략 : " + str(interest)
    +"\nk값은 : " + str(bestK))
    post_message(myToken,"#crypto", "코인의 현재가는 : " + str(pyupbit.get_current_price(coin)) + "\n해당 코인의 목표매수가는 : " +
     str(get_target_price(coin,bestK)))

    return bestK
