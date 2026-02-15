---
name: n8n-workflow
description: 使用 n8n 自动化文档工作流程——拥有 7800 多个工作流模板
author: claude-office-skills
version: "1.0"
tags: ['workflow', 'automation', 'n8n', 'integration']
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: n8n
  url: https://github.com/n8n-io/n8n
  stars: 172k
---

# N8N 工作流技能

## 概述

该技能利用 **n8n**（最受欢迎的工作流自动化平台，拥有 7800 多个社区模板）来实现文档工作流的自动化。支持链接多个文档操作、与 400 多个应用程序集成，并构建复杂的文档处理流程。

## 使用方法

1. 描述您想要完成的任务；
2. 提供所需的输入数据或文件；
3. 我将执行相应的操作。

**示例提示：**
- “自动化 PDF → OCR → 翻译 → 发送邮件的工作流程”；
- “监控文件夹中的新合同 → 审查 → 通知 Slack”；
- “从多个数据源生成每日报告”；
- “使用条件逻辑进行批量文档处理”。

## 相关领域知识

### n8n 基础知识

n8n 采用基于节点的工作流架构：

```
Trigger → Action → Action → Output
   │         │         │
   └─────────┴─────────┴── Data flows between nodes
```

### 主要节点类型

| 类型 | 示例 | 用途 |
|------|----------|----------|
| **触发器** | Webhook（Webhook）、Schedule（定时任务）、File Watcher（文件监控器） | 启动工作流 |
| **文档处理节点** | Read PDF（读取 PDF 文件）、Write DOCX（生成 DOCX 文件）、OCR（光学字符识别） | 处理文件 |
| **数据转换节点** | Code（自定义代码处理）、Set（设置数据）、Merge（合并数据） | 操作数据 |
| **结果输出节点** | Email（发送邮件）、Slack（发送通知）、Google Drive（存储结果） | 输出处理结果 |

### 工作流示例：合同审核流程

```json
{
  "nodes": [
    {
      "name": "Watch Folder",
      "type": "n8n-nodes-base.localFileTrigger",
      "parameters": {
        "path": "/contracts/incoming",
        "events": ["add"]
      }
    },
    {
      "name": "Extract Text",
      "type": "n8n-nodes-base.readPdf"
    },
    {
      "name": "AI Review",
      "type": "n8n-nodes-base.anthropic",
      "parameters": {
        "model": "claude-sonnet-4-20250514",
        "prompt": "Review this contract for risks..."
      }
    },
    {
      "name": "Save Report",
      "type": "n8n-nodes-base.writeFile"
    },
    {
      "name": "Notify Team",
      "type": "n8n-nodes-base.slack"
    }
  ]
}
```

### 自托管与云服务

| 选项 | 优点 | 缺点 |
|--------|------|------|
| **自托管** | 免费、完全控制、数据隐私保护 | 需要自行维护 |
| **n8n 云服务** | 无需安装、自动更新 | 规模使用时会产生费用 |

```bash
# Docker quick start
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

## 最佳实践

1. **从现有的模板开始使用，根据需求进行定制**；
2. **使用错误处理节点来确保工作流的可靠性**；
3. **使用 n8n 的凭证管理器安全存储凭证**；
4. **在生产环境使用前先用示例数据进行测试**。

## 安装方法

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## 资源

- [n8n 官方仓库](https://github.com/n8n-io/n8n)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)