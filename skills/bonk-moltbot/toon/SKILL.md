---
name: toon
description: 将 JSON 数据压缩为 TOON 格式，可节省约 40% 的数据量。适用于从 API 获取数据、读取 JSON 文件或处理任何输出结构化数据的场景。只需将输出内容通过 `toon` 命令进行处理：JSON 数据会被压缩，而非 JSON 格式的数据则会保持原样。
---

# TOON 数据压缩工具

将任何命令的输出通过 `toon` 工具进行处理，可以压缩 JSON 数据，从而节省大约 40% 的存储空间。

## 使用方法

```bash
# API responses
curl -s "https://api.example.com/data" | toon

# JSON files  
cat data.json | toon

# Any command - safe on non-JSON (passes through unchanged)
some_command | toon
```

## 安装方法

```bash
# Copy script to PATH
cp scripts/toon ~/.local/bin/
chmod +x ~/.local/bin/toon
```

安装依赖项：`npx`（Node.js）

## 示例

```json
[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]
```
→
```toon
[2]{id,name}:
  1,Alice
  2,Bob
```

## 使用场景

- **在获取 JSON API 数据时** **必须** 使用此工具。
- **在将 JSON 文件读取到程序上下文中时** **必须** 使用此工具。
- 该工具适用于所有类型的输出数据；非 JSON 类型的数据也可以安全地通过该工具进行处理。

## 参考资料

- 格式规范：https://toonformat.dev
- 命令行工具：`@toon-format/cli`