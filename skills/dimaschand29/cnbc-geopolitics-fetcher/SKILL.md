---
name: cnbc-geopolitics-fetcher
description: 自动化地收集地缘政治情报的代理程序：该程序会从过去24小时内CNBC发布的5篇最热门的新闻文章中提取结构化数据（标题、URL、市场影响以及关键事实），并将这些数据格式化后通过Discord webhook发送出去。适用于高管简报、地缘政治监控或自动化新闻推送流程。
version: 1.0.0
---
# CNBC地缘政治信息采集器

该工具能够从CNBC网站获取专业的地缘政治情报，并通过Discord实时发送给用户。

## 功能概述

- 从CNBC.com网站中提取过去24小时内发布的5篇最热门的地缘政治新闻文章。
- 提取这些文章的结构化情报数据，并以格式化的方式通过Discord webhook发送给指定接收者。

## 配置要求

### Discord Webhook

将Webhook地址存储在`references/config.md`文件中：

```markdown
## Discord Webhook
https://discord.com/api/webhooks/XXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 搜索参数

- **数据来源**：https://www.cnbc.com（世界、财经、地缘政治板块）
- **搜索关键词**：地缘政治、美国外交政策、能源市场、国际冲突
- **时间范围**：过去24小时（文章URL的日期格式需符合该时间范围）
- **输出数量**：精确5篇文章

## 使用方式

### 直接执行

```bash
cd skills/cnbc-geopolitics-fetcher
python scripts/fetch_cnbc_geopolitics.py --config references/config.md --count 5
```

### 使用自定义Webhook

```bash
python scripts/fetch_cnbc_geopolitics.py --webhook <discord_webhook_url> --count 5
```

### 使用输出文件

```bash
python scripts/fetch_cnbc_geopolitics.py --config references/config.md --output briefing.md
```

## 输出格式要求

- **数据要求**：
  - 严格禁止使用任何描述性词汇（如“惊人的”、“令人担忧的”等）
  - 每条信息必须包含标题、文章链接、市场影响以及具体事实。

## 自动化设置

- **Cron任务**：可设置每日自动执行（用于生成每日简报）

### 集成到Heartbeat系统中

将相关配置添加到`HEARTBEAT.md`文件中：

```markdown
- [ ] Fetch CNBC geopolitical briefing (rotate every 2-3 checks)
```

## 文件结构

整个项目的文件结构如下（请根据实际需求调整）：

```
skills/cnbc-geopolitics-fetcher/
├── SKILL.md                 # This file
├── scripts/
│   └── fetch_cnbc_geopolitics.py  # Main execution script
└── references/
    └── config.md            # Webhook and settings
```

## 错误处理机制

- 如果Webhook地址无效，程序将输出错误信息并退出。
- 如果未找到符合条件的文章，将返回“过去24小时内未发现相关文章”。
- 如果在调用Discord API时发生错误，程序会记录错误信息并继续执行。
- 如果网络请求超时，程序将重试一次，然后跳过当前处理步骤。

## 速率限制

- 对CNBC网站的请求频率受到robots.txt文件的约束，每秒最多1次请求。
- 对Discord Webhook的请求频率限制为每分钟30次。

## 安全注意事项

- Webhook地址存储在配置文件中（不会上传到共享代码仓库）。
- 脚本代码中不包含任何认证令牌。
- 由于Discord的限制，输出内容会被截断至2000个字符以内。

## 测试说明

```bash
# Test fetch without posting
python scripts/fetch_cnbc_geopolitics.py --count 3 --output test_briefing.md

# Test with mock webhook (Discord test URL)
python scripts/fetch_cnbc_geopolitics.py --webhook https://discord.com/api/webhooks/test --count 1
```