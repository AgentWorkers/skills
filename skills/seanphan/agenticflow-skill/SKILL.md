---
name: agenticflow-skills
description: 使用 AgenticFlow 构建 AI 工作流程、智能代理和劳动力系统的综合指南。适用于设计包含多种节点类型的工作流程、配置单个智能代理，或协调劳动力协作模式的情况。
license: MIT
---

# AgenticFlow 技能

AgenticFlow 是一个用于构建基于人工智能的自动化工作流程、智能代理和劳动力系统的平台。

## 快速导航

| 主题 | 使用场景 | 参考文档 |
|-------|-------------|-----------|
| **工作流程** | 使用节点构建自动化流程 | [workflow/overview.md](./reference/workflow/overview.md) |
| **代理** | 创建单个智能代理 | [reference/agent/overview.md](./reference/agent/overview.md) |
| **劳动力系统** | 协调多个代理以完成任务 | [reference/workforce/overview.md](./reference/workforce/overview.md) |

---

## 工作流程

工作流程是由顺序排列的节点组成的线性自动化管道。每个节点执行特定的操作。

| 文档 | 说明 |
|-------|-------------|
| [overview.md](./reference/workflow/overview.md) | 核心概念、架构、执行模型 |
| [how-to-build.md](./reference/workflow/how-to-build.md) | 分步构建指南 |
| [how-to-run.md](./reference/workflow/how-to-run.md) | 运行工作流程并处理结果 |
| [node-types.md](./reference/workflow/node-types.md) | 节点类型及发现机制 |
| [connections.md](./reference/workflow/connections.md) | 连接提供者及设置 |

### 节点类型概述

| 类别 | 示例节点类型 | 用途 |
|----------|-------------------|---------|
| **AI/大语言模型** | `claude_ask`, `openai_chat`, `gemini` | 调用 AI 模型、生成文本 |
| **图像生成** | `generate_image`, `dall_e` | 根据提示生成图像 |
| **数据处理** | `json_parse`, `text_transform` | 转换和处理数据 |
| **集成** | `slack_send`, `gmail`, `notion` | 连接到 300 多个外部服务 |
| **API 调用** | `http_request`, `webhook` | 发送 HTTP 请求和使用 Webhook |
| **文件操作** | `file_upload`, `pdf_parse` | 上传、下载和处理文件 |

> **注意**：AgenticFlow 中的工作流程是 **线性的且按顺序执行**——节点从上到下执行，没有分支或循环。

---

## 代理

代理是一个具有特定能力、工具和明确角色的 AI 实体。

**要了解代理配置，请阅读：** [reference/agent/overview.md](./reference/agent/overview.md)

---

## 劳动力系统

劳动力系统协调多个代理协同完成复杂任务。

**要了解协调模式，请阅读：** [reference/workforce/overview.md](./reference/workforce/overview.md)

### 常见模式

- **监督者**：一个代理将任务分配给专家代理 |
- **群体**：代理们自动进行协作 |
- **流水线**：代理之间依次传递任务 |
- **讨论**：代理们通过讨论达成共识 |

---

## 术语表

有关术语和定义，请参阅 [reference/glossary.md](./reference/glossary.md)。