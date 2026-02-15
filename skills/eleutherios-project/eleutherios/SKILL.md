---
name: eleutherios
description: 认知分析基础设施——用于查询知识图谱的工具，具备抑制检测（suppression detection）功能、协调签名（coordination signatures）以及多视角聚类（multi-perspective clustering）能力。该系统采用本地优先（local-first）的架构，完全不依赖云服务。
version: 1.1.0
author: Cedrus Strategic LLC
repository: https://github.com/Eleutherios-project/Eleutherios-docker
homepage: https://eleutherios.io
license: MIT
tags:
  - research
  - knowledge-graph
  - analysis
  - mcp
  - epistemic
  - osint
  - document-analysis
metadata:
  openclaw:
    mcp:
      server: "http://localhost:8100/mcp"
      transport: "streamable-http"
    requirements:
      - "Docker and Docker Compose"
      - "Eleutherios running locally (see setup below)"
    config:
      requiredEnv: []
      stateDirs: []
---

# Eleutherios – 认知分析基础设施

查询由您的文档集合构建的知识图谱。检测压制行为、协调模式，并对有争议的话题进行多视角分析。

## 该功能的用途

Eleutherios 将文档集合转换为包含声明级信息的知识图谱，然后运行检测算法以揭示传统搜索方法无法发现的模式：

- **压制行为检测**：识别资金削减、职业影响、出版障碍以及来源中的机构边缘化模式。
- **协调模式检测**：检测时间模式、共同语言和引用网络异常，这些异常表明存在协调一致的言论。
- **多视角聚类**：根据观点对声明进行分组，以便您可以全面了解有争议话题的各个方面。
- **来源拓扑分析**：绘制引用网络和来源之间的信任关系图。

## 何时使用该功能

当您需要以下情况时，请使用 Eleutherios：
- 研究可能存在机构操控共识的话题。
- 分析历史文献中的压制行为（例如，解密材料、国会证词）。
- 比较不同来源对同一话题的报道方式。
- 了解有争议的科学或历史辩论的来龙去脉。
- 调查引用空白和研究线索的突然中断。

**示例提示**：
- “Eleutherios 对托马斯·潘恩的压制行为有何发现？”
- “从我的知识图谱中获取关于等离子推进研究的观点。”
- “分析电引力学这一话题——有哪些相关来源？出现了哪些模式？”
- “评估斯梅德利·巴特勒 FBI 文件的来源拓扑结构。”

## 先决条件

**在使用此功能之前，必须先在本地运行 Eleutherios。**

### 快速入门（Docker）

```bash
# Clone the repository
git clone https://github.com/Eleutherios-project/Eleutherios-docker.git
cd Eleutherios-docker

# Start the stack
docker-compose up -d

# Verify MCP server is running
curl http://localhost:8100/health
```

MCP 服务器默认运行在端口 8100 上。Web 界面可通过 http://localhost:8080 访问。

### 导入文档

使用 Web 界面或 CLI 导入您的文档集合：

```bash
# Via CLI
docker exec -it eleutherios-api python aegis_import_wizard.py /path/to/documents

# Or use the web UI at http://localhost:8080
```

支持的格式：PDF、DOCX、TXT、MD、HTML

### 验证连接

运行 Eleutherios 后，测试 MCP 连接：

```bash
curl -X POST http://localhost:8100/mcp/list_domains \
  -H "Content-Type: application/json" \
  -d '{}'
```

您应该会收到包含语料库统计信息的 JSON 响应。

## 可用工具

### analyze_topic
对某个主题执行压制行为和协调模式检测。

```
Parameters:
  - topic (required): The topic to analyze
  - detail: "brief" | "standard" | "verbose" (default: "standard")
  - max_claims: Maximum claims to analyze (default: 100)

Returns:
  - Suppression score (0.0-1.0) with severity rating
  - Coordination score with pattern indicators
  - Relevant claims with source attribution
  - Detection signals (funding impacts, credential attacks, etc.)
```

### get_perspectives
使用语义分析按观点对声明进行聚类。

```
Parameters:
  - topic (required): The topic to analyze
  - max_clusters: Number of perspective clusters (default: 5)
  - claims_per_cluster: Claims per cluster (default: 5)

Returns:
  - Clustered perspectives with representative claims
  - Cluster labels and themes
  - Cross-cluster relationships
```

