---
name: feishu-api-docs
description: 从官方的 apifox 镜像中获取 Feishu (Lark) 的 API 文档。支持搜索和提取 API 架构信息。
---

# Feishu API 文档技能

该技能帮助 AI 代理查找 Feishu 开放平台（Feishu Open Platform）的正确 API 结构。

## 使用方法
```bash
node skills/feishu-api-docs/index.js search "create document"
node skills/feishu-api-docs/index.js get "im/v1/messages"
```