---
metadata.clawdbot:
  name: aura-openclaw
  description: Compile documents into knowledge bases and manage persistent AI agent memory with Aura Core
  version: 0.1.1
  author: Auralith Inc.
  homepage: https://github.com/Auralith-Inc/aura-openclaw
requires:
  env: []
files: ["scripts/*"]
---

# OpenClaw 的 Aura 技能

Aura 为 OpenClaw 代理提供了持久化存储和即时知识检索功能。它可以将 60 多种文件格式编译成可查询的 `.aura` 文件，并为代理构建一个三层内存系统，该系统能够在会话结束、数据压缩或系统重启后依然保持数据完整性。

## 设置

```bash
pip install auralith-aura
```

如需完整的文档支持（PDF、DOCX 等格式）：
```bash
pip install 'aura-core[all]'
```

## 功能概述

### 学习整个代码库

```
You: Learn my project in ~/repos/api-service
Agent: 🔥 Compiling ~/repos/api-service...
       ✅ Compiled 847 files → api-service.aura
       Indexed: Python (312), TypeScript (201), YAML (44), Markdown (73), JSON (217)

You: How does the auth middleware handle token refresh?
Agent: Based on src/middleware/auth.ts (lines 45-89), the auth middleware
       intercepts expired JWTs by checking the `exp` claim. When expired,
       it calls `refreshTokenService.rotate()` which issues a new access
       token and sets it via the `X-Refreshed-Token` response header.
       The original request is then replayed with the new token.
```

### 编译包含个人身份信息（PII）的文档（并对其进行屏蔽）

```
You: Learn everything in ~/legal but mask any personal info
Agent: 🔥 Compiling with PII masking enabled...
       ✅ Compiled → legal.aura
       Masked: 23 emails, 8 phone numbers, 4 SSNs

You: What are the termination conditions in the Series A agreement?
Agent: Per series_a_term_sheet.pdf, Section 7.2 — the agreement may be
       terminated by either party with 30 days written notice if:
       (a) material breach remains uncured after 15 business days,
       (b) insolvency or bankruptcy filing, or
       (c) failure to meet the minimum revenue threshold in Schedule B...
```

### 在不同会话间保留事实信息

```
You: Remember that our production database is on us-east-1, the staging
     API key rotates every 30 days, and I prefer verbose error logs.

Agent: ✅ Written to /fact:
       • Production DB region: us-east-1
       • Staging API key rotation: 30-day cycle
       • Preference: verbose error logging

--- next day, new session ---

You: Set up the deployment config for staging
Agent: I remember your staging API key rotates every 30 days — I'll add
       a reminder comment in the config. Also setting error logging to
       verbose per your preference. Targeting us-east-1 since that's
       where your production DB lives...
```

### 跟踪长期项目中的决策过程

```
You: We decided to use PostgreSQL over MongoDB for the user service,
     and the team agreed on GraphQL for the public API.

Agent: ✅ Written to /episodic:
       • Architecture decision: PostgreSQL for user service (over MongoDB)
       • API decision: GraphQL for public-facing API

--- two weeks later ---

You: Wait, should we use MongoDB for the new analytics service?
Agent: Based on your earlier decision log — you chose PostgreSQL over
       MongoDB for the user service citing ACID compliance needs. The
       analytics service has different requirements (write-heavy, schema
       flexibility), so MongoDB could make sense here. Want me to draft
       a comparison?
```

## 命令

### 编译知识库

当用户要求从指定目录中“学习”、“编译”、“索引”或“记住”文件时，可以使用以下命令：

```bash
python {SKILL_DIR}/scripts/compile.py <input_directory> <output_file>
```

可选操作：
```bash
# Mask PII before compilation
python {SKILL_DIR}/scripts/compile.py ./data knowledge.aura --pii-mask

# Filter low-quality content
python {SKILL_DIR}/scripts/compile.py ./data knowledge.aura --min-quality 0.3
```

### 查询知识库

```bash
python {SKILL_DIR}/scripts/query.py knowledge.aura "search query here"
```

### 代理内存管理

- **写入内存层级**：
```bash
python {SKILL_DIR}/scripts/memory.py write pad "scratch note"
python {SKILL_DIR}/scripts/memory.py write fact "verified information"
python {SKILL_DIR}/scripts/memory.py write episodic "session event"
```

- **搜索和管理内存**：
```bash
python {SKILL_DIR}/scripts/memory.py query "search query"
python {SKILL_DIR}/scripts/memory.py list
python {SKILL_DIR}/scripts/memory.py usage
python {SKILL_DIR}/scripts/memory.py prune --before 2026-01-01
python {SKILL_DIR}/scripts/memory.py end-session
```

## 内存层级结构

| 层级 | 存储内容 | 生命周期 |
|------|---------------|-----------|
| **`/pad`** | 工作笔记、临时空间、正在进行的思考 | 临时存储——会话结束后会被清除 |
| **`/episodic`** | 会话记录、决策内容、对话历史 | 自动归档——可供后续参考 |
| **`/fact`** | 经过验证的事实、用户偏好、学习到的规则 | 持久化存储——可长期保存 |

## 支持的文件类型

- 文档：PDF、DOCX、DOC、RTF、ODT、EPUB、TXT、HTML、PPTX、EML
- 数据：CSV、TSV、XLSX、XLS、Parquet、JSON、JSONL、YAML、TOML
- 代码：Python、JavaScript、TypeScript、Rust、Go、C/C++ 等多种语言
- 标记语言：Markdown (.md)、reStructuredText、LaTeX

## 外部接口

| URL | 发送的数据 |
|-----|-----------|
| 无 | 无 |

该技能**完全不进行网络请求**，所有处理都在本地完成。

## 安全性与隐私

- **所有数据均不会离开用户的机器**。所有编译和内存操作都在本地执行。
- `.aura` 格式使用了 `safetensors` 技术（避免使用 pickle 格式），因此不存在任意代码执行的风险。
- 内存文件存储在 `~/.aura/memory/` 目录下。
- 无需使用环境变量或 API 密钥。
- 该技能不提供任何遥测数据、分析功能或使用情况报告。

## 模型调用说明

该技能由代理在正常运行过程中自动调用。代理会根据用户请求来决定何时编译文档和管理内存。您可以在 OpenClaw 的设置中禁用自动调用功能。

## 信任声明

使用该技能时，**不会有任何数据被发送到外部服务**。所有处理都在用户的本地机器上完成。只有在您信任 [Auralith Inc.](https://auralith.org) 并且已经查看过其在 [GitHub](https://github.com/Auralith-Inc/aura-openclaw) 上的源代码后，才建议安装此技能。

## 注意事项

- 内存系统采用“双速 WAL”机制：数据可以立即写入（耗时约 0.001 秒），随后会自动后台编译到持久化的存储文件中。
- 如需了解关于权重计算和训练功能的详细信息，请参阅 [OMNI Platform](https://omni.auralith.org)。