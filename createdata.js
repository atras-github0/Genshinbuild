const { EnkaClient } = require("enka-network-api");
const genshindb  = require('./genshinDB.json');
const argument  = require('./argument.json');
const fs = require('fs');
const enka = new EnkaClient();
async function f(uid,charaindex,scoretype){
    let data = (await enka.fetchUser(uid));
    let chara = data.characters[charaindex]
    let charaPr = data.charactersPreview[charaindex]
    let datajson = "{"
    datajson += '"uid" : ' + data.uid + "," + '"input" : 0,"Character": {"Name" : "' + charaPr.characterData.name.get("jp") + '","Const" : ' + chara.unlockedConstellations.length + ', "Level" : '  + charaPr.level + ', "Love" : ' + chara.friendship + ','
    datajson += '"Status": {"HP": ' + Math.round(chara._data.fightPropMap['2000']) + ',"攻撃力" : ' + Math.round(chara._data.fightPropMap['2001']) + ',"防御力" : ' + Math.round(chara._data.fightPropMap['2002']) + ',"元素熟知" : ' + Math.round(chara._data.fightPropMap['28']) + ',"会心率" : ' + Math.round(chara._data.fightPropMap['22'] * 1000) / 10 + ',"会心ダメージ" : ' + Math.round(chara._data.fightPropMap['20'] * 1000) / 10 + ',"元素チャージ効率" : ' + Math.round(chara._data.fightPropMap['23'] * 1000) / 10 + ','
    let elementDMG = 0;
    switch(charaPr.characterData.element.id){
        case 'Fire': elementDMG = '40';break;
        case 'Electric': elementDMG = '41';break;
        case 'Water': elementDMG = '42';break;
        case 'Grass': elementDMG = '43';break;
        case 'Wind': elementDMG = '44';break;
        case 'Rock': elementDMG = '45';break;
        case 'Ice': elementDMG = '46';break;
    }
    datajson += '"' + genshindb[elementDMG] + '" : ' + Math.round(chara._data.fightPropMap[elementDMG] * 1000) / 10 + "},"
    datajson += '"Talent": { "通常" : ' + data._data.avatarInfoList[charaindex].skillLevelMap[charaPr.characterData.normalAttack.id] + ', "スキル" : '+ await data._data.avatarInfoList[charaindex].skillLevelMap[charaPr.characterData.elementalSkill.id] + ', "爆発" : ' + await data._data.avatarInfoList[charaindex].skillLevelMap[charaPr.characterData.elementalBurst.id] + "},"
    datajson += '"Base" : {"HP" : ' + Math.round(chara._data.fightPropMap["1"]) + ', "攻撃力" : ' + Math.round(chara._data.fightPropMap["4"]) + ', "防御力" : ' + Math.round(chara._data.fightPropMap["7"]) + "}}," 
    let weapon = data._data.avatarInfoList[charaindex].equipList[data._data.avatarInfoList[charaindex].equipList.length - 1]
    let weaponR = weapon.weapon.affixMap["1" + weapon.itemId] + 1
    datajson += '"Weapon": {"name": "' + enka.getWeaponById(weapon.itemId).name.get("jp") + '", "Level" : ' + weapon.weapon["level"] + ', "rarelity" : ' + chara.weapon.weaponData.stars + ',"totu" : ' + weaponR + ',"BaseATK" : ' + weapon.flat.weaponStats[0].statValue + ', "Sub" : {"name" : "' + genshindb[weapon.flat.weaponStats[1].appendPropId] + '"' + ', "value" : "' + weapon.flat.weaponStats[1].statValue + '"' + "}},"
    datajson += '"Score" : {"State" : ' + '"' + scoretype + '",'
    let ScoreList = {}
    let Scoretotal = 0
    for(let i = 0;i < 5;i++){
        let scoretemp = 0
        let artifact = chara.artifacts[i]
        if(typeof artifact === 'undefined'){
            scoretemp = 0
        }else{
            for(let j = 0;j < artifact.substats.total.length;j++){
                if(artifact.substats.total[j].id == 'FIGHT_PROP_CRITICAL_HURT'){
                    scoretemp += Math.round(artifact.substats.total[j].value * 1000) / 10
                }
                if(artifact.substats.total[j].id == 'FIGHT_PROP_CRITICAL'){
                    scoretemp += Math.round(artifact.substats.total[j].value * 1000) / 10 * 2
                }
                if(scoretype == "攻撃力" && artifact.substats.total[j].id == 'FIGHT_PROP_ATTACK_PERCENT'){
                    scoretemp += Math.round(artifact.substats.total[j].value * 1000) / 10
                }
                if(scoretype == "元素熟知" && artifact.substats.total[j].id == 'FIGHT_PROP_ELEMENT_MASTERY'){
                    scoretemp += Math.round(artifact.substats.total[j].value / 4 * 10)/10
                }
                if(scoretype == "HP" && artifact.substats.total[j].id == 'FIGHT_PROP_ELEMENT_MASTERY'){
                    scoretemp += Math.round(artifact.substats.total[j].value * 1000)/10
                }
                if(scoretype == "防御力" && artifact.substats.total[j].id == 'FIGHT_PROP_ELEMENT_MASTERY'){
                    scoretemp += Math.round(artifact.substats.total[j].value * 800)/10
                }
                if(scoretype == "元素チャージ効率" && artifact.substats.total[j].id == 'FIGHT_PROP_ELEMENT_MASTERY'){
                    scoretemp += Math.round(artifact.substats.total[j].value * 900)/10
                }
            }
        }
        scoretemp = Math.round(scoretemp * 10) / 10
        console.log(scoretemp)
        if(i == 0){ScoreList["flower"] = scoretemp}
        if(i == 1){ScoreList["wing"] = scoretemp}
        if(i == 2){ScoreList["clock"] = scoretemp}
        if(i == 3){ScoreList["cup"] = scoretemp}
        if(i == 4){ScoreList["crown"] = scoretemp}
        Scoretotal = Math.round((ScoreList["flower"] + ScoreList["wing"] + ScoreList["clock"] + ScoreList["cup"] + ScoreList["crown"]) * 10) /10
    }
    datajson += '"total" : ' + Scoretotal + ',"flower" : ' + ScoreList["flower"] + ',"wing" : ' + ScoreList["wing"] + ',"clock" : ' + ScoreList["clock"] + ',"cup" : ' + ScoreList["cup"] + ',"crown" : ' + ScoreList["crown"] + '},'
    datajson += '"Artifacts": {'
    let parsentList = ["攻撃力パーセンテージ","HPパーセンテージ","防御力パーセンテージ","会心率","会心ダメージ","元素チャージ効率","与える治癒効果","炎元素ダメージ","物理元素ダメージ","水元素ダメージ","氷元素ダメージ","草元素ダメージ","雷元素ダメージ","風元素ダメージ","岩元素ダメージ"]
    for(let k = 0;k < 5;k++){
        let artifact2 = chara.artifacts[k]
        if(k == 0){datajson += '"flower" : {'}
        if(k == 1){datajson += '"wing" : {'}
        if(k == 2){datajson += '"clock" : {'}
        if(k == 3){datajson += '"cup" : {'}
        if(k == 4){datajson += '"crown" : {'}
        if(artifact2 === undefined){}
        else{ 
            datajson += '"type" : "' + artifact2.artifactData.set.name.get("jp") + '",'
            let mainvalue = 0
            let mainname = genshindb[artifact2.mainstat.id]
            if(mainname==parsentList[0] || mainname==parsentList[1]|| mainname==parsentList[2]|| mainname==parsentList[3]|| mainname==parsentList[4]|| mainname==parsentList[5]|| mainname==parsentList[6]|| mainname==parsentList[7]|| mainname==parsentList[8]|| mainname==parsentList[9]|| mainname==parsentList[10]|| mainname==parsentList[11]|| mainname==parsentList[12]|| mainname==parsentList[13]|| mainname==parsentList[14]){
                mainvalue = Math.round(artifact2.mainstat.value * 1000) / 10
            }else{
                mainvalue = artifact2.mainstat.value
            }        
            datajson += '"Level" : ' + (artifact2.level - 1) + ',"rarelity" : ' + artifact2.artifactData.stars + ',"main": {"option" : "' + genshindb[artifact2.mainstat.id] + '","value" : ' + mainvalue + '},'
            datajson += '"sub": ['
            for(let l = 0;l < artifact2.substats.total.length;l++){
                let subvalue = 0
                let subname = genshindb[artifact2.substats.total[l].id]
                if(subname==parsentList[0] || subname==parsentList[1]|| subname==parsentList[2]|| subname==parsentList[3]|| subname==parsentList[4]|| subname==parsentList[5]|| subname==parsentList[6]|| subname==parsentList[7]|| subname==parsentList[8]|| subname==parsentList[9]|| subname==parsentList[10]|| subname==parsentList[11]|| subname==parsentList[12]|| subname==parsentList[13]|| subname==parsentList[14]){
                    subvalue = Math.round(artifact2.substats.total[l].value * 1000) / 10
                }else{
                    subvalue = artifact2.substats.total[l].value
                }
                datajson += '{"option": "' + genshindb[artifact2.substats.total[l].id] + '","value" : ' + subvalue
                if(l == artifact2.substats.total.length -1){datajson += '}'}
                else{datajson += '},'}
            }
            if(k == 4){datajson += "]}"}
            else{datajson += "]},"}
        }
    }
    datajson += '},"元素": "' + charaPr.characterData.element.name.get("jp").at(0) + '"}'
    fs.writeFile("data.json", datajson, (err) => {
        if (err) rej(err);
        if (!err) {
          console.log('JSONファイルを生成しました');
        }
    });
}
let type
if(argument.scoretype == 0){type = "攻撃力"}
if(argument.scoretype == 1){type = "HP"}
if(argument.scoretype == 2){type = "防御力"}
if(argument.scoretype == 3){type = "元素熟知"}
if(argument.scoretype == 4){type = "元素チャージ効率"}
f(argument.uid,argument.charaindex,type)
