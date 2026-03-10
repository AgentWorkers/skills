---
metadata.clawdbot:
  name: aura-openclaw
  description: Compile documents into knowledge bases and manage persistent AI agent memory with Aura Core
  version: 0.1.3
  author: Auralith Inc.
  homepage: https://github.com/Auralith-Inc/aura-openclaw
requires:
  env: []
files: ["scripts/*"]
---

# OpenClaw 的 Aura 技能

该技能为 OpenClaw 代理提供了持久化存储和即时知识检索功能。它可以将 60 多种文件格式编译成可查询的 `.aura` 文件，并为代理构建一个三层内存结构，该结构能够在会话结束、数据压缩或系统重启后仍然保持数据完整。

> **Memory OS v2.1**（`auralith-aura>=0.2.2`）：新增了时间衰减评分、噪声过滤、去重、布隆过滤器、SimHash 模糊匹配以及分层优先级评分等功能——且完全不占用系统 RAM 资源。

## 安装

```bash
pip install auralith-aura
```

如需完整的文档支持（PDF、DOCX 等格式），请安装：

```bash
pip install 'aura-core[all]
```

## 功能示例

### 学习整个代码库

```bash
You: 我想学习位于 ~/repos/api-service 的代码库。
Agent: 🔥 正在编译 ~/repos/api-service 的文件...
       ✅ 编译完成：api-service.aura
       索引内容：Python（312 个文件）、TypeScript（201 个文件）、YAML（44 个文件）、Markdown（73 个文件）、JSON（217 个文件）
```

### 了解身份验证中间件的工作原理

```bash
You: 身份验证中间件是如何处理令牌刷新的？
Agent: 根据 src/middleware/auth.ts（第 45-89 行）的实现，该中间件会检查 JWT 令牌的 `exp` 字段来判断令牌是否过期。如果令牌过期，它会调用 `refreshTokenService.rotate()` 函数生成新的访问令牌，并通过 `X-Refreshed-Token` 响应头将其发送给客户端。之后，原始请求会使用新的令牌重新发送。
```

### 对包含个人信息的文档进行编译并隐藏敏感数据

```bash
You: 我想学习位于 ~/legal 的所有文档，但需要隐藏其中的个人信息。
Agent: 🔥 已启用个人信息隐藏功能进行编译...
       ✅ 编译完成：legal.aura
       隐藏了 23 个电子邮件地址、8 个电话号码和 4 个社会安全号码（SSN）。
```

### 查看 Series A 协议中的终止条款

```bash
You: 请告诉我 Series A 协议中的终止条件是什么？
Agent: 根据 series_a_term_sheet.pdf 第 7.2 节，任何一方在以下情况下均可提前 30 天书面通知终止协议：
   (a) 重大违约行为在 15 个工作日内仍未得到解决；
   (b) 企业陷入破产或无力偿债；
   (c) 未能达到 Schedule B 中规定的最低收入标准。
```

### 在不同会话间保留信息

```bash
You: 请记住，我们的生产数据库位于 us-east-1 区域， staging API 密钥每 30 天更新一次，而且我希望错误日志详细一些。
Agent: ✅ 已记录如下：
   • 生产数据库区域：us-east-1
   • staging API 密钥更新周期：30 天
   • 错误日志设置为详细日志格式
```

### 跟踪项目中的决策过程

```bash
You: 我们决定使用 PostgreSQL 作为用户服务的数据存储系统，团队也一致同意使用 GraphQL 作为公共 API 的技术栈。
Agent: ✅ 已记录如下：
   • 数据库选择：用户服务使用 PostgreSQL（而非 MongoDB）
   • API 技术栈：公共 API 使用 GraphQL
```

## 命令说明

### 编译知识库

当用户要求你从指定目录中“学习”、“编译”、“索引”或“记住”文件时，可以使用以下命令：

```bash
python {SKILL_DIR}/scripts/compile.py <输入目录> <输出文件>
```

**选项说明：**
- `--pii-mask`：编译前隐藏个人信息。
- `--min-quality 0.3`：仅保留质量高于 0.3 的文件。

### 查询知识库

```bash
python {SKILL_DIR}/scripts/query.py knowledge.aura "搜索关键词"
```

### 管理代理内存

- **写入内存层级：**
  ```bash
  python {SKILL_DIR}/scripts/memory.py write pad "临时笔记"
  python {SKILL_DIR}/scripts/memory.py write fact "已验证的信息"
  python {SKILL_DIR}/scripts/memory.py write episodic "会话记录"
  ```
- **查询和清理内存：**
  ```bash
  python {SKILL_DIR}/scripts/memory.py query "搜索关键词"
  python {SKILL_DIR}/scripts/memory.py list
  python {SKILL_DIR}/scripts/memory.py usage
  python {SKILL_DIR}/scripts/memory.py prune --before 2026-01-01
  python {SKILL_DIR}/scripts/memory.py end-session
  ```

## 内存层级结构

| 层级 | 存储内容 | 生命周期 |
|------|---------------|-----------|
| `/pad` | 临时笔记、未完成的思考内容 | 会话间会被清除 |
| `/episodic` | 会话记录、决策内容、对话历史 | 自动归档，可供参考 |
| `/fact` | 已验证的事实、用户设置、学习到的规则 | 持久保存，永不丢失 |

## 支持的文件类型

- 文档格式：PDF、DOCX、DOC、RTF、ODT、EPUB、TXT、HTML、PPTX、EML
- 数据格式：CSV、TSV、XLSX、XLS、Parquet、JSON、JSONL、YAML、TOML
- 代码格式：Python、JavaScript、TypeScript、Rust、Go、C/C++ 等
- 标记语言：Markdown (.md)、reStructuredText、LaTeX

## 外部接口

- **无网络请求**：所有处理都在本地完成。

## 数据来源与安全性

- 每条内存记录都包含来源（代理/用户/系统）、命名空间、时间戳和唯一标识符 (`entry_id`)。所有数据都是直接写入的，没有经过任何推断或合成。
- `.aura` 格式使用了 `safetensors` 技术（避免代码执行风险）。
- 内存文件存储在 `~/.aura/memory/` 目录下。
- 无需使用环境变量或 API 密钥。
- 无数据传输或分析功能。

## 安全与隐私注意事项

- **所有数据均存储在本地**，不会被发送到外部服务。
- 编译和内存操作均在本地执行。
- `.aura` 文件使用 `safetensors` 技术进行存储（无潜在的安全风险）。
- 内存文件由 `Memory OS` 管理。

## 其他功能

- 可通过 `memory.show_usage()` 查看各层级的存储内容。
- 可使用 `memory.prune_shards` 删除过期的数据。
- 可通过 `memory.prune_shards` 删除特定数据片段。
- 可通过 `end-session` 命令结束当前会话。

## 注意事项

- 该技能由代理在正常运行过程中自动调用。你可以根据需要关闭自动调用功能。

**信任声明：**
使用此技能时，**不会有任何数据被发送到外部服务**。所有处理都在你的本地机器上进行。仅在你信任 [Auralith Inc.](https://auralith.org) 时才建议安装此技能。编译器和相关组件的源代码可在 [GitHub](https://github.com/Auralith-Inc/aura-core) 获取。

## 其他信息

- `Memory OS` 支持即时写入和后台数据持久化。
- 编译器和相关组件均为开源项目（Apache 2.0 许可证）。
- 如需更高级的权重计算和训练功能，可参考 [OMNI Platform](https://omni.auralith.org)。