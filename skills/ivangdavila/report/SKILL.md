---
name: Report
slug: report
version: 1.0.3
description: 配置自定义的定期报告。用户负责定义数据来源，而 Skill 负责安排报告的生成时间和格式设置。
changelog: Fixed path consistency, declared optional env vars in metadata
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":[],"env":{"optional":["USER_PROVIDED_API_KEYS"]}},"os":["linux","darwin","win32"]}}
---
## 数据存储

```
~/report/
├── memory.md               # Index + preferences
├── {name}/
│   ├── config.md           # Report configuration
│   ├── data.jsonl          # Historical data
│   └── generated/          # Past reports
```

首次使用时执行以下操作：`mkdir -p ~/report`

## 功能范围

该功能：
- ✅ 将报告配置存储在 `~/report/` 目录下
- ✅ 按预定时间生成报告
- ✅ 通过用户配置的渠道发送报告

**用户驱动的模型：**
- 用户定义需要包含的数据
- 用户授权访问所需的数据源
- 如果需要外部数据，用户需提供 API 密钥
- 该功能负责报告的调度和格式化工作

**该功能不执行以下操作：**
- ❌ 未经用户提供的凭据，不会访问任何 API
- ❌ 不会从用户未指定的数据源中提取数据
- ❌ 不会存储用户的凭据（用户通过环境变量提供）

## 环境变量

**无固定要求。** 用户根据需要提供 API 密钥：

```bash
# Example: if user wants Stripe data
export STRIPE_API_KEY="sk_..."

# Example: if user wants GitHub data  
export GITHUB_TOKEN="ghp_..."
```

配置文件中引用环境变量的名称，而非其具体值。

## 发送安全性

外部发送方式（Telegram/Webhook/电子邮件）会将报告内容发送到设备外部。
- 用户需要明确配置每个发送渠道
- 用户需自行负责验证接收方的可靠性
- 报告文件会保存在本地（`~/report/{name}/generated/` 目录下）

## 快速参考

| 任务 | 对应文件 |
|------|------|
| 配置方案 | `schema.md` |
| 输出格式 | `formats.md` |
| 发送选项 | `delivery.md` |

## 核心规则

### 1. 用户定义数据来源
在创建报告时：
1. 用户指定需要跟踪的数据
2. 如果需要使用外部 API，用户需提供相应的凭据
3. 凭据以环境变量的形式存储（仅存储变量名称，不存储具体值）

示例：
```
User: "Weekly report on my Stripe revenue"
Agent: "I'll need Stripe API access. Please set 
        STRIPE_API_KEY in your environment."
User: "Done"
→ Config stored with "source": {"type": "api", "env": "STRIPE_API_KEY"}
```

### 2. 报告配置
配置文件位于 `~/report/{name}/config.md` 中：
```yaml
name: weekly-revenue
schedule: "0 9 * * 1"  # Monday 9am
sources:
  - type: api
    env: STRIPE_API_KEY  # User provides
format: chat
delivery: telegram
```

### 3. 调度
| 频率 | Cron 表达式 | 例子 |
|------|-----------|---------|
| 每日 | `0 9 * * *` | 每天上午 9 点 |
| 每周 | `0 9 * * 1` | 每周一上午 9 点 |
| 每月 | `0 9 1 * *` | 每月 1 日 |
| 按需 | - | 用户请求时生成 |

### 4. 发送渠道
用户通过 `config.md` 文件进行配置：
- `chat` — 通过聊天消息发送
- `telegram` — 发送到 Telegram（用户需提供聊天 ID）
- `file` — 保存到 `~/report/{name}/generated/` 目录
- `email` — 通过用户配置的邮箱发送

### 5. 报告管理
```
"List my reports" → Read ~/report/memory.md
"Pause X report" → Update config
"Run X now" → Generate on-demand
```