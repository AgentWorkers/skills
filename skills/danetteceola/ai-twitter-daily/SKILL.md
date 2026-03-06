---
name: ai-twitter-daily
description: 生成来自顶尖AI研究人员和公司的每日AI Twitter报告。当用户请求AI Twitter摘要、每日AI新闻或希望跟踪AI社区讨论时，可以使用该报告。
---
# AI Twitter每日报告

生成全面的每日报告，追踪Twitter/X上的AI研究人员和公司动态。

## 设置

配置所需的环境变量：

```bash
export GROK_API_KEY="your-api-key-here"
export GROK_API_URL="https://api.cheaprouter.club/v1/chat/completions"  # optional
export GROK_MODEL="grok-4.20-beta"  # optional
```

## 使用方法

运行每日报告脚本：

```bash
python3 scripts/daily_report.py
```

## 报告内容涵盖：

- **用户互动**：谁回复了谁、谁转发了谁、谁提到了谁
- **高频被提及的内容**：AI模型、公司、论文、工具、项目、事件
- **热门话题**：通用人工智能（AGI）的发展趋势、开源与闭源技术、安全性与AI的伦理问题、具身化AI、多模态技术、新架构、智能体的研究进展
- **每日总结**：最新的AI发展动态及讨论热点

## 监控账户

请查看`references/users.txt`文件，获取22位以上顶级AI研究人员和组织的完整名单。

## 输出格式

采用结构化的中文报告形式，包含表格和项目符号列表，便于日常跟踪。