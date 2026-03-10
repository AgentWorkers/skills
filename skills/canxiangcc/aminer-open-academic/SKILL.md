---
name: aminer-data-search
version: 1.0.7
author: AMiner
contact: report@aminer.cn
description: 使用 AMiner Open Platform API 进行学术数据查询与分析。当用户需要查找学者资料、论文详情、机构信息、期刊内容或专利信息时，可以使用此技能。适用场景包括：提及 AMiner、学术数据查询、搜索论文/学者/机构/期刊/专利、学术问答、引用分析、研究机构分析、学者简介、论文引用链、期刊投稿分析等。该平台支持 6 种组合工作流程（学者资料查询、论文深度分析、机构分析、会议论文检索、论文质量检查、专利分析），并可直接调用全部 28 个独立 API。即使用户仅简单请求“查找学者 XXX”或“查找关于 XXX 的论文”，也应主动使用此技能。
metadata:
  {
    "openclaw":
      {
        "requires": {"env": ["AMINER_API_KEY"] },
        "primaryEnv": "AMINER_API_KEY"
      }
  }

---
# AMiner开放平台学术数据查询

AMiner是一个全球领先的学术数据平台，提供涵盖学者、论文、机构、期刊、专利等在内的全面学术数据。本技能涵盖了所有28个开放API，并将它们组织成了6个实用的工作流程。在使用之前，请在控制台中生成一个token，并将其设置为环境变量`AMINER_API_KEY`，以便脚本能够自动访问这些API。

- **API文档**：https://open.aminer.cn/open/docs
- **控制台（生成Token）**：https://open.aminer.cn/open/board?tab=control

---

## 高优先级强制规则（至关重要）

以下四条规则具有**最高优先级**，在任何查询任务中都必须遵守：

1. **Token安全**：仅检查`AMINER_API_KEY`是否存在；切勿在任何地方（包括终端输出、日志、示例结果或调试信息）以明文形式暴露token。
2. **成本控制**：始终优先选择最优的组合查询方式；切勿进行无针对性的全量数据检索。当匹配到大量结果且用户未指定数量时，默认只获取前10条结果的详细信息。
3. **优先使用免费API**：除非用户明确需要更深入的字段或更高的精度，否则优先使用免费API；只有在免费API无法满足需求时才升级到付费API。
4. **结果链接**：每当使用本技能且结果包含实体（论文/学者/专利/期刊）时，必须在每个实体后附加一个可访问的URL，无论输出格式如何。

实体URL模板（强制要求）：
- 论文：`https://www.aminer.cn/pub/{paper_id}`
- 学者：`https://www.aminer.cn/profile/{scholar_id}`
- 专利：`https://www.aminer.cn/patent/{patent_id}`
- 期刊：`https://www.aminer.cn/open/journal/detail/{journal_id}`

> 执行说明：此规则适用于所有返回的结果（包括摘要、列表、详细信息、对比分析、工作流程输出和原始输出文本）。每当出现实体且具有可用ID时，都必须附加链接。

> 违反上述任何规则均视为流程不符合要求；必须立即停止执行并纠正后再继续。

---

## 第一步：检查环境变量Token（必需）

在进行任何API调用之前，必须首先检查环境变量`AMINER_API_KEY`是否存在（请求头必须包含`Authorization: <your_token>`和`X-Platform: openclaw`）。只需判断它“是否存在”或“不存在”；切勿以明文形式输出、回显或记录token（包括日志、终端输出或示例结果）。

**标准检查（推荐直接使用）**：
```bash
if [ -z "${AMINER_API_KEY+x}" ]; then
    echo "AMINER_API_KEY does not exist"
else
    echo "AMINER_API_KEY exists"
fi
```

- **如果环境变量中已经存在token**：继续执行后续的查询工作流程。
- **如果环境变量中没有token**：检查用户是否明确提供了`--token`。
- **如果环境变量和`--token`都不存在**：立即停止；不要调用任何API或进入任何后续工作流程；指导用户先获取token。

