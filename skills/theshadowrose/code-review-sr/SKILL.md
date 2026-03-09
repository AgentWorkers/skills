---
slug: "code-review-sr"
name: "CodeReview Automated Code Review Assistant"
description: "这款基于人工智能的代码审查工具结合了快速的本地静态分析与深度的AI推理能力，能够检测出代码中的错误、安全漏洞、性能问题以及代码风格问题。它支持Anthropic、OpenAI和Ollama等大型语言模型；在离线状态下，该工具会切换为使用本地的正则表达式进行分析。"
author: "@TheShadowRose"
version: "1.0.4"
tags: ["code-review", "ai", "static-analysis", "security"]
license: "MIT"
env:
  ANTHROPIC_API_KEY: "Optional - for Anthropic/Claude models (or set CLAUDE_API_KEY)"
  OPENAI_API_KEY: "Optional - for OpenAI/GPT models"
  OLLAMA_HOST: "Optional - Ollama base URL, default http://localhost:11434"
  OLLAMA_PORT: "Optional - Ollama port, default 11434"
---
# 代码审查 — 由 AI 驱动的代码审查助手

该工具结合了 **快速的本地正则表达式匹配** 和 **深度的 AI 分析**，提供全面且具有操作性的代码审查服务。首先会进行一次本地的静态分析，然后将代码及初步分析结果发送给 AI 模型进行进一步审查，包括错误检测、安全分析、性能建议和代码风格反馈。

---

## 工作原理

1. **本地预检查**：基于正则表达式的匹配会立即执行，能够检测到硬编码的敏感信息、`eval` 语句的使用、SQL 注入漏洞、空的异常处理块、过长的函数等问题。
2. **AI 深度审查**：将完整的源代码和本地分析结果发送到您选择的 AI 模型（Anthropic、OpenAI 或 Ollama），以进行深入的错误分析、逻辑错误检查、性能评估和架构审查。
3. **优雅的回退机制**：即使未设置 API 密钥或 AI 调用失败，您仍能获得本地的静态分析结果。这不会影响您的工作流程。

## 使用方法

```javascript
const { CodeReview } = require('./src/code-review');

// AI-powered review (default: anthropic/claude-haiku-4-5)
const reviewer = new CodeReview({ model: 'anthropic/claude-haiku-4-5' });
const result = await reviewer.review('./src/auth.js');

console.log(result.score);        // 1-10
console.log(result.issues);       // Array of issues with severity, line, type, message
console.log(result.suggestions);  // Actionable improvement suggestions
console.log(result.summary);      // Concise quality summary
console.log(result.aiPowered);    // true

// Review an entire directory
const dirResult = await reviewer.reviewDir('./src', {
  include: ['*.js', '*.ts'],
  exclude: ['node_modules', '.git', 'dist'],
  concurrency: 3
});
console.log(dirResult.averageScore);
console.log(dirResult.totalIssues);
```

### 可用的 AI 模型

| 提供商 | 示例 | API 密钥环境变量 |
|----------|---------|-----------------|
| **Anthropic** | `anthropic/claude-haiku-4-5` | `ANTHROPIC_API_KEY` |
| **OpenAI** | `openai/gpt-4o-mini` | `OPENAI_API_KEY` |
| **Ollama**（本地） | `ollama/llama3` | 无需设置 API 密钥 |

```javascript
// OpenAI
const reviewer = new CodeReview({ model: 'openai/gpt-4o-mini' });

// Local Ollama
const reviewer = new CodeReview({ model: 'ollama/codellama' });

// Local-only (no AI, regex patterns only)
const reviewer = new CodeReview();
const result = await reviewer.review('./src/app.js');
// result.aiPowered === false
```

## 可检测的问题类型

| 类别 | 例子 |
|----------|---------|
| **错误** | 空引用、逻辑错误、竞态条件、空的异常处理块 |
| **安全问题** | SQL 注入、XSS 攻击、硬编码的敏感信息、`eval` 语句的使用 |
| **性能问题** | 重复查询、不必要的循环、内存泄漏 |
| **代码风格** | 命名不一致、过长的函数、在生产环境中使用 `console.log` |
| **逻辑问题** | 无法执行的代码、冗余的条件判断 |
| **可维护性** | 嵌套过深的回调函数、使用魔术数字、待处理的标记（TODO/FIXME） |

## 输出格式

```json
{
  "file": "./src/auth.js",
  "score": 5,
  "issues": [
    {
      "severity": "high",
      "line": 42,
      "type": "security",
      "message": "User input passed directly to SQL query without parameterization"
    },
    {
      "severity": "medium",
      "line": 87,
      "type": "bugs",
      "message": "Empty catch block silently swallows database connection errors"
    }
  ],
  "suggestions": [
    "Use parameterized queries or an ORM to prevent SQL injection on line 42",
    "Add error logging in the catch block on line 87",
    "Extract the authentication logic into a separate middleware module"
  ],
  "summary": "The auth module has a critical SQL injection vulnerability and several error handling gaps. Core logic is sound but needs security hardening.",
  "totalIssues": 2,
  "lines": 142,
  "aiPowered": true,
  "model": "anthropic/claude-haiku-4-5"
}
```

## 语言支持

该工具支持您的 AI 模型能够理解的所有编程语言。本地预检查部分能检测多种语言中的常见问题。已测试的语言包括：JavaScript、TypeScript、Python、Go、Rust、Java、C#、Ruby、PHP、Swift、Kotlin。

## 技术细节

- **无 npm 依赖**：完全基于 Node.js 开发，仅使用内置的 `https`、`http`、`fs` 和 `path` 模块。
- **文件截断**：在发送给 AI 之前，文件内容会被截断至 8,000 个字符以内，以符合 API 的字符限制。
- **并发控制**：可以配置文件处理的并行批次数量（默认为 3）。
- **优雅的故障处理**：即使 AI 服务失败，也能保证本地分析结果的可用性。

---

## ⚠️ 免责声明

本软件按“原样”提供，不附带任何明示或暗示的保证。

**请自行承担使用风险。**

- 作者对因使用或误用本软件而导致的任何损害、损失或后果（包括但不限于财务损失、数据丢失、安全漏洞、业务中断或间接/连带损害）概不负责。
- 本软件不构成财务、法律、交易或专业建议。用户需自行评估该软件是否适用于其具体用途、环境及风险承受能力。
- 对于软件的准确性、可靠性、完整性或适用性，作者不作任何保证。
- 作者不对第三方购买后如何使用、修改或分发本软件负责。

通过下载、安装或使用本软件，即表示您已阅读并同意完全自行承担使用风险。

**数据隐私声明：** 在配置 AI 模型时，本软件会将您的源代码及静态分析结果发送到指定的提供商（Anthropic、OpenAI 或本地 Ollama 实例）。请确保不要在包含敏感信息的代码上运行该工具，除非您清楚数据传输的去向。如果没有 API 密钥，所有分析都将仅限于本地进行。
作者对因软件漏洞、系统故障或用户错误导致的数据丢失、损坏或未经授权的访问不承担任何责任。请始终为重要数据备份。

## 支持与联系方式

| | |
|---|---|
| 🐛 **问题报告** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*本软件基于 [OpenClaw](https://github.com/openclaw/openclaw) 开发——感谢您的支持！*

---

🛠️ **需要定制功能？** 我们提供定制的 OpenClaw 代理和技能服务，价格从 500 美元起。只要您能描述需求，我就能为您实现。→ [在 Fiverr 上联系我](https://www.fiverr.com/s/jjmlZ0v)