# 🐾 社交研究（Ravens）——人们都在说什么？

> 由 Odin's Eye Enterprises 提供 — 古老的智慧，现代的智能。

这是一个分层式的 X/Twitter 研究工具，通过“乌鸦”（ravens）收集信息并返回相关情报。

## 功能介绍

1. **第一层** — 使用 FxTwitter API（免费、快速、可获取公开推文）
2. **第二层** — 作为备用方案，通过网页搜索扩大信息覆盖范围
3. **第三层** — 在必要时使用浏览器抓取（作为最后手段，可获取最完整的信息）
4. **简报** — 汇总研究结果并生成报告

## 触发语句

- “人们对……有什么看法？”
- “关于……的社交研究”
- “发送‘乌鸦’去收集信息”
- “最近有什么热门话题？”

## 使用方法

```bash
# Research a topic
python social_research.py "OpenAI GPT-5 reactions"

# Research with specific tier
python social_research.py "AI agents" --tier 1

# Get cached briefing
python social_research.py --briefing "topic"
```

## 相关文件

- `social_research.py` — 主要研究引擎
- `fxtwitter.py` — FxTwitter API 客户端
- `.cache/` — 缓存结果（自动管理）
- `.briefings/` — 汇总报告

## 系统要求

- Python 3.10 或更高版本
- 第一层（使用 FxTwitter API）无需 API 密钥（免费）
- 第二层支持通过代理工具进行网页搜索

## 对代理（Agents）的使用说明

请从技能目录（skill directory）中运行该工具：

```bash
python social_research.py "TOPIC"
```

输出结果将以结构化的方式显示在标准输出（stdout）上。

<!-- 黎明时分，Huginn 和 Muninn 飞翔在天空中……