---
name: arxiv-search-collector
description: "基于模型的arXiv检索工作流程：用于构建包含手动语言参数的论文集。具体步骤如下：  
1. 初始化检索过程；  
2. 为每个模型设计的查询获取元数据；  
3. 让模型根据索引过滤掉不相关的项目；  
4. 将过滤后的结果合并并去重，存储到每篇论文对应的元数据目录中。  
该流程适用于需要通过模型而非基于规则的启发式方法来进行查询规划和相关性过滤的场景。"
---

# ArXiv搜索收集器

当您需要基于模型的查询规划以及基于模型的相关性筛选时，请使用此技能。

## 核心原则

脚本只是工具，真正的推理和决策由模型完成：

1. 将原始主题扩展为多个具体的查询。
2. 对每个查询执行一次数据获取操作。
3. 读取每个查询的结果列表，并决定哪些索引需要保留。
4. 使用一个脚本合并保留的条目并去除重复项。

## 第1步：初始化运行

```bash
python3 scripts/init_collection_run.py \
  --output-root /path/to/data \
  --topic "LLM applications in Lean 4 formalization" \
  --keywords "Lean 4,LLM,formalization" \
  --categories "cs.AI,cs.LO" \
  --target-range 5-10 \
  --lookback 30d \
  --language English
```

此步骤会创建一个运行目录，其中包含`task_meta.json`、`task_meta.md`、`query_results/`和`query_selection/`。

## 语言参数

- `--language`参数必须为每次数据收集操作手动设置。
- 为了保持一致性，请在所有收集器脚本中使用相同的语言值。
- 如果`--language`设置为非英语（例如“Chinese”），生成的Markdown文件将使用该语言：
  - `task_meta.md`
  - `query_results/<label>.md`
  - `<arxiv_id>/metadata.md`
  - `papers_index.md`

## 查询编写规则

在运行每个查询之前，请遵循以下规则：

1. 根据最终的目标范围确定查询数量。
- 对于小型/中型目标（2-5篇或5-10篇论文），建议使用3个查询。
- 对于大型目标（10篇以上），建议使用4个查询。
- 避免编写太多质量较低的查询。
2. 为每个查询分配目标数量，然后进行过采样。
- 设定`target_max`为目标范围的上限。
- 计算`target_per_query = ceil(target_max / query_count)`。
- 使用`max_results = target_per_query * 2`来获取每个查询的结果（如果召回率更重要，可以设置为`* 3`）。
- 例如：目标范围为5-10篇论文，查询数量为3个，则`target_per_query=4`，每个查询将获取8-12篇论文。
3. 保留一个原始主题的查询，然后添加规范化的术语或同义词扩展。
- 第一个查询保留原始的主题表述。
- 其余查询使用规范化的术语和近义词。
- 优先选择符合arXiv索引规则的简洁名词短语。
4. 在同一语义组内使用`OR`连接同义词，在不同语义组之间使用`AND`连接。
- 同一组的同义词应使用`OR`连接以提高召回率。
  - 例如：组A（模型相关术语）：`LLM OR "大型语言模型" OR AI`。
- 组B（特定领域术语）：`"Lean 4" OR Lean OR "形式化语言"`。
- 不同语义组之间应使用`AND`连接以保持相关性。
  - 例如：`(LLM-group) AND (Lean-group)`。
- 推荐的模式：
  - `(<领域术语 AND OR>) AND (<方法/模型术语 AND OR>) [AND <可选约束条件>]`

### 查询示例（适用于arXiv API）

**主题A：LLM在Lean 4形式化中的应用**
- `all:"LLM applications in Lean 4 formalization"`
- `(all:"Lean 4" OR all:"Lean" OR all:"formal language") AND (all:"LLM" OR all:"large language model" OR all:"AI")`
- `(all:"Lean" OR all:"formalization") AND (all:"LLM" OR all:"large language model") AND all:"theorem proving"`
- `(all:"Lean" OR all:"proof assistant") AND (all:"AI" OR all:"LLM")`

**主题B：用于代码生成的智能工具**
- `all:"agentic tool use code generation"`
- `(all:"agentic" OR all:"autonomous agent") AND (all:"LLM" OR all:"large language model")`
- `(all:"tool use" OR all:"function calling") AND (all:"coding assistant" OR all:"code generation")`

**主题C：多模态推理与检索**
- `all:"multimodal reasoning retrieval"`
- `(all:"multimodal" OR all:"vision language") AND (all:"retrieval" OR all:"RAG")`
- `(all:"multimodal model" OR all:"vision language model") AND (all:"reasoning" OR all:"tool use")`

## 第2步：一次获取一个查询

模型会手动定义查询，例如：

- `all:"Lean 4"`
- `all:"LLM formalization"`
- `all:"AI formal verification"`

**推荐的批量模式（安全默认设置，串行执行）**

```bash
python3 scripts/fetch_queries_batch.py \
  --run-dir /path/to/run-dir \
  --plan-json /path/to/query_plan.json
```

