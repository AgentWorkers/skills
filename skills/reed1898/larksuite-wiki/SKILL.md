---
name: larksuite-wiki
description: 管理和导出 Lark Suite（Feishu）的 Wiki/知识库文档。支持阅读、搜索文档内容，与子文档进行同步，并可将文档内容增量式导出为本地 Markdown 文件。
homepage: https://open.larksuite.com
tags: [lark, wiki, knowledge-base, export, sync, markdown]
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "env": ["LARK_APP_ID", "LARK_APP_SECRET"] },
        "primaryEnv": "LARK_APP_ID",
      },
  }
---

# Lark Suite 维基

用于管理和导出 Lark Suite（Feishu）维基/知识库文档，支持递归同步和增量更新。

## 先决条件

1. 在 https://open.larksuite.com/console 创建一个 Lark/Feishu 应用程序。
2. 启用以下权限：
   - `docs:doc:read`
   - `drive:drive:read`
   - `wiki:wiki:read`
3. 发布该应用程序并授权其访问您的维基。
4. 设置环境变量（或编辑脚本默认值）：
   ```bash
   export LARK_APP_ID="cli_xxxxxxxx"
   export LARK_APP_SECRET="xxxxxxxx"
   ```

## 命令

### 列出维基空间
```bash
larksuite-wiki spaces
```

### 阅读文档（包含子文档链接）
```bash
larksuite-wiki read <doc_id_or_url>
```

### 导出单个文档
```bash
larksuite-wiki export <doc_id_or_url> --output ./docs/
```

### 显示文档树结构
```bash
larksuite-wiki tree <doc_id_or_url>
```

### 同步整个维基（递归导出）
```bash
# First sync - exports all documents
larksuite-wiki sync <doc_id_or_url> --output ./lark-wiki/

# Incremental sync - only exports changed documents
larksuite-wiki sync <doc_id_or_url> --output ./lark-wiki/

# Force re-export everything
larksuite-wiki sync <doc_id_or_url> --output ./lark-wiki/ --force
```

## 功能特点

### 1. ✅ 批量导出
通过一个命令即可导出整个知识库。

### 2. ✅ 递归导出子文档
自动跟踪并导出所有链接的子文档。

### 3. ✅ 保留目录结构
生成的文件夹结构与维基结构一致：
```
lark-wiki/
├── 01_首页/
│   ├── 01_首页.md
│   └── 01_日常复盘/
│       ├── 01_日常复盘.md
│       └── ...
├── 02_云聪金融分析/
│   └── ...
```

### 4. ✅ 增量同步
跟踪文档修订信息，仅导出已更改的文档：
- 将同步状态保存到 `.lark-sync-state.json` 文件中
- 比较修订版本号
- 跳过未更改的文档

## 快速入门

### 导出整个维基
```bash
# Get your wiki root document ID from the URL
# https://xxx.larksuite.com/wiki/TDCZweBJ2iMFO4kI1LAlSE62gnd

# Sync everything
python3 larksuite-wiki.py sync TDCZweBJ2iMFO4kI1LAlSE62gnd --output ./my-wiki/
```

### 每日增量同步
```bash
# Run daily - only exports changed documents
python3 larksuite-wiki.py sync TDCZweBJ2iMFO4kI1LAlSE62gnd --output ./my-wiki/
```

## 输出结构

每个文档都有自己的文件夹：
- 主 `.md` 文件
- 子文档对应的子文件夹
- 文件名前缀带有编号（如 01_、02_ 等）

## API 参考

- Lark 开放平台：https://open.larksuite.com/
- 维基 API：https://open.larksuite.com/document/uAjLw4CM/ukTMukTMukTM/reference/wiki-v1/space/overview
- Docx API：https://open.larksuite.com/document/uAjLw4CM/ukTMukTMukTM/reference/docx-v1/document/overview

## 注意事项

- 文档必须明确授权给您的应用程序使用。
- 某些区块类型可能无法完美转换为 Markdown 格式。
- 包含大量子文档的大型维基同步可能需要较长时间。
- 同步状态会保存在本地，以便进行增量更新。