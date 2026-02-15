---
name: powerdrill-data-analysis
description: 此技能适用于用户希望使用 Powerdrill 进行数据分析、数据探索、数据可视化或数据查询的场景。它涵盖了数据集的列表、创建和删除操作；将本地文件作为数据源上传；创建分析会话；运行基于自然语言的数据分析查询；以及检索图表、表格和分析结果等功能。相关操作请求包括但不限于：“分析我的数据”、“查询我的数据集”、“上传此文件以供分析”、“列出我的数据集”、“创建数据集”、“可视化销售趋势”、“继续之前的分析”以及任何涉及 Powerdrill 的数据探索任务。
license: MIT
compatibility: claude
metadata:
  audience: human
  workflow: powerdrill
---

# Powerdrill 数据分析技能

使用 `scripts/powerdrill_client.py` 中的 Python 客户端通过 Powerdrill API 分析数据。所有操作均基于 Powerdrill REST API v2（`https://ai.data.cloud/api`）进行。

## 先决条件与设置

在使用任何 Powerdrill 功能之前，用户必须具备以下条件：

1. **Powerdrill Teamspace**：按照以下链接创建：https://www.youtube.com/watch?v=I-0yGD9HeDw
2. **API 凭据**：按照以下链接获取：https://www.youtube.com/watch?v=qs-GsUgjb1g

在运行任何脚本之前，请设置以下环境变量：

```bash
export POWERDRILL_USER_ID="your_user_id"
export POWERDRILL_PROJECT_API_KEY="your_project_api_key"
```

唯一的 Python 依赖库是 `requests`。可以使用以下命令安装：`pip install requests`

如果调用失败并出现身份验证错误，请确认这两个环境变量已设置且 API 密钥有效。

## 使用方法

导入客户端模块并直接调用相关函数。所有函数会自动从环境中读取凭据。

```python
import sys
sys.path.insert(0, "/absolute/path/to/scripts")  # adjust to actual location
from powerdrill_client import *
```

或者通过命令行（CLI）进行操作：

```bash
python scripts/powerdrill_client.py <command> [args]
```

## 可用函数

### 数据集

#### `list_datasets(page_number=1, page_size=10, search=None) -> dict`
列出用户账户中的数据集。这通常是任何工作流程的第一步。

```python
result = list_datasets(search="sales")
for ds in result["data"]["records"]:
    print(ds["id"], ds["name"])
```

#### `create_dataset(name, description="") -> dict`
创建一个新的空数据集。返回 `{"data": {"id": "dset-...}}`。

```python
ds = create_dataset("Q4 Sales Data", "Quarterly sales analysis")
dataset_id = ds["data"]["id"]
```

#### `get_dataset_overview(dataset_id) -> dict`
获取数据集的概览信息、探索性问题以及关键词。在数据源同步完成后使用此函数。

```python
overview = get_dataset_overview(dataset_id)
print(overview["data"]["summary"])
for q in overview["data"]["exploration_questions"]:
    print(f"  - {q}")
```

#### `get_dataset_status(dataset_id) -> dict`
检查有多少数据源已同步、正在同步或无效。

```python
status = get_dataset_status(dataset_id)
# status["data"] = {"synched_count": 3, "synching_count": 0, "invalid_count": 0}
```

#### `delete_dataset(dataset_id) -> dict`
永久删除数据集及其所有数据源。此操作不可逆——请务必先征得用户同意。

### 数据源

#### `list_data_sources(dataset_id, page_number=1, page_size=10, status=None) -> dict`
列出数据集内的文件。可以根据状态（`synched`、`synching`、`invalid`）进行筛选。

```python
sources = list_data_sources(dataset_id, status="synched")
```

#### `create_data_source(dataset_id, name, *, url=None, file_object_key=None) -> dict`
从公共 URL 或上传的文件键创建数据源。必须提供 `url` 或 `file_object_key` 中的一个。

```python
# From public URL
ds = create_data_source(dataset_id, "report.pdf", url="https://example.com/report.pdf")

# From uploaded file (see upload_local_file)
ds = create_data_source(dataset_id, "data.csv", file_object_key=key)
```

#### `upload_local_file(file_path) -> str`
通过多部分上传（multipart upload）上传本地文件。返回 `file_object_key`，以便后续使用 `create_data_source()`。

支持的文件格式：`.csv`、`.tsv`、`.md`、`.mdx`、`.json`、`.txt`、`.pdf`、`.pptx`、`.docx`、`.xls`、`.xlsx`

#### `upload_and_create_data_source(dataset_id, file_path) -> dict`
便捷函数：一次性上传文件并创建数据源。

```python
result = upload_and_create_data_source(dataset_id, "/path/to/sales.csv")
datasource_id = result["data"]["id"]
```

#### `wait_for_dataset_sync(dataset_id, max_attempts=30, delay_seconds=3.0) -> dict`
轮询直到数据集中的所有数据源都同步完成。如果超时或检测到无效的数据源，将抛出 `RuntimeError`。

```python
upload_and_create_data_source(dataset_id, "data.csv")
wait_for_dataset_sync(dataset_id)  # blocks until synced
```

### 会话

#### `create_session(name, output_language="AUTO", job_mode="AUTO", max_contextual_job_history=10) -> dict`
创建一个分析会话。运行分析任务前必须先创建会话。

```python
session = create_session("Sales Analysis Session")
session_id = session["data"]["id"]
```

