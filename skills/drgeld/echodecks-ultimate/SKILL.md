---
name: echodecks-ultimate
description: 这款工具基于人工智能技术，提供卡片管理功能，并具备自动生成播客以及间隔重复学习的功能。
metadata: {"clawdbot":{"requires":{"envs":["ECHODECKS_API_KEY"]}}}
---

# EchoDecks Skill (v1)

该技能可与 EchoDecks 集成，用于管理闪卡、安排学习计划以及利用人工智能生成学习内容。

## 配置要求
使用该技能前，需要设置 `ECHODECKS_API_KEY` 环境变量。

## 工具

### `echodecks_get_decks`
- 列出所有可用的闪卡集或查看特定闪卡集的详细信息。
  - `id`（可选）：要查询的闪卡集的 ID。

### `echodecks_get_due_cards`
- 获取当前需要复习的闪卡。
  - `deck_id`（可选）：按特定闪卡集 ID 过滤需要复习的卡片。

### `echodecks_submit_review`
- 为某张闪卡提交复习任务。
  - `card_id`（必填）：要复习的闪卡的 ID。
  - `quality`（必填）：评分（0-3）：
    - 0：需要重新学习（表示未掌握或忘记）
    - 1：较难
    - 2：中等难度
    - 3：较容易

### `echodecks_generate_cards`
- 使用人工智能根据指定主题或文本内容生成新的闪卡。
  - `deck_id`（必填）：新闪卡所属的闪卡集 ID。
  - `topic`（可选）：用于生成闪卡的简短主题字符串。
  - `text`（可选）：用于生成闪卡的原始文本内容。
  **注意：** 必须提供 `topic` 或 `text` 中的一个。费用：10 个信用点。

### `echodecks_generate_podcast`
- 根据指定的闪卡集生成音频播客摘要或对话内容。
  - `deck_id`（必填）：源闪卡集的 ID。
  - `voice`（可选）：语音偏好（默认：“neutral”）。
  - `type`（可选）：“summary” 或 “conversation”（默认：“summary”）。
  **注意：** 费用：50 个信用点。

### `echodecks_get_podcasts`
- 查找特定闪卡集的现有播客内容。
  - `deck_id`（可选）：按闪卡集 ID 过滤。
  - `id`（可选）：具体的播客 ID。

### `echodecks_get_user_stats`
- 获取当前用户的个人资料和学习统计信息。

## 实现细节
所有工具均基于 `skills/echodecks-v1/echodecks_client.py` 实现。