在批量模式下，脚本会自动应用以下设置：
- 串行调用API
- `--min-interval-sec 5`（最小间隔时间）
- `--retry-max 4`（最大重试次数）
- `--retry-base-sec 5`（基础重试间隔）
- `--retry-max-sec 120`（最大重试间隔）
- `--retry-jitter-sec 1`（重试抖动时间）
- 通过`<run_dir>/.runtime/arxiv_api_state.json`文件来控制执行速率
- 根据`target_range`和查询数量自动设置`max_results`（默认过采样率为2倍，上限为60）
- 从`task_meta.json`中获取默认的语言/分类信息

`query_plan.json`文件至少需要包含`label`和`query`字段。
通常不需要手动设置`fetch-control`参数。

如果您需要逐个手动获取查询，请运行以下代码：

```bash
python3 scripts/fetch_query_metadata.py \
  --run-dir /path/to/run-dir \
  --label lean4 \
  --query 'all:"Lean 4"' \
  --max-results 30 \
  --min-interval-sec 5 \
  --retry-max 4 \
  --language English
```

输出文件：
- `query_results/<label>.json`（包含完整元数据的索引列表）
- `query_results/<label>.md`（人类可读的预览文件）

日期范围直接通过`submittedDate:[... TO ...]`参数传递给arXiv API的`search_query`方法。
不会进行第二次本地日期过滤。

`fetch_query_metadata.py`文件中的速率限制控制参数：
- `--min-interval-sec`（默认值5.0秒）
- `--retry-max`（默认值4）
- `--retry-base-sec`（默认值5.0秒）
- `--retry-max-sec`（默认值120.0秒）
- `--retry-jitter-sec`（默认值1.0秒）
- `--rate-state-path`（可选参数；默认值为`<run_dir>/.runtime/arxiv_api_state.json`）
- `--force`（强制参数；用于绕过缓存并重新获取数据）

## 第3步：模型过滤相关性

对于每个查询结果列表，模型会读取索引结果并决定哪些结果需要保留。

在合并结果时，可以使用索引和/或arXiv ID来指定保留的条件。
如果希望在后续迭代中排除某个查询结果，可以在`selection-json`中将该查询的标签设置为空列表。

## 第4步：合并和去重

```bash
python3 scripts/merge_selected_papers.py \
  --run-dir /path/to/run-dir \
  --keep lean4:0,2,4 \
  --keep llm-formalization:1,3 \
  --language English
```

或者使用`selection-json`文件来指定保留条件：

```json
{
  "lean4-round1": [0, 2, 4],
  "lean4-round2": [],
  "formalization-round2": [1, 3, 5]
}
```

如果`selection-json`中的列表为空，表示该查询被有意排除（即`keep`字段的值为0）。

最终输出文件包括：
- `<arxiv_id>/metadata.json`
- `<arxiv_id>/metadata.md`
- `papers_index.json`
- `papers_index.md`

## 第5步：迭代重试循环（增量式处理）

如果相关性较低或在第4步后的结果数量不足，可以执行迭代处理：

1. 查看`papers_index.md`和每篇论文的元数据质量。
2. 调整查询计划（通常通过添加更多的同义词`OR`条件或保留跨组的`AND`条件来扩大查询范围）。
3. 使用新的查询标签获取更多结果。
4. 以增量模式重新执行合并操作：

```bash
python3 scripts/merge_selected_papers.py \
  --run-dir /path/to/run-dir \
  --incremental \
  --selection-json /path/to/updated_selection.json \
  --language English
```

增量处理的流程如下：
- 从`query_selection/selected_by_query.json`中加载之前的查询标签选择。
- 新的`selection-json`中提供的标签会覆盖之前的选择。
- 可以添加新的标签。
- 通过将标签设置为`[]`来移除旧的标签。

当满足以下条件时停止重试：
- 相关性达到可接受的水平，或者
- 新的查询主要获取到低相关性的论文。

如果相关论文确实很少，可以接受最终的结果数量低于最初的目标范围。

## 注意事项

- 通过控制查询数量和`--max-results`参数来保守地使用API并发。
- 在第一阶段，每个查询的获取操作都是串行的（不允许并行调用API）。
- 默认情况下会重用缓存；只有在必要时才使用`--force`参数。
- 建议使用默认的运行时状态文件，以便同一阶段的各个步骤共享相同的冷却/限制策略。
- 如果arXiv API返回`429 Too Many Requests`错误，可以稍后重试或增加`--min-interval-sec`参数。
- 优先使用具体且精确的查询条件，让模型进行更严格的筛选。
- 请参考`references/io-contract.md`文件以获取详细的文件和数据结构信息。

## 相关技能

此技能是`arxiv-summarizer-orchestrator`的子技能。

**在处理流程中的位置**：
1. 第1步（数据收集）：`arxiv-search-collector`（此技能）
2. 第2步（论文处理）：`arxiv-paper-processor`
3. 第3步（批量报告）：`arxiv-batch-reporter`

此技能负责生成第二阶段和第三阶段所需的初始论文集结构和元数据。