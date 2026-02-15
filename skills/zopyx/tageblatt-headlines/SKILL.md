---
name: tageblatt-headlines
description: 从 https://www.tageblatt.de/ 下载每日新闻标题（Schlagzeilen），并将它们存档。当 Master 需要《TAGEBLATT》的头条新闻、希望将这些新闻保存在本地，或者需要一个自动化的工作流程（在每天早上 07:00 自动获取并转发最新头条新闻）时，可以使用此功能。
---

# Tageblatt 头条新闻

## 概述  
该技能包会从 **tageblatt.de** 网站获取首页内容，提取可见的文章标题（`<h2 class="article-heading">`），对其进行处理后以文本或 JSON 格式保存到本地。您可以使用它来进行临时查询（如“立即查看头条新闻”）、每日数据备份或自动接收通知。

## 快速入门  
1. **提取头条新闻**：  
   ```bash
   python3 skills/tageblatt-headlines/scripts/fetch_headlines.py \
     --limit 15 \
     --output data/tageblatt/$(date +%Y-%m-%d)_headlines.txt
   ```  
2. **选择 JSON 格式（如需进一步处理数据）**：  
   ```bash
   python3 skills/tageblatt-headlines/scripts/fetch_headlines.py \
     --format json --output data/tageblatt/$(date +%Y-%m-%d).json
   ```  
3. 脚本执行结果还会被输出到标准输出（STDOUT），非常适合立即通过 Telegram 发送结果。

## 自动化任务（每天 07:00）  
1. **设置 Cronjob（欧洲/柏林时间）**：  
   ```bash
   openclaw cron add <<'JSON'
   {
     "name": "tageblatt-headlines-07",
     "schedule": {
       "kind": "cron",
       "expr": "0 7 * * *",
       "tz": "Europe/Berlin"
     },
     "sessionTarget": "isolated",
     "payload": {
       "kind": "agentTurn",
       "model": "default",
       "message": "Run `python3 skills/tageblatt-headlines/scripts/fetch_headlines.py --limit 15 --output data/tageblatt/$(date +%F)_headlines.txt`. Send Master the list via Telegram (bulleted) and mention where the file was saved."
     }
   }
   JSON
   ```  
2. **添加可选的自动化发送功能**：任务成功运行后，可发送 Telegram 总结信息（参见上面的 Payload 示例）。  
3. **数据存储**：将结果保存到 `data/tageblatt/` 目录中；如需长期保存，请提交相应的归档文件。

## 错误处理与提示：  
- 该脚本仅使用标准库（`urllib`、`re`），无需额外安装依赖包。  
- 如果网站更改了标题的 HTML 结构，请检查 `scripts/fetch_headlines.py` 文件中的正则表达式（`HEADING_PATTERN`）。  
- 遇到网络问题时，脚本会返回退出代码 1；Cronjob 应在下一个周期自动重新运行。  
- 如需获取简短列表（例如前 5 条新闻），请使用 `--limit` 参数进行限制。

## 资源文件  
- `scripts/fetch_headlines.py`：用于下载网页内容并解析头条新闻的脚本（支持文本或 JSON 格式输出，可设置下载数量限制）。