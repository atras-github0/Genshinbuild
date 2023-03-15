const { EnkaClient } = require("enka-network-api");
const enka = new EnkaClient();
const argument  = require('./argument.json');
const fs = require('fs');

async function get(){
    let chara = {}
    let charaList = []
    let charadata = ((await enka.fetchUser(argument["uid"])).characters)
    for(let i = 0;i < charadata.length;i++){
        chara[charadata[i].characterData.name.get("jp")] = i
        charaList.push(charadata[i].characterData.name.get("jp"))
    }
    chara["chara"] = charaList
    fs.writeFile("chara.json", JSON.stringify(chara), (err) => {
        if (err) rej(err);
        if (!err) {
          console.log('JSONファイルを生成しました');
        }
    });
    console.log(chara)
}
get()