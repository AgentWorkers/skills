---
name: aoi-triple-memory-lite
version: 0.1.0
description: AOI Triple Memory (Lite) — 文件搜索功能及决策记录模板（无需插件支持）。
author: Aoineco & Co.
license: MIT
---
# AOI Triple Memory (Lite)

S-DNA: `AOI-2026-0215-SDNA-MEM01`

## 产品简介
这是一个公开可用、无需安装任何插件的内存管理工具：

## 来源与原创性
- AOI 的实现完全基于原创代码（未使用任何第三方代码）。
- 其设计理念借鉴了常见的“多层内存”概念（文件管理、搜索功能以及结构化的决策记录）：
  1) **基于文件的存储**：`MEMORY.md` 文件以及按日期格式命名的子文件（例如 `memory/2022-01-01.md`）。
  2) **决策记录**：包含标签的结构化笔记，用于记录决策过程。
  3) **快速搜索**：利用 `ripgrep` 在整个工作区范围内进行高效搜索。

## 产品特性
- **不支持** 外部嵌入数据库。
- **不提供** 自动数据捕获功能。
- **不支持** 与其他机器的同步。

## 命令操作
### 在工作区内搜索
```bash
aoi-memory search --q "Tempo Hackathon" --n 20
```

### 创建决策记录（模板）
```bash
aoi-memory new-note --title "Royalty rail decision" --tag royalty,base,usdc
```

## 开源治理说明（公开信息）
我们免费发布 AOI 相关的技能，并持续对其进行改进。每次发布版本都必须通过我们的安全审查流程，并附带可审计的变更日志。我们不会发布任何会削弱安全性或降低许可清晰度的更新。如果多次违反规定，将会逐步采取限制措施（从警告开始，到暂停发布，最终可能归档该技能）。

## 技术支持
- 如有疑问、漏洞或功能请求，请访问：https://github.com/edmonddantesj/aoi-skills/issues
- 请在问题描述中注明技能的名称：`aoi-triple-memory-lite`。

## 许可协议
MIT 许可协议