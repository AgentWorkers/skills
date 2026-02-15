---
name: jq
description: 命令行 JSON 处理工具：用于提取、过滤和转换 JSON 数据。
---

# jq

这是一个命令行工具，用于处理 JSON 数据，支持提取、过滤和转换 JSON 数据。

## 安装

**macOS / Linux (Homebrew):**
```bash
brew install jq
```

**所有平台:** 请访问 [jqlang.org/download](https://jqlang.org/download/) 以获取相关软件包、二进制文件和构建说明。

## 使用方法

```bash
jq '[filter]' [file.json]
cat file.json | jq '[filter]'
```

## 快速参考

```bash
.key                    # Get key
.a.b.c                  # Nested access
.[0]                    # First element
.[]                     # Iterate array
.[] | select(.x > 5)    # Filter
{a: .x, b: .y}          # Reshape
. + {new: "val"}        # Add field
del(.key)               # Remove field
length                  # Count
[.[] | .x] | add        # Sum
keys                    # List keys
unique                  # Dedupe array
group_by(.x)            # Group
```

## 命令参数

`-r` 以原始格式输出数据（不添加引号）  
`-c` 以紧凑格式输出数据  
`-s` 将输入数据转换为数组  
`-S` 对输出数据的键进行排序  

## 示例

```bash
jq '.users[].email' data.json          # Extract emails
jq -r '.name // "default"' data.json   # With fallback
jq '.[] | select(.active)' data.json   # Filter active
jq -s 'add' *.json                     # Merge files
jq '.' file.json                       # Pretty-print
```