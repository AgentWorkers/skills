---
name: Docs Generator
description: 自动化文档生成工具。支持生成API文档、README文件、CHANGELOG（变更日志）、贡献指南、架构文档、教程、FAQ（常见问题解答）以及参考手册。支持REST、GraphQL和OpenAPI规范。适用于技术文档编写及开发者工具的开发。
---
# 文档生成器 — 自动化文档生成工具

将编写文档的时间减少，将更多时间用于编写代码。

## 命令列表

```
┌─ api ──────── REST/GraphQL API documentation
├─ readme ───── Project README.md
├─ changelog ── Version change log
├─ contributing Contributing guide
├─ architecture System architecture docs
├─ tutorial ─── Tutorial / quick start guide
├─ faq ──────── Frequently asked questions
└─ reference ── Complete reference manual
```

## 使用方法

```bash
bash scripts/docs-generator.sh api rest users
bash scripts/docs-generator.sh readme myproject "A cool tool"
bash scripts/docs-generator.sh changelog 2.0.0 "New features"
```

## 参数

- `api <类型> <资源>` — 类型：restgraphql（RESTful GraphQL接口）；资源名称
- `readme <名称> <描述>` — 项目名称及描述
- `changelog <版本> <摘要>` — 版本号及版本更新摘要
- `contributing <项目>` — 贡献者项目名称
- `architecture <项目> <架构>` — 架构类型：单体应用/微服务/无服务器架构
- `tutorial <主题> <难度>` — 教程难度：初级/中级/高级
- `faq <主题> <数量>` — 生成指定数量的常见问题解答（FAQ）条目
- `reference <库> <语言>` — 库名称及使用语言

## 设计理念

文档也是一种产品。优质的文档 = 更多的用户 = 更少的技术问题。