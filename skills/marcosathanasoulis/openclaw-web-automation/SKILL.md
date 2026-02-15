---
name: openclaw-web-automation-basic
description: 当用户需要对公共网站进行快速、无需凭证的自动化操作（如查看网站摘要、进行关键词搜索或获取简单的页面信息）时，请使用此技能。该技能会运行本地的 OpenClaw 自动化工具包（OpenClaw Automation Kit），并返回结构化的数据结果。
---

# OpenClaw Web Automation（无需凭证）

该技能是执行公共网站自动化任务的最快捷方式。

适用于以下请求：
- “总结 https://www.yahoo.com” 的内容
- “检查 https://example.com 是否提到了价格信息”
- “统计公共页面中‘news’这个词的出现次数”

请勿将此技能用于需要登录的任务，应使用 award/login 流程来完成这些任务。

## 前提条件

- 本地已安装仓库。
- 已安装 Python 环境（执行 `pip install -e .`）。
- 使用此技能无需任何凭证。

## 需要运行的命令

在仓库根目录下执行：

```bash
python skills/openclaw-web-automation-basic/scripts/run_query.py --query "<user request>"
```

脚本会调用 `examples/public_page_check` 脚本，并返回 JSON 格式的结果。

## 结果处理

- 向用户返回简洁的总结信息：
  - 页面标题
  - 关键词
  - 关键词的出现次数
  - 1-3 条重要内容

- 如果查询没有提供 URL，系统将使用默认的 `https://www.yahoo.com` 作为目标页面。
- 如果解析失败，系统会请求用户提供目标 URL 和需要检查的文本。

## 安全性

- 仅适用于公共网站。
- 不会收集任何用户凭证。
- 不提供任何绕过反爬虫机制的方法。