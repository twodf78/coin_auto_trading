#퍼센트 매수/매도 전략
#보유하지 않은 코인은 변동성 돌파 전략 사용
import time
import pyupbit
import datetime
import numpy as np
import requests
from calBestCoinAndK import *
from setting import *

def autotrade(coin= "KRW-BTC", k= 0.5, coin_self_decided=True, k_self_decided=True):
    print("autotrade start")
    post_message(myToken,"#crypto", "코인 자동매매 시작 됨")
    # 자동매매 시작 / 무한루프를 통해서~
    while True:
        try:
            now = datetime.datetime.now() #현재시각
            start_time = get_start_time("KRW-BTC") # 09:00
            end_time = start_time + datetime.timedelta(days=1) #다음날 09:00
         
            #당일09:00-익일08:58 
            if start_time < now < end_time - datetime.timedelta(seconds=120): #120초를 빼줌
                #np.where()을 활용:
                #보유시(매수평균가가 0이 아닐 시) - 매수목표가 == 매수평균가 * 0.8
                #미보유시(매수평균가가 0일 시)    - 매수목표가 == 변동성 돌파 전략
                target_price =  np.where(upbit.get_avg_buy_price(coin)!=0,
                                        upbit.get_avg_buy_price(coin)*0.8,
                                        get_target_price(coin,k))
                #현재 가
                current_price = get_current_price(coin)
                #보유 원화
                krw = get_balance("KRW")

                #매수 금액 - 기존엔 계산을 하였는데 찾아보니 API에서 제공하였음
                #buyed_amount = (upbit.get_avg_buy_price(coin)) * get_balance(coin.split("-")[1]) 
                buyed_amount = upbit.get_amount(coin)
                
                #매수 목표가가 현재가보다 낮으면 매수
                if target_price <= current_price:
                    if krw > 5000:
                        #해당 코인이 보유중이었을 경우, 매수 금액만큼 또 매수
                        if upbit.get_avg_buy_price(coin)!=0:
                            buy_result = upbit.buy_market_order(coin, buyed_amount) #수수료 0.05프로 고려
                            post_message(myToken,"#crypto", "매수 완료. 내용 : " + str(buy_result))
                        #해당 코인 첫 매수일 경우, 보유원화의 8분의 1만큼만 매수
                        else:
                            buy_result = upbit.buy_market_order(coin, krw*1/8)
                            post_message(myToken,"#crypto", "매수 완료. 내용 : " + str(buy_result))

                #만약 평균매수가의 1.05프로가 현재가보다 낮을 경우(5프로 수익) 매도
                if upbit.get_avg_buy_price(coin)!=0 and upbit.get_avg_buy_price(coin)*1.05 <= current_price:
                    sell_result = upbit.sell_market_order(coin, balance*0.9995)
                    post_message(myToken,"#crypto", str(coin) + " sell : " +str(sell_result))
                #매수금액이 모자를 경우 + 매수평균가에서 10프로 이상 떨어졌을 경우 손절:
                if buyed_amount > krw and upbit.get_avg_buy_price(coin)*0.9 >= current_price:
                    sell_result = upbit.sell_market_order(coin, balance*0.9995)
                    post_message(myToken,"#crypto", str(coin) + " sell : " +str(sell_result))
                    

            #익일08:58-09:00
            #여기서는 종가 시점에서 제일 좋은 코인이 뭔지 파악만 함
            #매도는 시점과 상관 없이 매수 평균가에서 5프로 이상 수익이 났을 때만 진행함   
            else:
                #coin과 k가 둘다 직접 정한 것이 아닐 때
                if not coin_self_decided and not k_self_decided:
                    coin = get_best_ticker()
                    k = get_best_k(coin)
                #k만 직접 정하는 것이 아닐 때
                elif not k_self_decided:
                    k = get_best_k(coin)
                #coin만 직접 정하는 것이 아닐 때
                elif not coin_self_decided:
                    coin = get_best_coin(k)
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)