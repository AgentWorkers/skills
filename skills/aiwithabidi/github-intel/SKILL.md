---
name: github-intel
description: "**AI友好型GitHub仓库分析工具**  
该工具能够以AI友好的格式分析任意GitHub仓库。它可以将整个仓库转换为单个Markdown文档，使用Mermaid生成架构图，展示仓库的结构树、代码语言分布以及最近的活动记录。工具还提供了GitHub URL处理技巧、API快捷方式以及高级搜索功能。所有分析操作均为只读模式，不会执行仓库中的任何代码。  
**适用场景：**  
- 仓库分析  
- 代码架构审查  
- 开源项目研究  
- GitHub信息收集  
- 代码库理解  
**技术特性：**  
- 仅使用Python标准库，无额外依赖  
- 专为AI代理设计  
- 支持GitHub URL处理  
- 提供API快捷方式  
- 支持高级搜索功能  
**使用说明：**  
- 将需要分析的GitHub仓库URL传递给该工具  
- 工具会自动生成详细的分析报告（Markdown格式）  
- 包含架构图、代码语言统计、活动记录等关键信息  
**注意事项：**  
- 该工具仅用于读取和分析数据，不会对仓库中的代码进行任何修改或执行操作。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🔍", "requires": {"env": []}, "primaryEnv": "GITHUB_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 🔍 GitHub Intelligence

该工具能够以人工智能友好的格式分析任何GitHub仓库，将仓库内容转换为Markdown格式，生成架构图，并理解其结构和模式。

## 主要功能

- **分析仓库结构**：文件树、README文件、代码语言分布、最近的活动记录
- **生成架构图**：根据代码库结构生成Mermaid格式的流程图
- **将仓库转换为Markdown文档**：将整个仓库内容转换为单一的、可供AI读取的文档
- **查看代码语言分布**：按语言统计文件数量及占比
- **追踪最新活动**：最新的提交记录、贡献者信息以及发布历史
- **GitHub高级用法**：隐藏的仓库功能、API快捷方式、搜索操作符
- **自定义分析深度**：可配置目录遍历的深度
- **限制文件数量**：针对大型仓库设置文件数量上限
- **仅限读取权限**：绝不执行仓库中的任何代码
- **公开API接口**：无需使用GitHub令牌（如需提高请求速率限制，可选择使用令牌）

## 使用要求

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `GITHUB_TOKEN` | ❌ | 可选——将请求速率限制从每小时60次提升至5000次。请从[GitHub设置](https://github.com/settings/tokens)获取令牌 |

## 快速入门

```bash
PY=~/.openclaw/workspace/.venv/bin/python3

# Analyze a repository
$PY skills/github-intel/scripts/repo_analyzer.py https://github.com/anthropics/claude-code

# Convert repo to single markdown
$PY skills/github-intel/scripts/repo_to_markdown.py https://github.com/openai/openai-python

# Deep analysis
$PY skills/github-intel/scripts/repo_analyzer.py https://github.com/user/repo --depth 3
```

## 命令说明

### 仓库分析工具
```bash
# Basic analysis
$PY scripts/repo_analyzer.py https://github.com/owner/repo

# Deep directory traversal
$PY scripts/repo_analyzer.py https://github.com/owner/repo --depth 3

# With authentication for higher rate limits
GITHUB_TOKEN=ghp_xxx $PY scripts/repo_analyzer.py https://github.com/owner/repo
```

### 将仓库转换为Markdown文档
```bash
# Convert full repo
$PY scripts/repo_to_markdown.py https://github.com/owner/repo

# Limit files for large repos
$PY scripts/repo_to_markdown.py https://github.com/owner/repo --max-files 50

# Output to file
$PY scripts/repo_to_markdown.py https://github.com/owner/repo > repo.md
```

## 分析工具的输出格式

```
# Repository: owner/repo

## Structure
├── src/
│   ├── index.ts
│   └── ...
├── README.md
└── package.json

## README
[Full README content]

## Language Breakdown
- TypeScript: 78.2%
- JavaScript: 15.1%
- Shell: 6.7%

## Architecture (Mermaid)
graph TD
  A[CLI Entry] --> B[Command Parser]
  ...

## Recent Activity
- 2 days ago: feat: add streaming support
- 5 days ago: fix: handle timeout errors
```

## 参考资料

| 文件名 | 说明 |
|------|-------------|
| `references/github-tricks.md` | GitHub的URL技巧、API快捷方式、搜索操作符 |

## 脚本参考

| 脚本名 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/repo_analyzer.py` | 全面分析仓库内容并生成架构图 |
| `{baseDir}/scripts/repo_to_markdown.py` | 将仓库内容转换为Markdown文档 |

## ⚠️ 安全须知

**本工具仅具有读取权限，绝不执行以下操作：**
- 不会执行仓库中的任何代码
- 不会运行脚本、构建文件或执行编译命令
- 不会解析仓库中的任何内容
- 不会向任何仓库写入数据

所有分析操作仅限于读取仓库中的静态文件。

## 数据政策

该工具通过GitHub的API获取公开数据。分析结果不会被本地存储。

---

开发者：[M. Abidi](https://www.agxntsix.ai)

[LinkedIn](https://www.linkedin.com/in/mohammad-ali-abidi) · [YouTube](https://youtube.com/@aiwithabidi) · [GitHub](https://github.com/aiwithabidi) · [预约咨询](https://cal.com/agxntsix/abidi-openclaw)