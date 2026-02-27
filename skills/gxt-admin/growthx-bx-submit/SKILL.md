---
name: growthx-bx-submit
description: 将您的项目提交到 Built at GrowthX——这是一个专为 GrowthX 会员设计的社区展示平台。提交项目需要使用 GrowthX 的 API 密钥。
metadata: {"openclaw":{"emoji":"🚀","requires":{"env":["GROWTHX_API_KEY"],"bins":["curl","jq","git"]},"primaryEnv":"GROWTHX_API_KEY"}}
---
# 在 GrowthX 上构建 — 项目提交

将项目提交到 **Built at GrowthX**，这是一个专为 GrowthX 会员设计的社区展示平台。

## 使用场景

当用户需要执行以下操作时，请使用此功能：
- 将项目推送到 Built at GrowthX；
- 将项目发布到 GrowthX 的展示平台上；
- 在 GrowthX 上公开自己的项目成果。

## 获取 API 密钥

如果用户尚未配置 API 密钥，请引导他们按照以下步骤操作：
1. 登录 GrowthX 平台，进入 **Built at GrowthX**；
2. 转到个人资料页面，然后进入 API 密钥设置；
3. 点击 “生成 API 密钥”；生成的密钥会显示一次，请立即复制；
4. 将密钥添加到 OpenClaw 的配置文件中：在 `~/.openclaw/openclaw.json` 文件的 `skills.entries.growthx-bx-submit.apiKey` 位置设置该密钥，或者设置 `GROWTHX_API_KEY` 环境变量。

此 API 密钥与用户的 GrowthX 会员资格相关联。如果用户的会员资格过期，密钥将失效。

## API 端点

```
POST https://backend.growthx.club/api/v1/bx/projects/agent
```

### 认证

在请求头中包含 `x-api-key`：

```
x-api-key: <GROWTHX_API_KEY>
```

### 请求体（JSON）

**必填字段：**
| 字段 | 类型 | 限制条件 |
|-------|------|-------------|
| `name` | 字符串 | 最长 100 个字符。项目名称。 |
| `tagline` | 字符串 | 最长 200 个字符。关于项目的简短描述。 |

**可选字段：**
| 字段 | 类型 | 默认值 | 限制条件 |
|-------|------|---------|-------------|
| `description` | 字符串 | `""` | 最长 2000 个字符。项目的详细描述。 |
| `category` | 字符串 | `"SaaS"` | 例如：SaaS、Fintech、Marketplace、EdTech、HealthTech、AI/ML、Developer Tools、E-commerce |
| `stack` | 字符串数组 | `[]` | 技术栈标签，例如：`["React", "Node.js", "MongoDB"]` |
| `url` | 字符串 | `null` | 项目 URL（必须是有效的 URI） |
| `status` | 字符串 | `"shipped"` | 可能的值为：`shipped`、`idea`、`prototyping`、`beta` |

### 示例请求

```bash
curl -X POST "https://backend.growthx.club/api/v1/bx/projects/agent" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $GROWTHX_API_KEY" \
  -d '{
    "name": "TaskFlow",
    "tagline": "AI-powered task management for remote teams",
    "description": "TaskFlow uses AI to automatically prioritize and assign tasks based on team capacity and deadlines.",
    "category": "SaaS",
    "stack": ["React", "Node.js", "OpenAI", "PostgreSQL"],
    "url": "https://taskflow.app",
    "status": "shipped"
  }' | jq .
```

### 成功响应（201）

```json
{
  "project": {
    "_id": "...",
    "name": "TaskFlow",
    "tagline": "AI-powered task management for remote teams",
    "status": "shipped",
    "creator": { "name": "...", "avatar_url": "..." },
    "weighted_votes": 0,
    "raw_votes": 0
  }
}
```

## 代理行为

当用户请求提交项目时，请按照以下步骤操作：

### 第一步 — 在工作区中检测项目

