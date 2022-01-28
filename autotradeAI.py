#인공지능 종가 예측 전략

import time
import pyupbit
import datetime
import schedule
import requests
from calBestCoinAndK import *
from setting import *
from fbprophet import Prophet


predicted_close_price = 0 #전역변수
def predict_price(ticker):
    """Prophet으로 당일 종가 가격 예측"""
    global predicted_close_price
    df = pyupbit.get_ohlcv(ticker, interval="minute60")
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds','y']]

    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]
    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
    closeValue = closeDf['yhat'].values[0]
    predicted_close_price = closeValue


def autotrade(coin= "KRW-BTC", k= 0.5, coin_self_decided=True, k_self_decided=True):
    
    predict_price(coin)
    #한시간마다 한번씩 예측 값 변동
    schedule.every().hour.do(lambda: predict_price(coin))
    
    print("autotrade start")
    post_message(myToken,"#crypto", "코인 자동매매 시작 됨")

    # 자동매매 시작
    while True:
        try:
            now = datetime.datetime.now()
            start_time = get_start_time("KRW-BTC")
            end_time = start_time + datetime.timedelta(days=1)
            schedule.run_pending()
            
            #당일09:00-익일08:58 
            if start_time < now < end_time - datetime.timedelta(seconds=120):
                target_price = get_target_price(coin, k)
                current_price = get_current_price(coin)
                if target_price < current_price and current_price < predicted_close_price:
                    krw = get_balance("KRW")    
                    if krw > 5000:  
                        buy_result = upbit.buy_market_order(coin, krw*0.9995)
                        #매수 시 메세지 발송
                        post_message(myToken,"#crypto", str(coin) + " buy : " +str(buy_result))
            
            #익일08:58-09:00
            else:
                balance = get_balance(coin.split("-")[1])
                if balance*get_current_price(coin) > 5000: #해당 코인 가지고 있는게 5000원 어치 이상이면
                    upbit.sell_market_order(coin, balance*0.9995) #수수료 고려
                    post_message(myToken,"#crypto", str(coin) + " sell : " +str(sell_result))
                #coin과 k가 둘다 직접 정한 것이 아닐 때
                if not coin_self_decided and not k_self_decided:
                    coin = get_best_ticker()
                    k = get_best_k(coin)
                #k만 직접 정한 것이 아닐 때
                elif not k_self_decided:
                    k = get_best_k(coin)
                #coin만 직접 정한 것이 아닐 때
                elif not coin_self_decided:
                    coin = get_best_coin(k)
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)