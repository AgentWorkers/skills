---
name: parallel
description: 通过 Parallel.ai API 进行高精度的网络搜索和研究。该服务专为 AI 代理优化，提供丰富的摘录和引用信息，并支持访问经过身份验证的私有资源。
user-invocable: true
disable-model-invocation: true
triggers:
  - parallel
  - deep search
  - research
  - enrich
  - findall
  - monitor
  - extract
metadata:
  clawdbot:
    emoji: "🔬"
    primaryEnv: PARALLEL_API_KEY
    requires:
      bins: [python3, curl, jq]
      env: [PARALLEL_API_KEY]
---

# Parallel.ai

这是一个专为AI代理设计的高精度网络研究API。

## 设置

安装所需的Python包：

```bash
pip install parallel-sdk requests
```

设置您的API密钥：

```bash
export PARALLEL_API_KEY="your-key"
```

您可以在以下链接获取API密钥：https://platform.parallel.ai

**可选**——用于身份验证的源访问（基本使用无需此步骤）：

```bash
export BROWSERUSE_API_KEY="your-key"  # Only if using authenticated sources
```

## API概述

| API | 使用场景 | 速度 |
|-----|----------|-------|
| **Search** | 快速查询、当前事件 | 非常快 |
| **Task** | 深度研究、数据丰富化、生成报告 | 中等速度 |
| **FindAll** | 实体发现 → 结构化数据集 | 较慢（异步） |
| **Extract** | 从URL/PDF中提取干净内容 | 非常快 |
| **Monitor** | 持续跟踪并发送警报 | 定期更新 |

---

## Search API - 快速网络搜索

```bash
python3 {baseDir}/scripts/search.py "Who is the CEO of Anthropic?" --max-results 5
python3 {baseDir}/scripts/search.py "latest AI news" --json
```

---

## Task API - 深度研究与数据丰富化

```bash
# Simple question → answer
python3 {baseDir}/scripts/task.py "What was France's GDP in 2023?"

# Structured enrichment (company research)
python3 {baseDir}/scripts/task.py --enrich "company_name=Stripe,website=stripe.com" \
  --output "founding_year,employee_count,total_funding"

# Research report (markdown with citations)
python3 {baseDir}/scripts/task.py --report "Market analysis of the HVAC industry in USA"

# With authenticated sources (requires browser-use.com key)
export BROWSERUSE_API_KEY="your-key"
python3 {baseDir}/scripts/task.py "Extract specs from https://nxp.com/products/K66_180"
```

### 处理器

| 处理器 | 速度 | 深度 | 使用场景 |
|-----------|-------|-------|----------|
| `base` | 快速 | 轻量级 | 简单查询、事实核查 |
| `core` | 中等 | 标准 | 数据丰富化、结构化数据 |
| `ultra` | 慢速 | 深度 | 生成报告、多步骤研究 |

---

## FindAll API - 实体发现（2026年2月新增）

将自然语言转换为结构化数据集。例如：“查找俄亥俄州评分4星以上的所有牙科诊所” → 生成包含引用信息的丰富列表。

```bash
# Basic entity discovery
python3 {baseDir}/scripts/findall.py "Find all AI startups that raised Series A in 2025"

# With enrichment
python3 {baseDir}/scripts/findall.py "portfolio companies of Khosla Ventures" \
  --enrich "funding,employee_count,founder_names" --limit 50

# Lead generation
python3 {baseDir}/scripts/findall.py "residential roofing companies in Charlotte, NC" --generator pro

# Check status of running job
python3 {baseDir}/scripts/findall.py --status findall_abc123
```

### 生成器

| 生成器 | 覆盖范围 | 成本 | 使用场景 |
|-----------|----------|------|----------|
| `base` | 有限 | 低成本 | 快速发现、原型设计 |
| `core` | 平衡性良好 | 中等 | 大多数使用场景 |
| `pro` | 全面 | 高成本 | 最高召回率（61%的基准测试结果） |

### 工作原理
1. **输入**：将自然语言转换为实体类型及匹配条件 |
2. **搜索**：在网络上搜索符合条件的实体 |
3. **评估**：验证每个候选实体是否符合匹配条件 |
4. **丰富化**：为匹配到的实体提取额外字段 |

---

## Extract API - 提取干净内容（2026年2月新增）

可将任何URL转换为干净的Markdown格式——支持处理包含JavaScript的页面、PDF文件以及有付费墙的内容。

