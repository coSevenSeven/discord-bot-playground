## 使用虛擬環境

[簡介](https://dev.to/codemee/python-xu-ni-huan-jing-venv-nbg)

執行指令安裝

```terminal
python -m venv myenv
```

啟動

```
.\venv\Scripts\Activate
```

關閉

```
deactivate
```

## 建立、安裝套件清單

```
pip freeze > requirements.txt

pip install -r requirements.txt
```

## 安裝套件

```
pip install -U discord.py
```

## discord.py

- 基本設定
  - [client 建立、設定、啟用](https://ithelp.ithome.com.tw/articles/10351677)
  - [Intent BOT 權限](https://ithelp.ithome.com.tw/articles/10352867)
  - [事件監聽器](https://ithelp.ithome.com.tw/articles/10353255)
- 指令撰寫
  - [slash command](https://ithelp.ithome.com.tw/articles/10354641)
  - [右鍵、用戶指令](https://ithelp.ithome.com.tw/articles/10355260)
  - [可以輸入參數的指令](https://ithelp.ithome.com.tw/articles/10355878)
  - [限制指令輸出項目(選項)](https://ithelp.ithome.com.tw/articles/10355878)
- 指令優化
  - [Bot 指令框架](https://ithelp.ithome.com.tw/articles/10357208)
  - [定時任務](https://ithelp.ithome.com.tw/articles/10357775)
- UI
  - [嵌入式內容](https://ithelp.ithome.com.tw/articles/10358431)
  - [按鈕](https://ithelp.ithome.com.tw/articles/10359020)+
  - [下拉式選單](https://ithelp.ithome.com.tw/articles/10359610)
  - [訊息設定](https://ithelp.ithome.com.tw/articles/10360120)
  - [彈窗表單](https://ithelp.ithome.com.tw/articles/10360476)
  - [投票](https://ithelp.ithome.com.tw/articles/10360882)
- DEBUG
  - [日誌 LOG](https://ithelp.ithome.com.tw/articles/10361915)
  - [錯誤處理 (包含任務錯誤)](https://ithelp.ithome.com.tw/articles/10361989)
- Cog Class 功能拆分
  - [Cog 的使用](https://ithelp.ithome.com.tw/articles/10362985)
  - [Extension ( hot-reloading )](https://ithelp.ithome.com.tw/articles/10363117)
- 部屬
  - [Replit (沒有教學內容，因為已經失效)](https://ithelp.ithome.com.tw/articles/10363846)
  - [Render](https://ithelp.ithome.com.tw/articles/10364134)
  - [GCP 01](https://ithelp.ithome.com.tw/articles/10364612)
  - [GCP 02](https://ithelp.ithome.com.tw/articles/10365125)
- 示範
  - [定義需求](https://ithelp.ithome.com.tw/articles/10365542)
  - [專案架構與主程式](https://ithelp.ithome.com.tw/articles/10365964)
  - [功能實作 (上)](https://ithelp.ithome.com.tw/articles/10366618)
  - [功能實作 (下)](https://ithelp.ithome.com.tw/articles/10366975)

## 歷史訊息

[功能實作 (上)](https://ithelp.ithome.com.tw/articles/10366618)

如果想要讀取頻道的歷史訊息，可以使用 `channel.history`。

```py
counter = 0
async for message in channel.history(limit=200):
    if message.author == client.user:
        counter += 1
```

或是

```py
messages = [message async for message in channel.history(limit=123)]
```

## 定時提醒

[\[Day 30\] 開發實戰 (四)：功能實作 (下)](https://ithelp.ithome.com.tw/articles/10366975)
