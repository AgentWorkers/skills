---
name: zotero-cli
version: 1.0.0
description: Zotero 的命令行界面：您可以通过终端搜索 Zotero 图书馆中的内容、添加/编辑笔记、阅读附件以及管理参考文献。
homepage: https://github.com/jbaiter/zotero-cli
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "bins": ["python3"], "anyBins": ["zotcli", "zotero-cli"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "zotero-cli",
              "label": "Install zotero-cli Python package (pip)",
            },
            {
              "id": "pipx",
              "kind": "pipx",
              "package": "zotero-cli",
              "label": "Install zotero-cli Python package (pipx - recommended for systems with PEP 668 compliance)",
              "platforms": ["linux-debian", "linux-ubuntu", "linux-arch", "linux-fedora", "linux-rhel"],
            },
          ],
      },
  }
---

# Zotero CLI

Zotero CLI（命令行接口）是专为Zotero参考管理器设计的工具，通过Zotero API提供终端访问您的Zotero图书馆的功能。

## 快速入门

```bash
# Install (PEP 668 systems)
sudo apt install pipx && pipx ensurepath && pipx install zotero-cli

# Configure
zotcli configure

# Start using
zotcli query "machine learning"
zotcli add-note "\"deep learning\""
zotcli read "\"attention mechanism\""
```

📖 **详细指南：** [QUICKSTART.md](QUICKSTART.md)

## 安装

### pipx（推荐用于符合PEP 668标准的系统）
```bash
pipx install zotero-cli
```

### pip（通用安装方式）
```bash
pip install --user zotero-cli
export PATH="$HOME/.local/bin:$PATH"
```

### 虚拟环境
```bash
python3 -m venv ~/.venvs/zotero-cli
source ~/.venvs/zotero-cli/bin/activate
pip install zotero-cli
```

📖 **完整安装指南：** [INSTALL.md](INSTALL.md)

## 核心命令

| 命令 | 描述 |
|---------|-------------|
| `zotcli query "topic"` | 在图书馆中搜索指定主题的文献 |
| `zotcli add-note "paper"` | 添加新笔记 |
| `zotcli edit-note "paper"` | 编辑现有笔记 |
| `zotcli read "paper"` | 读取笔记中的第一份PDF附件 |
| `zotcli configure` | 配置API凭据 |

## 配置

```bash
# Set default editor
export VISUAL=nano  # or vim, emacs, code

# Run configuration
zotcli configure

# Verify setup
./scripts/setup_and_check.sh
```

## 辅助脚本

| 脚本 | 用途 |
|--------|---------|
| `setup_and_check.sh` | 自动化设置与验证 |
| `backup_restore.sh` | 备份和恢复配置 |
| `update_check.sh` | 检查是否有更新 |
| `quick_search.py` | 格式化搜索结果 |
| `export_citations.py` | 导出引用（BibTeX、RIS格式） |
| `batch_process.sh` | 批量处理多个查询 |

**使用示例：**

```bash
# Quick search
python scripts/quick_search.py "topic" --format table

# Export citations
python scripts/export_citations.py "topic" --format bib > refs.bib

# Backup
./scripts/backup_restore.sh backup

# Update check
./scripts/update_check.sh check
```

📖 **脚本文档：** [scripts/README.md](scripts/README.md)

## 查询语法

```bash
"neural AND networks"        # Boolean AND
"(deep OR machine) AND learning"  # OR + grouping
"learning NOT neural"        # NOT
"\"deep learning\""          # Phrase search
"transform*"                 # Prefix search
```

## 工作流程

### 文献综述
```bash
zotcli query "topic"
zotcli add-note "paper"
python scripts/export_citations.py "topic" --format bib > refs.bib
```

### 日常研究
```bash
python scripts/quick_search.py "\"recent\"" --format table
zotcli add-note "\"interesting paper\""
./scripts/backup_restore.sh backup
```

📖 **更多示例：** [EXAMPLES.md](EXAMPLES.md)

## 文档资源

| 文档 | 描述 |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | 5分钟快速入门指南 |
| [INSTALL.md](INSTALL.md) | 安装详细步骤 |
| [EXAMPLES.md](EXAMPLES.md) | 实用使用示例 |
| [scripts/README.md](scripts/README.md) | 辅助脚本说明 |

## 故障排除

**命令未找到：**
```bash
export PATH="$HOME/.local/bin:$PATH"
pipx ensurepath
```

**权限被拒绝（PEP 668系统）：**
```bash
pipx install zotero-cli
```

**配置错误：**
```bash
zotcli configure
```

📖 **详细故障排除指南：** [INSTALL.md](INSTALL.md)

## 快速参考

```bash
# Essential commands
zotcli query "topic"              # Search
zotcli add-note "paper"           # Add note
zotcli edit-note "paper"          # Edit note
zotcli read "paper"               # Read PDF

# Helper scripts
./scripts/setup_and_check.sh      # Setup
./scripts/backup_restore.sh backup # Backup
./scripts/update_check.sh check   # Update
./scripts/batch_process.sh queries.txt --output results.txt  # Batch
```

---

**如需完整文档，请参阅：**
- [QUICKSTART.md](QUICKSTART.md) - 快速入门
- [INSTALL.md](INSTALL.md) - 安装指南
- [EXAMPLES.md](EXAMPLES.md) - 使用示例
- [SKILL_SUMMARY.md](SKILL_SUMMARY.md) - 全面概述