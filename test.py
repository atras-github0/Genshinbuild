import json
import Generater
#Generater.generation(Generater.read_json('data.json'))
with open('./chara.json',encoding="utf-8") as f:
   jsn = json.load(f)
charaList = jsn["chara"]
print(charaList)