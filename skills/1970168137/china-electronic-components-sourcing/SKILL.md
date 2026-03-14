---
name: china-electronic-components-sourcing
version: 1.0.0
description: "面向国际买家的电子元件行业综合采购指南——提供关于中国半导体、无源元件、印刷电路板（PCB）、连接器及传感器制造产业集群的详细信息，包括供应链结构、区域特色以及行业趋势（更新至2026年）。"
author: "sourcing-china"
tags:
  - electronic-components
  - semiconductors
  - passives
  - PCBs
  - connectors
  - sourcing
  - supply-chain
invocable: true
---
# 中国电子元件采购技能

## 描述
该技能帮助国际电子采购商了解中国的电子元件制造市场。预计到2026年，中国电子元件市场的收入将超过5.2万亿元人民币。该技能基于最新的政府政策和行业报告，提供有关区域产业集群、供应链结构及行业趋势的可靠信息。

## 主要功能
- **行业概况**：了解中国电子元件行业的规模和发展目标。
- **供应链结构**：掌握从原材料到下游应用的完整产业链。
- **区域产业集群**：识别不同类型电子元件的专业制造基地（半导体、无源元件、印刷电路板、连接器、传感器等）。
- **子行业洞察**：获取关键子行业（半导体、无源元件、印刷电路板、连接器、传感器等）的详细信息。
- **采购建议**：提供评估和选择供应商的实际指导，包括验证方法和沟通最佳实践。

## 使用方法
您可以使用自然语言与该技能进行交互。例如：
- “2026年中国电子元件行业的整体状况如何？”
- “展示电子元件的供应链结构。”
- “哪些地区最适合采购汽车级半导体？”
- “介绍一下MLCC（多层陶瓷电容器）的制造产业集群。”
- “我该如何评估中国的印刷电路板供应商？”
- “在选择传感器供应商时，应该关注哪些认证要求？”

## 数据来源
该技能的数据来源于：
- 工业和信息化部（MIIT）的官方政策
- 中国国家统计局的数据
- 中国电子元件协会（CECA）的年度报告
- 行业研究出版物（更新至2026年第一季度）

## 实现方式
该技能的逻辑实现位于`do.py`文件中，该文件从`data.json`文件中读取结构化数据。所有数据均为行业层面的汇总信息，不包含个别工厂的联系方式。

## API参考
`do.py`文件中提供了以下Python函数，用于程序化访问相关数据：

### `get_industry_overview() -> Dict`
返回中国电子元件行业的规模、发展目标及关键政策举措的概览。

**示例：**
```python
from do import get_industry_overview
result = get_industry_overview()
# Returns: industry scale, 2026 targets, automation rates, key drivers, etc.
```

### `get_supply_chain_structure() -> Dict`
返回完整的电子元件供应链结构（上游、中游、下游）。

**示例：**
```python
from do import get_supply_chain_structure
result = get_supply_chain_structure()
# Returns: raw materials, manufacturing, application industries
```

### `get_regional_clusters(region: Optional[str] = None) -> Union[List[Dict], Dict]`
返回所有区域产业集群或按名称指定的产业集群。
- 如果`region`为空：返回所有产业集群的列表
- 如果指定了`region`：返回该区域的详细信息

**示例：**
```python
from do import get_regional_clusters
all_clusters = get_regional_clusters()
yangtze = get_regional_clusters("Yangtze River Delta")
```

### `find_clusters_by_specialization(specialization: str) -> List[Dict]`
查找专注于特定类型电子元件的产业集群。

**示例：**
```python
from do import find_clusters_by_specialization
results = find_clusters_by_specialization("automotive semiconductors")
```

### `get_subsector_info(subsector: str) -> Dict`
返回特定电子元件子行业的详细信息。

**示例：**
```python
from do import get_subsector_info
mlcc_info = get_subsector_info("MLCC")
semiconductor_info = get_subsector_info("semiconductors")
```

### `get_sourcing_guide() -> Dict`
返回供应商评估和采购的最佳实践。

**示例：**
```python
from do import get_sourcing_guide
guide = get_sourcing_guide()
# Returns: evaluation criteria, verification methods, communication tips
```

### `get_faq-question: Optional[str] = None) -> Union[List[Dict], Dict]`
返回常见问题列表或对特定问题的回答。

**示例：**
```python
from do import get_faq
all_faqs = get_faq()
moq_faq = get_faq("MOQ")
```

### `get_glossary(term: Optional[str] = None) -> Union[Dict, str]`
返回术语表或对特定术语的定义。

**示例：**
```python
from do import get_glossary
all_terms = get_glossary()
mlcc_def = get_glossary("MLCC")
```

### `search_data(query: str) -> List[Dict]`
在所有数据中搜索指定的查询字符串。

**示例：**
```python
from do import search_data
results = search_data("automotive")
```

### `get_metadata() -> Dict`
返回数据来源的元信息和最后一次更新时间。

**示例：**
```python
from do import get_metadata
meta = get_metadata()
```