---
name: json-toolkit
description: 一个多功能工具，适用于 JSON 文件：支持美化输出（pretty-print）、验证数据格式、压缩文件大小（minify）、对 JSON 对象的键进行排序（sort keys），以及通过点表示法（dot notation）进行数据查询。完全无需依赖任何外部库或框架。
triggers:
  - format json
  - pretty print json
  - validate json
  - query json
  - minify json
  - json tool
---
# JSON 工具包

这是一个完全依赖 Python 标准库的 JSON 数据处理工具，无需额外安装任何依赖库。它支持 JSON 文件的验证、格式化、压缩、查询和检查等功能。

## 主要功能

- **美化输出**：支持自定义缩进格式（2 个空格、4 个空格或任意数量的空格）。
- **压缩 JSON 数据**：减少文件大小，便于 API 使用或存储。
- **验证 JSON 数据**：检查 JSON 的语法正确性，并提供结构信息（如数据类型、键的数量、文件大小等）。
- **查询嵌套数据**：使用点表示法（dot notation）访问嵌套结构中的数据，支持数组索引。
- **按键排序**：将对象键按字母顺序排序，以便于差异对比。
- **支持标准输入（stdin）**：可与其他工具结合在 shell 管道中使用。

## 使用示例

- 美化 JSON 文件的输出：
  ```bash
  ```bash
python main.py data.json
```
  ```

- 仅验证 JSON 数据（不输出结果）：
  ```bash
  ```bash
python main.py config.json --validate
# ✓ Valid JSON
#   Type: object (12 keys)
#   Size: 4832 bytes
```
  ```

- 查询嵌套值：
  ```bash
  ```bash
python main.py users.json --query data.users.0.name
# "Alice"
```
  ```

- 为生产环境压缩 JSON 数据：
  ```bash
  ```bash
python main.py config.json --minify -o config.min.json
```
  ```

- 按键排序以便进行差异对比：
  ```bash
  ```bash
python main.py package.json --sort-keys -o package-sorted.json
```
  ```

- 从 curl 命令获取数据并处理：
  ```bash
  ```bash
curl -s https://api.example.com/data | python main.py - --query results.0
```
  ```

## 查询语法

使用点表示法访问嵌套结构。数组索引使用数字表示：

- `name`：顶级键
- `data.users`：嵌套对象键
- `data.users.0`：数组的第一个元素
- `data.users.0.email`：数组第一个元素的字段
- `config.servers.2.host`：深度嵌套的值

## 命令行选项

- `input`：JSON 文件路径（或缺省值 `-` 表示从标准输入读取）
- `-o, --output`：输出文件路径（默认为标准输出）
- `--indent N`：缩进数量（默认值为 2 个空格）
- `--minify`：输出压缩后的 JSON 数据（去除空白字符）
- `--query PATH` 或 `-q PATH`：提取指定路径处的数据
- `--validate`：仅验证 JSON 数据并打印统计信息，不输出结果
- `--sort-keys`：按字母顺序排序对象键
- `--json`：（默认值）始终输出有效的 JSON 数据