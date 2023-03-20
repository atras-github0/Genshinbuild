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
        datajson = "{"
        datajson += '"uid" : ' + str(data.uid) + "," + '"input" : 0,"Character": {"Name" : "' + charaPr.name + '","Const" : ' + str(chara.constellations_unlocked) + ', "Level" : '  + str(charaPr.level) + ', "Love" : ' + str(chara.friendship_level) + ','
        datajson += '"Status": {"HP": ' + str(chara.stats.FIGHT_PROP_MAX_HP.to_rounded()) + ',"攻撃力" : ' + str(math.floor((chara.stats.FIGHT_PROP_BASE_ATTACK.to_rounded()) * (1 + chara.stats.FIGHT_PROP_ATTACK_PERCENT.value) + chara.stats.FIGHT_PROP_ATTACK.to_rounded())) + ',"防御力" : ' + str(math.floor((chara.stats.FIGHT_PROP_BASE_DEFENSE.to_rounded()) * (1 + chara.stats.FIGHT_PROP_DEFENSE_PERCENT.value) + chara.stats.FIGHT_PROP_DEFENSE.to_rounded())) + ',"元素熟知" : ' + str(chara.stats.FIGHT_PROP_ELEMENT_MASTERY.to_rounded()) + ',"会心率" : ' + str(chara.stats.FIGHT_PROP_CRITICAL.to_percentage()) + ',"会心ダメージ" : ' + str(chara.stats.FIGHT_PROP_CRITICAL_HURT.to_percentage()) + ',"元素チャージ効率" : ' + str(chara.stats.FIGHT_PROP_CHARGE_EFFICIENCY.to_percentage())+ ','
        elementDMG = 0
        elementDMG2 = ""
    if charaPr.element.name == "Pyro":
        elementDMG = '40' 
        elementDMG2 = chara.stats.FIGHT_PROP_FIRE_ADD_HURT.to_percentage()
        element = "炎"
    elif charaPr.element.name == "Electro":
        elementDMG = '41'
        elementDMG2 = chara.stats.FIGHT_PROP_ELEC_ADD_HURT.to_percentage()
        element = "雷"
    elif charaPr.element.name == "Hydro":
        elementDMG = '42'
        elementDMG2 = chara.stats.FIGHT_PROP_WATER_ADD_HURT.to_percentage()
        element = "水"
    elif charaPr.element.name == "Dendro":
        elementDMG = '43'
        elementDMG2 = chara.stats.FIGHT_PROP_GRASS_ADD_HURT.to_percentage()
        element = "草"
    elif charaPr.element.name == "Anemo":
        elementDMG = '44'
        elementDMG2 = chara.stats.FIGHT_PROP_WIND_ADD_HURT.to_percentage()
        element = "風"
    elif charaPr.element.name == "Geo":
        elementDMG = '45'
        elementDMG2 = chara.stats.FIGHT_PROP_ROCK_ADD_HURT.to_percentage()
        element = "岩"
    elif charaPr.element.name == "Cryo":
        elementDMG = '46'
        elementDMG2 = chara.stats.FIGHT_PROP_ICE_ADD_HURT.to_percentage()
        element = "氷"

    datajson += '"' + db[elementDMG] + '" : ' + str(elementDMG2) + "},"
    datajson += '"Talent": { "通常" : ' + str(chara.skills[0].level) + ', "スキル" : '+ str(chara.skills[1].level) + ', "爆発" : ' + str(chara.skills[2].level) + "},"
    datajson += '"Base" : {"HP" : ' + str(chara.stats.BASE_HP.to_rounded()) + ', "攻撃力" : ' + str(chara.stats.FIGHT_PROP_BASE_ATTACK.to_rounded()) + ', "防御力" : ' + str(chara.stats.FIGHT_PROP_BASE_DEFENSE.to_rounded()) + "}}," 
    weapon = chara.equipments[len(chara.equipments) - 1]
    if weapon.detail.substats[0] == None:
        datajson += '"Weapon": {"name": "' + weapon.detail.name + '", "Level" : ' + str(weapon.level) + ', "rarelity" : ' + str(weapon.detail.rarity) + ',"totu" : ' + str(weapon.refinement) + ',"BaseATK" : ' + str(weapon.detail.mainstats.value) + '},'
    else: datajson += '"Weapon": {"name": "' + weapon.detail.name + '", "Level" : ' + str(weapon.level) + ', "rarelity" : ' + str(weapon.detail.rarity) + ',"totu" : ' + str(weapon.refinement) + ',"BaseATK" : ' + str(weapon.detail.mainstats.value) + ', "Sub" : {"name" : "' + db[weapon.detail.substats[0].prop_id] + '"' + ', "value" : ' + str(weapon.detail.substats[0].value) + "}},"
    datajson += '"Score" : {"State" : ' + '"' + scoretype + '",'
    ScoreList = {"flower" : 0,"wing" : 0,"clock" : 0,"cup" : 0,"crown" : 0,}
    Scoretotal = 0
    skipart = 0
    for i in range(5):
        scoretemp = 0
        artifact = chara.equipments[i - skipart].detail
        if (artifact.artifact_type != EquipType.Flower and i == 0) or (artifact.artifact_type != EquipType.Feather and i == 1) or (artifact.artifact_type != EquipType.Sands and i == 2) or (artifact.artifact_type != EquipType.Goblet and i == 3) or (artifact.artifact_type != EquipType.Circlet and i == 4):
            scoretemp = 0
            skipart += 1
        else:
            for j in range(len(artifact.substats)):
                artsub = artifact.substats[j]
                if(artsub.prop_id == 'FIGHT_PROP_CRITICAL_HURT'):
                    scoretemp += artsub.value
                if(artsub.prop_id == 'FIGHT_PROP_CRITICAL'):
                    scoretemp += artsub.value * 2
                if(scoretype == "攻撃力" and artsub.prop_id == 'FIGHT_PROP_ATTACK_PERCENT'):
                    scoretemp += artsub.value
                if(scoretype == "元素熟知" and artsub.prop_id == 'FIGHT_PROP_ELEMENT_MASTERY'):
                    scoretemp += round(artsub.value / 4 * 10)/10
                if(scoretype == "HP" and artsub.prop_id == 'FIGHT_PROP_HP_PERCENT'):
                    scoretemp += artsub.value
                if(scoretype == "防御力" and artsub.prop_id == 'FIGHT_PROP_DEFENSE_PERCENT'):
                    scoretemp += round(artsub.value * 8)/10
                if(scoretype == "元素チャージ効率" and artsub.prop_id == 'FIGHT_PROP_CHARGE_EFFICIENCY'):
                    scoretemp += round(artsub.value * 9)/10
        scoretemp = round(scoretemp * 10) / 10
        if(i == 0):ScoreList["flower"] = scoretemp
        if(i == 1):ScoreList["wing"] = scoretemp
        if(i == 2):ScoreList["clock"] = scoretemp
        if(i == 3):ScoreList["cup"] = scoretemp
        if(i == 4):ScoreList["crown"] = scoretemp
        Scoretotal = round((ScoreList["flower"] + ScoreList["wing"] + ScoreList["clock"] + ScoreList["cup"] + ScoreList["crown"]) * 10) /10
    datajson += '"total" : ' + str(Scoretotal) + ',"flower" : ' + str(ScoreList["flower"]) + ',"wing" : ' + str(ScoreList["wing"]) + ',"clock" : ' + str(ScoreList["clock"]) + ',"cup" : ' + str(ScoreList["cup"]) + ',"crown" : ' + str(ScoreList["crown"]) + '},'
    datajson += '"Artifacts": {'
    parsentList = ["攻撃パーセンテージ","HPパーセンテージ","防御パーセンテージ","会心率","会心ダメージ","元素チャージ効率","与える治癒効果","炎元素ダメージ","物理ダメージ","水元素ダメージ","氷元素ダメージ","草元素ダメージ","雷元素ダメージ","風元素ダメージ","岩元素ダメージ"]
    skipart2 = 0
    for k in range(5):
        artifact = chara.equipments[k - skipart2]
        if (artifact.detail.artifact_type != EquipType.Flower and k == 0) or (artifact.detail.artifact_type != EquipType.Feather and k == 1) or (artifact.detail.artifact_type != EquipType.Sands and k == 2) or (artifact.detail.artifact_type != EquipType.Goblet and k == 3) or (artifact.detail.artifact_type != EquipType.Circlet and k == 4):
            skipart2 += 1
        else: 
            if(k == 0):datajson += '"flower" : {'
            if(k == 1):datajson += '"wing" : {'
            if(k == 2):datajson += '"clock" : {'
            if(k == 3):datajson += '"cup" : {'
            if(k == 4):datajson += '"crown" : {'
            datajson += '"type" : "' + artifact.detail.artifact_name_set + '",'
            mainvalue = 0
            mainname = db[artifact.detail.mainstats.prop_id]
            if(mainname==parsentList[0] or mainname==parsentList[1] or mainname==parsentList[2] or mainname==parsentList[3] or mainname==parsentList[4]or mainname==parsentList[5]or mainname==parsentList[6]or mainname==parsentList[7]or mainname==parsentList[8]or mainname==parsentList[9]or mainname==parsentList[10]or mainname==parsentList[11]or mainname==parsentList[12]or mainname==parsentList[13]or mainname==parsentList[14]):
                mainvalue = artifact.detail.mainstats.value
            else:
                mainvalue = artifact.detail.mainstats.value        
            datajson += '"Level" : ' + str(artifact.level) + ',"rarelity" : ' + str(artifact.detail.rarity) + ',"main": {"option" : "' + artifact.detail.mainstats.name + '","value" : ' + str(mainvalue) + '},'
            datajson += '"sub": ['
            for l in range(len(artifact.detail.substats)):
                subvalue = 0
                subname = db[artifact.detail.substats[l].prop_id]
                if(subname==parsentList[0] or subname==parsentList[1]or subname==parsentList[2]or subname==parsentList[3]or subname==parsentList[4]or subname==parsentList[5]or subname==parsentList[6]or subname==parsentList[7]or subname==parsentList[8]or subname==parsentList[9]or subname==parsentList[10]or subname==parsentList[11]or subname==parsentList[12]or subname==parsentList[13]or subname==parsentList[14]):
                    subvalue = artifact.detail.substats[l].value
                else:
                    subvalue = artifact.detail.substats[l].value
                datajson += '{"option": "' + subname + '","value" : ' + str(subvalue)
                if(l == len(artifact.detail.substats) - 1):datajson += '}'
                else:datajson += '},'
            datajson += "]"
            if(k == 4):datajson += "}"
            else:datajson += "},"
    datajson += "}"
    datajson += ',"元素": "' + element + '"}'

    dict_sample = ast.literal_eval(datajson)
    with open('./data.json', 'w',encoding="utf-8") as f:
        json.dump(dict_sample, f, ensure_ascii=False)
    print(datajson)