#### `list_sessions(page_number=1, page_size=10, search=None) -> dict`
列出现有的会话。可用于查找之前的会话以继续分析。

#### `delete_session(session_id) -> dict`
删除会话。分析完成后用于清理。

### 分析任务（数据分析）

#### `create_job(session_id, question, dataset_id=None, datasource_ids=None, stream=False, output_language="AUTO", job_mode="AUTO") -> dict`
运行自然语言分析查询。这是核心的分析功能。

**非流式**（默认）：返回包含所有分析结果的完整响应。

```python
result = create_job(session_id, "What are the top 5 products by revenue?", dataset_id=dataset_id)
for block in result["data"]["blocks"]:
    if block["type"] == "MESSAGE":
        print(block["content"])
    elif block["type"] == "TABLE":
        print(f"Table: {block['content']['url']}")
    elif block["type"] == "IMAGE":
        print(f"Chart: {block['content']['url']}")
```

**流式**：返回解析后的结果，其中包含累积的文本和各个分析块。

### 响应块类型：
- `MESSAGE` - 分析文本
- `CODE` - 代码片段（Markdown 格式）
- `TABLE` - `{name, url, expires_at}` - 在过期前可下载
- `IMAGE` - `{name, url, expires_at}` - 在过期前可下载
- `SOURCES` - 引用来源
- `QUESTIONS` - 建议的后续问题
- `CHART_INFO` - 图表配置和数据

### 清理

#### `cleanup(session_id=None, dataset_id=None) -> None`
分析完成后删除会话和/或数据集。分析完成后务必调用此函数。

```python
cleanup(session_id=session_id, dataset_id=dataset_id)
```

#### `cleanup_session(session_id) -> None` / `cleanup_dataset(dataset_id) -> None`
删除单个资源。虽然会记录错误，但不会抛出异常。

## 推荐的工作流程

### 完整的分析流程（上传、分析、清理）

```python
from powerdrill_client import *

# 1. Create dataset and upload data
ds = create_dataset("My Analysis")
dataset_id = ds["data"]["id"]

upload_and_create_data_source(dataset_id, "/path/to/data.csv")
wait_for_dataset_sync(dataset_id)

# 2. Create session and run analysis
session = create_session("Analysis Session")
session_id = session["data"]["id"]

result = create_job(session_id, "What are the key trends?", dataset_id=dataset_id)
for block in result["data"]["blocks"]:
    if block["type"] == "MESSAGE":
        print(block["content"])

# 3. Ask follow-up questions (same session for context)
result = create_job(session_id, "Break this down by region", dataset_id=dataset_id)

# 4. Cleanup when done
cleanup(session_id=session_id, dataset_id=dataset_id)
```

### 分析现有数据集

```python
from powerdrill_client import *

# 1. Find the dataset
datasets = list_datasets(search="sales")
dataset_id = datasets["data"]["records"][0]["id"]

# 2. Explore it
overview = get_dataset_overview(dataset_id)
print(overview["data"]["summary"])

# 3. Create session and analyze
session = create_session("Quick Analysis")
session_id = session["data"]["id"]

result = create_job(session_id, overview["data"]["exploration_questions"][0], dataset_id=dataset_id)

# 4. Cleanup session when done (keep dataset)
cleanup_session(session_id)
```

### 命令行（CLI）使用方法

```bash
# List datasets
python scripts/powerdrill_client.py list-datasets --search "sales"

# Create dataset + upload file
python scripts/powerdrill_client.py create-dataset "Test Data"
python scripts/powerdrill_client.py upload-file dset-xxx /path/to/file.csv
python scripts/powerdrill_client.py wait-sync dset-xxx

# Create session and run a job
python scripts/powerdrill_client.py create-session "My Session"
python scripts/powerdrill_client.py create-job SESSION_ID "Summarize the data" --dataset-id dset-xxx

# Cleanup
python scripts/powerdrill_client.py cleanup --session-id SESSION_ID --dataset-id dset-xxx
```

## 错误处理

- **身份验证错误**：检查 `POWERDRILL_USER_ID` 和 `POWERDRILL_PROJECT_API_KEY` 是否正确。请用户参考上述设置视频进行配置。
- **数据集未找到**：重新运行 `list_datasets()` 以确认数据集是否存在。数据集可能已被删除。
- **任务执行失败**：确保数据集至少有一个已同步的数据源（使用 `wait_for_dataset_sync()`）。尝试重新提交问题。
- **上传超时**：`wait_for_dataset_sync()` 会尝试最多 30 次（每次间隔 90 秒）。可以使用 `get_dataset_status()` 手动检查。
- **数据源无效**：检查文件格式是否受支持。请使用正确的文件类型重新上传。
- **速率限制**：在尝试重新上传之前请稍作等待，避免连续快速调用 API。

## 重要注意事项

- 运行分析任务前务必创建会话。
- 分析完成后务必调用 `cleanup()` 删除会话和数据集。
- 会话会保留分析的上下文——对于相关的后续问题，请使用相同的会话。
- 任务响应中的 `TABLE` 和 `IMAGE` 链接会在过期前失效——请及时下载结果。
- 上传文件后请调用 `wait_for_dataset_sync()`，然后再进行分析。
- 数据集和会话的名称长度限制为 128 个字符。
- 支持的文件格式：`.csv`、`.tsv`、`.md`、`.mdx`、`.json`、`.txt`、`.pdf`、`.pptx`、`.docx`、`.xls`、`.xlsx`