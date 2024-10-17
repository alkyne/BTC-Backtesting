# Bitcoin Moving Average Backtesting
## Research Questions
- RQ1) 대불장의 끝을 판단하는 방법은? 어디가 하락장의 초입인가?
- RQ2) 상승장에서 최고의 수익을 내는 전략은?
- RQ3) 하락장에서도 수익을 내는 전략은?
- RQ4) 긴 하락장을 끝으로 상승장의 시작을 판단하는 방법은? 어디가 상승장의 초입인가?
## File Description
### 1) gather_data.py
- This file is used to gather the data from the Binance API.
- Save the data to csv file.

### 2) data_processing.py
- This file is used to process the data.
- Calculate the MA and save to csv file.

### 3) Back_test.ipynb
- This is the jupyter notebook for the backtesting. 
- It contains the code for the moving average strategy and the backtesting process.

### 4) Back_test_rsi.ipynb
- 현재 RSI가 특정 RSI보다 높으면 매수 안 하고 참는다.
    - 리스크 관리 전략

### 5) Find-bear-signal.ipynb
- 대불장 이후 하락장의 시작은 어떻게 찾을까? (RQ1)

## Telegram
- Result notes
    - https://t.me/btc_backtesting