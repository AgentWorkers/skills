---
name: evm-audit-cli
description: 使用 OpenRouter 进行基于 AI 的智能合约审计：这是一个轻量级的替代方案，无需 Docker。
env:
  required:
    - OPENROUTER_API_KEY
---
# EVM Audit CLI

这是一个基于人工智能的智能合约安全审计工具，体积轻量级，无需使用 Docker。

## 功能概述

1. **读取本地的 Solidity 文件**：无需从区块浏览器获取合约代码。
2. **通过 OpenRouter 调用 AI 模型**：使用 GPT-4o-mini（或其他模型）进行智能合约分析。
3. **解析审计报告**：以 JSON 格式输出审计结果。

## 不支持的功能

- ❌ 无法从 Etherscan 获取合约代码（仅支持本地文件）。
- ❌ 不需要 Docker 环境。
- ❌ 不支持静态代码分析（请使用 `slither-audit` 工具进行静态分析）。

## 系统要求

```bash
# Get free API key from https://openrouter.ai
export OPENROUTER_API_KEY=your_key
```

## 使用方法

```bash
python3 evm-audit-cli.py /path/to/contracts/

# With specific model
python3 evm-audit-cli.py ./contracts/ --model openai/gpt-4o

# JSON output
python3 evm-audit-cli.py ./contracts/ --format json
```

## 示例输出

```
# Audit Report: Vulnerable.sol
**Model:** openai/gpt-4o-mini

- **Reentrancy Attack** (critical)
  The withdraw function can be exploited via a reentrancy attack.

**Note:** AI analysis - verify findings manually
```

## 支持的 AI 模型

默认模型：`openai/gpt-4o-mini`（速度快，成本低）

其他可选模型：
- `openai/gpt-4o`（功能更强大）
- `anthropic/claude-3.5-sonnet`（如果可用）
- `google/gemini-2.0-flash-exp`（速度快）

## 使用限制

- 仅支持本地 Solidity 文件。
- AI 分析可能存在遗漏的问题，建议手动进行验证。
- 对于专业审计，建议结合手动审查和 `slither-audit` 工具使用。

## 相关工具

- `slither-audit`：基于 Slither 的静态代码分析工具，不依赖 AI，无需 API 密钥。
- `evmbench`：基于 Docker 的全面智能合约审计工具。