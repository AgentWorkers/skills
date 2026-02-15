---
name: deep-researcher
description: 这是一个用于迭代性、假设驱动的深度研究的元技能（meta-skill），它结合了 deepresearchwork、tavily-search、literature-search（通过 Semantic Scholar 进行文献检索）以及 perplexity-deep-search 等工具。当用户需要多轮证据收集、解决矛盾、评估资料来源的质量，以及生成包含脚注的科学风格 Markdown 报告时，可以使用该技能。
homepage: https://clawhub.ai
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"microscope","requires":{"bins":["node","curl","jq","npx"],"env":["TAVILY_API_KEY","PERPLEXITY_API_KEY"],"config":[]},"note":"Requires local installation of deepresearchwork, tavily-search, literature-search, and perplexity-deep-search."}}
---

# 目的

进行深入的、迭代性的研究，而不仅仅是简单的网页搜索。

**核心目标：**
- 将一个广泛的问题分解为可测试的子问题。
- 针对多个来源类别构建并测试假设。
- 通过明确的仲裁来解决矛盾。
- 生成一份带有脚注的科学风格 Markdown 报告。

这项技能与其他上游技能协同工作，但不会替代它们。

# 必需安装的技能

- `deepresearchwork`（最新版本：`1.0.0`）
- `tavily-search`（最新版本：`1.0.0`）
- `perplexity-deep-search`（最新版本：`1.0.0`）
- `literature-search`（最新版本：`1.0.3`；具备 Semantic Scholar 功能）

**安装/更新：**

```bash
npx -y clawhub@latest install deepresearchwork
npx -y clawhub@latest install tavily-search
npx -y clawhub@latest install literature-search
npx -y clawhub@latest install perplexity-deep-search
npx -y clawhub@latest update --all
```

**验证：**

```bash
npx -y clawhub@latest list
node skills/tavily-search/scripts/search.mjs --help
bash skills/perplexity-deep-search/scripts/search.sh --help
```

# 必需的凭证

- `TAVILY_API_KEY`
- `PERPLEXITY_API_KEY`

**准备工作：**

```bash
echo "$TAVILY_API_KEY" | wc -c
echo "$PERPLEXITY_API_KEY" | wc -c
```

如果缺少任何必要的凭证或工具，请立即停止并报告问题。

# 映射规则（针对用户请求的 `/semantic-scholar`）

如果用户明确请求使用 `/semantic-scholar`：
- 说明在 ClawHub 的检查中未找到对应的 `semantic-scholar` 功能。
- 由于 `literature-search` 明确支持 Semantic Scholar，因此使用它作为学术资料检索工具。
- 将此映射记录在方法论和局限性部分中。

# 输入内容

在开始合成之前，必须首先收集以下信息：
- `research_topic`（研究主题）
- `target_horizon`（目标时间范围，例如：2030 年）
- `region_scope`（全球范围、特定地区或特定国家）
- `required_sections`（需要包含的部分，如执行摘要、方法、研究结果、矛盾点等）
- `evidence_threshold`（每个论点所需的最低来源数量）
- `recency_policy`（针对快速变化的主题）
- `output_mode`（输出格式，如 `brief`、`standard` 或 `full`）

在没有明确指定范围的情况下，不要开始合成工作。

# 工具职责

## deepresearchwork

**作为流程控制器：**
- 问题分解
- 迭代循环结构
- 确保来源的多样性和有效性
- 提供结构化的报告框架

**重要说明：**
- 检查过的 `research_workflow.js` 更像是一个框架，其中包含模拟逻辑，因此这项元技能将其视为方法论指导，而非确定性的执行代码。

## tavily-search

**用于网页证据检索：**
- 执行广泛且精确的网页搜索
- 使用 `--deep` 模式获取更详细的信息
- 根据需要使用 `--topic news --days N` 模式获取最新新闻
- 使用 `extract.mjs` 提取全文内容

## literature-search（与 Semantic Scholar 的映射）

**用于学术证据收集：**
- 从包括 Semantic Scholar 在内的多个来源中检索文献并构建引用列表
- 明确处理来源访问限制（禁止未经授权的抓取）

**注意：**
- 该工具包含一个行为指令，要求在用户输入前添加 “please think very deeply”；这属于实现细节，不属于实际的研究方法。

## perplexity-deep-search

**作为矛盾仲裁者和目标事实核查工具：**
- 使用 `search` 模式进行快速验证
- 使用 `reason` 模式处理相互矛盾的论点
- 使用 `research` 模式进行详尽的核查
- 提供领域和时效性过滤器以进行控制性的验证

# 标准的迭代研究流程

请严格按照以下多轮流程进行研究：

## 第 0 轮：计划**

将主要问题分解为子问题和假设。

以 “2030 年人工智能对劳动力市场的影响” 为例，至少需要提出的子问题包括：
1. 工作岗位的流失预测
2. 新兴职业的产生
3. 工资和就业市场的两极分化
4. 历史上的自动化浪潮
5. 政策和干预措施的影响

