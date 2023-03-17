import asyncio
import subprocess,os,json
import time
import Generater
import getchara
import createdata
import connect
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,QuickReply,QuickReplyButton,MessageAction,PostbackTemplateAction,PostbackAction
)
import os

from getchara import get

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

buildflag = False
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
    uid = 0
    line_bot_api.push_message(event.source.user_id,TextSendMessage(text=event.type)) 
    if (event.message.text[:5] == "build") or (event.message.text[:3] == "ビルド"):
        line_bot_api.push_message(event.source.user_id,TextSendMessage(text="aaa"))     
        if event.message.text[:5] == "build":
            if event.message.text[5:6] == " " or event.message.text[5:6] == "　":
                line_bot_api.push_message(event.source.user_id,TextSendMessage(text="bbb"))     
                try:
                    print(int(event.message.text[6:15]))
                except:
                    print("ERROR")
                else:    
                    line_bot_api.push_message(event.source.user_id,TextSendMessage(text="ccc"))           
                    uid = int(event.message.text[6:15])
                    dict = {"uid":uid,"charaindex":1,"scoretype":3}
                    with open('./argument.json', 'w') as f:
                        json.dump(dict, f, ensure_ascii=False)
                    asyncio.run(getchara.get(uid))
                    with open('./chara.json',encoding="utf-8") as f:
                        chara = json.load(f)
                    chara_list = chara["chara"]
                    items = [QuickReplyButton(action=PostbackTemplateAction(label=f"{chara}", data=f"{chara}",type="postback")) for chara in chara_list]
                    messages = TextSendMessage(text="キャラを選択してね！",
                               quick_reply=QuickReply(items=items))
                    line_bot_api.push_message(event.source.user_id, messages=messages)
            elif len(event.message.text) == 5:
                line_bot_api
        if event.message.text[:3] == "ビルド":
            if event.message.text[3] == " " or event.message.text[3] == "　":
                line_bot_api

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

dict = {"uid":830307817,"charaindex":1,"scoretype":3}

#with open('./argument.json', 'w') as f:
   # json.dump(dict, f, ensure_ascii=False)
#cwd = os.path.abspath(os.path.dirname(__file__))   
#subprocess.run(["node", f'{cwd}/createdata.js'])
#Generater.generation(Generater.read_json('data.json'))
