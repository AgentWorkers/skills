---
name: timecamp
description: **使用场景：**  
当用户询问关于 TimeCamp 的时间跟踪、时间记录、任务管理、计时器等功能时使用该文档。该文档会在检测到以下关键词时触发显示：  
“timecamp”、“time entries”、“timer”、“tracking”、“hours”、“timesheet”、“tasks list”、“start timer”、“stop timer”、“activities”、“computer activities”。
metadata:
  openclaw:
    emoji: ⏱️
    requires:
      env: ["TIMECAMP_API_KEY"]
---

# TimeCamp 技能

TimeCamp 提供了两个工具：**CLI**（命令行界面）用于快速执行个人操作（如计时、记录条目等），以及 **Data Pipeline**（数据管道）用于数据分析与报告生成。

## Bootstrap（如果缺失，请先克隆）

在使用这两个工具之前，请执行以下步骤：

1. 询问用户数据仓库（repo）应存放的位置（默认为 `~/utils`，但任何位置均可）。
2. 如果指定位置中不存在数据仓库，请确认是否需要克隆该仓库。

**示例流程及命令：**

```bash
# Ask first:
# "I don't see TimeCamp repos locally. Clone to ~/utils, or use a different location?"

REPOS_DIR=~/utils  # replace if user picked a different path
mkdir -p "$REPOS_DIR"

if [ ! -d "$REPOS_DIR/timecamp-cli/.git" ]; then
  git clone https://github.com/timecamp-org/timecamp-cli.git "$REPOS_DIR/timecamp-cli"
fi

if [ ! -d "$REPOS_DIR/good-enough-timecamp-data-pipeline/.git" ]; then
  git clone https://github.com/timecamp-org/good-enough-timecamp-data-pipeline.git "$REPOS_DIR/good-enough-timecamp-data-pipeline"
fi
```

## 工具 1：TimeCamp CLI（个人操作）

TimeCamp CLI 的路径为 `~/utils/timecamp-cli`，通过 `npm link` 命令全局安装。

| 操作 | 命令            |
|--------|-------------------|
| 查看当前计时器状态 | `timecamp status`     |
| 启动计时器 | `timecamp start --task "项目 A" --note "描述"` |
| 停止计时器 | `timecamp stop`       |
| 查看今日条目 | `timecamp entries`      |
| 按日期查询条目 | `timecamp entries --date 2026-02-04` |
| 查询指定时间范围的条目 | `timecamp entries --from 2026-02-01 --to 2026-02-04` |
| 查看所有用户的条目 | `timecamp entries --from 2026-02-01 --to 2026-02-04 --all-users` |
| 添加条目 | `timecamp add-entry --date 2026-02-04 --start 09:00 --end 10:30 --duration 5400 --task "项目 A" --note "描述"` |
| 更新条目 | `timecamp update-entry --id 101234 --note "已更新" --duration 3600` |
| 删除条目 | `timecamp remove-entry --id 101234` |
| 列出任务 | `timecamp tasks`       |

## 工具 2：Data Pipeline（数据分析与报告）

Data Pipeline 是一个基于 Python 的数据管道工具，位于 `~/utils/good-enough-timecamp-data-pipeline` 目录下。**所有数据分析、报告生成及批量数据获取操作均需使用此工具。**

### 运行命令

```bash
cd ~/utils/good-enough-timecamp-data-pipeline && \
uv run --with-requirements requirements.txt dlt_fetch_timecamp.py \
  --from YYYY-MM-DD --to YYYY-MM-DD \
  --datasets DATASETS \
  --format jsonl \
  --output ~/data/timecamp-data-pipeline
```

### 可用的数据集

| 数据集 | 描述                |
|---------|---------------------|
| `entries` | 包含项目/任务详细信息的条目记录 |
| `tasks` | 显示项目与任务的层级结构（附带导航路径） |
| `computer_activities` | 桌面应用程序的使用情况记录 |
| `users` | 用户信息（包含所属组及启用状态） |
| `application_names` | 应用程序信息表（ID 对应名称及类别） |

