---
name: wakapi-sync
description: 每日Wakapi（兼容WakaTime）统计结果 → 本地CSV文件。获取当天的统计数据，并更新CSV文件中的总计数据、热门项目以及使用频率最高的语言信息。
metadata: {"openclaw": {"requires": {"env": ["WAKAPI_URL", "WAKAPI_API_KEY", "WAKAPI_OUT_DIR"]}, "primaryEnv": "WAKAPI_OUT_DIR"}}
---
# wakapi-sync

将 Wakapi（兼容 WakaTime）的每日统计数据导出到本地的 CSV 文件中。

## 功能说明
- 从 Wakapi 获取当天的统计数据，并更新以下 CSV 文件：
  - `daily-total.csv`（每天 1 行）
  - `daily-top-projects.csv`（每天 N 行）
  - `daily-top-languages.csv`（每天 N 行）

## 系统要求
- Node.js 18+ 版本

## 配置参数（环境变量）
- `WAKAPI_URL`（必需）
  - 例如：`https://wakapi.example.com`
- `WAKAPI_API_KEY`（必需）
  - 你的 Wakapi API 密钥。
- `WAKAPI_OUT_DIR`（必需）
  - CSV 文件的输出目录。
  - 例如：`~/wakapi-data`

可选参数：
- `WAKAPI_TOP_NPROJECTS`（默认值：10）
- `WAKAPI_TOP_N LANGUAGES`（默认值：10）

身份验证：
- 使用 `Authorization: Basic base64(<api_key>)` 进行身份验证（与当前的 Wakapi 设置一致）。

## 使用方法
运行以下命令：

```bash
node scripts/wakapi-daily-summary.mjs
```

## 输出 CSV 文件的结构

### daily-total.csv
列：
- `date`（YYYY-MM-DD）
- `total_seconds`（总耗时）
- `total_hours`（总小时数）
- `projects_count`（项目数量）
- `languages_count`（使用的语言数量）

### daily-top-projects.csv
列：
- `date`（日期）
- `rank`（排名）
- `project`（项目名称）
- `seconds`（耗时）
- `hours`（小时数）
- `percent`（占比）

### daily-top-languages.csv
列：
- `date`（日期）
- `rank`（排名）
- `language`（使用的语言）
- `seconds`（耗时）
- `hours`（小时数）
- `percent`（占比）