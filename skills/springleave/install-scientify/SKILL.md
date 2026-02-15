---
name: install-scientify
description: "安装 Scientify——这款由 AI 驱动的研发工作流程自动化插件。它提供了许多实用的功能，包括创意生成、文献检索、研究流程管理、Arxiv 数据库搜索以及工作区管理等功能。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔬",
        "install":
          [
            {
              "id": "scientify",
              "kind": "node",
              "package": "scientify",
              "label": "Install Scientify plugin (npm)",
            },
          ],
      },
  }
---

# 安装 Scientify

**Scientify** 是一个基于人工智能（AI）的研究工作流程自动化插件，专为 OpenClaw 设计。

## 您将获得的功能

### 功能（由大型语言模型（LLM）提供支持）

| 功能 | 描述 |
|-------|-------------|
| **创意生成** | 生成创新的研究想法。搜索 arXiv/GitHub，下载论文，分析文献，并输出 5 个带有引用信息的创意。 |
| **研究流程** | 从创意到实施的全流程自动化研究工作流程：创意 → 文献调研 → 计划 → 实施 → 审查 → 循环改进。 |
| **文献综述** | 从收集到的论文中生成结构化的笔记和总结。 |
| **arxiv** | 在 arXiv.org 上搜索论文并下载对应的 .tex 文件。 |

### 命令（直接使用，无需依赖 LLM）

| 命令 | 描述 |
|---------|-------------|
| `/research-status` | 显示工作区状态 |
| `/papers` | 列出已下载的论文 |
| `/ideas` | 列出生成的创意 |
| `/projects` | 列出所有项目 |
| `/project-switch <id>` | 切换项目 |
| `/project-delete <id>` | 删除项目 |

### 所需工具

- **arxiv**：提供 arXiv.org 的搜索 API，支持关键词搜索、日期筛选以及自动下载 .tex 文件的功能。

## 安装方法

运行以下命令：

```bash
npm install -g scientify
```

或者在使用该插件时让 OpenClaw 自动完成安装。

之后，请将其添加到您的 OpenClaw 配置文件中：

```json
{
  "plugins": ["scientify"]
}
```

## 使用示例

### 生成研究创意

```
帮我调研 "长文档摘要" 领域，生成一些创新的研究想法
```

### 日常文献跟踪

```
帮我设置一个定时任务，每天检查 arXiv 上关于 "transformer efficiency" 的新论文，发到飞书
```

### 检查工作区状态

```
/research-status
```

## 链接

- npm: https://www.npmjs.com/package/scientify
- GitHub: https://github.com/tsingyuai/scientific
- 开发者：tsingyuai