---
name: joplin-api
description: 通过 REST API 管理 Joplin 笔记。可用于编程方式创建、读取、更新、删除或搜索 Joplin 笔记。
allowed-tools: Bash(joplin-api:*)
homepage: https://joplinapp.org/help/api/references/rest_api/
metadata:
  openclaw:
    requires:
      bins: [python3]
    install:
      - id: deps
        kind: pip
        package: requests python-dotenv
        label: Install Python dependencies
    env:
      - name: JOPLIN_BASE_URL
        required: false
        default: http://localhost:41184
        description: Joplin Data API base URL
      - name: JOPLIN_TOKEN
        required: true
        description: API Token from Joplin Web Clipper settings
      - name: JOPLIN_IMPORT_DIR
        required: false
        default: /root/.openclaw/workspace
        description: Allowed directory for import operations
      - name: JOPLIN_EXPORT_DIR
        required: false
        default: /root/.openclaw/workspace
        description: Allowed directory for export operations
---
# Joplin API 技能

通过 Joplin Data API 管理 Joplin 的笔记、笔记本和标签。

---

## 环境变量

| 变量        | 是否必需 | 默认值    | 说明                          |
|------------|---------|---------|-------------------------------------------|
| `JOPLIN_BASE_URL` | 否       | `http://localhost:41184` | Joplin API 的 URL                      |
| `JOPLIN_TOKEN` | 是       | -         | 来自 Web Clipper 的 API 令牌                |

---

## 快速入门

### 1. 获取 API 令牌

1. 打开 Joplin → **工具** → **选项** → **Web Clipper**
2. 启用该服务并复制 API 令牌

### 2. 测试连接

```bash
python3 joplin.py ping
```

---

## 基本命令

```bash
python3 joplin.py ping                    # Test connection
python3 joplin.py create --title "Title"  # Create note
python3 joplin.py search "keyword"        # Search
python3 joplin.py list --type notes       # List notes
python3 joplin.py stats                   # Statistics
```

---

## 安全性

- 导入/导出操作仅限于工作区目录
- 敏感系统目录被禁止访问

---

## 文档资料

- `references/API.md` - 完整的 API 参考文档
- `references/CONFIGURATION.md` - 配置示例