---
name: openclaw-workspace-pro
description: 适用于 OpenClaw 代理的生产就绪型工作空间设置。该设置实现了工件工作流程（artifact workflows）、秘密管理（secret management）、内存压缩（memory compaction）以及基于 OpenAI 的 Shell + Skills 最佳实践的长时间运行代理模式（long-running agent patterns）。通过一个命令即可完成安装，将您的工作空间转换为生产就绪型环境。
version: 1.0.0
author: Eugene Devyatyh
repository: https://github.com/Eugene9D/openclaw-workspace-pro
metadata:
  openclaw:
    install:
      - id: setup
        kind: script
        script: ./install.sh
        label: Install Workspace Pro enhancements
---
# OpenClaw Workspace Pro

专为长时间运行的 OpenClaw 代理设计的企业级工作空间解决方案。

## 功能介绍

OpenClaw Workspace Pro 通过以下方式优化您的工作空间，使其更符合生产环境的要求：

- **🗂 工件流程（Artifact Workflow）**：为报告、代码、数据和导出文件提供标准化的输出结构。
- **🔒 秘密管理（Secrets Management）**：使用安全的 `.env` 文件格式存储敏感信息，避免明文密码的暴露。
- **🧠 内存压缩（Memory Compaction）**：通过系统化的归档流程防止内存占用过高。
- **📦 长期运行模式（Long-Running Patterns）**：支持容器复用、检查点机制以及数据连续性保障。
- **🛡 安全基线（Security Baseline）**：设置网络允许列表，确保凭证的安全处理。

