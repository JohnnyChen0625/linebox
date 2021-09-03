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

app = Flask(__name__)

line_bot_api = LineBotApi('a5fgbmbz1//19Uyz4T0r3ZPSuObREXBzD/k1gzFg0QnYkBpaTXQ4PCzwzxpxx0R/Tzbi2E5tcPOmxxjDSvj9seXZF4l/D3J4CiNqYBgTlt5KlXnqFWK+K8WM32TK4x16khtYEt7f++Iv03KEjkaFvQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0ab4fcd0bd6e2374fc3c6c2a8349b034')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '不好意思，您說甚麼'

    if msg in ['hi', 'Hi']:
        r = '您好哇'
    elif msg == '你吃飯了嗎?':
        r = '還沒呦!你呢?'
    elif '訂位' in msg:
        r = '您想訂位是嗎?'
    elif msg == '你是誰':
        r = '我是機器人'


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()