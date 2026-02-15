---
name: seo-ranker
description: 这是一项用于端到端SEO审计和页面优化的元技能，它通过整合brave-search、summarize、api-gateway和markdown-converter等工具来实现。当用户想要了解某个页面为何未能在目标关键词上获得排名，并需要具体的改写建议以及反向链接分析数据时，可以使用这项技能。
homepage: https://clawhub.ai
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"📈","requires":{"bins":["node","npx","summarize","uvx"],"env":["BRAVE_API_KEY","MATON_API_KEY","OPENAI_API_KEY","ANTHROPIC_API_KEY","XAI_API_KEY","GEMINI_API_KEY"],"config":[]},"note":"Requires local installation of brave-search, summarize, api-gateway, and markdown-converter. At least one summarize model API key must be present."}}
---

# 目的

执行一个完整的SEO排名诊断和优化流程：
1. 检查实时的搜索引擎结果页（SERP）竞争情况；
2. 将竞争对手的内容结构与用户提供的内容进行比较；
3. 在能够通过API访问的情况下，补充难度数据及反向链接信息；
4. 生成具体的重写指导以及优化后的Markdown草稿。

这是一个协调性技能，它不能替代上游工具。

# 必需安装的技能

- `brave-search`（最新版本：`1.0.1`）
- `summarize`（最新版本：`1.0.0`）
- `api-gateway`（最新版本：`1.0.29`）
- `markdown-converter`（最新版本：`1.0.0`）

安装/更新：

```bash
npx -y clawhub@latest install brave-search
npx -y clawhub@latest install summarize
npx -y clawhub@latest install api-gateway
npx -y clawhub@latest install markdown-converter
npx -y clawhub@latest update --all
```

验证：

```bash
npx -y clawhub@latest list
```

# 必需的凭证

- `BRAVE_API_KEY`（用于`brave-search`）
- `MATON_API_KEY`（用于`api-gateway`）
- 选择一个`summarize`模型密钥：
  - `OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`XAI_API_KEY`或`GEMINI_API_KEY`

可选：
- `FIRECRAWL_API_KEY`（用于通过`summarize`提取难度较高的页面信息）
- `APIFY_API_TOKEN`（在`summarize`中作为YouTube数据的备用方案）

# 预飞行检查（Preflight Check）

**强制要求：**
- 如果缺少任何凭证，切勿默默失败。必须返回一个`MissingAPIKeys`部分，列出缺失的变量及被阻塞的步骤。
- 继续执行未受阻的步骤，并在必要时明确标记输出为“部分完成”（Partial）。

# 用户需要首先提供的输入信息

- `target_url`（目标网址）
- `target_keyword`（示例关键词：`AI tools`）
- `region_locale`（用于SERP解析的国家/语言）
- `content_source`（内容来源：URL、粘贴的文本或文件路径）
- `content_type`（内容类型：`blog`、`category page`、`product page`、`landing page`）
- `business_goal`（业务目标：`traffic`、`leads`、`sales`）
- `rewrite_scope`（重写范围：`light`、`moderate`、`full`）
- `data_provider_preference`（数据提供者偏好：`semrush`、`ahrefs`、`gsc-only`、`none`）

在明确关键词意图和内容目标之前，不要开始重写操作。

# 工具职责

## brave-search

用于实时SERP侦察：
- 获取目标关键词的顶级搜索结果；
- 识别主要竞争对手及搜索意图模式；
- 收集候选URL以进行进一步分析。

**操作限制：**
- 需要`BRAVE_API_KEY`；
- 支持使用`--content`选项提取内容。

## summarize

用于分析竞争对手的结构化内容：
- 概括每个顶级URL的内容；
- 提取标题结构（H1-H4）、主题覆盖范围、实体使用频率；
- 评估内容深度和修辞风格差异。

**操作限制：**
- 需要一个支持的模型API密钥；
- 支持使用`--extract-only`、`--json`和长度控制选项。

## api-gateway

仅在存在有效连接时，用于外部SEO数据API：
- 提供关键词难度信息、反向链接域名、竞争对手链接交叉情况以及搜索性能数据。

**操作限制：**
- 需要`MATON_API_KEY`；
- 每个应用都需要激活的OAuth连接（`ctrl.maton.ai`连接生命周期管理）；
- 仅凭API密钥无法访问第三方数据。

**重要提示：**
- 在`api-gateway`的服务列表中，`semrush`和`ahrefs`并未作为原生应用名称列出；
- 如果用户已经拥有这些服务的有效连接路径，可以直接使用Semrush/Ahrefs的集成；否则需使用其他可用的SEO工具（例如`google-search-console`）或手动提取竞争对手链接。

## markdown-converter

用于将用户提供的内容转换为可编辑的Markdown格式：
- 将输入的文档/文件转换为Markdown格式（使用`uvx markitdown ...`命令）；
- 保留标题、列表和表格格式，以便进行精确的重写。

# 标准的因果信号链（Canonical Causal Signal Chain）

1. **输入阶段**：用户提供URL和目标关键词（如需要，还需提供内容来源）。
2. **SERP审计阶段（brave-search）**：获取实时的SERP数据并识别前三名竞争对手。
3. **竞争对手内容阶段（summarize）**：分析主要竞争对手的URL，包括：
  - 标题层次结构
  - 主题覆盖范围和实体使用情况
  - 统计数据的运用及证据
  - 句子复杂度和内容长度。
4. **数据获取阶段（api-gateway）**：检查是否可以获取所需的数据；
  - 如果关键词难度或反向链接数据不可用，请求用户提供凭证或连接信息，并切换到备用方案。

**面向用户的提示信息格式：**
- `DataGateStatus`：数据可用/被阻塞
- `Reason`：缺少凭证、连接失败或数据提供者不支持
- `Action`：下一步的具体操作及相关链接

**截至2026年2月14日的信息：**
- Semrush在其官方网站上主要提供7天试用套餐；
- Semrush的14天试用通常与某些插件或合作伙伴优惠相关。

**用户请求14天试用时：**
- 首先询问用户希望使用的联盟链接/推荐链接；
- 如果用户未提供，分享Semrush的官方试用页面：`https://www.semrush.com/sem/`；
- 可以提供Ahrefs的免费试用链接（适用于已验证的网站）：`https://ahrefs.com/webmaster-tools`。

