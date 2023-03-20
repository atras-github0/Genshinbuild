import asyncio
import os,json
import Generater
import getchara
import createdata
import dropbox
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dropbox import DropboxOAuth2FlowNoRedirect
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,QuickReply,QuickReplyButton,MessageAction,PostbackTemplateAction,PostbackAction,PostbackEvent,ImageMessage, ImageSendMessage,ButtonComponent
)

from getchara import get

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
SPREADSHEET_KEY = os.getenv("SPREAD_KEY")

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
dbx = dropbox.Dropbox(oauth2_refresh_token=REFRESH_TOKEN, app_key=APP_KEY, app_secret=APP_SECRET)

scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("genshinbuild-aeaea1bcd7b8.json", scope)
gc = gspread.authorize(creds)

worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

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
    if (event.message.text[:5] == "build") or (event.message.text[:3] == "ビルド"):
        if event.message.text[:5] == "build":
            checkUID(event,5)
        if event.message.text[:3] == "ビルド":
            checkUID(event,3)
    else:checkUID(event,0)

@handler.add(PostbackEvent)
def handle_postback(event):
    postbackdata = str(event.postback.data).split(",")
    if(postbackdata[1] == "chara"):
        #line_bot_api.push_message(event.source.user_id,TextSendMessage(text=postbackdata[0]))
        with open('./chara.json',encoding="utf-8") as f:
            chara = json.load(f)
        with open('./argument.json',encoding="utf-8") as f:
            arg = json.load(f)
        dict = {"uid":arg["uid"],"charaindex":chara[postbackdata[0]],"scoretype":3}
        with open('./argument.json', 'w',encoding="utf-8") as f:
            json.dump(dict, f, ensure_ascii=False)
        with open('./argument.json',encoding="utf-8") as f:
            arg = json.load(f)
        #line_bot_api.push_message(event.source.user_id,TextSendMessage(text=arg['charaindex']))
        score_list = ["攻撃力","HP","防御力","元素熟知","元素チャージ効率"]
        items = [QuickReplyButton(action=PostbackAction(label=f"{type}", data=f"{type},score")) for type in score_list]
        messages = TextSendMessage(text="換算方法を選択してね",quick_reply=QuickReply(items=items))
        line_bot_api.push_message(event.source.user_id, messages=messages)

    if(postbackdata[1] == "score"):
        with open('./argument.json',encoding="utf-8") as f:
            arg = json.load(f)
        dict = {"uid":arg["uid"],"charaindex":arg["charaindex"],"scoretype":postbackdata[0]}
        with open('./argument.json', 'w', encoding="utf-8") as f:
            json.dump(dict, f, ensure_ascii=False)
        with open('./argument.json',encoding="utf-8") as f:
            arg = json.load(f)
        asyncio.run(createdata.create(arg["uid"],arg["charaindex"],arg["scoretype"]))
        with open('./data.json',encoding="utf-8") as f:
            data = json.load(f)
        #line_bot_api.push_message(event.source.user_id,TextSendMessage(text='30秒くらいかかるからちょっとまってね！'))

        Generater.generation(Generater.read_json("data.json"))

        cwd = os.path.abspath(os.path.dirname(__file__))
        computer_path= f"{cwd}/Image.png"
        dropbox_path=f"/Images/Image{event.source.user_id}.jpg"

        computer_path2= f"{cwd}/ImagePr.png"
        dropbox_path2=f"/Images/ImagePr{event.source.user_id}.jpg"

        dbx.files_upload(open(computer_path, "rb").read(), dropbox_path)
        dbx.files_upload(open(computer_path2, "rb").read(), dropbox_path2)

        url = getShereLink(dropbox_path)
        url2 = getShereLink(dropbox_path2)

        line_bot_api.push_message(event.source.user_id,ImageSendMessage(original_content_url=url,preview_image_url=url2))
        #continue_list = ["他のキャラで続ける","終わる"]
        #items = [QuickReplyButton(action=PostbackAction(label=f"{cont}", data=f"{cont},continue")) for cont in continue_list]
        #messages = TextSendMessage(text="続ける？",quick_reply=QuickReply(items=items))
        #line_bot_api.push_message(event.source.user_id, messages=messages)
    if(postbackdata[1] == "continue"):
        if postbackdata[0] == "他のキャラで続ける":
            id = event.source.user_id
            idlist = worksheet.col_values(1)
            if id in idlist:
                index = idlist.index(id)
                uid = int(worksheet.cell(index + 1, 2).value)
                asyncio.run(getchara.get(uid))
                with open('./chara.json',encoding="utf-8") as f:
                   chara = json.load(f)
                chara_list = chara["chara"]
                items = [QuickReplyButton(action=PostbackAction(label=f"{chara}", data=f"{chara},chara")) for chara in chara_list]
                messages = TextSendMessage(text="キャラを選択してね！",quick_reply=QuickReply(items=items))
                line_bot_api.push_message(event.source.user_id, messages=messages)
        elif postbackdata[0] == "終わる":
            return
def getShereLink(dropboxpath):
    setting = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.public)
    link = dbx.sharing_create_shared_link_with_settings(path=dropboxpath, settings=setting)

    # 共有リンク取得
    links = dbx.sharing_list_shared_links(path=dropboxpath, direct_only=True).links
    url : str = ""
    if links is not None:
        for link in links:
            url = link.url 
            url = url.replace('www.dropbox','dl.dropboxusercontent').replace('?dl=0','')
    return url

def checkUID(event,index):
    text:str = event.message.text.replace(" ","").replace("　","")
    if len(event.message.text) == index:
        id = event.source.user_id
        idlist = worksheet.col_values(1)
        if id in idlist:
            index = idlist.index(id)
            uid = int(worksheet.cell(index + 1, 2).value)
            dict = {"uid":uid,"charaindex":1,"scoretype":3}
            with open('./argument.json', 'w',encoding="utf-8") as f:
                json.dump(dict, f, ensure_ascii=False)
            asyncio.run(getchara.get(uid))
            with open('./chara.json',encoding="utf-8") as f:
                chara = json.load(f)
            chara_list = chara["chara"]
            items = [QuickReplyButton(action=PostbackAction(label=f"{chara}", data=f"{chara},chara")) for chara in chara_list]
            messages = TextSendMessage(text="キャラを選択してね！",quick_reply=QuickReply(items=items))
            line_bot_api.push_message(event.source.user_id, messages=messages)
    else:
        try:
            print(int(text[index:index + 9]))
        except:
            print("ERROR")
        else:    
            uid = int(text[index:index + 9])
            id = event.source.user_id
            idlist = worksheet.col_values(1)
            if id in idlist:
                index = idlist.index(id)
                worksheet.update(f'B{index + 1}',str(uid))
            else:
                items = [id, uid]
                worksheet.append_row(items)
            dict = {"uid":uid,"charaindex":1,"scoretype":3}
            with open('./argument.json', 'w',encoding="utf-8") as f:
                json.dump(dict, f, ensure_ascii=False)
            asyncio.run(getchara.get(uid))
            with open('./chara.json',encoding="utf-8") as f:
                chara = json.load(f)
            chara_list = chara["chara"]
            items = [QuickReplyButton(action=PostbackAction(label=f"{chara}", data=f"{chara},chara")) for chara in chara_list]
            messages = TextSendMessage(text="キャラを選択してね！",quick_reply=QuickReply(items=items))
            line_bot_api.push_message(event.source.user_id, messages=messages)

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

