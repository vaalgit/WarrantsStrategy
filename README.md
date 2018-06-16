# WarrantsStrategy

這是一個股市進出場時機通知工具(結合LINE bot)通知。

## 環境需求

-  Python3

## install & launch pipenv

```
pip install pipenv
pipenv sync --dev 
pipenv shell
code . #this for vscode, you can use other IDE
```

## 使用方法

```
python warrants_strategy.py
```

## 系統架構

### Data fetcher
- parsing 1筆/多筆 http://mis.twse.com.tw/stock/fibest.jsp 的stock/Warrants資料
- parsing 警示股的資訊 (API 目前尚未得知，需要自己去try)
- parsing 權證的detail info (行使比例、槓桿、隱波 etc..)
### Strategy Controller
- design mock data
- 策略implement
- 策略模組化/可靈活替換不同策略
### LINE bot dispatcher
- auth research/and implemnt
- design mock data for notification uesd

### 網頁窗口(用來推廣)
- TBD

## 注意事項

TBD

## 附上免責聲明

本人旨在為廣大投資人提供正確可靠之資訊及最好之服務，作為投資研究的參考依據，若因任何資料之不正確或疏漏所衍生之損害或損失，本人將不負法律責任。是否經由本網站使用下載或取得任何資料，應由您自行考量且自負風險，因任何資料之下載而導致您電腦系統之任何損壞或資料流失，您應負完全責任。

## Reference Link
- 股票爬蟲 ref: https://github.com/Asoul/tsrtc

## 聯絡我

有 Bug 麻煩跟我說：

- `chihyuanchou@gmail.com`

最後更新時間：`2018/06/16`
