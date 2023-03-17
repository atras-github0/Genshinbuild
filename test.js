const fs = require('fs');

fs.writeFile("test.json", "{'test' : 'testdayo'}", (err) => {
    if (err) rej(err);
    if (!err) {
      console.log('JSONファイルを生成しました');
    }
});