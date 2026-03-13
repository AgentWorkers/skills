---
name: openclaw-oura
description: >
  **Oura Ring 数据源（适用于 OpenClaw，一级支持）**  
  该数据源用于通过 Oura 的个人访问令牌（Personal Access Token）连接 Oura 账户，获取用户的相关数据（如睡眠状态、设备可用性、活动记录），并将这些数据转换为结构稳定的 JSON 格式，以便后续在 Wellness 平台中使用。同时，该数据源还会为任何聊天频道生成简短的摘要信息。
---
# Oura（个人访问令牌）

这是一个用于获取Oura数据的源技能。它会从Oura获取数据，并输出格式化的每日JSON数据以及便于人类阅读的摘要。该技能不会硬编码数据输出的目标渠道。

## 配置

**必需的环境变量：**
- `OURA_ACCESS_TOKEN`

**可选的环境变量：**
- `OURA_TZ`（默认值：`Asia/Shanghai`）

## 获取并格式化当天的数据

```bash
python3 scripts/oura_fetch_daily.py --date today --out /tmp/oura_raw_today.json
python3 scripts/oura_normalize_daily.py /tmp/oura_raw_today.json --out /tmp/oura_today.json
python3 scripts/oura_render.py /tmp/oura_today.json --format markdown --channel generic
```

## 注意事项：

- API参考文档：`references/oura_api.md`
- 输出数据格式：`references/output_schema.md`