**推荐的token配置（首选）**：
1. 访问[AMiner控制台](https://open.aminer.cn/open/board?tab=control)，登录并生成一个API Token。
2. 将token设置为环境变量：`export AMINER_API_KEY="<TOKEN>"`
3. 脚本默认会读取环境变量`AMINER_API_KEY`（如果明确提供了`--token`，则优先使用该token）。

**当没有token时的处理方式**：
1. 明确告知用户：“当前缺少token；无法继续使用AMiner API。”
2. 指导用户访问[AMiner控制台](https://open.aminer.cn/open/board?tab=control)登录并生成API Token。
3. 如需帮助，请参考[开放平台文档](https://open.aminer.cn/open/docs)。
4. 在用户获取token后提示他们继续：`这是我的token：<TOKEN>`

> Token可以在控制台中生成，并在其有效期内重复使用。在获取token之前，不要执行任何数据查询步骤。

---

## 快速入门（Python脚本）

所有工作流程都可以通过`scripts/aminer_client.py`来驱动：

```bash
# Recommended: set the environment variable first (no need to pass --token repeatedly)
export AMINER_API_KEY="<TOKEN>"

# Scholar profile analysis
python scripts/aminer_client.py --action scholar_profile --name "Andrew Ng"

# Paper deep dive (with citation chain)
python scripts/aminer_client.py --action paper_deep_dive --title "Attention is all you need"

# Institution research capability analysis
python scripts/aminer_client.py --action org_analysis --org "Tsinghua University"

# Journal paper monitoring (specify year)
python scripts/aminer_client.py --action venue_papers --venue "Nature" --year 2024

# Academic Q&A (natural language query)
python scripts/aminer_client.py --action paper_qa --query "latest advances in transformer architecture"

# Patent search and details
python scripts/aminer_client.py --action patent_search --query "quantum computing"
```

您也可以直接调用单个API：
```bash
python scripts/aminer_client.py --action raw \
  --api paper_search --params '{"title": "BERT", "page": 0, "size": 5}'

# Or temporarily override the environment variable by explicitly passing --token
python scripts/aminer_client.py --token <TOKEN> --action raw \
  --api paper_search --params '{"title": "BERT", "page": 0, "size": 5}'
```

**原始模式错误预防规则（强制要求）**：
1. 在调用之前，验证函数签名（参数名称和类型必须完全匹配）；切勿通过语义来“猜测参数”。
2. 原始参数的约束由`references/api-catalog.md`规定；如果与现有知识冲突，始终以文档为准。
3. `paper_info`仅用于批量基本信息；参数必须为`{"ids": [...]}`。
4. `paper_detail`仅支持单篇论文的详细信息；参数必须为`{"paper_id": "..."}`。**切勿**传递`ids`。
5. 当需要多篇论文的详细信息时：首先使用低成本的接口进行过滤（例如`paper_info` / `paper_search_pro`），然后仅对目标子集调用`paper_detail`（如果用户未指定数量，则默认获取前10篇）。
6. 在执行之前，输出“要调用的函数名称 + 参数JSON”以便自我检查，然后再发起请求。

---

## 稳定性和故障处理策略（必读）

客户端`scripts/aminer_client.py`内置了请求重试和回退策略，以减少网络波动和临时服务错误对结果的影响。

- **超时和重试**
  - 默认请求超时：`30秒`
  - 最大重试次数：`3次`
  - 退避策略：指数级退避（`1秒 -> 2秒 -> 4秒`）+ 随机抖动
- **可重试的状态码**
  - `408 / 429 / 500 / 502 / 503 / 504`
- **不可重试的情况**
  - 常见的`4xx`错误（例如参数错误、认证问题）默认不会被重试；会直接返回错误信息。
- **工作流程回退**
  - 如果`paper_search`没有结果，`paper_deep_dive`会自动回退到`paper_search_pro`。
  - 如果`query`模式没有结果，`paper_qa`会自动回退到`paper_search_pro`。
- **可追踪的调用链**
  - 综合工作流程的输出会包含`source_api_chain`，标明生成结果所结合的API。

---

## 论文搜索API选择指南

当用户说“搜索论文”时，首先确定目标是“查找ID”、“过滤结果”、“问答”还是“生成分析报告”，然后选择相应的API：

| API | 重点 | 使用场景 | 成本 |
|---|---|---|---|
| `paper_search` | 标题搜索，快速获取`paper_id` | 知道论文标题，首先定位目标论文 | 免费 |
| `paper_search_pro` | 多条件搜索和排序（作者/机构/期刊/关键词） | 主题搜索，按引用次数或年份排序 | 每次调用0.01元 |
| `paper_qa_search` | 自然语言问答/主题关键词搜索 | 用户用自然语言描述需求；先进行语义搜索 | 每次调用0.05元 |
| `paper_list_by_search_venue` | 返回更完整的论文信息（适合分析） | 需要更丰富的字段进行分析/报告 | 每次调用0.30元 |
| `paper_list_by_keywords` | 多关键词批量检索 | 批量主题检索（例如AlphaFold + 蛋白质折叠） | 每次调用0.10元 |
| `paper_detail_by_condition` | 按年份和期刊维度检索详细信息 | 期刊年度监测，选择分析的期刊 | 每次调用0.20元 |

推荐路由（默认）：

1. **已知标题**：`paper_search -> paper_detail -> paper_relation`
2. **条件过滤**：`paper_search_pro -> paper_detail`
3. **自然语言问答**：`paper_qa_search`（如果没有结果则回退到`paper_search_pro`）
4. **期刊年度分析**：`venue_search -> venue_paper_relation -> paper_detail_by_condition`

补充规则（强烈推荐）：

1. **仅通过标题搜索**时，始终先使用`paper_search`（免费）来快速定位论文ID。
2. **对于复杂的语义检索**（自然语言、多条件、模糊表达），优先使用`paper_qa_search`。
3. 使用`paper_qa_search`时，首先将自然语言需求分解为结构化条件，然后再填写字段（例如年份、主题关键词、作者/机构等）。
4. `query`和`topic_high/topic_middle/topic_low`是**互斥的**：只能选择其中一个；不要同时传递。
5. 使用`query`模式时，直接输入自然语言字符串；使用`topic_*`模式时，先使用同义词/英文变体进行扩展。
6. 例如：查询“2012年的AI相关论文”：
   - `year` → `[2012]`
   - 选项A：`query` → `"artificial intelligence"`
   - 选项B：`topic_high` → `[["artificial intelligence","ai","Artificial Intelligence"]`（启用`use_topic`）

---

## 处理超出工作流程范围的请求（必需）

当用户的请求**不在上述6个工作流程范围内**，或者现有工作流程无法直接处理时，必须执行以下步骤：

1. 首先阅读`references/api-catalog.md`以确认可用的接口、参数约束和响应字段。
2. 根据用户的目标选择最合适的API，并设计最短可行的调用链（先定位ID，然后补充详细信息，再扩展关系）。
3. 如有必要，结合多个API来完成查询，并在结果中标注`source_api_chain`以明确数据来源路径。
4. 如果存在多种组合方式，优先选择成本较低、稳定性较高且能满足需求的组合。
5. 尽可能使用“最优查询组合”；避免无针对性的全量检索；先进行低成本搜索和过滤，然后再获取少量目标的详细信息。
6. 当结果数量较多且用户未指定数量时，默认只查询前10条详细信息并首先返回摘要；例如，当匹配到1000篇论文时，不要为全部1000篇论文调用详细信息API以降低用户成本。
7. 对于`raw`调用，需要进行参数级别的验证：例如`paper_info`使用`ids`，`paper_detail`使用`paper_id`；不要混淆它们。
8. 如果用户没有明确请求深入信息，优先使用免费路径（例如`paper_search` / `paper_info` / `venue_search`）；只有在确认免费路径不够用时才补充付费API。
9. 在返回最终实体列表时，必须包含相应的URL；如果实体ID缺失，在输出结果之前补充这些ID。

> 不要因为“没有合适的工作流程”就放弃查询；根据`api-catalog`积极完成API组合。

---

## 6个组合工作流程

### 工作流程1：学者个人资料

**使用场景**：了解学者的完整学术资料，包括个人简介、研究兴趣、发表的论文、专利和研究项目。

**调用链**：
```
Scholar search (name → person_id)
    ↓
Parallel calls:
  ├── Scholar details (bio/education/honors)
  ├── Scholar portrait (research interests/experience/work history)
  ├── Scholar papers (paper list)
  ├── Scholar patents (patent list)
  └── Scholar projects (research projects/funding info)
```

**命令**：
```bash
python scripts/aminer_client.py --token <TOKEN> --action scholar_profile --name "Yann LeCun"
```

**示例输出字段**：
- 基本信息：姓名、机构、标题、性别
- 个人简介（双语）
- 研究兴趣和领域
- 教育背景（结构化）
- 工作经验（结构化）
- 论文列表（ID + 标题）
- 专利列表（ID + 标题）
- 研究项目（标题/资助金额/日期）

---

### 工作流程2：论文深度分析

**使用场景**：根据论文标题或关键词检索完整的论文信息和引用关系。

**调用链**：
```
Paper search / Paper search pro (title/keyword → paper_id)
    ↓
Paper details (abstract/authors/DOI/journal/year/keywords)
    ↓
Paper citations (which papers this paper cites → cited_ids)
    ↓
(Optional) Batch retrieve basic info for cited papers
```

**命令**：
```bash
# Search by title
python scripts/aminer_client.py --token <TOKEN> --action paper_deep_dive --title "BERT"

# Search by keyword (using pro API)
python scripts/aminer_client.py --token <TOKEN> --action paper_deep_dive \
  --keyword "large language model" --author "Hinton" --order n_citation
```

---

### 工作流程3：机构分析

**使用场景**：分析机构的学者数量、论文产出和专利数量；适用于竞争性研究或合作伙伴评估。

**调用链**：
```
Org disambiguation pro (raw string → org_id, handles alias/full-name differences)
    ↓
Parallel calls:
  ├── Org details (description/type/founding date)
  ├── Org scholars (scholar list)
  ├── Org papers (paper list)
  └── Org patents (patent ID list, supports pagination, up to 10,000)
```

> 如果多个机构名称相同，机构搜索会返回候选列表；使用机构消歧功能进行精确匹配。

**命令**：
```bash
python scripts/aminer_client.py --token <TOKEN> --action org_analysis --org "MIT"
# Specify raw string (with abbreviation/alias)
python scripts/aminer_client.py --token <TOKEN> --action org_analysis --org "Massachusetts Institute of Technology, CSAIL"
```

---

### 工作流程4：特定期刊的论文

**使用场景**：追踪特定年份在特定期刊上发表的论文；适用于投稿研究或研究趋势分析。

**调用链**：
```
Venue search (name → venue_id)
    ↓
Venue details (ISSN/type/abbreviation)
    ↓
Venue papers (venue_id + year → paper_id list)
    ↓
(Optional) Batch paper detail query
```

**命令**：
```bash
python scripts/aminer_client.py --token <TOKEN> --action venue_papers --venue "NeurIPS" --year 2023
```

---

### 工作流程5：论文问答搜索

**使用场景**：使用自然语言或结构化关键词智能搜索论文；支持SCI过滤、基于引用的排序、作者/机构限制。

**核心API**：`Paper QA Search`（每次调用0.05元），支持：
- `query`：自然语言问题；系统会自动将其分解为关键词
- `topic_high/middle/low`：细粒度的关键词权重控制（嵌套数组OR/AND逻辑）
- `sci_flag`：仅显示SCI论文
- `force_citation_sort`：按引用次数排序
- `force_year_sort`：按年份排序
- `author_terms / org_terms`：按作者名称或机构名称过滤
- `author_id / org_id`：按作者ID或机构ID过滤（推荐用于消歧）
- `venue_ids`：按会议/期刊ID列表过滤

**命令**：
```bash
# Natural language Q&A
python scripts/aminer_client.py --token <TOKEN> --action paper_qa \
  --query "deep learning methods for protein structure prediction"

# Fine-grained keyword search (must contain A and B, bonus for C)
python scripts/aminer_client.py --token <TOKEN> --action paper_qa \
  --topic_high '[["transformer","self-attention"],["protein folding"]]' \
  --topic_middle '[["AlphaFold"]]' \
  --sci_flag --sort_citation
```

---

### 工作流程6：专利分析

**使用场景**：在特定技术领域搜索专利，或检索学者/机构的专利组合。

**单独搜索的调用链**：
```
Patent search (query → patent_id)
    ↓
Patent details (abstract/filing date/application number/assignee/inventor)
```

**通过学者/机构搜索的调用链**：
```
Scholar search → Scholar patents (patent_id list)
Org disambiguation → Org patents (patent_id list)
    ↓
Patent info / Patent details
```

**命令**：
```bash
python scripts/aminer_client.py --token <TOKEN> --action patent_search --query "quantum computing chip"
python scripts/aminer_client.py --token <TOKEN> --action scholar_patents --name "Shou-Cheng Zhang"
```

---

## 单个API快速参考

> 有关完整的参数描述，请阅读`references/api-catalog.md`

| # | 名称 | 方法 | 价格 | API路径（基础域名：datacenter.aminer.cn/gateway/open_platform） |
|---|------|------|------|------|
| 1 | 论文问答搜索 | POST | 0.05元 | `/api/paper/qa/search` |
| 2 | 学者搜索 | POST | 免费 | `/api/person/search` |
| 3 | 论文搜索 | GET | 免费 | `/api/paper/search` |
| 4 | 论文搜索高级版 | GET | 0.01元 | `/api/paper/search/pro` |
| 5 | 专利搜索 | POST | 免费 | `/api/patent/search` |
| 6 | 机构搜索 | POST | 免费 | `/api/organization/search` |
| 7 | 机构搜索 | POST | 免费 | `/api/venue/search` |
| 8 | 学者详情 | GET | 1.00元 | `/api/person/detail` |
| 9 | 学者项目 | GET | 3.00元 | `/api/project/person/v3/open` |
| 10 | 学者论文 | GET | 1.50元 | `/api/person/paper/relation` |
| 11 | 学者专利 | GET | 1.50元 | `/api/person/patent/relation` |
| 12 | 学者肖像 | GET | 0.50元 | `/api/person/figure` |
| 13 | 论文信息 | POST | 免费 | `/api/paper/info` |
| 14 | 论文详情 | GET | 0.01元 | `/api/paper/detail` |
| 15 | 论文引用 | GET | 0.10元 | `/api/paper/relation` |
| 16 | 专利信息 | GET | 免费 | `/api/patent/info` |
| 17 | 专利详情 | GET | 0.01元 | `/api/patent/detail` |
| 18 | 机构详情 | POST | 0.01元 | `/api/organization/detail` |
| 19 | 机构专利 | GET | 0.10元 | `/api/organization/patent/relation` |
| 20 | 机构学者 | GET | 0.50元 | `/api/organization/person/relation` |
| 21 | 机构论文 | GET | 0.10元 | `/api/organization/paper/relation` |
| 22 | 机构详情 | POST | 0.20元 | `/api/venue/detail` |
| 23 | 机构论文 | POST | 0.10元 | `/api/venue/paper/relation` |
| 24 | 机构消歧 | POST | 0.01元 | `/api/organization/na` |
| 25 | 机构消歧高级版 | POST | 0.05元 | `/api/organization/na/pro` |
| 26 | 按期刊搜索论文 | GET | 0.30元 | `/api/paper/list/by/search/venue` |
| 27 | 论文批量查询 | GET | 0.10元 | `/api/paper/list/citation/by/keywords` |
| 28 | 按年份和期刊查询论文详情 | GET | 0.20元 | `/api/paper/platform/allpubs/more/detail/by/ts/org/venue` |

---

## 参考资料

- 完整的API参数文档：请阅读`references/api-catalog.md`
- Python客户端源代码：`scripts/aminer_client.py`
- 测试用例：`evals/evals.json`
- 官方文档：https://open.aminer.cn/open/docs
- 控制台：https://open.aminer.cn/open/board?tab=control