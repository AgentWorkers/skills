---
name: scholargraph
description: 这是一个学术文献智能工具包，用于多源论文的搜索、分析以及借助人工智能（AI）技术构建知识图谱。
metadata:
  openclaw:
    emoji: "📚"
    version: "1.0.0"
    source:
      type: github
      url: https://github.com/Josephyb97/ScholarGraph
      license: MIT
    requires:
      bins:
        - bun
      optionalBins:
        - python3
      env:
        - AI_PROVIDER
      optionalEnv:
        - OPENAI_API_KEY
        - DEEPSEEK_API_KEY
        - QWEN_API_KEY
        - ZHIPU_API_KEY
        - SERPER_API_KEY
        - NCBI_API_KEY
        - IEEE_API_KEY
        - CORE_API_KEY
        - UNPAYWALL_EMAIL
        - CROSSREF_MAILTO
        - SERPAPI_KEY
    install:
      command: bun install
      verify: bun run cli.ts --help
    security:
      network: true
      filesystem: true
      llmPrompts: true
      notes: |
        - Makes API calls to academic sources (arXiv, Semantic Scholar, etc.)
        - Stores data in local SQLite database
        - Uses custom LLM system prompts for structured output
        - Optional Python dependencies (pymupdf, python-pptx) for PDF/PPT features
---
# ScholarGraph - 学术文献智能工具包

## 概述

ScholarGraph 是一个全面的学术文献智能工具包，它利用人工智能技术帮助研究人员高效地搜索、分析和管理学术论文。该工具包支持11个学术搜索来源，并具备基于领域的智能来源选择功能以及PDF下载能力。

## 安全性与隐私

该工具包的运行权限如下：

- **网络访问**：查询学术API（arXiv、Semantic Scholar、OpenAlex、PubMed、CrossRef、DBLP、IEEE、CORE、Google Scholar、Unpaywall）和网络搜索服务
- **文件系统**：读取/写入配置文件、下载PDF文件、将知识图谱存储在SQLite数据库（`data/knowledge-graphs.db`中）
- **大语言模型（LLM）集成**：向AI提供商发送自定义系统提示以获取结构化的JSON输出（如概念提取、论文分析等）
- **可选的Python**：PDF图表提取（`pymupdf`）和PPT导出（`python-pptx`）需要Python 3.8或更高版本

**数据存储**：所有数据均存储在本地，不会收集任何遥测数据或分析信息。

**API密钥**：可选的API密钥仅用于相应的服务，且不会被传输到其他地方。

