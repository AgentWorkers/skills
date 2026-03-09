---
name: tech-weekly-briefing
description: >
  **生成每周科技新闻简报**  
  从6家主要的英文科技媒体（TechCrunch、The Verge、Wired、Ars Technica、MIT Technology Review、The Information）中收集新闻。汇总过去7天的新闻内容，筛选出被多家媒体报道的热门新闻，并生成用户所需语言的精选报告。系统支持每日自动获取RSS源、智能去重、过滤低质量内容以及基于公司的交互式导航功能。适用于用户需要获取科技周报、外媒科技新闻或希望监控多来源验证的英文科技媒体报道的场景。
---
# 技术周刊简报功能

该功能能够从主要的英文科技媒体来源生成结构化的每周科技新闻简报，并提供交互式的导航界面。

## 核心原则

**数据完整性第一**：严禁伪造数据。所有市场数据和新闻必须从真实来源获取后才能用于生成报告。

---

## 媒体来源

### 主要来源（持续更新）

| 媒体 | RSS地址 | 状态 | 数据获取方式 |
|--------|---------|--------|--------------|
| **TechCrunch** | https://techcrunch.com/feed/ | ✅ 持续更新 | urllib |
| **The Verge** | https://www.theverge.com/rss/index.xml | ✅ 持续更新 | urllib |
| **Wired** | https://www.wired.com/feed/rss | ✅ 持续更新 | urllib |
| **Ars Technica** | https://arstechnica.com/feed/ | ✅ 持续更新 | urllib |
| **MIT Technology Review** | https://www.technologyreview.com/feed/ | ✅ 持续更新 | urllib |
| **The Information** | https://www.theinformation.com/feed | ✅ 持续更新 | curl（可绕过403错误） |

### 辅助来源（已配置，待验证）

| 媒体 | 状态 | 备注 |
|--------|--------|------|
| Axios | ⚠️ 已配置 | 需要验证 |
| Bloomberg Tech | ⚠️ 已配置 | 可能需要付费 |
| Reuters Tech | ⚠️ 已配置 | 需要验证 |
| WSJ Tech | ⚠️ 已配置 | 可能需要付费 |

---

## 数据收集工作流程

### 第一步：每日数据获取（每天00:00）

**命令：**
```bash
cd ~/.openclaw/workspace-group/skills/tech-weekly-briefing && python3 scripts/generate-briefing.py daily
```

**功能：**
1. 从所有6个主要来源获取RSS数据
2. 过滤掉低质量内容（如促销信息、体育新闻、生活方式相关内容）
3. 根据标题或URL的相似性删除重复文章
4. 将数据保存到 `data/articles_YYYY-MM-DD.json` 文件中

**Cron任务设置：**
```bash
# Add to crontab
crontab -e

# Add this line for daily fetch at 00:00:
0 0 * * * cd ~/.openclaw/workspace-group/skills/tech-weekly-briefing && python3 scripts/generate-briefing.py daily >> /tmp/tech-weekly-cron.log 2>&1
```

### 第二步：每周报告生成（每周六09:00）

**命令：**
```bash
cd ~/.openclaw/workspace-group/skills/tech-weekly-briefing && python3 scripts/generate-briefing.py weekly
```

**功能：**
1. 加载过去7天的文章
2. 汇总来自不同来源的相似新闻
3. 筛选出热点新闻（至少被2家媒体报道）
4. 按公司名称对新闻进行分类
5. 生成格式化的报告
6. 将报告保存到 `/tmp/tech-weekly-briefing-YYYYMMDD.txt` 文件中

**Cron任务设置：**
```bash
# Every Saturday at 09:00 Beijing Time
0 9 * * 6 cd ~/.openclaw/workspace-group/skills/tech-weekly-briefing && python3 scripts/generate-briefing.py weekly >> /tmp/tech-weekly-cron.log 2>&1
```

---

## 报告格式规范

### 报告结构（共4个部分）

```
📊 外媒科技周报 | YYYY-MM-DD

1️⃣ 概览 (Overview) - Chinese only
2️⃣ 🔥 热点新闻 (Hot News) - English titles, all source links
3️⃣ 🚗 Robotaxi Weekly - All autonomous driving news
4️⃣ [Inline Buttons] - Company categorization
```

### 第一部分：概述

**语言：** 中文
**内容：** 用一段文字总结所有热点新闻
**格式：**
```
📈 概览
本周扫描X家科技媒体，获取X篇文章，聚类为X条独特新闻。
X条热点新闻被≥2家媒体报道：[①news summary; ②news summary; ③news summary; ④news summary]
```

### 第二部分： 🔥 热点新闻

**筛选标准：** 被至少2家媒体报道的新闻
**语言：** 仅显示英文标题（正文不提供中文翻译）
**格式：**
```
🔥 热点新闻（按媒体报道数倒序）

1️⃣ [English Title]
📰 X家：
• Source1: https://link1
• Source2: https://link2
• Source3: https://link3

2️⃣ [English Title]
📰 X家：
• Source1: https://link1
• Source2: https://link2
```

**要求：**
- 所有媒体链接必须可点击
- 按报道次数降序排列
- 最多展示20条热点新闻

### 第三部分：🚗 Robotaxi周刊

**范围：** 所有关于自动驾驶的新闻（不限报道数量）
**关键词：** robotaxi, Waymo, Zoox, Aurora, Cruise, autonomous, self-driving
**格式：**
```
🚗 Robotaxi Weekly / 自动驾驶一周汇总

1. [Title]
   📰 Source | 🔗 https://link

2. [Title]
   📰 Source | 🔗 https://link
```

### 第四部分：内嵌按钮

