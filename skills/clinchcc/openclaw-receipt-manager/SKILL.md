---
name: receipt-manager
description: Receipt management skill. Use when: (1) User sends a receipt image, (2) User asks about expenses or receipts, (3) User wants monthly spending summary.
---

# 收据管理器

用于在本地存储和查询收据数据。

## 触发条件

- 收据、费用、发票、支出、报销申请

## 使用方法

### 1. 初始化（首次使用）

```bash
python3 scripts/receipt_db.py init
```

### 2. 添加收据

当 OpenClaw 识别到收据图片后，数据会通过处理程序自动保存到数据库中。

### 3. 查询

```bash
# List all
python3 scripts/receipt_db.py list

# Search
python3 scripts/receipt_db.py search --q "walmart"

# Monthly summary
python3 scripts/receipt_db.py summary --month 2026-02
```

## 相关文件

- `scripts/receipt_db.py` - 主要的命令行工具
- `scripts/handler.py` - 从 OpenClaw 接收 JSON 数据并保存到数据库
- `data/receipts/` - 本地 SQLite 数据库及收据图片文件

## 隐私政策

所有数据均存储在您的本地机器上，不会上传到云端。