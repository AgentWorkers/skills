---
name: amplitude
description: "**Amplitude 产品分析工具**：通过 Amplitude API 跟踪事件、分析用户行为、执行群体分析（cohort analysis）、管理用户属性以及查询用户转化路径（funnel data）和用户留存数据（retention data）。该工具帮助您深入了解产品使用情况、衡量功能采纳率（feature adoption rates）并分析用户使用路径（user journeys）。专为 AI 代理（AI agents）设计，仅依赖 Python 标准库（Python stdlib），无任何外部依赖项。适用于产品分析、用户行为追踪、转化路径分析（funnel analysis）和用户群体细分（cohort segmentation）等场景。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "📉", "requires": {"env": ["AMPLITUDE_API_KEY", "AMPLITUDE_SECRET_KEY"]}, "primaryEnv": "AMPLITUDE_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 📉 Amplitude

Amplitude 是一款强大的产品分析工具，支持通过其 API 追踪用户事件、分析用户行为、进行群体分析（cohort analysis）、管理用户属性以及查询用户转化路径（funnel data）和用户留存数据（retention data）。

## 主要功能

- **事件追踪**（Event Tracking）：记录带有属性的用户事件。
- **用户分析**（User Analytics）：统计活跃用户数量、会话数和用户参与度。
- **转化路径分析**（Funnel Analysis）：通过事件序列分析用户转化过程。
- **用户留存分析**（Retention Analysis）：分析用户随时间的留存率。
- **群体管理**（Cohort Management）：创建和管理用户群体。
- **用户属性管理**（User Property Management）：设置和查询用户属性。
- **收入分析**（Revenue Analysis）：跟踪用户生命周期价值（LTV）和平均收入（ARPU）。
- **数据分段**（Data Segmentation）：根据属性和事件进行数据查询。
- **事件细分**（Event Segmentation）：统计事件发生次数及详细分布。
- **仪表盘导出**（Dashboard Export）：导出图表数据。

## 必需参数

| 参数          | 是否必需 | 说明                          |
|--------------|---------|---------------------------------------------|
| `AMPLITUDE_API_KEY` | ✅      | Amplitude 的 API 密钥/令牌                     |
| `AMPLITUDE_SECRET_KEY` | ✅      | 用于数据导出和仪表盘功能的秘密密钥                |

## 快速入门

```bash
# Track an event
python3 {baseDir}/scripts/amplitude.py track '{"user_id":"user123","event_type":"purchase","event_properties":{"amount":29.99}}'
```

```bash
# Track batch events
python3 {baseDir}/scripts/amplitude.py track-batch events.json
```

```bash
# Set user properties
python3 {baseDir}/scripts/amplitude.py identify '{"user_id":"user123","user_properties":{"plan":"pro","company":"Acme"}}'
```

```bash
# Get active user counts
python3 {baseDir}/scripts/amplitude.py active-users --start 2026-01-01 --end 2026-02-01
```

## 命令说明

### `track`  
用于追踪一个事件。  
```bash
python3 {baseDir}/scripts/amplitude.py track '{"user_id":"user123","event_type":"purchase","event_properties":{"amount":29.99}}'
```

### `track-batch`  
批量追踪多个事件。  
```bash
python3 {baseDir}/scripts/amplitude.py track-batch events.json
```

### `identify`  
设置用户属性。  
```bash
python3 {baseDir}/scripts/amplitude.py identify '{"user_id":"user123","user_properties":{"plan":"pro","company":"Acme"}}'
```

### `active-users`  
获取活跃用户数量。  
```bash
python3 {baseDir}/scripts/amplitude.py active-users --start 2026-01-01 --end 2026-02-01
```

### `events`  
获取事件数据。  
```bash
python3 {baseDir}/scripts/amplitude.py events --start 2026-01-01 --end 2026-02-01 --event purchase
```

### `funnel`  
运行转化路径分析。  
```bash
python3 {baseDir}/scripts/amplitude.py funnel '{"events":[{"event_type":"page_view"},{"event_type":"signup"},{"event_type":"purchase"}]}' --start 2026-01-01 --end 2026-02-01
```

### `retention`  
进行用户留存分析。  
```bash
python3 {baseDir}/scripts/amplitude.py retention --start 2026-01-01 --end 2026-02-01
```

### `cohorts`  
列出所有用户群体。  
```bash
python3 {baseDir}/scripts/amplitude.py cohorts
```

### `cohort-get`  
获取特定群体的详细信息。  
```bash
python3 {baseDir}/scripts/amplitude.py cohort-get abc123
```

### `revenue`  
进行收入分析。  
```bash
python3 {baseDir}/scripts/amplitude.py revenue --start 2026-01-01 --end 2026-02-01
```

### `user-search`  
搜索用户信息。  
```bash
python3 {baseDir}/scripts/amplitude.py user-search "user@example.com"
```

### `user-activity`  
获取用户活动记录。  
```bash
python3 {baseDir}/scripts/amplitude.py user-activity user123
```

### `segments`  
根据属性和事件对数据进行分段查询。  
```bash
python3 {baseDir}/scripts/amplitude.py segments --event purchase --group-by platform --start 2026-01-01 --end 2026-02-01
```

## 输出格式

所有命令默认以 JSON 格式输出。若需可读性更强的输出格式，可使用 `--human` 选项。  
```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/amplitude.py track --limit 5

# Human-readable
python3 {baseDir}/scripts/amplitude.py track --limit 5 --human
```

## 脚本参考

| 脚本          | 说明                          |
|--------------|---------------------------------------------|
| `{baseDir}/scripts/amplitude.py` | 主要的命令行工具（CLI），支持所有 Amplitude 操作        |

## 数据存储政策

本工具 **绝不将数据存储在本地**。所有请求均直接发送至 Amplitude API，结果会直接返回到标准输出（stdout），数据始终保存在 Amplitude 服务器上。

## 开发者信息  
---  
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关内容可查看 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
本功能属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的业务配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)