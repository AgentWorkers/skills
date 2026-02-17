---
name: q-kdb-code-review
description: 基于人工智能的代码审查工具，专为 Q/kdb+ 设计——帮助您在金融领域使用这种简洁高效的编程语言时及时发现并修复错误。
version: 1.0.0
homepage: https://github.com/beee003/astrai-openclaw
metadata:
  clawdbot:
    emoji: "⚡"
    requires:
      env: ["ASTRAI_API_KEY"]
    primaryEnv: "ASTRAI_API_KEY"
    files: ["plugin.py", "config.example.toml"]
tags: [q, kdb, kdb-plus, quant, finance, code-review, hft, trading, timeseries]
---
# q-kdb-code-review  
一款基于人工智能的Q/kdb+代码审查工具——能够检测量化金融领域中最简洁的Q语言代码中的错误、性能问题及安全漏洞。  

## 功能介绍  
该工具深入理解Q语言的惯用法、性能优化模式及常见陷阱，专为量化开发人员、kdb+数据库管理员及交易基础设施团队设计。  

**能够检测的问题包括：**  
- 隐式类型转换中的错误（例如：在比较操作中混合使用long和float类型）  
- 函数调用中参数数量错误导致的错误  
- 在受保护的评估操作中未正确处理信号（signals）  
- 内存使用效率低下的查询（例如：当只需要部分列时却选择了所有列）  
- 在可并行执行的操作中未充分利用并行处理能力  
- 在用户提供的字符串上不安全地使用`eval`/`value`函数（可能导致代码注入攻击）  
- 在并发插入操作中未正确锁定表  
- 在高基数连接列上未使用`g#`分组属性  
- 应该使用`aj`（asof连接）或`wj`（window连接）的查询却使用了N平方连接操作  
- 在定时器回调（.z.ts）中存在的竞态条件  
- 未受保护的IPC（Inter-Process Communication）处理程序（.z.pg、.z.ps）以及暴露的.z.pw文件  

**严格性模式：**  
| 模式 | 检查内容 |  
|------|---------------|  
| `standard` | 错误、代码正确性、类型错误、连接语义、空值处理 |  
| `strict` | 标准模式下的所有检查内容 + 性能问题（属性检查、并行处理优化、代码风格） |  
| `security` | 标准模式下的所有检查内容 + 通过字符串执行代码注入的风险、未受保护的IPC处理程序、暴露的.z.pw文件风险 |

**智能路由机制：**  
Astrai通过复杂的算法将复杂的Q语言代码（包括自定义信号生成和实时条件执行（CEP）路由到最合适的AI模型；简单的表操作（如选择、插入、模式定义）则路由到成本更低、响应更快的模型。从而实现最低成本下的最佳审查效果。  

**BYOK（自带API密钥）：**  
您可以使用自己的API密钥进行代码审查，费用由您选择的AI服务提供商承担。Astrai会根据您的配置自动选择最合适的模型进行处理。  

