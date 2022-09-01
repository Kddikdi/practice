from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import urllib.request
import json
import scrape as sc
from argparse import ArgumentParser
import sys
app = Flask(__name__)

#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
LINE_CHANNEL_ACCESS_TOKEN = "UgX1CESXPKUlVz6mB/FdPBAqh9wm2g8kAWV8CQUhpdZs2KwKlHQkS6QW1DOW0tqbES27wHgzQ7U0oEtz7lcBGwC5YbQsdSA5lRRU16BGRXsel5pOAVviAIZnoYU286984rg8OEhSYAPEKdEkF6Y9fQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "ee8a66cfbbdaabbfeff91dd06fb1787c"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
  # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
  # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
  # handleの処理を終えればOK
    return 'OK'

## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #ユーザからの検索ワードを取得
    word = event.message.text
    #記事取得関数を呼び出し
    result = sc.getNews(word)
    #応答メッセージ（記事検索結果を送信）
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result))

# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)