### assess_source
分析特定来源在知识拓扑结构中的位置。

```
Parameters:
  - source_identifier (required): Document title or source file name
  - detail: "brief" | "standard" | "verbose" (default: "standard")

Returns:
  - Citation network position
  - Claim types (PRIMARY vs META)
  - Trust score aggregation
  - Related sources
```

### get_claim_context
深入研究某个特定声明的完整背景信息。

```
Parameters:
  - claim_id (required): The claim identifier
  - include_graph: Include graph relationships (default: true)

Returns:
  - Full claim text and metadata
  - Source document context
  - Related entities
  - Citation relationships
```

### list_domains
获取语料库统计信息和可用领域。

```
Parameters: none

Returns:
  - Total claims, documents, entities
  - Domain breakdown
  - Corpus health metrics
```

## 示例工作流程

```
You: "What suppression patterns exist for Thomas Paine in my knowledge graph?"

[Skill calls analyze_topic with topic="Thomas Paine"]

Response: "Thomas Paine shows a CRITICAL suppression score of 0.831. 
Key indicators:
- Credential inversion: Despite being a Founding Father, systematically 
  marginalized in educational curricula
- Evidence avoidance: Critics attack character rather than engage arguments
- Career/social impacts: Documented ostracism, denied burial in consecrated ground

47 claims analyzed across 3 documents. Strongest signals from 
'Age of Reason' and 'Rights of Man' analysis."

You: "Show me the different perspectives on his work"

[Skill calls get_perspectives with topic="Thomas Paine"]

Response: "Found 4 distinct perspective clusters:
1. Revolutionary Hero (12 claims) - Focus on Common Sense, independence
2. Religious Critic (9 claims) - Age of Reason, deism arguments  
3. Institutional Dismissal (8 claims) - Character attacks, marginalization
4. Modern Rehabilitation (6 claims) - Academic reassessment

Cluster 3 shows classic suppression rhetoric: ad hominem attacks
without substantive engagement with Cluster 2's actual arguments."
```

## 配置

### 自定义 MCP 端口

如果 Eleutherios 运行在其他端口上，请更新您的 OpenClaw 配置文件：

```yaml
# In your OpenClaw workspace skills config
eleutherios:
  mcp:
    server: "http://localhost:YOUR_PORT/mcp"
```

### 远程服务器

对于远程运行的 Eleutherios 实例（例如，在家庭实验室服务器上）：

```yaml
eleutherios:
  mcp:
    server: "http://192.168.1.100:8100/mcp"
```

**安全提示**：仅将 Eleutherios 部署在可信任的网络环境中。MCP 服务器默认没有身份验证机制。

## 故障排除

### “连接被拒绝”错误
- 确认 Eleutherios 是否正在运行：`docker ps | grep eleutherios`
- 检查 MCP 端口：`curl http://localhost:8100/health`
- 确保防火墙没有阻止端口 8100 的访问。

### 结果为空
- 确认文档已成功导入：访问 localhost:8080 的 Web 界面。
- 如有需要，请运行提取操作：在查询之前必须先处理文档。

### 响应缓慢
- 大型语料库的查询可能需要 10-30 秒。
- 使用 `max_claims` 参数来限制查询范围。
- 考虑在配备 GPU 的硬件上运行以加快嵌入生成速度。

## 隐私与安全

- **数据本地化**：所有数据都存储在您的机器上，不依赖云服务。
- **无数据传输**：Eleutherios 不会向外部发送任何数据。
- **数据所有权**：您可以使用自己的文档构建知识图谱。

## 链接

- **官方网站**：https://eleutherios.io
- **GitHub**：https://github.com/Eleutherios-project/
- **文档**：https://github.com/Eleutherios-project/Eleutherios-docker/blob/main/README.md
- **问题反馈**：https://github.com/Eleutherios-project/Eleutherios-docker/issues

## 关于 Eleutherios

Eleutherios（源自希腊神话中的自由之神 Zeus Eleutherios）是一个开源的认知防御基础设施，专为研究那些无法信任机构把关人的话题的研究人员设计。

由 Cedrus Strategic LLC 开发，并获得 MIT 许可。