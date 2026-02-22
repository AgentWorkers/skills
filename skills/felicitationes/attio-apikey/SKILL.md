---
name: attio-apikey
description: >
  OpenClaw 的 Direct Attio CRM 集成功能，支持完整的 CRUD 操作（查询、创建、更新和删除）。  
  可以实时查询、创建、更新和删除公司、人员和笔记等数据。  
  直接使用 Attio 的 API 密钥进行通信，无需 OAuth 或代理服务器。
compatibility: OpenClaw with exec tool
credentials:
  requiredEnv:
    - ATTIO_API_KEY
metadata:
  author: felixwithoutx
  version: "1.0.1"
  tags:
    - attio
    - crm
    - sales
    - pipeline
  license: MIT
---
# Attio Direct Skill

Attio Direct 提供了与 Attio CRM 的集成功能，支持完整的 CRUD（创建、读取、更新、删除）操作。

## 设置

1. 从 https://app.attio.com/settings/api 获取 API 密钥。
2. 将 `.env.example` 文件复制到 `.env` 文件中，并添加你的 API 密钥。

## 快速命令

```bash
# Read data
python3 attio_client.py companies
python3 attio_client.py people

# Create
python3 attio_client.py companies --create --data '{"name": "Acme"}'

# Update
python3 attio_client.py companies --update --id RECORD_ID --data '{"funnel_stage": "Nurture"}'

# Delete
python3 attio_client.py companies --delete --id RECORD_ID

# Add note
python3 attio_client.py companies --note "Title|Content" --id RECORD_ID
```

## 功能特性

- 支持对公司和人员的完整 CRUD 操作。
- 可为任何记录添加备注。
- 支持分页查询（默认每页显示 5000 条记录）。
- 通过直接调用 API 进行操作，无需 OAuth 验证。

## 相关文件

```
attio-direct/
├── attio_client.py    # Main CLI
├── .env.example       # API key template
├── README.md          # Setup instructions
└── SKILL.md          # This file
```