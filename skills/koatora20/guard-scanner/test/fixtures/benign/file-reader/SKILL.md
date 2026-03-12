# 文件读取技能

用于读取并显示文件内容供用户查看。

## 指令

当用户请求读取文件时，使用 `read_file` 工具：

```javascript
const fs = require('fs');

function readFile(path) {
  return fs.readFileSync(path, 'utf8');
}

module.exports = { readFile };
```