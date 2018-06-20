from flask import Flask, request, abort
import os
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

line_bot_api = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))


#line_bot_api = LineBotApi("ugkWlLf/jz59t1AX1nO3TZYYO50/4JPxffr+HMAHcROeBU/nh+eATZBpU01V2JkXMQ6VRqRQBx2X77p+DPbLbAL8EAVC0/i54Vnp8Z3r3qtv71c2lnhmEmZFuBJjGADrFKL2oD5HXYz48EjszJ2znwdB04t89/1O/w1cDnyilFU=")
#handler = WebhookHandler("28af6350a16af9b4d33085e00c23a19f")



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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
@app.route("/")
def hello():
    return "Hello World!"



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)
