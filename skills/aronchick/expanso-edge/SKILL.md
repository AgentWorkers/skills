---
name: expanso
description: OpenClaw的数据处理管道：通过Expanso市场部署相关技能，实现数据的本地转换、分析和处理。
homepage: https://skills.expanso.io
emoji: "⚡"
metadata:
  clawdis:
    always: false
    primaryEnv: EXPANSO_EDGE_BOOTSTRAP_TOKEN
    requires:
      bins:
        - curl
      env:
        - EXPANSO_EDGE_BOOTSTRAP_URL
        - EXPANSO_EDGE_BOOTSTRAP_TOKEN
    install:
      - curl -fsSL https://get.expanso.io/edge/install.sh | bash
      - curl -fsSL https://get.expanso.io/cli/install.sh | sh
    config:
      requiredEnv:
        - name: EXPANSO_EDGE_BOOTSTRAP_URL
          description: Bootstrap URL from Expanso Cloud (e.g., https://start.cloud.expanso.io)
        - name: EXPANSO_EDGE_BOOTSTRAP_TOKEN
          description: Bootstrap token from Expanso Cloud Settings → Edge Nodes
---

# OpenClaw 的 Expanso 技能

您可以将数据处理管道部署到本地 Expanso Edge 上。这些技能在本地运行，能够保护您的凭据安全，并支持离线操作。

## 什么是 Expanso？

- **Expanso Edge**：在您的机器上执行管道的本地运行时环境。
- **Expanso Cloud**：负责编排和将管道部署到您的 Edge 节点。
- **Expanso Skills**：为常见数据任务预先构建好的管道。

## 设置

### 1. 创建一个 Expanso Cloud 账户

1. 访问 [cloud.expanso.io](https://cloud.expanso.io) 并注册。
2. 创建一个新的组织（或使用现有的组织）。
3. 记下您的 **Cloud Endpoint URL**（例如：`https://abc123.us1.cloud.expanso.io`）。

### 2. 安装所需工具

```bash
# Install Expanso Edge (local runtime)
curl -fsSL https://get.expanso.io/edge/install.sh | bash

# Install Expanso CLI (deploy to cloud)
curl -fsSL https://get.expanso.io/cli/install.sh | sh
```

### 3. 获取 Bootstrap Token

1. 在 Expanso Cloud 中，进入 **设置 → Edge 节点**。
2. 点击 **“添加 Edge 节点”**。
3. 复制 **Bootstrap URL** 和 **Bootstrap Token**。

### 4. 将您的 Edge 节点连接到 Cloud

```bash
# Set the bootstrap URL and token from Expanso Cloud
export EXPANSO_EDGE_BOOTSTRAP_URL="https://start.cloud.expanso.io"
export EXPANSO_EDGE_BOOTSTRAP_TOKEN="your-token-from-cloud"

# Start Edge (it will register automatically)
expanso-edge
```

这样，您的本地 Edge 节点就可以接收来自 Cloud 的管道部署了。

### 5. 部署一个技能

```bash
# Browse skills at https://skills.expanso.io
# Then deploy one:
expanso-cli job deploy https://skills.expanso.io/text-summarize/pipeline-cli.yaml
```

该管道将通过 Expanso Cloud 部署到您的本地 Edge 节点上。

## 可用的技能

在 **[skills.expanso.io](https://skills.expanso.io)** 上可以浏览 172 多种技能：

| 类别 | 示例 |
|----------|----------|
| **AI** | 文本摘要、图像描述、音频转录 |
| **安全** | 个人身份信息（PII）脱敏、秘密扫描、哈希计算 |
| **转换** | JSON 格式化、CSV 转 JSON、数组过滤 |
| **实用工具** | UUID 生成、电子邮件验证、MIME 类型检测 |

## 示例：PII 脱敏

要求 OpenClaw 对敏感数据进行脱敏：

> “从这条客户反馈中删除个人身份信息（PII）”

OpenClaw 会使用在您的本地 Expanso Edge 上运行的 `pii-redact` 技能来处理数据——您的 API 密钥和数据永远不会离开您的机器。

## 工作原理

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│  OpenClaw   │────▶│ Expanso Edge  │────▶│ Your Data    │
│  (asks)     │     │ (processes)   │     │ (stays local)│
└─────────────┘     └───────────────┘     └──────────────┘
                           │
                    ┌──────┴──────┐
                    │Expanso Cloud│
                    │(orchestrates)│
                    └─────────────┘
```

## 资源

- [技能市场](https://skills.expanso.io)：浏览和部署技能。
- [Expanso Cloud](https://cloud.expanso.io)：管理您的 Edge 节点。
- [文档](https://docs.expanso.io)：完整指南和 API 参考。
- [GitHub](https://github.com/expanso-io/expanso-skills)：技能源代码。