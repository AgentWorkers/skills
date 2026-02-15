---
name: token-counter
description: 跟踪并分析 OpenClaw 令牌在主会话、定时任务（cron）以及子代理会话中的使用情况，同时记录令牌的类别、客户端、模型和工具相关信息。当用户询问令牌的具体使用去向、需要每日/每周的令牌使用报告、希望深入了解单次会话的详细数据，或者正在规划令牌成本优化方案时，可以使用此功能；此外，该功能还能从日志数据中获取相关证据以支持决策。
---

# 令牌计数器（Token Counter）

## 概述

使用此功能可以从本地 OpenClaw 数据生成令牌使用报告。该工具会解析会话记录（`.jsonl` 文件）、会话元数据以及 Cron 任务定义，并按类别、客户端、工具、模型以及最常用的令牌类型生成使用报告。

## 快速入门

运行命令：

```bash
$OPENCLAW_SKILLS_DIR/token-counter/scripts/token-counter --period 7d
```

## 常用命令

1) 生成基本报告：

```bash
$OPENCLAW_SKILLS_DIR/token-counter/scripts/token-counter --period 7d
```

2) 仅显示选定的详细信息：

```bash
$OPENCLAW_SKILLS_DIR/token-counter/scripts/token-counter \
  --period 1d \
  --breakdown tools,category,client
```

3) 分析单个会话：

```bash
$OPENCLAW_SKILLS_DIR/token-counter/scripts/token-counter \
  --session agent:main:cron:d3d76f7a-7090-41c3-bb19-e2324093f9b1
```

4) 导出 JSON 数据：

```bash
$OPENCLAW_SKILLS_DIR/token-counter/scripts/token-counter \
  --period 30d \
  --format json \
  --output $OPENCLAW_WORKSPACE/token-usage/token-usage-30d.json
```

5) 保存每日数据快照：

```bash
$OPENCLAW_SKILLS_DIR/token-counter/scripts/token-counter \
  --period 1d \
  --save
```

生成的 JSON 数据将保存在以下路径：
`$OPENCLAW_WORKSPACE/token-usage/daily/YYYY-MM-DD.json`

## 默认设置和数据来源

- 会话索引文件：`$OPENCLAW_DATA_DIR/agents/main/sessions/sessions.json`
- 会话记录文件：`$OPENCLAW_DATA_DIR/agents/main/sessions/*.jsonl`
- Cron 任务定义文件：`$OPENCLAW_DATA_DIR/cron/jobs.json`

解析器会读取辅助工具的 `usage` 字段以统计令牌使用情况，并根据工具调用记录来确定令牌的来源。

## 关于令牌来源的说明

- 工具相关令牌的归属是基于启发式的判断：如果一条辅助消息中包含多个工具调用，这些令牌会平均分配到相应的工具调用中。
- 会话的 `totalTokens` 值可能来自会话元数据或会话记录中的令牌使用总和（以较大的值为准）。
- 客户端类型的识别基于规则（`personal`、`bonsai`、`mixed`、`unknown`），识别依据包括路径、域名或电子邮件信息。

## 验证功能

运行命令：

```bash
python3 $OPENCLAW_SKILLS_DIR/skill-creator/scripts/quick_validate.py \
  $OPENCLAW_SKILLS_DIR/token-counter
```

## 参考资料

请参阅：
- `references/classification-rules.md`，了解类别/客户端识别逻辑及关键词映射规则。