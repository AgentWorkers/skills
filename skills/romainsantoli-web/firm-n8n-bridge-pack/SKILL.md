---
name: firm-n8n-bridge-pack
version: 1.0.0
description: n8n 工作流桥接包：用于将 OpenClaw 管道导出为 n8n 格式，并导入 n8n 工作流。包含两个桥接工具。
author: romainsantoli-web
license: MIT
metadata:
  openclaw:
    registry: ClawHub
    requires:
      - mcp-openclaw-extensions >= 3.0.0
tags:
  - n8n
  - workflow
  - bridge
  - automation
  - export
---
# firm-n8n-bridge-pack

> ⚠️ 本内容由人工智能生成，使用前需经过人工验证。

## 目的

该工具用于将 OpenClaw 的工作流程与 n8n 自动化平台进行集成。它可以将 OpenClaw 的工作流程导出为 n8n 的 JSON 格式（包含 20 种节点类型的映射），并能够将 n8n 的工作流程导入 OpenClaw 同时进行验证。

## 所需工具（2 个）

| 工具 | 描述 |
|------|-------------|
| `openclaw_n8n_workflow_export` | 将 OpenClaw 的工作流程导出为 n8n 的 JSON 格式 |
| `openclaw_n8n_workflow_import` | 将 n8n 的工作流程导入 OpenClaw 并进行验证 |

## 使用方法

```yaml
skills:
  - firm-n8n-bridge-pack

# Export/import workflows:
openclaw_n8n_workflow_export config_path=/path/to/config.json pipeline_name=my-pipeline
openclaw_n8n_workflow_import workflow_path=/path/to/workflow.json
```

## 系统要求

- `mcp-openclaw-extensions` 版本需大于或等于 3.0.0 |
- 推荐使用 n8n 版本 1.0 或更高版本