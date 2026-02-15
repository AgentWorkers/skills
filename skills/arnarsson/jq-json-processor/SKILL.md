---
name: jq-json-processor
description: 使用 `jq`（一个轻量级且灵活的命令行 JSON 处理工具）来处理、过滤和转换 JSON 数据。
homepage: https://jqlang.github.io/jq/
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["jq"]},"install":[{"id":"brew","kind":"brew","formula":"jq","bins":["jq"],"label":"Install jq (brew)"},{"id":"apt","kind":"apt","package":"jq","bins":["jq"],"label":"Install jq (apt)"}]}}
---

# jq JSON 处理器

使用 jq 对 JSON 数据进行处理、过滤和转换。

## 快速示例

### 基本过滤
```bash
# Extract a field
echo '{"name":"Alice","age":30}' | jq '.name'
# Output: "Alice"

# Multiple fields
echo '{"name":"Alice","age":30}' | jq '{name: .name, age: .age}'

# Array indexing
echo '[1,2,3,4,5]' | jq '.[2]'
# Output: 3
```

### 处理数组
```bash
# Map over array
echo '[{"name":"Alice"},{"name":"Bob"}]' | jq '.[].name'
# Output: "Alice" "Bob"

# Filter array
echo '[1,2,3,4,5]' | jq 'map(select(. > 2))'
# Output: [3,4,5]

# Length
echo '[1,2,3]' | jq 'length'
# Output: 3
```

### 常见操作
```bash
# Pretty print JSON
cat file.json | jq '.'

# Compact output
cat file.json | jq -c '.'

# Raw output (no quotes)
echo '{"name":"Alice"}' | jq -r '.name'
# Output: Alice

# Sort keys
echo '{"z":1,"a":2}' | jq -S '.'
```

### 高级过滤
```bash
# Select with conditions
jq '[.[] | select(.age > 25)]' people.json

# Group by
jq 'group_by(.category)' items.json

# Reduce
echo '[1,2,3,4,5]' | jq 'reduce .[] as $item (0; . + $item)'
# Output: 15
```

### 处理文件
```bash
# Read from file
jq '.users[0].name' users.json

# Multiple files
jq -s '.[0] * .[1]' file1.json file2.json

# Modify and save
jq '.version = "2.0"' package.json > package.json.tmp && mv package.json.tmp package.json
```

## 常见用例

**从 API 响应中提取特定字段：**
```bash
curl -s https://api.github.com/users/octocat | jq '{name: .name, repos: .public_repos, followers: .followers}'
```

**转换类似 CSV 的数据：**
```bash
jq -r '.[] | [.name, .email, .age] | @csv' users.json
```

**调试 API 响应：**
```bash
curl -s https://api.example.com/data | jq '.'
```

## 提示

- 使用 `-r` 以原始字符串格式输出数据（会删除引号）
- 使用 `-c` 以紧凑格式输出数据（单行显示）
- 使用 `-S` 对对象键进行排序
- 使用 `--arg name value` 传递参数
- 连接多个 jq 操作：`jq '.a' | jq '.b'`

## 文档

完整手册：https://jqlang.github.io/jq/manual/
交互式教程：https://jqplay.org/