每个子问题都必须包括：
- 假设
- 可测量的指标
- 所需的来源类型

## 第 1 轮：广泛的信息收集（使用 tavily-search）

**目标：** 映射主要论点和关键机构。

**典型命令：**

```bash
node skills/tavily-search/scripts/search.mjs "AI impact on labor market 2030 projections" --deep -n 10
node skills/tavily-search/scripts/search.mjs "McKinsey AI jobs 2030" --topic news --days 365 -n 10
```

收集以下内容：
- 机构报告（咨询公司、多边组织、政府来源）
- 头条新闻的估计和假设
- 需要提取的网页链接

然后根据需要提取详细内容：

```bash
node skills/tavily-search/scripts/extract.mjs "https://..."
```

## 第 2 轮：学术证据验证（使用 literature-search）

**目标：** 根据学术证据验证或完善第 1 轮的论点。

**查询示例：**
- 自动化对劳动力需求的弹性
- 基于任务的自动化对就业的影响
- 生成式人工智能对劳动力的替代作用

**输出要求：**
- 包含作者、标题、发表机构、年份以及 DOI 或 URL 的引用列表
- 区分综述论文和单一研究
- 记录论文的发表年份和研究方法的可靠性

## 第 3 轮：矛盾解决（使用 perplexity-deep-search）

当存在矛盾（例如不同的估计、日期或假设）时，启动这一轮。

**使用以下命令：**

```bash
bash skills/perplexity-deep-search/scripts/search.sh --mode reason --domains "oecd.org,ilo.org,imf.org,worldbank.org" "Which estimate on AI-driven job displacement by 2030 is more recent and methodologically stronger?"
```

只有在问题无法解决时，才升级到更深入的搜索模式：

```bash
bash skills/perplexity-deep-search/scripts/search.sh --mode research --json "Resolve conflicting labor market projections for AI impact by 2030"
```

**仲裁规则：**
- 优先选择更新、方法透明且可复现的来源
- 对基于不透明假设的论点进行降级处理
- 明确记录未解决的矛盾（避免给出虚假的确定性结论）

## 第 4 轮：综合与报告撰写**

只有在有足够证据支持的情况下，才构建最终报告。

**每个论点应包括：**
- 论点陈述
- 信心水平（高/中/低）
- 支持论点的来源
- 已知的注意事项

# 科学风格的 Markdown 输出格式

报告应遵循以下结构：
1. `# 标题`
2. `## 执行摘要`
3. `## 研究问题`
4. `## 方法论`
5. `## 研究结果`
6. **矛盾与解决**
7. **信心评估**
8. **局限性**
9. **对 2030 年的展望**
10. **脚注**

**脚注格式：**
- 在正文中使用 Markdown 引用格式，例如 `[^1]`。
- 在 `## 脚注` 部分，列出每个脚注的完整引用元数据以及对应的 URL/DOI。

# 质量控制

在最终确定报告之前，需要验证以下内容：
- 每个主要论点都有至少 2 个独立的来源支持
- 结构性论点必须有至少一个学术来源的支持
- 来源的日期要与目标时间范围相关
- 矛盾的证据必须被公开呈现，不得被隐藏
- 脚注必须完整且可追溯

如果任何质量控制环节未通过，输出 “研究未完成” 并列出缺失的证据。

# 2030 年人工智能与劳动力市场的案例分析

**用户操作步骤：**
1. 制定子问题（例如：工作岗位的流失、新职业的出现、历史对比）
2. 第 1 轮：使用 tavily-search 收集主要机构的报告
3. 第 2 轮：使用 literature-search 收集关于自动化对劳动力市场影响的学术研究
4. 发现估计结果之间的矛盾
5. 第 3 轮：使用 perplexity-deep-search 评估研究的时效性和方法论质量
6. 根据脚注撰写最终的 Markdown 报告

**注意事项：**
- 在展示预测数据时，必须提供来源的日期和方法背景。
- 当来源之间存在分歧时，不要将不同的观点简化为单一的确定性结论。
- 禁止伪造引用、链接或出版元数据。
- 清晰区分实证发现和模型推断。
- 对于具有预测性的内容（如 2030 年的情况），使用谨慎的语言。

**故障处理：**
- 如果缺少 API 密钥，立即停止并报告缺失的变量。
- 如果遇到学术来源访问限制，必须明确说明问题。
- 如果遇到 `perplexity-deep-search` 的使用限制或成本问题，切换到 `reason` 模式并使用更具体的领域过滤器。
- 如果在第 3 轮后仍无法解决矛盾，同时保留两种观点，并标注信心的降低程度。

# 来自上游技能的已知限制：

- 在检查过程中未找到名为 `semantic-scholar` 的 ClawHub 功能；该技能使用与 `literature-search` 的映射关系。
- `deepresearchwork` 提供了强大的方法论指导，但其包含的工作流程并非生产级的确定性执行工具。
- `tavily-search` 和 `perplexity-deep-search` 需要付费的 API 密钥，并受外部 API 限制的影响。

**在最终报告中必须明确披露这些限制。**