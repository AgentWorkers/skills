---
name: json-repair-kit
description: 通过 Node.js 的解析功能来修复格式错误的 JSON 文件。这种方法可以修复 JSON 文件中的尾随逗号、单引号、未加引号的键以及其他常见的语法错误（例如配置文件或手动编辑的数据文件中的问题）。
---
# JSON 修复工具

这是一个用于修复损坏或格式不正确的 JSON 文件的实用程序。它通过将这些文件解析为 JavaScript 对象，然后再将其序列化为有效的 JSON 格式来修复问题（例如文件末尾有多余的逗号、使用单引号或未加引号的键等问题）。

## 使用方法

```bash
# Repair a file in place (creates .bak backup)
node skills/json-repair-kit/index.js --file path/to/broken.json

# Repair and save to a new file
node skills/json-repair-kit/index.js --file broken.json --out fixed.json

# Scan directory and repair all .json files (recursive)
node skills/json-repair-kit/index.js --dir config/ --recursive
```

## 支持的修复类型：

- **文件末尾的逗号**：`{"a": 1,}` -> `{"a": 1}`
- **单引号**：`{'a': 'b'}` -> `{"a": "b"}`
- **未加引号的键**：`{key: "value"}` -> `{"key": "value"}`
- **注释**：会删除 JavaScript 风格的注释 `//`（如果解析器支持该功能；标准 Node.js 的 `eval` 方法在处理字符串外的行注释时也会删除这些注释）。
- **十六进制/八进制数字**：`0xFF` -> `255`

## 安全性：

- **备份**：在覆盖文件之前会自动创建一个备份文件（除非使用了 `--no-backup` 选项；默认情况下是安全的）。
- **验证**：在写入修复后的 JSON 内容之前，会先验证其是否为有效的 JSON 格式。
- **安全解析环境**：使用 `vm.runInNewContext` 进行解析，确保解析过程无法访问全局变量或系统进程，从而提高安全性（比直接使用 `eval()` 更安全）。