**布局：**
```
[🔴 OpenAI (X篇)] [🟣 Anthropic (X篇)]
[🔵 Google (X篇)] [🍎 Apple (X篇)]
[🟢 NVIDIA (X篇)] [🚗 Waymo]
[📋 查看全部]
```

**跟踪的公司：**
- OpenAI, Anthropic, Google, Apple, Microsoft, Amazon, Meta
- Tesla, NVIDIA, Waymo, Zoox, Aurora, Cruise
- Nintendo, Sony, Netflix, Block, Robinhood

---

## 内容验证规则

### 规则1：严禁伪造数据

**必须遵守：**
- 在生成报告前执行数据获取命令
- 仅使用实际获取的数据
- 如果命令失败，将缺失的数据标记为 `[获取失败]`

**严禁：**
- 未执行命令就填写价格或百分比
- 不能使用过时的缓存数据（必须带有时间戳）
- 不得猜测或估算任何数值

### 规则2：准确标注来源

**必须遵守：**
- 每条新闻都必须有来源链接
- 多来源的新闻必须列出所有来源
- 使用RSS中的实际URL，而非自动生成的链接

### 规则3：去重

**去重算法：**
1. 标题关键词的Jaccard相似度 ≥ 18%
2. 或者连续3个以上单词完全匹配
3. 保留最早发布的文章

### 规则4：低质量内容过滤

**被过滤的内容：**
- 体育相关内容（如“棒球比赛”、“锦标赛”、“锦标赛”）
- 促销信息（如“促销码”、“折扣”、“优惠券”）
- 购物相关内容（如“床垫品牌”、“KitchenAid促销”、“Norton优惠券”）
- 生活方式相关内容（如“观鸟”、“冲咖啡”、“睡眠优惠”）

**记录：** 所有被过滤的内容都会在每日数据获取过程中被记录下来

---

## 手动操作

### 检查数据收集状态

```bash
# View today's collected articles
ls -la ~/.openclaw/workspace-group/skills/tech-weekly-briefing/data/

# Check article count
python3 -c "import json; data=json.load(open('data/articles_$(date +%Y-%m-%d).json')); print(f'{len(data)} articles today')"
```

### 验证媒体来源

```bash
# Test RSS accessibility
curl -s "https://techcrunch.com/feed/" | head -5
curl -s -A "Mozilla/5.0" "https://www.theinformation.com/feed" | head -5
```

### 强制重新获取数据

```bash
rm ~/.openclaw/workspace-group/skills/tech-weekly-briefing/data/articles_$(date +%Y-%m-%d).json
python3 scripts/generate-briefing.py daily
```

### 生成测试报告

```bash
# Use existing data to generate report
python3 scripts/generate-briefing.py weekly

# View output
cat /tmp/tech-weekly-briefing-$(date +%Y%m%d).txt
```

---

## 故障排除

### 如果The Information返回403错误

**原因：** Python的urllib模块可能被阻止访问，但curl可以正常使用
**解决方法：** 脚本会自动使用`curl`的subprocess模块来获取The Information的数据
**验证方法：**
```bash
curl -s -A "Mozilla/5.0" "https://www.theinformation.com/feed" | head -10
```

### 未找到文章

**检查：**
1. 数据目录：`ls data/`
2. 最后一次数据获取日志：`cat /tmp/tech-weekly-cron.log`
3. RSS源的状态：`blogwatcher blogs`

### 报告中存在重复文章

**原因：** 相似性阈值设置得过低或过高
**调整方法：** 修改`generate-briefing.py`中的`is_same_news()`函数

### 报告中缺少某些公司

**添加公司：**
1. 修改`generate-briefing.py`中的`COMPANY_KEYWORDS`列表
2. 重新运行每周报告生成任务

---

## 文件结构

```
tech-weekly-briefing/
├── SKILL.md                          # This file
├── scripts/
│   ├── generate-briefing.py          # Main script
│   ├── setup-sources.py              # Initial RSS setup
│   └── weekly-cron.sh                # Cron wrapper
├── data/
│   ├── articles_YYYY-MM-DD.json      # Daily fetched articles
│   └── company_data_YYYY-MM-DD.json  # Company categorization
└── assets/
    └── (optional assets)
```

---

## 所需依赖库

- Python 3.10及以上版本
- `blogwatcher`命令行工具（用于监控RSS源）
- `curl`（用于获取The Information的数据）
- 标准库：`json`, `re`, `urllib`, `subprocess`, `datetime`

---

## 关键性能指标

| 指标 | 目标值 |
|--------|--------|
| 每日数据获取成功率 | ≥95%（6个来源） |
| 文章去重准确率 | ≥90% |
| 低质量内容过滤精度 | ≥85% |
| 热点新闻识别率（≥2个来源） | 确保所有多来源的新闻都被收录 |
| 报告生成时间 | <30秒 |

---

## 版本历史

| 版本 | 更新日期 | 主要变更 |
|---------|------|---------|
| 1.0.0 | 2026-03-09 | 首次发布，包含6个来源，支持双语格式，添加公司链接功能 |

---

## 使用示例

### 用户请求：“生成科技周报”

```
1. Check if data exists: ls data/articles_*.json
2. If no data: Run daily fetch first
3. Run: python3 scripts/generate-briefing.py weekly
4. Send report with inline buttons
```

### 用户请求：“查看OpenAI的新闻”

```
1. Load company_data_*.json
2. Filter OpenAI articles
3. Display with bilingual format
```

### 用户请求：“添加新的跟踪公司”

```
1. Edit COMPANY_KEYWORDS in generate-briefing.py
2. Add: "CompanyName": ["keyword1", "keyword2"]
3. Re-run weekly report
```

---

**最后更新时间：** 2026-03-09
**维护者：** OpenClaw Agent
**状态：** 已准备好投入生产使用