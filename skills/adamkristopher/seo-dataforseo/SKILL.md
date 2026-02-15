---
name: seo-dataforseo
description: "使用 DataForSEO API 进行 SEO 关键词研究。该 API 支持关键词分析、YouTube 关键词研究、竞争对手分析、搜索引擎结果页（SERP）分析以及趋势跟踪等功能。适用于以下场景：用户需要研究关键词、分析搜索量/点击成本（CPC）/竞争情况、获取关键词建议、评估关键词的难度、分析竞争对手、了解热门话题，或优化着陆页的关键词。使用该服务前，需确保您拥有 DataForSEO API 账户，并在 `.env` 文件中配置相应的凭据。"
---

# SEO关键词研究（DataForSEO）

## 设置

安装依赖项：

```bash
pip install -r scripts/requirements.txt
```

通过在项目根目录下创建一个`.env`文件来配置凭据：

```
DATAFORSEO_LOGIN=your_email@example.com
DATAFORSEO_PASSWORD=your_api_password
```

从以下地址获取凭据：https://app.dataforseo.com/api-access

## 快速入门

| 用户请求 | 调用的函数 |
|-----------|-----------------|
| "为[主题]研究关键词" | `keyword_research("主题")` |
| "获取[想法]相关的YouTube关键词数据" | `youtube_keyword_research("想法")` |
| "分析竞争对手[domain.com]" | `competitor_analysis("domain.com")` |
| "当前的热门搜索是什么？" | `trending_topics()` |
| "对[列表]进行关键词分析" | `full_keyword_analysis(["kw1", "kw2"])` |
| "为[主题]的着陆页生成关键词" | `landing_page_keyword_research(["kw1"], "competitor.com")` |

通过导入`scripts/main.py`来执行这些函数：

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts")))
from main import *

result = keyword_research("AI website builders")
```

## 工作流程模式

每个研究任务都遵循三个阶段：

### 1. 研究
调用API函数。每个函数调用都会访问DataForSEO API并返回结构化的数据。

### 2. 自动保存
所有结果会自动保存为带有时间戳的JSON文件，文件保存路径为`results/{类别}/`。文件命名格式为：`YYYYMMDD_HHMMSS__操作__关键词__额外信息.json`

### 3. 总结
研究完成后，读取保存的JSON文件，并在`results/summary/`目录下生成一个Markdown格式的总结报告，其中包含数据表格、排名较高的关键词以及战略建议。

## 主要函数

这些是`scripts/main.py`中的主要函数，每个函数都会协调多个API调用以完成整个研究流程。

| 函数 | 功能 | 收集的数据 |
|----------|---------|----------------|
| `keyword_research(keyword)` | 单个关键词的深入分析 | 概述、建议、相关关键词、难度 |
| `youtube_keyword_research(keyword)` | YouTube内容研究 | 概述、建议、YouTube搜索结果页排名、YouTube热门趋势 |
| `landing_page_keyword_research(keywords, competitor_domain)` | 着陆页SEO分析 | 概述、用户意图、难度、搜索结果页分析、竞争对手关键词 |
| `full_keyword_analysis(keywords)` | 战略性内容规划 | 概述、难度、用户意图、关键词建议、历史搜索量、Google趋势 |
| `competitor_analysis(domain, keywords)` | 竞争对手分析 | 竞争对手使用的关键词、Google广告关键词、竞争对手的域名 |
| `trending_topics(location_name)` | 当前热门搜索 | 当前流行的搜索词 |

### 参数

所有函数都接受一个可选的`location_name`参数（默认值为“United States”）。大多数函数还提供了布尔标志，用于跳过特定的子分析（例如`include_suggestions=False`）。

### 单个API函数

如需更细粒度的控制，可以从API模块中导入相应的函数。请参阅[references/api-reference.md](references/api-reference.md)，以获取包含参数、限制和示例的25个API函数的完整列表。

## 结果存储

结果会自动保存到`results/`目录中，保存结构如下：

```
results/
├── keywords_data/    # Search volume, CPC, competition
├── labs/             # Suggestions, difficulty, intent
├── serp/             # Google/YouTube rankings
├── trends/           # Google Trends data
└── summary/          # Human-readable markdown summaries
```

### 结果管理

```python
from core.storage import list_results, load_result, get_latest_result

# List recent results
files = list_results(category="labs", limit=10)

# Load a specific result
data = load_result(files[0])

# Get most recent result for an operation
latest = get_latest_result(category="labs", operation="keyword_suggestions")
```

### 实用工具函数

```python
from main import get_recent_results, load_latest

# List recent files across all categories
files = get_recent_results(limit=10)

# Load latest result for a category
data = load_latest("labs", "keyword_suggestions")
```

## 创建总结报告

研究完成后，在`results/summary/`目录下创建一个Markdown格式的总结文档。文档应包含以下内容：

- **数据表格**：显示搜索量、每次点击成本（CPC）、竞争情况、关键词难度
- **排名列表**：按搜索量或机会得分排序的关键词
- **搜索结果页分析**：展示当前排名较高的关键词
- **内容策略建议**：关于内容策略、标题和标签的建议

为总结文件起一个描述性的名称（例如`results/summary/ai-tools-keyword-research.md`）。

## 提示

1. **具体说明** —— “获取‘AI网站构建器’的关键词建议”比“研究AI相关内容”更具体。
2. **生成总结报告** —— 研究完成后务必生成一个具有明确名称的总结文档。
3. **批量处理相关关键词** —— 一次传递多个相关关键词以便进行比较。
4. **明确目标** —— 指定研究目的（例如“为YouTube视频”或“为着陆页”）会决定哪些数据最为重要。
5. **请求竞争对手分析** —— “显示哪些视频正在排名”有助于识别内容上的差距。

## 默认设置

- **位置**：United States（代码2840）
- **语言**：English
- **API限制**：搜索量/概述最多700个关键词，难度/用户意图分析最多1000个关键词，热门趋势分析最多5个关键词，关键词建议最多200个关键词