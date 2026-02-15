---
name: remote-agent
description: 用于与外部垂直代理（如 Google ADK、VeADK 等）进行通信，以执行特定任务。
metadata: { "openclaw": { "emoji": "🔗", "requires": { "env": ["REMOTE_AGENT_URL"] } } }
---

# 远程代理桥接（Remote Agent Bridge）

此功能允许 OpenClaw 通过标准的 HTTP 接口将任务委托给外部、专门化的 AI 代理。当用户的请求需要特定领域的专业知识（例如企业数据、财务分析、法律审核）时，可以使用此功能，因为这些任务通常由独立的代理系统来处理。

## 配置

请确保在 OpenClaw 环境中设置了以下环境变量（可以通过 `.env` 或 `openclaw config` 文件进行配置）：

- `REMOTE_AGENT_URL`：外部代理的 HTTP 端点（例如 `https://remote-agent.example.com/run` 或您的 Google ADK 端点）。
- `REMOTE_AGENT_KEY`：（可选）用于身份验证的承载令牌（Bearer token）。

## 使用方法

当用户提出的问题属于某个专门化远程代理的处理范围时，使用此功能来转发请求。

### 命令

```bash
python3 skills/remote-agent/scripts/client.py --query "<USER_QUERY>" [--agent "<AGENT_ID>"]
```

### 示例

**场景 1：财务分析（VeADK）**

用户：“分析 TechCorp 的第三季度收益报告。”
处理思路：用户需要财务分析，应将该任务委托给 ‘financial-expert’ 代理。
操作步骤：

```bash
python3 skills/remote-agent/scripts/client.py --agent "financial-expert" --query "Analyze the Q3 earnings report for TechCorp"
```

**场景 2：企业知识（Google ADK）**

用户：“公司的远程工作政策是什么？”
处理思路：这需要内部知识，我将询问 ‘hr-bot’。
操作步骤：

```bash
python3 skills/remote-agent/scripts/client.py --agent "hr-bot" --query "company policy on remote work"
```

**场景 3：自定义 LangChain 后端**

用户：“运行数据处理流程。”
操作步骤：

```bash
python3 skills/remote-agent/scripts/client.py --query "Run the data processing pipeline"
```