### 数据格式：**jsonl**

### 输出结果存储位置

所有输出文件将保存在 `~/data/timecamp-data-pipeline/timecamp/*.jsonl` 目录下。

### 使用示例

```bash
cd ~/utils/good-enough-timecamp-data-pipeline && \
uv run --with-requirements requirements.txt dlt_fetch_timecamp.py \
  --from 2026-02-11 --to 2026-02-14 \
  --datasets entries,users,tasks \
  --format jsonl --output ~/data/timecamp-data-pipeline

cd ~/utils/good-enough-timecamp-data-pipeline && \
uv run --with-requirements requirements.txt dlt_fetch_timecamp.py \
  --from 2026-01-01 --to 2026-02-14 \
  --datasets computer_activities,users,application_names \
  --format jsonl --output ~/data/timecamp-data-pipeline

cd ~/utils/good-enough-timecamp-data-pipeline && \
uv run --with-requirements requirements.txt dlt_fetch_timecamp.py \
  --from 2026-01-01 --to 2026-02-14 \
  --datasets computer_activities,users,application_names,entries,tasks \
  --format jsonl --output ~/data/timecamp-data-pipeline
```

## 使用 DuckDB 进行数据分析

可以直接通过 DuckDB 查询持久化存储的数据。

```bash
DUCKDB=~/.duckdb/cli/latest/duckdb
DATA=~/data/timecamp-data-pipeline/timecamp

# Hours per person
$DUCKDB -c "
SELECT user_name, round(sum(TRY_CAST(duration AS DOUBLE))/3600.0, 1) as hours
FROM read_json_auto('$DATA/entries*.jsonl')
GROUP BY user_name ORDER BY hours DESC
"

# Hours per person per day
$DUCKDB -c "
SELECT user_name, date, round(sum(TRY_CAST(duration AS DOUBLE))/3600.0, 1) as hours
FROM read_json_auto('$DATA/entries*.jsonl')
GROUP BY user_name, date ORDER BY user_name, date
"

# Top applications by time (join activities with app names)
$DUCKDB -c "
SELECT COALESCE(an.full_name, an.application_name, an.app_name, 'Unknown') as app,
       round(sum(ca.time_span)/3600.0, 2) as hours
FROM read_json_auto('$DATA/computer_activities*.jsonl') ca
LEFT JOIN read_json_auto('$DATA/application_names*.jsonl') an
  ON ca.application_id = an.application_id
GROUP BY 1 ORDER BY hours DESC LIMIT 20
"

# People who logged < 30h in a given week
$DUCKDB -c "
SELECT user_name, round(sum(TRY_CAST(duration AS DOUBLE))/3600.0, 1) as hours
FROM read_json_auto('$DATA/entries*.jsonl')
WHERE date BETWEEN '2026-02-03' AND '2026-02-07'
GROUP BY user_name
HAVING sum(TRY_CAST(duration AS DOUBLE))/3600.0 < 30
ORDER BY hours
"
```

### 使用流程：

1. 首先使用 DuckDB 检查现有数据是否完整；如果数据缺失，则通过 Data Pipeline 获取；如果数据已存在，则直接使用。
2. 使用 DuckDB 进行查询的命令格式为：`$DUCKDB -c "SELECT ... FROM read_json_auto('$DATA/entries*.jsonl') ..."`

## 重要说明：

- 条目的持续时间以秒为单位（例如：3600 表示 1 小时）。
- `activities` 中的 `time_span` 也以秒为单位。
- `applications_cache.json` 文件位于 Data Pipeline 目录中，用于缓存应用程序名称的查询结果。
- 对于 JSONL 格式的输出文件，DuckDB 会自动匹配所有数据集的文件（文件扩展名为 `.jsonl`）。

## 安全注意事项：

- 在添加、更新或删除条目之前，请务必确认操作的正确性。
- 在执行任何修改操作之前，请先显示相应的命令内容。
- 停止计时器时，请先显示当前正在运行的计时器信息。