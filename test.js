const fs = require('fs');

fs.writeFile("test.txt", '{"test" : "testdayo"}', (err) => {
    if (err) rej(err);
    if (!err) {
      console.log('JSONファイルを生成しました');
    }
});