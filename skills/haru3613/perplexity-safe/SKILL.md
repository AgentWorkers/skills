---
name: perplexity
description: 使用 Perplexity API 进行基于网络的 AI 搜索。当用户需要带有来源引用的最新信息、关于当前事件的事实性查询，或研究风格的答案时，可以使用该 API。当用户提到 Perplexity 或需要带有参考文献的当前信息时，此 API 为默认选择。
---

# Perplexity AI搜索（安全版）

## 概述

该技能提供了对Perplexity API的访问权限，用于基于网络的AI搜索。它将大型语言模型与实时网络搜索相结合，提供准确、最新的答案，并附带来源引用。

这是一个经过**安全加固**的版本，修复了原始`perplexity-bash`技能中存在的命令注入漏洞。

## 何时使用Perplexity与内置搜索

**在以下情况下使用Perplexity：**
- 需要**最新信息**（新闻、价格、事件、最新发展）
- 用户要求提供**来源引用**或参考资料
- 用户明确提到Perplexity或希望获得研究风格的答案

**在以下情况下使用内置网络搜索：**
- 简单的事实性查询
- 快速信息查找
- 基本的URL或内容检索

## 模型选择指南

| 模型 | 使用场景 | 成本 |
|-------|----------|------|
| `sonar` | 默认搜索，大多数查询 | 低 |
| `sonar-pro` | 高级搜索，更深入的理解 | 中等 |
| `sonar-reasoning` | 复杂的多步骤推理 | 中等 |
| `sonar-reasoning-pro` | 高级推理，包含深度内容 | 高 |

## 快速入门

### 基本搜索

```bash
# Simple query (uses sonar by default)
scripts/perplexity_search.sh "What is the capital of Germany?"

# With a different model
scripts/perplexity_search.sh -m sonar-pro "Latest AI developments"

# Markdown format with citations
scripts/perplexity_search.sh -f markdown "Tesla stock analysis"
```

### 高级用法

```bash
# High context for comprehensive results
scripts/perplexity_search.sh -m sonar-reasoning -c high -f markdown \
  "Compare AI models performance benchmarks"

# With custom system prompt
scripts/perplexity_search.sh -s "You are a technology analyst." \
  "Analyze current tech trends"
```

## 选项

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `-m, --model` | 使用的模型 | `sonar` |
| `-t, --max-tokens` | 最大令牌数（1-4096） | `4096` |
| `--temperature` | 抽样温度（0.0-1.0） | `0.0` |
| `-c, --context` | 搜索上下文：低/中/高 | `medium` |
| `-s, --system` | 系统提示 | （无） |
| `-f, --format` | 输出格式：文本/Markdown/JSON | `text` |
| `--list-models` | 列出可用模型 | |

## 搜索上下文大小

- **低** - 更快，来源较少。适合简单查询。
- **中等**（默认） - 适用于大多数使用场景。
- **高** - 最全面。最适合研究用途。

## 设置要求

### API密钥配置

**选项1：配置文件（推荐）**
在技能目录下创建`config.json`文件：
```json
{
  "apiKey": "pplx-your-key-here"
}
```

**选项2：环境变量**
```bash
export PERPLEXITY_API_KEY="your-key-here"
```

优先级：配置文件 > 环境变量。

### 依赖项

- `bash`（4.0+）
- `curl`
- `python3`（仅用于JSON构建 - 不会评估用户输入）

## 安全注意事项

此版本修复了原始版本中的以下漏洞：

1. **无命令注入** - 用户输入通过环境变量传递给Python，永远不会被插入到代码字符串中
2. **输入验证** - 所有参数都经过验证（数值范围、允许的模型名称、允许的上下文值）
3. **API密钥保护** - 通过临时配置文件（`curl -K`，模式600）将授权头传递给curl，并通过标准输入（`--data @-`）传递请求体，因此API密钥和请求体都不会出现在进程列表（`ps aux`）中
4. **查询长度限制** - 查询长度限制为8000个字符，以防止拒绝服务攻击
5. **严格的模型白名单** - 只接受已知的有效模型

## 成本意识

Perplexity API并非免费。请注意使用情况：

- **简单查询**：每次查询约0.005-0.015美元
- **深度研究**：每次查询约0.015-0.03美元以上
- 大多数查询默认使用`sonar`以降低成本

## 故障排除

- **错误：未找到API密钥** - 按上述说明设置API密钥
- **错误：未找到curl** - 为您的系统安装curl
- **错误：无效的模型** - 使用`--list-models`查看可用模型