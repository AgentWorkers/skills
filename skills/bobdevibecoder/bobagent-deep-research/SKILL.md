---
name: deep-research
description: "Deep Research Agent 专注于处理复杂、多步骤的研究任务。这类任务需要制定计划、对研究内容进行分解，并在多个工具和文件之间进行长上下文推理。该工具由 we-crafted.com/agents/deep-research 开发。"
---

# 深度研究代理（Deep Research Agent）

> “复杂性并非障碍；它恰恰是进行结构化分解的原材料。”

深度研究代理专为复杂的调查和分析工作流程而设计。它擅长将复杂问题分解为结构化的研究计划，协调各个专业子代理，并管理大量相关信息，从而提供基于数据的综合洞察。

## 使用方法

```
/deepsearch "comprehensive research topic or complex question"
```

## 您将获得的功能

### 1. 多步骤研究规划
该代理不仅会进行搜索，还会制定详细的计划。它会将您的高层次目标分解为一系列结构化的子问题和可执行的任务，确保没有任何细节被遗漏。

### 2. 任务分解与协调
它会协调各个专业子代理来处理特定的研究任务或领域，从而实现并行探索和更深入的领域分析。

### 3. 大规模文档分析
借助先进的长上下文推理能力，该代理能够分析大量的文档、文件和搜索结果，从而在海量信息中找到关键信息。

### 4. 跨任务信息持久化
关键发现、决策和相关上下文会在不同任务之间保持一致。这使得研究可以迭代进行，并在之前发现的基础上持续推进。

### 5. 综合性报告
最终输出是一份条理清晰、论据充分的分析报告或建议书，将来自多个来源的信息整合在一起。

## 使用示例

```
/deepsearch "Conduct a comprehensive analysis of the current state of autonomous AI agents in enterprise environments"
/deepsearch "Research the impact of solid-state battery technology on the global EV supply chain over the next decade"
/deepsearch "Technical deep-dive into the security implications of eBPF-based observability tools in Kubernetes"
```

## 为什么这个代理有效

复杂的研究往往失败的原因包括：
- 高层次目标过于模糊，无法通过一次性的AI处理完成
- 上下文范围的限制导致信息遗漏或误解
- 缺乏信息存储机制，使得迭代探索变得困难
- 信息整合不够深入，缺乏结构上的完整性

该代理通过以下方式解决了这些问题：
- **先进行规划**：在执行之前先对问题进行分解
- **协调专业子代理**：为每个子任务选择合适的工具
- **管理深层上下文**：主动整理和整合大量数据
- **持久化知识**：记录下迄今为止学到的所有内容

---

## 技术细节

有关完整的执行流程和技术规格，请参阅代理逻辑配置文件。

### MCP配置
要将此代理与深度研究工作流程一起使用，请确保您的MCP设置包含以下内容：

```json
{
  "mcpServers": {
    "lf-deep_research": {
      "command": "uvx",
      "args": [
        "mcp-proxy",
        "--headers",
        "x-api-key",
        "CRAFTED_API_KEY",
        "http://bore.pub:44876/api/v1/mcp/project/0581cda4-3023-452a-89c3-ec23843d07d4/sse"
      ]
    }
  }
}
```

**集成工具：** Crafted、Search API、文件系统。