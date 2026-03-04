---
name: data-pods
description: 创建并管理模块化、可移植的数据库Pod（基于SQLite、元数据及嵌入技术）。支持文档导入及嵌入处理，以实现语义搜索功能。整个过程完全自动化——只需简单请求即可完成。
---
# 数据Pods

## 概述
用于创建和管理可移植的、基于用户同意范围的数据库Pods。支持文档的导入以及基于语义的搜索功能。

## 架构
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Ingestion  │ ──► │   DB Pods   │ ──► │  Generation │
│  (ingest)   │     │  (storage)  │     │   (query)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## 触发操作
- “创建Pod” / “新建Pod”
- “列出我的Pods”
- “向Pod中添加内容” / “添加备注”
- “查询Pod” / “搜索Pod”
- “导入文档” / “添加文件”
- “进行语义搜索”
- “导出Pod”

## 核心功能

### 1. 创建Pod
当用户请求创建Pod时：
1. 获取Pod的名称和类型（学者/健康/共享/项目）
2. 运行命令：`python3 .../scripts/pod.py create <名称> --类型 <类型>`
3. 确认创建成功

### 2. 手动添加内容
当用户请求添加内容时：
1. 获取Pod的名称、标题和内容
2. 运行命令：`python3 .../scripts/pod.py add <Pod> --标题 "<标题>" --内容 "<内容>" --标签 "<标签>"`
3. 确认添加成功

### 3. 自动导入文档
当用户希望导入文件时：
1. 获取Pod的名称和文件夹路径
2. 运行命令：`python3 .../scripts/ingest.py ingest <Pod> <文件夹>`
3. 支持的文件格式：PDF、TXT、MD、DOCX、PNG、JPG
4. 如果安装了sentence-transformers插件，会自动对文本进行嵌入处理

### 4. 语义搜索
当用户希望进行搜索时：
1. 提供Pod的名称和搜索关键词
2. 运行命令：`python3 .../scripts/ingest.py search <Pod> "<关键词>"`
3. 返回带有引用信息的排序结果

### 5. 基本查询
当用户希望搜索笔记内容时：
1. 运行命令：`python3 .../scripts/pod.py query <Pod> --文本 "<查询内容>`

### 6. 导出
当用户希望导出数据时：
1. 运行命令：`python3 .../scripts/podsync.py pack <Pod>`

## 依赖项
```bash
pip install PyPDF2 python-docx pillow pytesseract sentence-transformers
```

## 数据存储位置
`~/.openclaw/data-pods/`

## 主要命令
```bash
# Create pod
python3 .../scripts/pod.py create research --type scholar

# Add note
python3 .../scripts/pod.py add research --title "..." --content "..." --tags "..."

# Ingest folder
python3 .../scripts/ingest.py ingest research ./documents/

# Semantic search
python3 .../scripts/ingest.py search research "transformers"

# List documents
python3 .../scripts/ingest.py list research

# Query notes
python3 .../scripts/pod.py query research --text "..."
```

## 附加说明：
- 文档导入时会自动分割成多个部分进行处理
- 通过嵌入技术实现语义搜索功能
- 文件哈希值用于防止重复导入
- 所有数据均存储在本地SQLite数据库中