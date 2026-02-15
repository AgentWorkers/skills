---
name: youtrack
description: 通过 REST API 与 YouTrack 项目管理系统进行交互。可以读取项目信息和问题详情、创建任务、根据时间跟踪数据生成发票，以及管理知识库文章。该系统可用于查看项目和工作项、创建或更新问题、根据时间跟踪数据生成客户发票，以及处理知识库文章。
---

# YouTrack

YouTrack 提供了项目管理、时间跟踪和知识库集成功能。

## 快速入门

### 认证

要生成一个永久性的 API 令牌，请按照以下步骤操作：
1. 从主导航菜单中选择 **管理** > **访问管理** > **用户**
2. 找到您的用户并点击以打开设置
3. 生成一个新的永久性 API 令牌
4. 将该令牌设置为环境变量：

```bash
export YOUTRACK_TOKEN=your-permanent-token-here
```

**重要提示：** 请通过传递 `--rate` 参数到 `invoice_generator.py` 或在代码中更新 `hourly_rate` 参数来配置您的每小时费用（默认为 $100/小时）。

然后您可以使用任何 YouTrack 脚本：

```bash
# List all projects
python3 scripts/youtrack_api.py --url https://your-instance.youtrack.cloud --list-projects

# List issues in a project
python3 scripts/youtrack_api.py --url https://your-instance.youtrack.cloud --list-issues "project: MyProject"

# Generate invoice for a project
python3 scripts/invoice_generator.py --url https://your-instance.youtrack.cloud --project MyProject --month "January 2026" --from-date "2026-01-01"
```

## Python 脚本

### `scripts/youtrack_api.py`

这是一个用于所有 YouTrack 操作的核心 API 客户端。

**在您的 Python 代码中：**
```python
from youtrack_api import YouTrackAPI

api = YouTrackAPI('https://your-instance.youtrack.cloud', token='your-token')

# Projects
projects = api.get_projects()
project = api.get_project('project-id')

# Issues
issues = api.get_issues(query='project: MyProject')
issue = api.get_issue('issue-id')

# Create issue
api.create_issue('project-id', 'Summary', 'Description')

# Work items (time tracking)
work_items = api.get_work_items('issue-id')
issue_with_time = api.get_issue_with_work_items('issue-id')

# Knowledge base
articles = api.get_articles()
article = api.get_article('article-id')
api.create_article('project-id', 'Title', 'Content')
```

**命令行使用方法：**
```bash
python3 scripts/youtrack_api.py --url https://your-instance.youtrack.cloud \
    --token YOUR_TOKEN \
    --list-projects

python3 scripts/youtrack_api.py --url https://your-instance.youtrack.cloud \
    --get-issue ABC-123

python3 scripts/youtrack_api.py --url https://your-instance.youtrack.cloud \
    --get-articles
```

### `scripts/invoice_generator.py`

该脚本根据时间跟踪数据生成客户发票。

**在您的 Python 代码中：**
```python
from youtrack_api import YouTrackAPI
from invoice_generator import InvoiceGenerator

api = YouTrackAPI('https://your-instance.youtrack.cloud', token='your-token')
generator = InvoiceGenerator(api, hourly_rate=100.0)

# Get time data for a project
project_data = generator.get_project_time_data('project-id', from_date='2026-01-01')

# Generate invoice
invoice_text = generator.generate_invoice_text(project_data, month='January 2026')
print(invoice_text)
```

**命令行使用方法：**
```bash
python3 scripts/invoice_generator.py \
    --url https://your-instance.youtrack.cloud \
    --project MyProject \
    --from-date 2026-01-01 \
    --month "January 2026" \
    --rate 100 \
    --format text
```

将脚本的输出保存为文本文件，并将其转换为 PDF 格式提供给客户。

## 常见工作流程

### 1. 列出所有项目
```bash
python3 scripts/youtrack_api.py --url https://your-instance.youtrack.cloud --list-projects
```

### 2. 在项目中查找问题
```bash
# All issues in a project
python3 scripts/youtrack_api.py --url https://your-instance.youtrack.cloud --list-issues "project: MyProject"

# Issues updated since a date
python3 scripts/youtrack_api.py --url https://your-instance.youtrack.cloud --list-issues "project: MyProject updated >= 2026-01-01"

# Issues assigned to you
python3 scripts/youtrack_api.py --url https://your-instance.youtrack.cloud --list-issues "assignee: me"
```

### 3. 创建新问题
```python
from youtrack_api import YouTrackAPI

api = YouTrackAPI('https://your-instance.youtrack.cloud')
api.create_issue(
    project_id='MyProject',
    summary='Task title',
    description='Task description'
)
```

### 4. 生成月度发票
```bash
# Generate invoice for January 2026
python3 scripts/invoice_generator.py \
    --url https://your-instance.youtrack.cloud \
    --project ClientProject \
    --from-date 2026-01-01 \
    --month "January 2026" \
    --rate 100 \
    --format text > invoice.txt
```

将脚本的输出保存为文本文件，并将其转换为 PDF 格式提供给客户。

### 5. 阅读知识库
```python
from youtrack_api import YouTrackAPI

api = YouTrackAPI('https://your-instance.youtrack.cloud')

# All articles
articles = api.get_articles()

# Articles for specific project
articles = api.get_articles(project_id='MyProject')

# Get specific article
article = api.get_article('article-id')
```

## 开票逻辑

发票生成器使用以下计算方式：
1. 将每个问题所记录的总时间（以分钟为单位）相加
2. 将时间转换为 30 分钟的增量（向上取整）
3. 最小收费时间为 30 分钟（按配置的费率计算）
4. 将结果乘以费率（默认为 $100/小时，即每半小时 $50）

示例：
- 15 分钟 → $50（最低收费 30 分钟）
- 35 分钟 → $100（向上取整为 60 分钟）
- 60 分钟 → $100
- 67 分钟 → $150（向上取整为 90 分钟）

## 环境变量

- `YOUTRACK_TOKEN`：您的永久性 API 令牌（建议使用环境变量而非作为参数传递）
- 通过 `export YOUTRACK_TOKEN=your-token` 来设置该变量

## API 详情

请参阅 `REFERENCES.md` 以获取以下信息：
- 完整的 API 端点文档
- 查询语言示例
- 字段 ID 和结构

## 错误处理

如果出现以下情况，脚本将抛出错误：
- 令牌缺失或无效
- 网络问题
- API 错误（如 404、403 等）

请查看 `stderr` 文件以获取错误详细信息。