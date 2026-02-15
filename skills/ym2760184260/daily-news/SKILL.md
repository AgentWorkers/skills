---
name: daily-news
description: 每天从百度、谷歌等来源获取热门新闻。
metadata:
  openclaw:
    requires:
      bins: ["python"]
      env: ["PYTHONIOENCODING=utf-8"]
    command-dispatch: tool
    command-tool: exec
    command-arg-mode: raw
---

# 每日新闻技能

该技能允许代理通过运行Python脚本来从多个来源（如百度、谷歌趋势等）获取每日头条新闻。

## 使用说明

要获取每日新闻摘要，请执行位于 `{baseDir}/daily_news.py` 的Python脚本。使用以下命令：
```bash
   python "{baseDir}/daily_news.py"
   ```
脚本将按照用户要求的格式输出新闻内容。
请将脚本的输出直接作为最终答案返回。

## 设置要求

请确保已安装所需的Python包：
```bash
pip install -r "{baseDir}/requirements.txt"
```