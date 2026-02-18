---
name: index1-doctor
description: 诊断 index1 环境：检查 Python、Ollama、模型以及索引的运行状态。
version: 2.0.1
license: Apache-2.0
author: gladego
tags: [index1, diagnostics, mcp, troubleshooting]
---
# index1 Doctor

这是一个用于诊断index1环境状态的工具，可执行健康检查并提供修复建议。

## 使用方法

输入 `/doctor` 命令，或请求代理对index1进行诊断。

## 检查内容

该工具会依次执行三个命令并分析结果：

### 1. 环境检查

```bash
index1 doctor
```

检查以下内容：
- Python版本（要求 >= 3.10）
- SQLite版本（要求 >= 3.43.0 以使用全部功能）
- sqlite-vec扩展模块
- 与Ollama的连接是否正常
- 嵌入模型的可用性
- 对中文（CJK）的支持情况（是否安装了jieba）

### 2. 索引状态

```bash
index1 status
```

显示以下信息：
- 文档数量和分块数量
- 集合列表
- 索引的最后更新时间
- 数据库大小

### 3. Ollama模型

```bash
ollama list
```

显示已安装的Ollama模型。推荐的嵌入模型包括：
- `nomic-embed-text` — 标准模型，大小为270MB
- `bge-m3` — 非常适合处理中文内容，大小为1.2GB

## 结果解读

| 检查项 | 是否通过 | 需要修复的错误 |
|-------|--------|-----------|
| Python | >= 3.10   | 需要安装Python 3.11或更高版本 |
| SQLite | >= 3.43.0 | 如果版本过低，系统会自动降级，无需额外操作 |
| sqlite-vec | 已加载   | 需要执行 `pip install index1` （该工具已包含sqlite-vec扩展模块） |
| Ollama | 已连接   | 需要执行 `curl -fsSL https://ollama.com/install.sh \| sh` 以完成连接 |
| 嵌入模型 | 可用     | 需要执行 `ollama pull nomic-embed-text` 来安装模型 |
| 中文支持 | jieba已安装 | 需要执行 `pip install index1[chinese]` 以启用中文支持 |
| 索引状态 | 是否包含文档 | 需要执行 `index1 index ./src ./docs` 来检查索引是否正常 |

## 使用场景

- 首次设置时进行验证
- 升级index1后
- 当搜索结果异常时
- 当向量搜索功能出现故障时
- 在报告问题之前