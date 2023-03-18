import asyncio
import subprocess,os,json
import time
import Generater
import getchara
import createdata
import connect
import dropbox
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,QuickReply,QuickReplyButton,MessageAction,PostbackTemplateAction,PostbackAction,PostbackEvent
)
import os

from getchara import get

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
dbx = dropbox.Dropbox('sl.BaxRgS2FgsQFzIvoNxXbBIY4S8p9yNI1Sh9i_UJLFKbnR09B79rfHCoqt9WGyoIn7J5TbfYr3n3r56USVDCyjmm_LpjeJiCghcW7q2cP8PvUqVROcydpJCphqsZR9r8IIsqgmeNQriaP')

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
                    with open('./argument.json', 'w',encoding="utf-8") as f:
                        json.dump(dict, f, ensure_ascii=False)
                    asyncio.run(getchara.get(uid))
                    with open('./chara.json',encoding="utf-8") as f:
                        chara = json.load(f)
                    chara_list = chara["chara"]
                    items = [QuickReplyButton(action=PostbackAction(label=f"{chara}", data=f"{chara},chara")) for chara in chara_list]
                    messages = TextSendMessage(text="キャラを選択してね！",
                               quick_reply=QuickReply(items=items))
                    line_bot_api.push_message(event.source.user_id, messages=messages)
            elif len(event.message.text) == 5:
                line_bot_api
        if event.message.text[:3] == "ビルド":
            if event.message.text[3] == " " or event.message.text[3] == "　":
                line_bot_api

@handler.add(PostbackEvent)
def handle_postback(event):
    postbackdata = str(event.postback.data).split(",")
    if(postbackdata[1] == "chara"):
        line_bot_api.push_message(event.source.user_id,TextSendMessage(text=postbackdata[0]))
        with open('./chara.json',encoding="utf-8") as f:
            chara = json.load(f)
        with open('./argument.json',encoding="utf-8") as f:
            arg = json.load(f)
        dict = {"uid":arg["uid"],"charaindex":chara[postbackdata[0]],"scoretype":3}
        with open('./argument.json', 'w',encoding="utf-8") as f:
            json.dump(dict, f, ensure_ascii=False)
        score_list = ["攻撃力","HP","防御力","元素熟知","元素チャージ効率"]
        items = [QuickReplyButton(action=PostbackAction(label=f"{type}", data=f"{type},score")) for type in score_list]
        messages = TextSendMessage(text="換算方法を選択してね",
                quick_reply=QuickReply(items=items))
        line_bot_api.push_message(event.source.user_id, messages=messages)
    if(postbackdata[1] == "score"):
        line_bot_api.push_message(event.source.user_id,TextSendMessage(text=postbackdata[0]))
        with open('./argument.json',encoding="utf-8") as f:
            arg = json.load(f)
        dict = {"uid":arg["uid"],"charaindex":arg["charaindex"],"scoretype":postbackdata[0]}
        with open('./argument.json', 'w', encoding="utf-8") as f:
            json.dump(dict, f, ensure_ascii=False)
        with open('./argument.json',encoding="utf-8") as f:
            arg = json.load(f)
        asyncio.run(createdata.create(arg["uid"],arg["charaindex"],arg["scoretype"]))
        dbx.files_create_folder('/Images')
        f = open('./Image.png', 'rb')
        dbx.files_upload(f.read(),'/Images/image.jpg')
        f.close()
        setting = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.public)
        link = dbx.sharing_create_shared_link_with_settings(path='/Images/image.jpg', settings=setting)

        # 共有リンク取得
        links = dbx.sharing_list_shared_links(path=path, direct_only=True).links
        if links is not None:
            for link in links:
                url = link.url 
                url = url.replace('www.dropbox','dl.dropboxusercontent').replace('?dl=0','')
                line_bot_api.push_message(event.source.user_id,TextSendMessage(text=url))

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
