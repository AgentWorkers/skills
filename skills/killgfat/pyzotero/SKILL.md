---
name: pyzotero-cli
version: 1.0.0
description: Zotero 的命令行界面：您可以通过终端搜索本地 Zotero 图书馆、列出收藏夹以及管理其中的条目。
homepage: https://github.com/urschrei/pyzotero
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "anyBins": ["pyzotero"], "bins": ["python3"] },
        "install":
          [
            {
              "id": "pipx_cli",
              "kind": "pipx",
              "package": "pyzotero[cli]",
              "label": "Install pyzotero CLI (pipx - recommended for PEP 668-compliant systems)",
              "platforms": ["linux-debian", "linux-ubuntu", "linux-arch", "linux-fedora", "linux-rhel"],
            },
            {
              "id": "pip_cli",
              "kind": "pip",
              "package": "pyzotero[cli]",
              "label": "Install pyzotero CLI (pip)",
            },
          ],
      },
  }
---

# Pyzotero CLI

这是一个用于Zotero的命令行接口，允许您在终端中搜索本地Zotero图书馆、列出收藏夹以及管理文献。

## 快速入门

```bash
# Install (PEP 668 systems)
pipx install "pyzotero[cli]"

# Enable local API in Zotero 7
# Settings > Advanced > "Allow other applications on this computer to communicate with Zotero"

# List collections
pyzotero listcollections

# Search library
pyzotero search -q "machine learning"

# Full-text search (includes PDFs)
pyzotero search -q "attention mechanisms" --fulltext
```

📖 **详细指南：** [QUICKSTART.md](QUICKSTART.md)

## 安装

### pipx（推荐用于符合PEP 668标准的系统）
```bash
pipx install "pyzotero[cli]"
```

### pip（通用安装方式）
```bash
pip install --user "pyzotero[cli]"
export PATH="$HOME/.local/bin:$PATH"
```

📖 **完整安装指南：** [INSTALL.md](INSTALL.md)

## 先决条件

### 启用本地Zotero访问权限

**使用CLI的前提条件：**
1. 安装Zotero 7（或更高版本）。
2. 进入**Zotero > 设置 > 高级设置**。
3. 勾选“允许其他应用程序与此Zotero实例进行通信”。
4. 重启Zotero。

## 核心命令

| 命令 | 功能描述 |
|---------|-------------|
| `pyzotero search -q "主题"` | 搜索指定主题的文献 |
| `pyzotero search --fulltext` | 使用全文功能进行搜索（包括PDF文件） |
| `pyzotero search --collection ID` | 在特定收藏夹中搜索文献 |
| `pyzotero listcollections` | 列出所有收藏夹 |
| `pyzotero itemtypes` | 显示文献的类型 |

## 搜索示例

### 基本搜索
```bash
# Search titles and metadata
pyzotero search -q "machine learning"

# Phrase search
pyzotero search -q "\"deep learning\""
```

### 全文搜索
```bash
# Search in PDFs and attachments
pyzotero search -q "neural networks" --fulltext
```

### 高级过滤
```bash
# Filter by item type
pyzotero search -q "methodology" --itemtype book --itemtype journalArticle

# Search within collection
pyzotero search --collection ABC123 -q "test"
```

## 输出格式

### 人类可读格式
```bash
pyzotero search -q "python"
```

### JSON格式
```bash
pyzotero search -q "topic" --json

# Process with jq
pyzotero search -q "topic" --json | jq '.[] | .title'
```

## 文档资源

| 文档 | 说明 |
|----------|-------------|
| [QUICKSTART.md] | 5分钟快速入门指南 |
| [INSTALL.md] | 安装详细步骤 |
| [EXAMPLES.md] | 实用使用示例 |
| [README.md] | 项目概述 |

## 故障排除

**连接错误（本地Zotero）：**
```
Make sure Zotero is running
Enable local API: Settings > Advanced > "Allow other applications on this computer to communicate with Zotero"
Restart Zotero
```

**命令未找到：**
```bash
export PATH="$HOME/.local/bin:$PATH"
pipx ensurepath
```

**权限问题（符合PEP 668标准的系统）：**
```bash
pipx install "pyzotero[cli]"
```

📖 **详细故障排除指南：** [INSTALL.md](INSTALL.md)

## 快速参考

```bash
# Search
pyzotero search -q "topic"
pyzotero search -q "topic" --fulltext
pyzotero search -q "topic" --json

# List
pyzotero listcollections
pyzotero itemtypes

# Filter
pyzotero search -q "topic" --itemtype journalArticle
pyzotero search --collection ABC123 -q "topic"
```

---

**如需完整文档，请参阅：**
- [QUICKSTART.md] - 快速入门
- [INSTALL.md] - 安装指南
- [EXAMPLES.md] - 使用示例
- [README.md] - 项目概述