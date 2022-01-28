#변동성 돌파 전략
import time
import pyupbit
import datetime
from calBestCoinAndK import *
from setting import *

#함수의 인자들은 기본값이 있음
def autotrade(coin= "KRW-BTC", k= 0.5, coin_self_decided=True, k_self_decided=True):
    print("autotrade start")
    #코인 자동매매 시작하는 알림 SLACK으로 전송
    post_message(myToken,"#crypto", "코인 자동매매 시작 됨")
    # 자동매매 시작 / 무한루프를 통해서~
    while True:
        try:
            now = datetime.datetime.now() #현재시각
            start_time = get_start_time("KRW-BTC") # 09:00
            end_time = start_time + datetime.timedelta(days=1) #다음날 09:00

            #당일09:00-익일08:58
            if start_time < now < end_time - datetime.timedelta(seconds=120): #2분을 빼줌
                #매수목표가
                target_price = get_target_price(coin, k)
                #현재가
                current_price = get_current_price(coin)
       
                if target_price <= current_price: #매수 목표가가 현재가보다 낮으면
                    krw = get_balance("KRW")
                    if krw > 5000:
                        buy_result = upbit.buy_market_order(coin, krw*0.9995) #수수료 0.05프로 고려
                        
                        post_message(myToken,"#crypto", str(coin) + " buy : " +str(buy_result))

            #익일08:58-09:00
            else:
                #coin변수는 어느 시장인지의 정보도 담겨 있음. 잔고 조회 시 "-" 뒷 부분인 코인 이름만 필요
                balance = get_balance(coin.split("-")[1])
                if balance*get_current_price(coin) > 5000: #해당 코인 가지고 있는게 5000원 어치 이상이면
                    sell_result = upbit.sell_market_order(coin, balance*0.9995) #수수료 고려

                    post_message(myToken,"#crypto", str(coin) + " sell : " +str(sell_result))
                #시간을 2분이나 뺀 이유:

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







        