import json
import os
import subprocess
import Generater
#Generater.generation(Generater.read_json('data.json'))
with open('./chara.json',encoding="utf-8") as f:
   jsn = json.load(f)
charaList = jsn["chara"]
print(charaList)
cwd = os.path.abspath(os.path.dirname(__file__))   
subprocess.run(["node", './getchara.js'])