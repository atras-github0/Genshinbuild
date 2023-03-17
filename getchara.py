import ast
import asyncio
import json
from enkanetwork import * 
enka = EnkaNetworkAPI()

assets = Assets(lang="jp")

async def get(uid):
    async with enka:
        chara = {}
        charaList = []
        charadata = ((await enka.fetch_user_by_uid(uid)).characters)
    for i in range(len(charadata)):
        chara[charadata[i].name] = i
        charaList.append(charadata[i].name)
    chara["chara"] = charaList
    with open('./chara.json', 'w',encoding="utf-8") as f:
        json.dump(chara, f, ensure_ascii=False)
asyncio.run(get())