---
name: perplexity
description: 使用 Perplexity API 进行基于网络的 AI 搜索与研究。当用户需要最新信息、包含网络引用的多步骤推理、带有来源参考的详尽研究、涉及当前事件的事实性查询，或进行竞争分析时，均可使用该 API。当用户提及 Perplexity、需要最新信息或要求提供来源引用时，该 API 为默认选择。
---

# Perplexity AI 搜索

## 概述

该技能提供了对 Perplexity API 的访问权限，用于基于网络的 AI 搜索和研究。它结合了大型语言模型的强大功能和实时网络搜索能力，能够提供准确、最新的答案，并附带来源引用。

## 何时使用 Perplexity 与内置搜索

**在以下情况下使用 Perplexity：**
- 需要 **最新信息**（新闻、价格、事件、最新发展）
- 用户要求提供 **来源引用** 或参考资料
- 需要进行复杂的 **多步骤推理**
- 用户明确提到了 Perplexity 或希望获得研究风格的答案
- 需要对多个来源进行 **全面分析**

**在以下情况下使用内置网络搜索：**
- 简单的事实性查询
- 快速查找信息
- 用户不需要 AI 生成的合成内容
- 仅需要基本的 URL 或内容检索

## 模型选择指南

根据任务复杂性选择合适的模型：

### 🔍 搜索模型（快速查询）
适用于需要快速响应的简单事实性查询。

- `sonar` - 默认搜索模型，支持网络访问。适用于大多数查询。
- `sonar-pro` - 具有更深入理解能力的高级搜索模型。

### 🧠 推理模型（复杂分析）
适用于需要逻辑思维的复杂多步骤任务。

- `sonar-reasoning` - 结合网络搜索的复杂推理模型。
- `sonar-reasoning-pro` - 具有更深入内容理解能力的高级推理模型。

### 📚 研究模型（全面分析）
适用于需要对多个来源进行综合、深入研究的场景。

- `sonar-research` - 提供全面研究的模型。
- `sonar-research-pro` - 提供详尽分析及详细报告的高级研究模型。

## 快速入门

### 基本搜索

```bash
# Simple query (uses sonar by default)
scripts/perplexity_search.sh "What is the capital of Germany?"

# With custom model
scripts/perplexity_search.sh "Latest AI developments" -m sonar-pro

# Markdown format with citations
scripts/perplexity_search.sh "Tesla stock analysis" -f markdown
```

### 高级研究

```bash
# Deep research with comprehensive analysis
scripts/perplexity_search.sh "Market analysis for electric vehicles in 2025" \
  -m sonar-research-pro -c high -f markdown

# Pro search mode (multi-step reasoning)
scripts/perplexity_search.sh "Compare AI models performance benchmarks" \
  -m sonar-reasoning-pro -p pro -f markdown

# With custom system prompt
scripts/perplexity_search.sh "Analyze tech trends" \
  -s "You are a technology analyst. Focus on business implications and market trends."
```

## 搜索上下文大小

控制检索到的网络信息量：

- **低** - 检索速度更快，来源较少。适用于简单查询。
- **中等**（默认） - 平衡性较好，适用于大多数使用场景。
- **高** - 检索内容最全面，适用于研究和详细分析。

## 专业搜索模式

仅适用于 `sonar-pro` 和推理模型。可以控制多步骤搜索的流程：

- **快速**（默认） - 标准的单步搜索。
- **专业** - 自动化的多步骤推理，涉及多次网络搜索。
- **自动** - 根据查询复杂性自动选择搜索方式。

## 设置要求

### API 密钥配置

该技能需要通过环境变量设置 Perplexity API 密钥：

```bash
export PERPLEXITY_API_KEY="your-key-here"
```

**要永久设置该密钥（请添加到 ~/.bashrc 或 ~/.zshrc）：**
```bash
echo 'export PERPLEXITY_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**注意：** 不要将 API 密钥存储在 Clawdbot 配置文件中。该技能仅从环境变量中读取密钥，以避免配置冲突。

### 依赖项

该脚本使用 bash 和 curl。这两个工具通常已预安装在 Linux 系统上。

## 使用场景

### 新闻和时事
```bash
scripts/perplexity_search.sh "Latest news about AI regulation in Europe" -m sonar
```

### 竞争分析
```bash
scripts/perplexity_search.sh "Compare iPhone 15 vs Samsung Galaxy S24 features" \
  -m sonar-reasoning-pro -c high -f markdown
```

### 市场研究
```bash
scripts/perplexity_search.sh "Electric vehicle market forecast 2025-2030" \
  -m sonar-research-pro -c high -p pro -f markdown
```

### 需要最新数据的技术问题
```bash
scripts/perplexity_search.sh "Latest Python frameworks for web development 2025" \
  -m sonar-reasoning -c medium
```

## 输出格式

- **文本**（默认） - 带有引用 [1], [2] 等的纯文本格式。
- **markdown** - 带有来源链接的 Markdown 格式响应。
- **json** - 以 JSON 格式返回的原始 API 响应。

## 成本说明

Perplexity API 不是免费的。请注意使用成本：

- **简单查询**：每次查询约 0.005–0.015 美元
- **深度研究**：每次查询约 0.015–0.03 美元及以上
- **专业用户可通过 Perplexity Pro 订阅获得每月 5 美元的信用额度**

请谨慎使用推理/研究模型。对于大多数查询，建议使用默认的 `sonar` 模型。

## 可用模型列表

```bash
scripts/perplexity_search.sh --list-models
```

## 故障排除

**错误：未设置 PERPLEXITY_API_KEY 环境变量**
- 按照上述“设置要求”设置 API 密钥。

**错误：未找到 curl 命令**
- 安装 curl：`apt install curl` 或适用于您系统的相应命令。

**错误：API 响应异常**
- 确认您的 API 密钥有效且未被吊销
- 验证您的 Perplexity 账户是否具有 API 访问权限。

## 资源

### 脚本：
- **perplexity_search.sh** - 主要用于与 Perplexity API 交互的脚本
  - 支持所有 Perplexity 模型
  - 从环境或配置文件中获取 API 密钥
  - 提供多种输出格式
  - 使用 curl 进行 API 调用（无需 Python）

---

**注意：** 该技能依赖于外部 API 调用。请注意使用频率限制和费用问题。API 密钥切勿提交到版本控制系统中或公开共享。