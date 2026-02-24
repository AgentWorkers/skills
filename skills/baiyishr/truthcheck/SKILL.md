---
name: truthcheck
description: "使用 TruthCheck CLI 来验证声明、核实内容、检查 URL 的可信度，并追踪声明的来源。适用场景包括：  
(1) 用户要求对某个声明进行事实核查；  
(2) 用户希望确认某个 URL 或信息来源是否可靠；  
(3) 用户想要了解某个声明的起源；  
(4) 用户对错误信息或内容真实性有疑问。  
安装方法：`pip install truthcheck`"
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["truthcheck"] } } }
---
# TruthCheck 技能

这是一个用于验证 AI 内容的命令行工具（CLI），可以核实声明、检查 URL 以及追踪错误信息。

## 命令

### 验证声明
```bash
truthcheck verify "claim text" --llm gemini
```
- 返回 0-100 分的 TruthScore，其中包含详细信息（发布者、内容、佐证信息、事实核查结果）
- `--llm` 选项可选，但可提高准确性
- 使用 `--json` 可获得结构化输出

### 检查 URL 的可信度
```bash
truthcheck check https://example.com
truthcheck check "text with multiple URLs"
truthcheck check -f file.txt
```
- 识别不存在的虚假 URL
- 评估发布者的可信度

### 追踪声明的来源
```bash
truthcheck trace "claim text"           # balanced, ~1-2 min
truthcheck trace "claim text" --quick   # fast, ~30 sec
truthcheck trace "claim text" --deep    # thorough, ~3-5 min
```
- 查找原始来源并构建传播路径（即声明的传播链）

### 查找发布者信息
```bash
truthcheck lookup "publisher name"
```

### 同步发布者数据库
```bash
truthcheck sync
```
定期运行以保持发布者评分的准确性

## 解释 TruthScore

| 分数 | 标签 | 含义 |
|-------|-------|---------|
| 80-100 | 真实 | 有强有力的证据支持该声明 |
| 60-79 | 可能真实 | 有一定证据支持，但结论不明确 |
| 40-59 | 不确定 | 证据相互矛盾或不足 |
| 20-39 | 可能虚假 | 证据倾向于否定该声明 |
| 0-19 | 虚假 | 有强有力的证据与该声明相矛盾 |

## LLM 集成（可选）

TruthCheck 也可以独立使用，但添加 `--llm` 可以提高内容分析的准确性。

```bash
truthcheck verify "some claim" --llm gemini    # recommended, fast & free tier
truthcheck verify "some claim" --llm openai    # GPT models
truthcheck verify "some claim" --llm anthropic # Claude models
truthcheck verify "some claim" --llm ollama    # local models, fully offline
```

**隐私政策：** API 密钥仅存储在您的本地环境中。TruthCheck 从不将您的密钥发送到任何外部服务——它们仅用于直接调用相应的 LLM 提供商的 API。

## 环境变量

| 变量 | 使用场景 | 说明 |
|----------|-------------|-------------|
| `GEMINI_API_KEY` | `--llm gemini` | Google AI API 密钥（免费 tier 可用） |
| `OPENAI_API_KEY` | `--llm openai` | OpenAI API 密钥 |
| `ANTHROPIC_API_KEY` | `--llm anthropic` | Anthropic API 密钥 |
| `BRAVE_API_KEY` | `--search brave` | Brave Search API 密钥 |

对于 `--llm ollama`（在本地运行）或默认的 DuckDuckGo 搜索，不需要这些密钥。

## 提示：
- 根据搜索结果的不同，验证命令可能需要 15-60 秒的时间
- 不使用 `--llm` 时：仅基于发布者声誉、佐证信息和事实核查进行基本评分
- 使用 `--llm` 时：会加入 AI 内容分析以提高准确性
- `--search brave` 提供的搜索结果优于默认的 DuckDuckGo
- 对于批量验证，需要逐个处理每个声明