扫描当前工作区中的标准项目文件，以确定用户已开发的项目。需要读取的文件包括：
- `package.json` — 项目名称、描述、关键词、首页信息、仓库地址；
- `pyproject.toml` / `setup.py` / `setup.cfg` — 项目名称、描述、URL；
- `Cargo.toml` — 项目名称、描述、仓库地址、关键词；
- `go.mod` — 模块名称；
- `pubspec.yaml` — 项目名称、描述、首页信息；
- `README.md` — 项目标题（第一个 `#` 标题）和开头段落；
- `git remote -v` — 仓库地址。

**对于单仓库项目（monorepo）：**
检查工作区配置文件（`package.json` 中的 `workspaces`、`pnpm-workspace.yaml`、`turbo.json`、`nx.json`），或者包含单独配置文件的子目录。每个具有独立 `name` 和 `description` 的仓库包都可能是一个项目。

**字段的获取方式：**
| 字段 | 获取方式 |
|-------|-------------|
| `name` | 从配置文件或 `README.md` 的第一个标题中获取项目名称 |
| `tagline` | 从配置文件或 `README.md` 的第一句话中获取项目描述 |
| `description` | 综合 `README.md` 的内容和配置文件中的描述（1-3 句） |
| `stack` | 从配置文件中的依赖项判断技术栈（例如：`react` 表示使用 React 技术栈） |
| `url` | 从配置文件中的 `homepage` 或 `git remote` 中获取项目 URL |
| `category` | 根据依赖项和 `README.md` 内容判断项目类别（例如：`stripe` 表示 Fintech 类型项目） |
| `status` | 默认值为 `"shipped"`；如果 `README.md` 明确标注为 “WIP/prototype/beta”，则使用相应的状态 |

### 第二步 — 显示检测到的项目

向用户展示检测到的项目。如果检测到多个项目（例如单仓库项目），列出所有项目并询问用户希望提交哪个：
> 我在您的工作区中发现了以下项目：
> 1. **项目名称** — 简短描述
> 2. **其他项目** — 简短描述
>
> 您希望将哪个项目提交到 Built at GrowthX？

如果只检测到一个项目，直接展示该项目详情并请求用户确认。

### 第三步 — 填补缺失的信息

对于选定的项目，展示自动检测到的信息，并请求用户补充或更正以下内容：
- `name` 和 `tagline` 是必填项；如果无法自动获取 `tagline`，请让用户提供；
- 显示自动检测到的 `stack`、`category`、`url`、`description` 和 `status`，让用户进行确认或修改；
- `status` 的默认值为 `"shipped"`，除非 `README.md` 或其他信息表明项目仍处于开发阶段。

### 第四步 — 确认并提交

向用户展示将要提交的项目的详细信息：
> **即将提交到 Built at GrowthX 的项目信息：**
> - 名称：TaskFlow
> - 描述：专为远程团队设计的 AI 驱动的任务管理工具
> - 类别：SaaS
- 技术栈：React、Node.js、OpenAI、PostgreSQL
- URL：https://taskflow.app
- 状态：已发布（`shipped`）
>
> 是否确认提交？

只有在用户确认后，才使用 `x-api-key` 在 curl 请求中发送 API 请求。

### 第五步 — 报告结果

如果提交成功，告知用户项目已提交，并提供项目的链接（如果有的话）；如果失败，请向用户说明错误原因。

## 错误处理

| 状态码 | 含义 | 告诉用户的提示 |
|--------|---------|----------------------|
| `401` | API 密钥无效或已被吊销 | “您的 API 密钥无效或已被吊销。请在 Built at GrowthX 的设置中重新生成密钥。” |
| `403` | 会员资格未激活 | “您的 GrowthX 会员资格未激活。提交项目需要激活的会员资格。” |
| `400` | 验证错误（例如名称/描述缺失、字段过长等） | 显示响应体中的具体错误信息。 |