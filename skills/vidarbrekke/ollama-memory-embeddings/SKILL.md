---
slug: ollama-memory-embeddings
version: "1.0.4"
display_name: Ollama Memory Embeddings
displayName: Ollama Memory Embeddings
name: ollama-memory-embeddings
description: >
  Configure OpenClaw memory search to use Ollama as the embeddings server
  (OpenAI-compatible /v1/embeddings) instead of the built-in node-llama-cpp
  local GGUF loading. Includes interactive model selection and optional import
  of an existing local embedding GGUF into Ollama.
---

# Ollama内存嵌入（Ollama Memory Embeddings）

此技能配置了OpenClaw的内存搜索功能，使其通过OpenAI兼容的`/v1/embeddings`端点使用Ollama作为嵌入服务器。

> **仅影响嵌入（Embeddings）**：此技能不会影响聊天或补全功能的路由逻辑，仅会改变内存搜索时生成的嵌入向量的方式。

## 功能介绍

- 该技能会被安装到`~/.openclaw/skills/ollama-memory-embeddings`目录下。
- 确认Ollama已安装且可访问。
- 允许用户选择所需的嵌入模型：
  - `embeddinggemma`（默认值，最接近OpenClaw内置模型）
  - `nomic-embed-text`（质量高，效率较高）
  - `all-minilm`（体积小，速度最快）
  - `mxbai-embed-large`（质量最高，但文件较大）
- 可以通过`ollama create`命令将现有的本地嵌入文件（格式为GGUF）导入到Ollama中（系统会自动检测`embeddinggemma`、`nomic-embed`、`all-minilm`和`mxbai-embed`类型的GGUF文件）。
- 系统会自动处理模型名称的标准化（包括`:latest`标签）。
- 更新OpenClaw配置文件`agents.defaults.memorySearch`中的相关设置：
  - `provider = "openai"`
  - `model = <选定的模型>:latest`
  - `remotebaseUrl = "http://127.0.0.1:11434/v1/"`
  - `remote.apiKey = "ollama"`（客户端需要提供此密钥，但Ollama本身会忽略该值）
- 安装完成后会进行配置文件的校验（读取并验证JSON格式是否正确）。
- 可选地重启OpenClaw代理（支持`openclaw gateway restart`、`systemd`、`launchd`等重启方式）。
- 安装过程中可以选择是否重新构建内存索引（`openclaw memory index --force --verbose`）。
- 包含两步验证流程：
  1. 检查选定的模型是否存在于Ollama的模型列表中。
  2. 调用Ollama的嵌入端点并验证返回的响应是否有效。
- 提供一个用于强制应用配置更改的脚本`enforce.sh`。
- 还提供了一个可选的配置漂移自动修复工具`watchdog.sh`。

## 安装方法

```bash
bash ~/.openclaw/skills/ollama-memory-embeddings/install.sh
```

请从[此仓库](...)下载并执行安装命令。

## 非交互式使用方法

```bash
bash ~/.openclaw/skills/ollama-memory-embeddings/install.sh \
  --non-interactive \
  --model embeddinggemma \
  --reindex-memory auto
```

### 安装自动修复机制（包括 watchdog）

```bash
bash ~/.openclaw/skills/ollama-memory-embeddings/install.sh \
  --non-interactive \
  --model embeddinggemma \
  --reindex-memory auto \
  --install-watchdog \
  --watchdog-interval 60
```

> **注意：**在非交互式模式下，`--import-local-gguf auto`选项会被视为`no`（即不自动导入本地GGUF文件）。如需自动导入，请使用`--import-local-gguf yes`。

**可选参数：**
- `--model <id>`：`embeddinggemma`、`nomic-embed-text`、`all-minilm`、`mxbai-embed-large`之一
- `--import-local-gguf <auto|yes|no>`：默认值为`no`（建议使用`yes`）
- `--import-model-name <name>`：默认模型名称为`embeddinggemma-local`
- `--restart-gateway <yes|no>`：默认值为`no`（仅在明确请求时重启代理）
- `--skip-restart`：`--restart-gateway no`的别名
- `--openclaw-config <path>`：配置文件路径的覆盖选项
- `--install-watchdog`：在macOS系统上安装用于自动修复配置变化的watchdog工具
- `--watchdog-interval <sec>`：watchdog的检查间隔（默认为60秒）
- `--reindex-memory <auto|yes|no>`：内存重建模式（默认为`auto`）
- `--dry-run`：仅输出计划中的更改和命令，不实际执行任何操作

## 验证安装结果

```bash
~/.openclaw/skills/ollama-memory-embeddings/verify.sh
```

如果安装失败，可以使用`--verbose`选项输出详细的API响应内容。

## 强制应用配置更改与自动修复

**强制应用配置更改：**
```bash
~/.openclaw/skills/ollama-memory-embeddings/enforce.sh \
  --model embeddinggemma \
  --openclaw-config ~/.openclaw/openclaw.json
```

**仅检查配置漂移情况：**
```bash
~/.openclaw/skills/ollama-memory-embeddings/enforce.sh \
  --check-only \
  --model embeddinggemma
```

**一次性运行watchdog工具（检查并修复配置漂移）：**
```bash
~/.openclaw/skills/ollama-memory-embeddings/watchdog.sh \
  --once \
  --model embeddinggemma
```

**在macOS系统上通过launchd安装watchdog：**
```bash
~/.openclaw/skills/ollama-memory-embeddings/watchdog.sh \
  --install-launchd \
  --model embeddinggemma \
  --interval-sec 60
```

## GGUF文件的检测范围

安装程序会在以下已知缓存目录中查找匹配的嵌入文件（格式为GGUF）：
- `~/.node-llama-cpp/models`
- `~/.cache/node-llama-cpp/models`
- `~/.cache/openclaw/models`

- 文件名格式为`*embeddinggemma*.gguf`、`*nomic-embed*.gguf`、`*all-minilm*.gguf`、`*mxbai-embed*.gguf`

其他类型的嵌入文件不会被自动检测到，需要手动导入。

## 其他注意事项：

- 该技能不会修改OpenClaw的核心代码，仅更新用户配置文件。
- 在进行配置更改之前会先创建配置文件的备份。
- 如果本地没有相应的GGUF文件，系统会从Ollama服务器下载所需的模型。
- 为了确保与Ollama的兼容性，模型名称会自动加上`:latest`标签。
- 如果嵌入模型发生变化，系统会重新生成内存向量以避免数据检索时的不匹配问题。
- 当配置参数（`provider`、`model`、`baseUrl`、`apiKey`）发生变化时，系统才会自动重新构建内存索引。
- 强制应用配置更改时需要提供有效的API密钥（`apiKey`），但不要求密钥值必须为`"ollama"`。
- 只有在需要写入配置文件时才会创建备份。
- 系统支持旧版本的配置格式：如果`agentsdefaults.memorySearch`配置不存在，系统会使用旧的配置路径进行数据写入，以保持兼容性。