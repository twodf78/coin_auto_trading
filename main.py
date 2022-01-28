"""
이 파일을 하나만을 실행시키므로써
모든 전략들 중 하나,
코인 직접 선정 / 자동 선정,
k값 직접 선정 / 자동 선정
에 세 가지 선택지를 사용자에게 부여함
전체 프로세스의 시작점
"""

import sys
import time
import autotradePercentage
import autotradeAI
import autotradeVolatility
import pyupbit
from calBestCoinAndK import *
from setting import *
input = sys.stdin.readline

#코인을 직접 골랐는 지 아닌 지를 나타내는 bool 전역변수
coin_self = True
#k값을 직접 골랐는 지 아닌 지를 나타내는 bool 전역변수
k_self = True
#추후 함수 호출 시 필요함

 
msg_strategy = """코인 매수할 방법을 선택하세요.
1. 변동성 돌파 전략 
2. 인공지능 종가 예측 전략 
3. 퍼센트 매수 / 매도 전략
4. 종합 전략
"""
msg_coinDecision = """\n코인을 직접 선택하실 건지, 
자동으로 선정 된 높은 수익률의 코인을 선택하실 건지 결정해주세요.
1. 직접 선택(원화시장만 가능)
2. 자동 선정(시간이 조금 걸립니다. 잠시만 기다려주세요)

"""
msg_whichCoin = """\n어떤 코인을 고르실 건가요?
예시처럼 입력해주세요.
예: KRW-BTC
(원화-코인의 약자)
입력이 올바르지 않거나 해당 코인이 업비트 API에서 제공 되지 않는 경우 재입력해야합니다.

"""
msg_re = "\n다시 처음부터 골라주세요\n"

msg_kDecision = """k값을 결정해주세요.
1. 직접 결정(0.1~0.9까지 선정 가능.)
2. 자동 선정(0.5~0.9까지의 값 중 해당 코인의 가장 수익률 높은 값 선정)

*k값은 높을 수록 수익률이 낮고 리스크가 낮음
"""

msg_whatK = """\n 직접 결정하는 것을 선택하셨습니다.
0.1부터 0.9까지의 숫자 중 직접 입력하세요:

"""

def decideCoin():
    """코인을 어떻게 선택할 것인지에 대한 구현"""
    print(msg_coinDecision)
    ans = input().strip()    
    if ans not in ["1","2"]:
        print(msg_re)
        return 0

    #1인 경우 직접 선택
    if ans == "1":
        print(msg_whichCoin)
        coin = input().strip()
        
        #입력 된 코인이 업비트 API에서 제공하는 코인이 아닌 경우 / 형식에 맞춰 입력된 게 아닌 경우
        if coin not in pyupbit.get_tickers(fiat="KRW"):
            print("\n형식에 맞춰 다시 제대로 입력해주세요.")
            #그대로 재귀 형식으로 다시 함수 호출
            return decideCoin()
    #2인 경우 자동 선택
    elif ans == "2" :
        coin_self = False
        #calBestCoinAndK.py 모듈 참조. 수익률이 제일 높은 코인 뽑아옴
        coin = get_best_ticker()

    #그 외의 경우 일단 리턴. main부분에서 처리
    else:
        print(msg_re)
        return 0
    return coin

def decideK(coin):
    """k값을 어떻게 선택할 것인지에 대한 구현"""
    print(msg_kDecision)
    ans = input().strip()
    if ans not in ["1","2"]:
        print(msg_re)
        return 0
    #1인 경우. 0.1~0.9에서 직접 선정
    if ans == "1":
        print(msg_whatK)
        k = float(input().strip())
        #범위 벗어나면 재귀로 함수 호출 - 다시 입력
        if k<0.1 or k>0.9:
            print("\n범위에서 벗어났습니다 다시 입력해주세요.")
            return decideK(coin)
    #2인 경우. 0.5~0.9에서 제일 큰 수익률 내는 k값 반환
    #0.5부터 시작되는 이유는 자동으로 선정 시 리스크를 최소화하는 방향을 지키기 위함
    elif ans == "2":
        k_self = False
        k = get_best_k(coin)
    return k

while(True):
    print(msg_strategy)
    ans = input().strip()

    if ans not in ["1","2","3"]:
        print(msg_re)
        continue

    #coin결정
    coin = decideCoin()
    #coin, k 결정 시 이상한 값 넣으면 다시 처음부터
    if not coin: continue
    #k결정
    k = decideK(coin)
    if not k: continue

    # 1인 경우, 변동성 돌파 전략
    if ans == "1":
        autotradeVolatility.autotrade(coin, k, coin_self,k_self)
    # 2인 경우, 인공지능 종가 예측 전략(+변동성 돌파 전략)
    elif ans == "2":
        autotradeAI.autotrade(coin, k, coin_self,k_self)
    # 3인 경우, 퍼센트 매수/매도 전략(+변동성 돌파 전략)
    elif ans == "3":
        autotradePercentage.autotrade(coin, k, coin_self,k_self)

