---
name: json-modifier
description: 安全地应用结构化的 JSON 修补程序（RFC 6902）到文件中。当您需要更新配置文件、`package.json` 或内存中的 JSON 数据时，可以使用此技能，而无需重写整个文件或使用不稳定的正则表达式。
---
# JSON Modifier

这是一个用于使用 [RFC 6902 JSON Patch](https://jsonpatch.com/) 格式修改 JSON 文件的工具。支持精确地添加、删除、替换、移动、复制以及验证 JSON 数据结构。

## 使用方法

```bash
# Modify a file in place
node skills/json-modifier/index.js --file path/to/config.json --patch '[{"op": "replace", "path": "/key", "value": "new_value"}]'

# Modify and save to a new file
node skills/json-modifier/index.js --file input.json --patch '[...]' --out output.json

# Use a patch file
node skills/json-modifier/index.js --file input.json --patch-file patches/update.json
```

## 修补格式（RFC 6902）

修补操作必须是一个包含多个操作对象的 JSON 数组。

### 示例

**替换一个值：**
```json
[
  { "op": "replace", "path": "/version", "value": "2.0.0" }
]
```

**添加一个新键：**
```json
[
  { "op": "add", "path": "/features/new_feature", "value": true }
]
```

**删除一个键：**
```json
[
  { "op": "remove", "path": "/deprecated_key" }
]
```

**向数组中追加元素：**
```json
[
  { "op": "add", "path": "/list/-", "value": "item" }
]
```

## 安全性

- 在应用修补操作之前，会先验证修补内容是否与原始 JSON 文件一致。
- 采用原子性写入方式（先将数据写入临时文件，再重命名原始文件）。
- 保留原有的缩进格式（默认为两个空格）。