import asyncio
import math
from enkanetwork import EnkaNetworkAPI
from enkanetwork import Assets
from enkanetwork import*

enka = EnkaNetworkAPI()

async def main():
    async with enka:
         assets = Assets(lang="jp")
         data = await enka.fetch_user_by_uid(830307817)
         chara = data.characters[1]
         print(chara.name)