5. **优化阶段（LLM重写）**：
- 根据意图和主题完整性重写用户内容；
- 添加相关的自然词汇（符合LSI（链接构建）原则；
- 优化标题标签和元描述；
- 改进标题结构和内部链接。

6. **输出阶段**：
- 提供优化后的Markdown文档；
- 提供优先级的行动清单；
- 提供至少5个反向链接来源（附带置信度标签）。

# 重写原则

- 保持事实的准确性（不要捏造统计数据或案例研究）；
- 优先考虑语义上的覆盖范围，而非单纯填充关键词；
- 保持关键词使用的自然性和与意图的一致性；
- 添加易于阅读的结构（清晰的H2/H3标题、简洁的段落、可操作的列表项）。

# 输出内容

必须返回以下信息：
- `SERPFindings`：主要竞争对手、观察到的搜索意图模式、用户页面与竞争对手在结构/内容上的差距；
- `DataGateStatus`：数据提供者的状态、凭证/连接情况；
- `OptimizedMarkdown`：完全重写的文档、修改后的标题和元描述；
- `BacklinkOpportunities`：竞争对手使用的5个反向链接来源及替代方案；
- `NextActions`：具体的实施步骤（按顺序排列）。

# 质量控制

在最终输出之前，需验证以下内容：
- 主要竞争对手列表来自实时的SERP数据，而非内存中的数据；
- 重写内容符合检测到的搜索意图；
- 不得伪造引用或反向链接信息；
- 关键词的放置要自然（避免重复或垃圾信息）；
- 明确披露任何数据缺失的情况。

**故障处理规则：**
- 如果缺少`BRAVE_API_KEY`，返回`MissingAPIKeys`，跳过SERP阶段，并请求用户提供竞争对手的URL；
- 如果缺少`summarize`模型密钥，返回`MissingAPIKeys`，跳过`summarize`阶段，并使用可用片段进行结构审计；
- 如果缺少`MATON_API_KEY`，返回`MissingAPIKeys`，跳过`api-gateway`的数据补充步骤，继续进行仅针对页面本身的优化；
- 如果`api-gateway`连接失败（例如400错误），保持流程以备用模式运行，并提供详细的连接设置步骤；
- 如果使用的服务（如Semrush/Ahrefs）不支持，需说明限制并切换到GSC/手动模式。

**注意事项：**
- 从不保证排名结果；
- 不得将备用方案的结果视为经过服务提供商验证的数据；
- 不得隐瞒任何依赖关系的故障；
- 建议要具体、可衡量，并基于实际的SERP情况提出。