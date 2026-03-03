---
name: deepwiki-mcp-skill
description: 您可以使用 DeepWiki MCP 来向任何 GitHub 仓库提问或阅读相关文档。当您需要理解代码库的架构、查找特定的 API，或获取关于某个仓库的详细信息时，都可以使用它。
metadata:
  short-description: Query GitHub repo docs via DeepWiki
---
# DeepWiki 技能

使用此技能可以查询 GitHub 仓库的文档，并对代码库提出问题。

## 先决条件

- `uxc` 已安装，并且已添加到 `PATH` 环境变量中。
- 具备访问 `mcp.deepwiki.com/mcp` 的网络权限。

**注意：** 仓库必须先在 DeepWiki 上进行索引。请访问 https://deepwiki.com 以对仓库进行索引。

### 安装 uxc

选择以下方法之一进行安装：

**Homebrew（macOS/Linux）：**
```bash
brew tap holon-run/homebrew-tap
brew install uxc
```

**安装脚本（macOS/Linux，运行前请仔细阅读）：**
```bash
curl -fsSL https://raw.githubusercontent.com/holon-run/uxc/main/scripts/install.sh -o install-uxc.sh
less install-uxc.sh
bash install-uxc.sh
```

**Cargo：**
```bash
cargo install uxc
```

## 核心工作流程

1. 默认情况下，使用固定的命令链接：
   - `command -v deepwiki-mcp-cli`
   - 如果该命令不存在，请使用以下命令创建它：`uxc link deepwiki-mcp-cli mcp.deepwiki.com/mcp`
   - `deepwiki-mcp-cli -h`
   - 如果检测到命令冲突且无法安全地重复使用，请停止操作，并联系技能维护者选择其他命令名称。

2. 对某个仓库提出问题：
   - `deepwiki-mcp-cli ask_question repoName=owner/repo question='你的问题'`

3. 查看仓库的文档结构：
   - `deepwiki-mcp-cli read_wiki_structure repoName=owner/repo`

4. 查看仓库的文档内容：
   - `deepwiki-mcp-cli read_wiki_contents repoName=owner/repo`

## 可用工具

- **ask_question**：对 GitHub 仓库提出任何问题，并获得基于 AI 的回复。
- **read_wiki_structure**：获取仓库的文档主题列表。
- **read_wiki_contents**：查看仓库的文档内容。

## 使用示例

### 询问代码库的相关信息
```bash
deepwiki-mcp-cli ask_question repoName=facebook/react question='How does useState work?'
```

### 探索仓库结构
```bash
deepwiki-mcp-cli read_wiki_structure '{"repoName":"facebook/react"}'
```

### 查看文档
```bash
deepwiki-mcp-cli read_wiki_contents repoName=facebook/react
```

## 输出解析

响应结果是一个 MCP JSON 格式的数据包。请从 `.data.content[].text` 中提取所需内容。

## 注意事项

- 每个问题最多只能查询 10 个仓库。
- 一些热门仓库可能已经被索引在 DeepWiki 上。
- 回答内容基于实际的代码库内容。
- `deepwiki-mcp-cli <操作> ...` 等价于 `uxc mcp.deepwiki.com/mcp <操作> ...`。
- 如果链接设置暂时不可用，请使用直接的 `uxc mcp.deepwiki.com/mcp ...` 命令作为备用方案。

## 参考文件

- 工作流程详情：`references/usage-patterns.md`