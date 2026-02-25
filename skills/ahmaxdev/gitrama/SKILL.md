---
name: gitrama
description: 由 AI 支持的 Git 历史查询功能。当用户询问 Git 历史记录、提交信息、分支名称、仓库洞察、代码变更情况，或希望了解代码库中发生的事情时，可使用此功能。触发关键词包括：`git history`、`commit message`、`branch name`、`who changed`、`what happened`、`repo summary`、`code archaeology`、`semantic search git`、`generate commit`、`smart commit`、`git log analysis`、`contributor insights`。
version: 1.0.0
homepage: https://gitrama.ai
metadata:
  openclaw:
    emoji: "🌿"
    requires:
      bins:
        - git
        - pip
      binsAnyOf:
        - python3
        - python
    install:
      pip:
        - gitrama
---
# Gitrama — 强大的 Git 历史分析工具

Gitrama 是一个命令行工具（CLI），它为你的 Git 历史记录提供了基于人工智能的语义搜索和分析功能。该工具内置了 **AskGIT**，这是一个能够理解整个仓库上下文的人工智能助手。

所有人工智能处理都在服务器端通过 `api.gitrama.ai` 完成，无需使用 API 密钥——只需安装即可使用。

## 主要功能

### 1. AskGIT — 语义 Git 历史查询
你可以用自然语言提问来查询仓库的相关信息：
- “上个月对认证模块做了哪些修改？”
- “谁是 API 层的主要贡献者？”
- “总结最近 20 条提交的内容”
- “从 v1.0 到 v2.0 之间发生了哪些破坏性变更？”

**命令：** `gtr chat`

AskGIT 会自动从 10 个 Git 子进程调用中收集相关信息（分支信息、最近提交的更改、差异、贡献者等），并将这些数据发送到 `api.gitrama.ai` 进行智能分析。

### 2. 智能提交信息生成
根据暂存区的更改生成规范的提交信息：
- 分析 `git diff --staged` 的输出
- 生成符合项目提交规范的提交信息（例如：`feat:`、`fix:`、`docs:` 等）
- 遵循项目的提交命名规则

**命令：** `gtr commit`

### 3. 分支名称生成
根据任务描述生成简洁明了的分支名称：
- 遵循 Git 分支命名规范
- 包含类型前缀（如 `feature/`、`bugfix/`、`hotfix/`）
- 确保名称简洁且具有描述性

**命令：** `gtr branch`

### 4. Git 日志分析与仓库洞察
提供关于仓库的智能分析结果：
- 贡献者的活动模式
- 按代码领域划分的更改频率
- 发布历史总结
- 技术债务指标

**命令：** 先运行 `gtr chat`，然后询问仓库相关的洞察信息

## 安装

Gitrama 通过 PyPI 进行分发：

```bash
pip install gitrama
```

验证安装是否成功：

```bash
gtr version
```

## 配置

Gitrama 无需配置 API 密钥或额外设置，安装完成后即可直接使用。所有人工智能处理都在服务器端 `api.gitrama.ai` 完成。

可选的配置选项如下：

```bash
gtr config
```

## 使用示例

当用户需要查询 Git 历史或仓库信息时，运行相应的 Gitrama 命令：

```bash
# Start an interactive chat about the repo
gtr chat

# Generate a commit message for staged changes
gtr commit

# Generate a branch name
gtr branch "add user authentication with OAuth"

# Quick shortcuts
gtr c   # alias for commit
gtr b   # alias for branch
gtr ch  # alias for chat
```

## 数据流程

- 通过 Git 子进程调用在本地收集提交记录、差异和分支信息
- 将这些数据发送到 `api.gitrama.ai` 进行处理
- 用户的机器上不会存储或使用任何 API 密钥
- 所有的智能分析功能都在服务器端运行

## 重要说明

- Gitrama 必须在 Git 仓库内部运行
- AskGIT 会保留最多 40 条对话记录以支持多轮交互
- 该工具会自动收集仓库的上下文信息，无需手动配置
- 传输到 `api.gitrama.ai` 的仓库数据仅用于生成响应，不会被存储

## 错误处理

- 如果安装后找不到 `gtr` 命令：
```bash
# Ensure pip scripts are on PATH
python3 -m gitrama --version
```

- 如果连接过程中出现错误：
```bash
# Verify api.gitrama.ai is reachable
curl -s https://api.gitrama.ai/health
```

## 链接

- 官网：https://gitrama.ai
- PyPI 页面：https://pypi.org/project/gitrama/