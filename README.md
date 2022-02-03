## 안녕하세요, 코인 자동매매 프로그램입니다.

---


> [**주의사항**]투자책임은 본인한테 있습니다. 해당 프로그램을 얼마든 참조하셔도 좋지만 설명을 자세히 보고 신중히 선택하세요.

[제 블로그](https://twodf78.github.io/project/coin(0)/)에 가셔서 해당 프로그램 관련하여 더 상세하게 보실 수 있습니다.



## 1.참조

이 프로그램은 조코딩 님의 유튜브 채널과 깃허브 소스,
파이썬을 이용한 비트코인 자동매매 (개정판)의 깃허브 소스를 참조하여
만들었음을 알려드립니다.

**조코딩님**

코인 자동매매 프로그램 유튜브 영상

<https://www.youtube.com/watch?v=5vofEMqMyGk&list=PLU9-uwewPMe3KKFMiIm41D5Nzx_fx2PUJ&index=3>

깃허브 소스

<https://github.com/youtube-jocoding/pyupbit-autotrade>


**파이썬을 이용한 비트코인 자동매매 (개정판)**

<https://github.com/sharebook-kr/book-cryptocurrency>



## 2. 설명

상세한 설명은 [제 블로그](https://twodf78.github.io/project/coin(1)/)의 코인 자동거래 프로그램과 관련 된 포스트들에서 참조하실 수 있습니다.

****



해당 프로그램은 main.py 를 실행시켜서 진행이 됩니다.

그 전에 각 파일의 역할에 대해서 설명을 드리겠습니다.

- ### main.py

  이 파일은 여러 프로그램들을 묶어서 이 파일 하나만 실행시켜 사용자 입장에서 편하게 여러 전략을 골라 쓸 수 있도록 하게 하는 파일입니다. 사용자는 터미널 창에서 이 파일을 실행시키고, 출력이 되는 메세지를 따라서 전략을 고를 수 있고, 코인을 선정할 수 있으며, k값을 지정할 수 있습니다.

- ### setting.py

  이 파일은 사용자가 직접 기입해야 하는 부분이 있습니다. 바로 API key 기입 부분인데, 

  ```python
  #업비트 API key 문자열로 전달 
  access = "Your access key"
  secret = "Your secret key"
  #Slack Token 문자열로 전달
  myToken = "Your Token"
  ```

  위 코드에 상응 하는 위치에 발급 받은 업비트 API key 및 Slack Token 코드를 기입하시면 됩니다. (*큰 따옴표 붙여야 합니다.)

- ### autotradeVolatility.py

  해당 코드는 변동성 돌파 전략을 기반하여 자동매매를 하는 코드입니다. 모듈 형식으로 되어 있기 때문에 직접 실행을 시킬 수는 없습니다. 

  변동성 돌파 전략은 매수목표가에 도달하면 매수를 하고 종가 시점에서 무조건 매도를 하는 전략입니다. 

  매수목표가를 결정하는 수식은 다음과 같습니다.

  > 매수목표가 = 당일 시가 + (전날 고가 - 전날 저가) * K값

  코드로는 다음과 같이 구현되어 있습니다.

  ```python
  df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
  target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
  ```

  > 이 중 k값은 사용자가 지정하는 값으로 0.1 ~ 0.9 사이의 값이 될 수 있습니다. 
  >
  > k값이 0.1로 가까워질 수록 매수목표가가 낮아지기 때문에 매수를 하기 쉬워집니다.
  >
  > 즉, **리스크**가 높아지고 **수익률**이 상대적으로 높아질 것입니다. 
  >
  > k값이 0.9로 가까워질 수록 매수목표가가 높아지기 때문에 매수를 하기 어려워집니다.
  >
  > 즉, **리스크**가 낮아지고 **수익률**이 상대적으로 낮아질 것입니다.

- ### autotradePercentage.py

  해당 코드는 변동성 돌파 전략 + 기존의 가지고 있는 코인일 경우에는 매수목표가를 매수평균가의 몇 퍼센트로 잡는 전략을 기반하였습니다. 또한 매도는 종가 시점에서 하는 것이 아닌 수익률이 5프로가 되었을 경우 무조건 매도를 합니다.

  우선 매수에 관련해서 알려드리겠습니다.

  ```python
  target_price =  np.where(upbit.get_avg_buy_price(coin)!=0,
                           upbit.get_avg_buy_price(coin)*0.8,
                           get_target_price(coin,k))
  ```

  위 코드처럼 매수목표가는 선택된 코인이 보유 중인 경우, 보유 중이지 않는 경우로 나눠집니다.

  전자인 경우는 매수목표가는 매수평균가에서 20프로 떨어졌을 경우고,

  후자인 경우는 변동성 돌파 전략을 따릅니다.

  

- ### autotradeAI.py

  해당 코드는 변동성 돌파 전략 + 인공지능 종가 예측으로 자동매매하는 코드입니다. 

  기본적으로는 변동성 돌파 전략으로 자동매매를 진행을 하는데, 매수 시 조건이 하나 더 붙습니다. 바로 인공지능을 사용하여 종가 시점에서의 가격을 예측하여, 매수 가격이 이 가격보다 높으면 매수를 하지 않는 것입니다. 이 종가 예측 가격은 **predicted_close_price**라는 변수에 저장이 되어 있고, 매수 조건을 보는 코드는 아래와 같습니다.

  ```python
  target_price = get_target_price(coin, k)
  current_price = get_current_price(coin)
  if target_price < current_price and current_price < predicted_close_price:
      #매수 진행하는 코드
  ```

  이 전략의 장점은 autotradePercentage.py에 구현 된 변동성 돌파 전략보다 리스크가 더 낫다는 것입니다. 종가 예측 가격이 완벽하진 않겠지만 정확성을 보입니다. 그렇기에 변동성 돌파 전략의 맹점을 어느정도 타파하고 있습니다. 그 맹점은 시장가가 바로 매수목표가까지 상승을 하여 매수가 된 후 종가 시점까지 하락을 할 때 발생합니다. 

- ### calBestCoinAndK.py

  해당 코드는 main.py의 코인과 k값을 선정하는 부분에서, 사용자가 자동 선정을 고를 시 실행 되는 코드입니다. 

  코인 자동 선정 과정은 다음과 같습니다. 모든 코인에 대해서, 과거 15일 기반의 데이터를 분석하여 수익률이 제일 높았던 코인을 가져옵니다.

  k값 자동 선정 과정은 다음과 같습니다. 선정된 코인에 대해서 0.5~0.9사이의 k값 중의 수익률이 제일 높은 k값으로 선정합니다. 범위가 0.1~0.9가 아닌 범위가 0.5~0.9인 이유가 있습니다. k값이 낮을 경우 수익률이 더 높을 수도 있지만, 리스크가 훨씬 높아지기 때문에 자동 선정일 경우 리스크가 더 낮아야한다는 방향성에 부합하도록 만들었습니다.



## 3. 준비 과정



- anaconda - python 3.8버전 이하 설치

  anaconda가 업데이트 되면서 fbprophet library를 지원하지 않기 시작했습니다. 그래서 어쩔 수 없이 downgrade를 시킨 후 진행을 해야합니다. anaconda를 설치 후 fbprophet library설치가 실패 시 아래와 같이 downgrade를 진행시켜주면 됩니다.

  ```git
  conda create -n downgrade python=3.8 anaconda
    
  conda activate downgrade
  ```

  fbprophet 외에도 pyupbit, schedule 등 라이브러리를 설치해줘야 하는데 콘솔창에서 이렇게 진행해주면 됩니다.

  ```git
  pip install pyupbit
  pip install schedule
  conda install -c conda-forge fbprophet
  ```



## 4. 실행 과정



- main.py 실행

  ```git
  python main.py
  ```

  main.py를 실행합니다. 실행한 후 출력되는 instructions에 따라 코인 자동매매 프로그램을 실행시켜주면 됩니다.

  - 1.  코인 매수/매도 전략 선택

  - 2. 코인 종류 선택 

       - 직접 선택일 경우:

         ```
         print(pyupbit.get_tickers("KRW"))
         ```

         위 코드의 실행 결과:

         ![image-20220201234240137](../images/README/image-20220201234240137.png)

         위 출력 결과 중 하나의 코인을 고르면 됩니다.

         **(KRW-코인약자) 형식으로 쓰셔야 합니다**

       - 자동 선택일 경우:

         과거 데이터 기반으로 수익률이 제일 높은 코인을 가져옵니다.

  - 3. k값 선택

       - 직접 선택일 경우:

         0.1~0.9값 중 하나의 값을 직접 선택하시면 됩니다.

       - 자동 선택일 경우:

         0.5~0.9값 중 하나의 코인에 대해서 최고의 k값이 선정됩니다.



## 5. 상세 세팅 - 커스텀마이징



- ### 코인 수익률 자동 계산시 k값

  현재는 k값을 설정해주지 않고 제일 높은 수익률의 코인을 구할 때, k값을 0.7일 때의 상황으로 상정합니다.

  만약 기본적으로 제일 높은 수익률의 코인을 구할 때 k값이 0.7이 아닌 다른 값을 원한다면, 

  **calBestCoinAndK.py** 의 **get_best_ticker()** 함수 정의 부분에서 k변수 기본값을 변경해주면 됩니다.

  ```python
  def get_best_ticker(k=0.7):
  ```

  이 부분에서 k에 원하시는 다른 값으로 할당해주면 됩니다.

  

- ### 퍼센트 매수/ 매도 전략

  - 매수목표가 설정

    현재는 이 전략에서 매수목표가는 매수평균가의 80%로 설정이 되어있습니다.

    즉 20프로 손실이 나면 추가매수를 하는 것입니다.

    만약 다른 값을 원한다면, **autotradeVolatility.py**의 아래 코드에서 다른 값을 할당해주면 됩니다.

    ```pyt
    target_price =  np.where(upbit.get_avg_buy_price(coin)!=0,
                             upbit.get_avg_buy_price(coin)*0.8,
                             get_target_price(coin,k))
    ```

    위 코드에서 

    upbit.get_avg_buy_price(coin)*0.8 부분을

    upbit.get_avg_buy_price(coin)*0.9 (10프로 손실 시 추가 매수)등 다른 값으로 변경해주면 됩니다.

  - 매도목표가 설정

    현재는 이 전략에서 매도목표가는 매수평균가의 105%로 설정이 되어있습니다.

    즉 5프로 수익이 나면 매도를 하는 것입니다.

    만약 수익률을 변경하고 싶으시면, **autotradeVolatility.py**의 아래 코드에서 다른 값을 할당해주면 됩니다.

    ```python
    #만약 평균매수가의 1.05프로가 현재가보다 낮을 경우(5프로 수익) 매도
    if upbit.get_avg_buy_price(coin)!=0 and upbit.get_avg_buy_price(coin)*1.05 <= current_price:
    ```

    위 코드에서 

    upbit.get_avg_buy_price(coin)*1.05 부분을

    upbit.get_avg_buy_price(coin)*1.1 (10프로 수익 시 매도)등 다른 값으로 변경해주면 됩니다.

    
