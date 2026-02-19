---
name: index1-doctor
description: 诊断 index1 环境：检查 Python、Ollama、模型以及索引的运行状态。
version: 2.0.3
license: Apache-2.0
author: gladego
tags: [index1, diagnostics, mcp, troubleshooting]
---
# index1 Doctor

这是一个用于诊断 index1 环境状态的工具，可以执行健康检查并提供修复建议。

## 使用方法

输入 `/doctor` 命令，或让代理来诊断 index1 的状态。

## 检查内容

该工具会依次执行三个命令并分析结果：

### 1. 环境检查

```bash
index1 doctor
```

检查以下内容：
- Python 版本（要求 >= 3.10）
- SQLite 版本（要求 >= 3.43.0 以支持全部功能）
- sqlite-vec 扩展
- ONNX 嵌入功能（内置，版本为 bge-small-en-v1.5）
- Ollama 连接性（可选，用于多语言/中文处理）
- 嵌入模型的可用性
- 中文/简体中文支持（jieba）

### 2. 索引状态

```bash
index1 status
```

显示以下信息：
- 文档数量和分块数量
- 集合列表
- 最后一次索引时间
- 数据库大小

### 3. Ollama 模型

```bash
ollama list
```

显示已安装的模型。推荐的嵌入模型包括：
- `nomic-embed-text` — 标准模型，大小为 270MB
- `bge-m3` — 非常适合处理中文内容，大小为 1.2GB

## 解释结果

| 检查项 | 是否通过 | 需要修复 |
|-------|--------|---------|
| Python | >= 3.10 | 需要安装 Python 3.11 或更高版本 |
| SQLite | >= 3.43.0 | 如果版本过低，系统会自动降级，无需额外操作 |
| sqlite-vec | 已加载 | 需要执行 `pip install index1` （该工具已包含该依赖） |
| Ollama | 已连接 | 需要执行 `curl -fsSL https://ollama.com/install.sh \| sh` |
| 嵌入模型 | 可用 | 需要执行 `ollama pull nomic-embed-text` |
| 中文支持 | jieba 已加载 | 需要执行 `pip install index1[chinese]` |
| 索引 | 是否包含文档 | 需要执行 `index1 index ./src ./docs` |

## 使用场景

- 首次设置时进行验证
- 升级 index1 后
- 当搜索结果异常时
- 当向量搜索功能失效时
- 在报告问题之前