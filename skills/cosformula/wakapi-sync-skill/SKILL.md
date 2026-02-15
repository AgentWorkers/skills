---
name: wakapi-sync
description: 每日Wakapi（兼容WakaTime）统计结果 → 本地CSV文件。获取当天的统计数据，并更新CSV文件中的总计数据、热门项目以及使用频率最高的语言信息。
metadata: {"openclaw": {"requires": {"env": ["WAKAPI_URL", "WAKAPI_API_KEY", "WAKAPI_OUT_DIR"]}, "primaryEnv": "WAKAPI_OUT_DIR"}}
---

# wakapi-sync

将Wakapi（兼容WakaTime）的每日统计数据导出到本地的CSV文件中。

## 功能概述
- 从Wakapi获取当天的统计数据，并更新以下CSV文件：
  - `daily-total.csv`（每天1行）
  - `daily-top-projects.csv`（每天N行）
  - `daily-top-languages.csv`（每天N行）

## 系统要求
- Node.js 18及以上版本

## 配置参数（环境变量）
- `WAKAPI_URL`（必需）
  - 例如：`https://wakapi.app.cosformula.org`
- `WAKAPI_API_KEY`（必需）
  - 你的Wakapi API密钥。
- `WAKAPI_OUT_DIR`（必需）
  - CSV文件的输出目录。
  - 例如：`/Users/zhaoyiqun/clawd/obsidian-vault/编码统计/wakapi`

可选参数：
- `WAKAPI_TOP_N_ProjectS`（默认值：10）
- `WAKAPI_TOP_N LANGUAGES`（默认值：10）

## 认证方式
- 使用`Authorization: Basic base64(<api_key>)`进行认证（与当前的Wakapi设置一致）。

## 使用方法
运行：

```bash
node scripts/wakapi-daily-summary.mjs
```

## 输出CSV文件的结构

### daily-total.csv
列：
- `date`（YYYY-MM-DD）
- `total_seconds`（总耗时，秒）
- `total_hours`（总耗时，小时）
- `projects_count`（项目数量）
- `languages_count`（使用的语言数量）

### daily-top-projects.csv
列：
- `date`（日期）
- `rank`（排名）
- `project`（项目名称）
- `seconds`（该项目耗时，秒）
- `hours`（该项目耗时，小时）
- `percent`（该项目占总时间的百分比）

### daily-top-languages.csv
列：
- `date`（日期）
- `rank`（排名）
- `language`（使用的语言）
- `seconds`（该语言耗时，秒）
- `hours`（该语言耗时，小时）
- `percent`（该语言占总时间的百分比）