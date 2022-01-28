"""
다른 파일들을 위한 모듈.
업비트 API key 및 Slack 토큰을 여기서 기입.

다른 파일들에서 공통적으로 많이 쓰는 함수를 
여기다 저장.
"""
import time
import pyupbit
import datetime
import requests

#업비트 API key 문자열로 전달 
access = "Your access key"
secret = "Your secret key"
#Slack Token 문자열로 전달
myToken = "Your Token"

#이곳에서 로그인하여서 
#개인 정보의 관한 함수들(ex.get_balance())들도 이 모듈로
#전달이 가능하게끔 만듦
upbit = pyupbit.Upbit(access, secret)

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
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


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
   