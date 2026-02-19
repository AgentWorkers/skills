---
name: discogs-claw
description: 使用 `curl` 在 Discogs 上搜索黑胶唱片的价格。根据唱片的状态（condition），返回最低价、中间价和最高价的建议。
metadata: {"clawdbot":{"emoji":"💿","requires":{"bins":["jq","curl"]}}}
---
# Discogs Claw

使用 Discogs API 在 Discogs 上搜索黑胶唱片的价格。

## 设置

### 选项 1：环境变量（推荐）

```bash
export DISCOGS_TOKEN="your_discogs_token_here"
```

### 选项 2：配置文件
配置文件位于 `~/.openclaw/credentials/discogs.json` 或 `/data/.openclaw/credentials/discogs.json`。

```json
{
  "DISCOGS_TOKEN": "your_discogs_token_here"
}
```

## 使用方法

### 运行该技能

该技能接受一个包含搜索查询的 JSON 输入。

```bash
# Example search
echo '{"query": "Daft Punk - Random Access Memories"}' | ./scripts/discogs.sh
```

## 示例输出
运行脚本后的示例 JSON 输出如下：

```json
{
  "title": "Daft Punk - Random Access Memories",
  "prices": {
    "low": "25.00 USD",
    "median": "35.00 USD",
    "high": "60.00 USD"
  },
  "marketplace": {
    "num_for_sale": 150,
    "lowest_price": "22.50 USD"
  }
}
```

根据这些数据，代理应输出一个非常客观的响应，仅包含上述信息，忽略关于唱片的进一步历史细节。只需显示唱片标题、艺术家名称和价格信息。响应中不应使用表情符号。

## 所需工具

- `curl`
- `jq`
- Discogs API 令牌（`DISCOGS_TOKEN`）