## 设置流程：  
1. 在 [as-trai.com](https://as-trai.com) 获取免费的API密钥。  
2. 设置您的API密钥：  
   ```bash
   export ASTRAI_API_KEY="your_key_here"
   ```  
3. （可选）添加用于BYOK功能的提供商密钥：  
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   export OPENAI_API_KEY="sk-..."
   ```  
4. 在任意`.q`文件上运行`/review-q`命令即可开始代码审查。  

## 使用方法：  
```
/review-q                          Review current Q file
/review-q --strict                 Strict mode: bugs + performance + style
/review-q --focus security         Security mode: eval injection, IPC, .z.pw
/review-q --file tick.q            Review a specific file
```  

### 示例输出：  
```
Reviewing tick.q (strict mode)...
Model: claude-opus-4-6 via Astrai

Found 3 issues:

[CRITICAL] Line 12: Missing `s# attribute on time column
  `trade` table uses `aj` but `time` column lacks sorted attribute.
  Without `s#`, asof join scans linearly — O(n) instead of O(log n).
  Fix: trade: `trade upsert update `s#time from trade

[WARNING] Line 34: Using `each` where vector operation suffices
  {x*y} each' (price;qty) can be replaced with price*qty
  Vector multiply is ~100x faster than each-both.

[INFO] Line 45: Consider `peach` for independent symbol processing
  Processing each symbol sequentially. Since operations are independent,
  `peach` would utilize all cores.
  Fix: results: func peach syms

Summary: 1 critical, 1 warning, 1 info. Focus on the missing sorted
attribute — it will cause aj performance to degrade from microseconds
to milliseconds at scale.
```  

## 环境变量：  
| 变量 | 是否必需 | 说明 |  
|----------|----------|-------------|  
| `ASTRAI_API_KEY` | 是 | 来自[as-trai.com](https://as-trai.com)的API密钥 |  
| `ANTHROPIC_API_KEY` | 否 | BYOK：Anthropic提供商密钥 |  
| `OPENAI_API_KEY` | 否 | BYOK：OpenAI提供商密钥 |  
| `GOOGLE_API_KEY` | 否 | BYOK：Google AI提供商密钥 |  
| `DEEPSEEK_API_KEY` | 否 | BYOK：DeepSeek提供商密钥 |  
| `MISTRAL_API_KEY` | 否 | BYOK：Mistral提供商密钥 |  
| `GROQ_API_KEY` | 否 | BYOK：Groq提供商密钥 |  
| `TOGETHER_API_KEY` | 否 | BYOK：Together AI提供商密钥 |  
| `FIREWORKS_API_KEY` | 否 | BYOK：Fireworks AI提供商密钥 |  
| `COHERE_API_KEY` | 否 | BYOK：Cohere提供商密钥 |  
| `PERPLEXITY_API_KEY` | 否 | BYOK：Perplexity提供商密钥 |  
| `REVIEW_STRICTNESS` | 否 | 默认严格性模式：`standard`、`strict`或`security` |  

## 外部接口：  
| 接口 | 功能 |  
|----------|---------|  
| `as-trai.com/v1/chat/completions` | Astrai推理路由器——将代码审查请求路由到最合适的AI模型 |  

## 安全性与隐私保护：  
- **代码不存储：**您的Q语言代码仅会被发送到选定的AI提供商进行推理，不会被Astrai存储。  
- **BYOK模式：**如果您使用自己的API密钥，请求会直接通过Astrai的路由系统发送到您的提供商账户；Astrai在请求生命周期结束后会立即销毁您的密钥。  
- **传输安全：**所有通信均使用HTTPS/TLS协议。  
- **无数据收集：**该工具不会发送任何分析数据或监控信息，仅传输代码审查请求。  
- **本地处理：**文件读取和结果格式化均在您的机器上完成。  

## 为何Q语言需要专门的代码审查工具：  
Q语言具有以下独特特性：  
- **极度的简洁性：**一条Q语言代码可能相当于Python中的20行代码；这种高密度使得手动审查时难以发现错误。  
- **隐式的类型转换：**Q语言在许多操作中会自动进行类型转换，这可能导致错误结果（例如：将long类型与float类型进行比较）。  
- **巨大的性能差异：**使用Q语言的惯用法与非惯用法之间的性能差距可能高达1000倍；例如：在时间列上缺少排序属性会导致O(log n)的连接操作变成O(n)的复杂度。  
- **复杂的语法规则：**Q语言中的副词（`/`、`\`、`'`、`:`、`:`、`:`）会以微妙的方式影响函数行为；错误的用法可能导致错误结果。  
- **AI模型的局限性：**通用AI模型难以理解Q语言的特定语法；该工具提供详细的提示，帮助模型理解Q语言的语法、kdb+的内部机制及金融领域的使用模式。  

## 定价：  
该工具基于Astrai的推理服务进行收费，费用取决于您选择的AI模型：  
| 计划类型 | 费用 | 包含内容 |  
|------|------|----------|  
| 免费 | $0 | 每天1,000次请求 |  
| Pro | $49/月 | 每天50,000次请求，优先路由服务 |  
| Business | $199/月 | 无限请求量，专属技术支持 |  

在BYOK模式下，您需要直接按提供商的费率支付费用；Astrai的路由服务包含在套餐价格中。