**源代码**：遵循MIT许可证，开源代码位于 [https://github.com/Josephyb97/ScholarGraph](https://github.com/Josephyb97/ScholarGraph)。

## 功能

### 核心模块（6个）

1. **文献搜索** - 多来源学术论文发现（11个来源）
   - **免费来源**：arXiv、Semantic Scholar、OpenAlex（2.5亿篇以上）、PubMed（生物医学）、CrossRef（1.5亿个DOI）、DBLP（计算机科学）、网络搜索
   - **需要API密钥的来源**：IEEE Xplore、CORE、Google Scholar（SerpAPI）、Unpaywall（开放获取PDF）
   - 基于适配器的插件架构，便于扩展
   - 自动检测领域并采用互补的搜索策略（生物医学/计算机科学/工程/物理学）
   - 根据领域优先级选择搜索来源
   - 通过多种策略解析URL以获得更好的搜索结果
   - 支持PDF下载

2. **概念学习器** - 快速构建知识框架
   - 生成结构化的学习卡片
   - 包含代码示例和相关论文
   - 支持初级/中级/高级的学习深度

3. **知识缺口检测器** - 主动识别知识盲点
   - 分析特定领域的知识覆盖情况
   - 识别关键、推荐和可选的知识缺口
   - 提供学习建议和时间预估

4. **进度跟踪器** - 实时监控研究领域
   - 跟踪研究主题和关键词
   - 生成每日/每周/每月报告
   - 监控热门论文和主题

5. **论文分析器** - 深度分析论文
   - 提取关键贡献和见解
   - 支持快速/标准/深度分析模式
   - 生成结构化的分析报告

6. **知识图谱构建器** - 可视化概念之间的关系
   - 构建交互式知识图谱
   - 支持Mermaid和JSON输出格式
   - 查找概念之间的学习路径
   - 基于SQLite的持久化存储
   - 双向概念-论文索引

### 高级功能（9个）

7. **评论检测器** - 自动识别评论论文
   - 多维度评分（标题30% + 引用25% + 摘要25% + AI 20%）
   - 支持中英文关键词
   - 基于置信度的过滤，并允许用户确认

8. **概念提取器** - 从评论论文中提取概念
   - 通过AI提取15-30个核心概念
   - 四级分类（基础/核心/高级/应用）
   - 重要性评分和关系识别
   - 去重和合并不同评论中的概念

9. **评论到图谱的工作流程** - 端到端流程
   - 搜索评论 -> 识别 -> 确认 -> 分析 -> 提取概念
   - 构建知识图谱 -> 用关键论文丰富图谱 -> 索引 -> 存储
   - 支持交互式或自动确认模式

10. **知识图谱查询** - 双向文献索引
    - 概念 -> 论文：查找与概念相关的论文
    - 论文 -> 概念：查找论文涵盖的概念
    - 基于多个概念的论文推荐
    - 优化后的SQLite查询性能

11. **概念比较** - 比较两个概念
    - 识别相似点和差异
    - 提供使用场景建议

12. **论文比较** - 比较多篇论文
    - 找出共同主题和差异
    - 生成综合分析

13. **评论分析** - 对论文进行批判性分析
    - 识别优点和缺点
    - 找出研究缺口和改进建议
    - 支持自定义关注领域

14. **学习路径** - 找到最佳学习路径
    - 发现概念之间的路径
    - 生成拓扑学习顺序
    - 用Mermaid图表可视化

15. **图谱管理** - 管理持久化的知识图谱
    - 列出所有保存的图谱
    - 查看图谱统计信息
    - 将图谱导出为JSON
    - 用Mermaid可视化

16. **论文可视化** - 交互式论文展示
    - 将论文分析转换为HTML幻灯片展示
    - 支持学术主题（深色/浅色）和响应式排版
    - 支持键盘/触摸/滚动导航和编辑模式（E键）
    - PDF图表提取（`pymupdf`）和PPT导出（`python-pptx`）
    - 每张幻灯片包含标题、摘要、关键点、方法、实验、贡献、局限性、参考文献

17. **交互式知识图谱** - 使用D3.js实现力导向可视化
    - 将知识图谱转换为交互式HTML
    - 节点大小反映论文数量，边粗细反映概念之间的紧密程度
    - 支持缩放/平移、节点拖动、点击查看详细信息、搜索、图例
    - 纸张预览功能：点击“查看演示文稿”可在新标签页中打开论文幻灯片
    - 类别颜色：基础=#4FC3F7，核心=#FFB74D，高级=#CE93D8，应用=#81C784

## 技术特性

- **11个学术搜索来源**：arXiv、Semantic Scholar、OpenAlex、PubMed、CrossRef、DBLP、IEEE Xplore、CORE、Google Scholar、Unpaywall、网络搜索
- **互补搜索策略**：自动检测查询领域并选择最佳来源组合
- **插件架构**：基于插件的搜索源架构，便于扩展
- **PDF下载**：支持多种URL解析策略（直接下载、Unpaywall、OpenAlex开放获取PDF、CORE）
- **支持多种AI提供商**：包括OpenAI、Anthropic、DeepSeek、Qwen、Zhipu AI等
- **SQLite持久化**：知识图谱存储在SQLite数据库中
- **双向索引**：支持概念-论文和论文-概念的双向查询
- **速率限制**：对每个来源设置速率限制，并提供自动重试和延迟机制
- **交互式HTML输出**：支持论文幻灯片展示和D3.js知识图谱可视化
- **多种输出格式**：Markdown、JSON、Mermaid、HTML、PPTX
- **TypeScript + Bun**：快速且类型安全的运行时环境
- **命令行接口（CLI）和编程接口（API）**

## 安装

```bash
# Clone repository
git clone https://github.com/Josephyb97/ScholarGraph.git
cd ScholarGraph

# Install dependencies
bun install

# Initialize configuration
bun run cli.ts config init
```

## 配置

设置您的AI提供商：

```bash
# Using OpenAI
export AI_PROVIDER=openai
export OPENAI_API_KEY="your-api-key"

# Using DeepSeek
export AI_PROVIDER=deepseek
export DEEPSEEK_API_KEY="your-api-key"

# Using Qwen (通义千问)
export AI_PROVIDER=qwen
export QWEN_API_KEY="your-api-key"
```

### 学术来源API密钥（可选，可扩展搜索范围）

```bash
export NCBI_API_KEY="your-key"           # PubMed high-speed access (10 req/s)
export IEEE_API_KEY="your-key"           # IEEE Xplore engineering papers
export CORE_API_KEY="your-key"           # CORE open access full text
export UNPAYWALL_EMAIL="your@email.com"  # Unpaywall OA PDF resolver
export CROSSREF_MAILTO="your@email.com"  # CrossRef polite pool (higher rate)
export SERPAPI_KEY="your-key"            # Google Scholar (via SerpAPI)
export SERPER_API_KEY="your-key"         # Web search via Serper
```

## 使用示例

### 搜索文献
```bash
# Auto-select best sources based on query domain
lit search "transformer attention" --limit 20

# Specify domain for optimized source selection
lit search "CRISPR gene editing" --domain biomedical

# Use specific sources (comma-separated)
lit search "deep learning" --source semantic_scholar,arxiv,openalex --sort citations

# Search and download PDFs
lit search "attention is all you need" --download --limit 3
```

### 下载PDF
```bash
# Search and download PDFs
lit download "transformer" --limit 5 --output ./papers
```

### 学习概念
```bash
lit learn "BERT" --depth advanced --papers --code --output bert-card.md
```

### 识别知识缺口
```bash
lit detect --domain "Deep Learning" --known "CNN,RNN" --output gaps.md
```

### 分析论文
```bash
lit analyze "https://arxiv.org/abs/1706.03762" --mode deep --output analysis.md
```

### 构建知识图谱
```bash
lit graph transformer attention BERT GPT --format mermaid --output graph.md
```

### 比较概念
```bash
lit compare concepts CNN RNN --output comparison.md
```

### 比较论文
```bash
lit compare papers "url1" "url2" "url3" --output comparison.md
```

### 批判性分析
```bash
lit critique "paper-url" --focus "novelty,scalability" --output critique.md
```

### 找到学习路径
```bash
lit path "Machine Learning" "Deep Learning" --concepts "Neural Networks" --output path.md
```

### 搜索评论论文
```bash
lit review-search "attention mechanism" --limit 10
```

### 从评论构建知识图谱
```bash
# From search query (interactive mode)
lit review-graph "deep learning" --output dl-graph --enrich

# From specific URL
lit review-graph "https://arxiv.org/abs/xxxx" --output my-graph --enrich

# Auto-confirm mode (non-interactive)
lit review-graph "transformer" --output tf-graph --enrich --auto-confirm
```

### 查询知识图谱
```bash
# Find papers by concept
lit query concept "transformer" --graph dl-graph --limit 20

# Find concepts by paper
lit query paper "https://arxiv.org/abs/1706.03762" --graph dl-graph
```

### 管理知识图谱
```bash
# List all graphs
lit graph-list

# View graph statistics
lit graph-stats dl-graph

# Visualize graph
lit graph-viz dl-graph --format mermaid --output graph.md

# Export graph
lit graph-export dl-graph --output dl-graph.json
```

### 论文可视化
```bash
# Generate interactive HTML presentation
lit paper-viz "https://arxiv.org/abs/1706.03762" --output attention.html

# With theme and PPT export
lit paper-viz "https://arxiv.org/abs/1706.03762" --mode deep --theme academic-light --ppt

# Manually provide figures
lit paper-viz "https://example.com/paper" --figures ./my-figures
```

### 交互式知识图谱
```bash
# Generate interactive D3.js graph from existing knowledge graph
lit graph-interactive dl-graph --output dl-interactive.html

# Without paper data (lighter weight)
lit graph-interactive my-graph --no-paper-viz
```

## 使用场景

### 1. 快速领域入门
- 学习核心概念
- 识别知识缺口
- 构建知识图谱
- 规划学习路径

### 2. 深度理解论文
- 深入分析论文
- 进行批判性分析
- 从论文中学习新概念
- 与相关论文进行比较

### 3. 研究进度跟踪
- 监控研究主题
- 跟踪最新论文
- 生成进度报告

### 4. 概念比较
- 比较不同的技术方法
- 评估不同模型
- 构建比较图谱

### 5. 基于评论的知识构建
- 搜索并识别评论论文
- 从评论中提取概念
- 构建持久化的知识图谱
- 查询概念-论文之间的关系

### 6. 论文可视化与图谱探索
- 分析论文并生成交互式HTML展示
- 从评论构建知识图谱
- 生成交互式D3.js图谱并附带论文预览
- 点击节点可查看论文详细信息和打开演示文稿

## 项目结构

```
ScholarGraph/
├── cli.ts                      # Unified CLI entry
├── config.ts                   # Configuration management
├── README.md                   # Project documentation
├── CHANGELOG.md                # Version history
├── SKILL.md                    # This file
│
├── shared/                     # Shared modules
│   ├── ai-provider.ts          # AI provider abstraction
│   ├── types.ts                # Type definitions
│   ├── validators.ts           # Parameter validation
│   ├── errors.ts               # Error handling
│   └── utils.ts                # Utility functions
│
├── literature-search/          # Literature search module
│   └── scripts/
│       ├── search.ts           # Search engine core
│       ├── types.ts            # Type definitions
│       ├── query-expander.ts   # Query expansion
│       ├── search-strategy.ts  # Complementary search strategy
│       ├── pdf-downloader.ts   # PDF download module
│       └── adapters/           # Search source adapters
│           ├── base.ts         # Adapter interface & base class
│           ├── registry.ts     # Adapter registry
│           ├── index.ts        # Barrel export
│           ├── arxiv-adapter.ts
│           ├── semantic-scholar-adapter.ts
│           ├── web-adapter.ts
│           ├── openalex-adapter.ts
│           ├── pubmed-adapter.ts
│           ├── crossref-adapter.ts
│           ├── dblp-adapter.ts
│           ├── ieee-adapter.ts
│           ├── core-adapter.ts
│           ├── unpaywall-adapter.ts
│           └── google-scholar-adapter.ts
│
├── concept-learner/            # Concept learning module
├── knowledge-gap-detector/     # Gap detection module
├── progress-tracker/           # Progress tracking module
├── paper-analyzer/             # Paper analysis module
│
├── review-detector/            # Review paper identification
│   └── scripts/
│       ├── detect.ts           # Multi-dimensional scoring
│       └── types.ts
│
├── concept-extractor/          # Concept extraction from reviews
│   └── scripts/
│       ├── extract.ts          # AI-powered extraction
│       └── types.ts
│
├── knowledge-graph/            # Knowledge graph module
│   └── scripts/
│       ├── graph.ts            # Graph building core
│       ├── indexer.ts          # Bidirectional indexing
│       ├── storage.ts          # SQLite persistence
│       └── enricher.ts         # Key paper association
│
├── paper-viz/                  # Paper visualization
│   └── scripts/
│       ├── types.ts            # Presentation data interfaces
│       ├── slide-builder.ts    # PaperAnalysis → slides
│       ├── html-generator.ts   # Self-contained HTML generation
│       ├── pdf-figure-extractor.ts  # PDF figure extraction (pymupdf)
│       └── ppt-exporter.ts     # PPT export (python-pptx)
│
├── graph-viz/                  # Interactive knowledge graph
│   └── scripts/
│       ├── types.ts            # D3 graph data interfaces
│       ├── graph-data-adapter.ts # KnowledgeGraph → D3 data
│       ├── html-generator.ts   # Interactive HTML (D3.js v7)
│       └── paper-viz-bridge.ts # Graph → paper presentation bridge
│
├── workflows/                  # End-to-end workflows
│   └── review-to-graph.ts      # Review to graph pipeline
│
├── data/                       # Data directory (auto-created)
│   └── knowledge-graphs.db     # SQLite database
│
├── downloads/                  # PDF downloads (auto-created)
│   └── pdfs/
│       └── metadata.json       # Download index
│
└── test/                       # Tests and documentation
    ├── ADVANCED_FEATURES.md
    ├── TEST_RESULTS.md
    └── scripts/
```

## 支持的AI提供商

### 国际提供商
- OpenAI
- Anthropic (Claude)
- Azure OpenAI
- Groq
- Together AI
- Ollama（本地）

### 中国提供商
- 通义千问 (Qwen/DashScope)
- DeepSeek
- 智谱AI (GLM)
- MiniMax
- Moonshot (Kimi)
- 百川AI (Baichuan)
- 零一万物 (Yi)
- 豆包 (Doubao)

## 输出格式

### Markdown报告
- 包含定义、组成部分、历史和应用的知识卡片
- 包含分析和建议的知识缺口报告
- 包含热门主题的进度报告
- 包含方法、实验和贡献的论文分析报告
- 包含相似点和差异的比较分析报告
- 包含优点、缺点和建议的批判性分析报告

### JSON数据
- 用于程序化处理的结构化数据

### Mermaid图表
- 交互式知识图谱和学习路径

### 交互式HTML
- 支持键盘/触摸/滚动导航的论文幻灯片展示
- 使用D3.js实现的力导向知识图谱，支持缩放、搜索和论文面板

## 系统要求

- Bun 1.3或更高版本，或Node.js 18或更高版本
- AI提供商的API密钥
- 需要互联网连接以进行论文搜索
- Python 3.8或更高版本（可选，用于PDF图表提取和PPT导出）

## 许可证

MIT许可证

## 链接

- GitHub: [https://github.com/Josephyb97/ScholarGraph](https://github.com/Josephyb97/ScholarGraph)
- 问题报告: [https://github.com/Josephyb97/ScholarGraph/issues](https://github.com/Josephyb97/ScholarGraph/issues)
- 讨论区: [https://github.com/Josephyb97/ScholarGraph/discussions](https://github.com/Josephyb97/ScholarGraph/discussions)

## 版本

当前版本：1.0.0

## 作者

ScholarGraph团队

---

**设计灵感来源**：
- [frontend-slides](https://github.com/zarazhangrui/frontend-slides) - 论文幻灯片展示设计参考
- [Argo Scholar](https://github.com/poloclub/argo-scholar) - 交互式知识图谱设计参考

*详细文档请参阅README.md*
*高级功能请参阅test/ADVANCED_FEATURES.md*
*测试结果请参阅test/TEST_RESULTS.md*