```bash
# Basic extraction with excerpts
python3 {baseDir}/scripts/extract.py https://stripe.com/docs/api

# Full content (not just excerpts)
python3 {baseDir}/scripts/extract.py https://arxiv.org/pdf/2301.00000.pdf --full

# Focused extraction
python3 {baseDir}/scripts/extract.py https://sec.gov/10-K.htm --objective "Extract risk factors"

# Multiple URLs at once
python3 {baseDir}/scripts/extract.py https://url1.com https://url2.com --json
```

### 使用场景
- **API文档**：提取完整的参考文献和代码示例 |
- **PDF研究论文**：提取方法论、结果和引用信息 |
- **证券文件**：从10-K报表和收益报告中提取特定内容 |
- **新闻文章**：获取不含广告、导航栏和付费墙的干净文本 |

---

## Monitor API - 持续跟踪（2026年2月新增）

设置定期查询——在内容发生变化时接收警报。

```bash
# Create a monitor
python3 {baseDir}/scripts/monitor.py create "Track AI funding news" --cadence daily
python3 {baseDir}/scripts/monitor.py create "Alert when AirPods drop below $150" --cadence hourly

# With webhook notifications
python3 {baseDir}/scripts/monitor.py create "OpenAI product announcements" \
  --cadence daily --webhook https://your-endpoint.com/webhook

# List all monitors
python3 {baseDir}/scripts/monitor.py list

# Get events (detected changes)
python3 {baseDir}/scripts/monitor.py events monitor_abc123
python3 {baseDir}/scripts/monitor.py events monitor_abc123 --lookback 10d

# Delete a monitor
python3 {baseDir}/scripts/monitor.py delete monitor_abc123
```

### 查询频率
- **每小时**：适用于变化迅速的主题、股票/价格跟踪 |
- **每天**：新闻、行业动态（最常见） |
- **每周**：变化较慢的内容、政策更新 |

### 示例查询
- **新闻**：“当有人提到Parallel Web Systems时通知我” |
- **竞争情报**：“苹果发布新MacBook型号时提醒我” |
- **价格**：“当PS5 Pro在Best Buy重新有货时通知我” |
- **政策**：“跟踪OpenAI服务条款的变更”

---

## 身份验证的源（2026年1月新增）

Task API支持通过MCP服务器访问需要身份验证的私有数据源：
- 内部维基和仪表板 |
- 行业数据库（如NXP、IEEE等） |
- 客户关系管理系统（CRM）和订阅服务

使用[browser-use.com](https://browser-use.com)进行MCP集成：

### 设置
1. 从[browser-use.com](https://browser-use.com)获取API密钥 |
2. 创建一个包含保存的登录会话的**个人资料** |
3. 设置`BROWSERUSE_API_KEY`环境变量

### 使用方法
```bash
export BROWSERUSE_API_KEY="your-key"
python3 {baseDir}/scripts/task.py "Extract migration guide from NXP K66 docs"
```

---

## 各API的使用场景

| 场景 | API | 使用原因 |
|----------|-----|-----|
| 快速查询事实 | Search | 快速且简单 |
| 公司信息丰富化 | Task | 提供带有引用的结构化输出 |
| 构建潜在客户列表 | FindAll | 发现、验证并丰富数据 |
| 从URL提取内容 | Extract | 支持处理包含JavaScript的页面、PDF文件和有付费墙的内容 |
| 持续跟踪 | Monitor | 设置一次后接收警报 |
| 深度研究报告 | Task | 进行多步骤研究并生成带有引用的报告 |
| 访问受保护的内容 | Task + MCP | 需要身份验证 |

---

## API参考

- 文档：https://docs.parallel.ai |
- 平台：https://platform.parallel.ai |
- 更新日志：https://parallel.ai/blog |

---

## 安全性与权限

**该技能的功能：**
- 通过`api.parallel.ai`发送API请求以进行网络搜索、研究、内容提取和监控 |
- `monitor.py`使用`requests`库；其他脚本使用`parallel-sdk`包 |
- 所有脚本均为只读研究工具，不会修改任何本地或远程数据 |
- `BROWSERUSE_API_KEY`（可选）仅用于通过`api.browser-use.com`进行身份验证的访问 |

**该技能不执行以下操作：**
- 不会将您的API密钥发送到除`api.parallel.ai`和`api.browser-use.com`之外的任何端点 |
- 不会访问本地文件、数据库或系统资源 |
- 不会读取配置文件或访问文件系统 |
- 不会写入磁盘（除非使用`--json`选项生成JSON输出） |
- 代理无法自主调用该技能（`disable-model-invocation: true`）

**Python依赖库：`parallel-sdk`、`requests`（通过`pip install parallel-sdk requests`安装）**

首次使用前，请查看`scripts/`目录以确认脚本的行为。