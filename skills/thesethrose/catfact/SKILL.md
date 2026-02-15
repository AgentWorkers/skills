---
name: Cat Fact
description: 来自 catfact.ninja 的随机猫咪趣闻及品种信息（免费使用，无需 API 密钥）
read_when:
  - Wanting random cat facts
  - Looking up cat breeds
  - Building fun bot responses
metadata: {"clawdbot":{"emoji":"🐱","requires":{"bins":["curl"]}}}
---

# 猫咪趣闻

这些猫咪趣闻来自 catfact.ninja（无需 API 密钥）。

## 使用方法

```bash
# Get a random cat fact
curl -s "https://catfact.ninja/fact"

# Get a random fact (short)
curl -s "https://catfact.ninja/fact?max_length=100"

# Get cat breeds
curl -s "https://catfact.ninja/breeds?limit=5"
```

## 程序化接口（JSON 格式）

```bash
curl -s "https://catfact.ninja/fact" | jq '.fact'
```

## 一行代码示例

```bash
# Random fact
curl -s "https://catfact.ninja/fact" --header "Accept: application/json" | jq -r '.fact'

# Multiple facts
for i in {1..3}; do curl -s "https://catfact.ninja/fact" --header "Accept: application/json" | jq -r '.fact'; done
```

## API 端点

| 端点          | 描述                        |
|--------------|-----------------------------|
| `GET /fact`     | 随机展示一条猫咪趣闻                |
| `GET /breeds`    | 显示所有猫咪品种列表                |

更多信息：https://catfact.ninja