---
name: odds-api-io
description: 您可以使用 Query Odds-API.io 来查询体育赛事、博彩公司以及相应的投注赔率。例如，您可以输入 “Inter 对阵 Arsenal 的赔率是多少？” 或 “获取 Paddy the Baddie 对阵 Gaethje 的赔率”。当您需要调用 Odds-API.io v3 的 API 或解析其返回的数据时，可以使用该服务；不过使用该服务需要提供用户自己的 API 密钥。
---

# Odds-API.io

## 概述
使用 Odds-API.io 可以通过事件 ID 搜索事件并获取赛事赔率。该工具包含一个简单的命令行界面（CLI）辅助工具以及详细的 API 端点参考信息。

## 快速工作流程
1. 通过 `ODDS_API_KEY` 或 `--api-key` 提供 API 密钥（切勿将密钥存储在该工具中）。
2. （如需要）查找相应的运动项目和博彩公司。
3. 搜索事件以获取其 ID。
4. 获取该事件的赔率信息及对应的博彩公司列表。

```bash
# 1) List sports and bookmakers
python3 odds-api-io/scripts/odds_api.py sports
python3 odds-api-io/scripts/odds_api.py bookmakers

# 2) Search for an event
python3 odds-api-io/scripts/odds_api.py search --query "Inter vs Arsenal" --sport football

# 3) Fetch odds for the chosen event ID
python3 odds-api-io/scripts/odds_api.py odds --event-id 123456 --bookmakers "Bet365,Unibet"

# Optional: one-step search + odds
python3 odds-api-io/scripts/odds_api.py matchup --query "Inter vs Arsenal" --sport football --bookmakers "Bet365,Unibet"
```

## 命令行界面（CLI）辅助工具
使用 `scripts/odds_api.py` 进行 API 调用。在子命令前传递全局参数，例如 `--api-key` 和 `--dry-run`。建议在测试时使用 `--dry-run` 选项来预览 API 请求结果（无需输入密钥）。对于 `odds` 或 `matchup` 命令，可以使用 `--summary` 选项以获取简洁的输出格式。

## 参考资料
请查阅 `references/odds-api-reference.md` 文件，其中包含基础 URL、API 端点说明以及响应字段的详细信息。