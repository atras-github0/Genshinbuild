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

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
    if event.message.text[:5] == "build" or event.message.text[:3] == "ビルド":
        if event.message.text[:5] == "build":
            buildflag = True
            if event.message.text[5] == " " or event.message.text[5] == "　":
                try:
                    print(int(event.message.text[6:15]))
                except:
                    print("ERROR")
                else:
                    uid = int(event.message.text[6:15])
                    dict = {"uid":uid,"charaindex":1,"scoretype":3}
                    with open('./argument.json', 'w') as f:
                        json.dump(dict, f, ensure_ascii=False)
                    cwd = os.path.abspath(os.path.dirname(__file__))   
                    subprocess.run(["node", f'{cwd}/getchara.js'])
                    with open('./chara.json') as f:
                        jsn = json.load(f)
                    charaList = jsn["chara"]
                    items = [QuickReplyButton(action=MessageAction(label=f"{chara}", text=f"{chara}")) for chara in charaList]
                    messages = TextSendMessage(text="キャラを選んでね！",
                               quick_reply=QuickReply(items=items))
                    line_bot_api.reply_message(event.reply_token, messages=messages)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="wwwww"))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
