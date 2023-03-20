import ast
import asyncio
import json
import math
from enkanetwork import * 
enka = EnkaNetworkAPI()

with open('./argument.json',encoding="utf-8") as f:
    arg = json.load(f)
assets = Assets(lang="jp")
async def create(uid,charaindex,scoretype):
    async with enka:
        with open('./genshinDB.json',encoding="utf-8") as f:
            db = json.load(f)
        element = ""
        data = await enka.fetch_user_by_uid(uid)
        chara = data.characters[charaindex]
        charaPr = data.player.characters_preview[charaindex]
        print(data.characters[charaindex].stats.FIGHT_PROP_ATTACK_PERCENT)
        print((chara.stats.FIGHT_PROP_DEFENSE.to_rounded()))

asyncio.run(create(830307817,0,"攻撃力"))