这些功能均基于 OpenAI 的 [Shell + Skills + Compaction](https://developers.openai.com/blog/skills-shell-tips) 最佳实践进行设计。

## 安装

**自动安装：**  
```bash
clawhub install openclaw-workspace-pro
```

**手动安装：**  
```bash
cd /data/.openclaw/workspace
git clone https://github.com/Eugene9D/openclaw-workspace-pro.git
cd openclaw-workspace-pro
./install.sh
```

## 安装内容

### 目录结构  
```
workspace/
├── artifacts/           # Standardized output location
│   ├── reports/        # Analysis, summaries, documentation
│   ├── code/           # Generated scripts, apps, configs
│   ├── data/           # Cleaned datasets, processed files
│   └── exports/        # API responses, database dumps
├── memory/
│   └── archive/        # Compressed memory summaries
├── .env                # Secrets (gitignored)
└── .gitignore          # Security
```

### 新增的文档文件：  
- **AGENTS.md**：详细介绍工件流程、长期运行模式及秘密管理机制。  
- **MEMORY-COMPACTION.md**：包含每周/每月的维护工作流程。  
- **TOOLS.md**：包含网络安全允许列表的相关内容。

### 模板文件：  
- `.env.example`：用于存储敏感信息的模板文件。  
- `.gitignore`：用于排除不需要版本控制的文件。

## 使用方法

### 工件流程（Artifact Workflow）

在生成交付物时，请按照以下步骤操作：  
```bash
# Reports
/data/.openclaw/workspace/artifacts/reports/YYYY-MM-DD-project-name.md

# Code
/data/.openclaw/workspace/artifacts/code/YYYY-MM-DD-script-name.py

# Data
/data/.openclaw/workspace/artifacts/data/YYYY-MM-DD-dataset.csv
```

**优势：**  
- 明确的文件管理边界。  
- 便于文件检索。  
- 支持版本跟踪。  
- 避免文件杂乱无章。

### 秘密管理（Secrets Management）

**使用 OpenClaw Pro 之前：**  
```markdown
# TOOLS.md
API_KEY=sk-abc123xyz...  ❌ Plaintext, exposed in git
```

**使用 OpenClaw Pro 之后：**  
```bash
# .env (gitignored)
API_KEY=sk-abc123xyz...

# TOOLS.md
API Key: $API_KEY  ✅ Reference only
```

### 内存压缩（Memory Compaction）

为长时间运行的代理程序优化内存使用：

**每周（根据需要）：**  
1. 查看过去 7-14 天的日志。  
2. 提取关键信息并更新 `MEMORY.md` 文件。  
3. 删除过时的数据。

**每月：**  
1. 将超过 30 天的日志归档到 `memory/archive/YYYY-MM-summary.md` 文件中。  
2. 归档完成后删除原始日志文件。  
详细的工作流程请参阅 `MEMORY-COMPACTION.md`。

## 为何选择 OpenClaw Workspace Pro？

### 问题所在

默认的 OpenClaw 工作空间存在以下问题：  
- 文件分散无序（缺乏结构）。  
- API 密钥以明文形式存储（存在安全风险）。  
- 内存使用量持续增长（超出系统限制）。  
- 无法有效管理交付物。  
- 需要手动维护（容易导致系统混乱）。

### 解决方案

OpenClaw Workspace Pro 采用了 OpenAI 推荐的最佳实践：  
- ✅ 标准化的工件处理流程。  
- ✅ 安全的秘密管理机制。  
- 系统化的内存压缩策略。  
- 适用于长时间运行的代理程序。  
- 明确的操作流程。

### 实际效果

- **安全性**：有效防止凭证泄露。  
- **组织性**：交付物管理更加清晰。  
- **可扩展性**：支持长时间连续运行。  
- **维护性**：定期维护确保系统稳定运行。

## 配置要求

### 环境变量（.env 文件）

安装完成后，请配置 `.env` 文件中的环境变量：  
```bash
# Example: YouTube API
YOUTUBE_API_KEY=your_key_here
YOUTUBE_OAUTH_CLIENT_ID=your_id_here

# Example: Task Management
VIKUNJA_API_TOKEN=your_token_here
```

### 网络安全

请编辑 `TOOLS.md` 文件中的网络允许列表：  
```markdown
### Approved Domains
- *.googleapis.com (YouTube API)
- api.brave.com (search)
- tasks.playrockets.com (Vikunja)
```

**新增域名时，请进行安全审查。**

## 系统要求：  
- OpenClaw 版本：2026.2.9 或更高。  
- 工作空间目录：`/data/.openclaw/workspace`。  
- 需要具备 Shell 访问权限以完成安装。

## 升级说明  

```bash
cd /data/.openclaw/workspace/openclaw-workspace-pro
git pull
./install.sh
```

## 卸载方法

OpenClaw Workspace Pro 是非破坏性的。卸载方法如下：  
```bash
# Remove added files (safe, preserves your data)
rm -rf artifacts/ memory/archive/
rm .env .gitignore MEMORY-COMPACTION.md

# Restore AGENTS.md, TOOLS.md from backup
cp AGENTS.md.backup AGENTS.md
cp TOOLS.md.backup TOOLS.md
```

## 技术支持

- **问题反馈：** [https://github.com/Eugene9D/openclaw-workspace-pro/issues](https://github.com/Eugene9D/openclaw-workspace-pro/issues)  
- **讨论区：** [https://discord.com/invite/clawd](https://discord.com/invite/clawd)  
- **ClawHub：** [https://clawhub.ai/skills/openclaw-workspace-pro](https://clawhub.ai/skills/openclaw-workspace-pro)  

## 许可证

本软件采用 MIT 许可证。详细许可信息请参阅 `LICENSE` 文件。

## 致谢

本项目的开发基于以下资源：  
- OpenAI 的 [Shell + Skills + Compaction](https://developers.openai.com/blog/skills-shell-tips) 最佳实践。  
- OpenClaw 社区的使用经验。  
- Glean 公司的企业级技能部署方案。  

**开发者：** Eugene Devyatyh  

**版本信息：** 1.0.0  
**更新时间：** 2026-02-13  
**兼容性：** OpenClaw 2026.2.9 及更高版本。