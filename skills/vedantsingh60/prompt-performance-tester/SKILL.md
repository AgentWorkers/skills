# Prompt Performance Tester

**支持9种AI提供商的模型无关性提示基准测试。**

输入任意模型ID，系统会自动检测对应的提供商。您可以比较Claude、GPT、Gemini、DeepSeek、Grok、MiniMax、Qwen、Llama和Mistral等提供商的响应延迟、成本、质量和一致性。

---

## 🚀 为什么需要这个工具？

### 问题背景
跨不同提供商比较大型语言模型（LLM）的性能需要手动测试：
- 没有系统化的方法来衡量模型之间的性能
- 成本差异显著，但难以直接比较
- 质量因使用场景和提供商而异
- 手动API测试耗时且容易出错

### 解决方案
您可以同时测试任何受支持提供商的任何模型的提示响应。系统会提供基于延迟、成本和质量的性能指标和建议。

### 成本对比示例
以每天10,000次请求、平均每次请求包含28个输入令牌和115个输出令牌为例：
- Claude Opus 4.6：约30.15美元/天（903美元/月）
- Gemini 2.5 Flash-Lite：约0.05美元/天（1.50美元/月）
- DeepSeek Chat：约0.14美元/天（4.20美元/月）
- Opus与Flash-Lite的月成本差异：901.50美元

---

## ✨ 您将获得什么

### 模型无关的多提供商测试
输入任意模型ID，系统会从模型名称前缀自动检测对应的提供商。
无需修改代码即可支持新模型。

| 提供商 | 示例模型 | 前缀 | 必需的API密钥 |
|----------|---------------|--------|--------------|
| **Anthropic** | claude-opus-4-6, claude-sonnet-4-6, claude-haiku-4-5-20251001 | `claude-` | ANTHROPIC_API_KEY |
| **OpenAI** | gpt-5.2-pro, gpt-5.2, gpt-5.1 | `gpt-`, `o1`, `o3` | OPENAI_API_KEY |
| **Google** | gemini-2.5-pro, gemini-2.5-flash, gemini-2.5-flash-lite | `gemini-` | GOOGLE_API_KEY |
| **Mistral** | mistral-large-latest, mistral-small-latest | `mistral-`, `mixtral-` | MISTRAL_API_KEY |
| **DeepSeek** | deepseek-chat, deepseek-reasoner | `deepseek-` | DEEPSEEK_API_KEY |
| **xAI** | grok-4-1-fast, grok-3-beta | `grok-` | XAI_API_KEY |
| **MiniMax** | MiniMax-M2.1 | `MiniMax`, `minimax` | MINIMAX_API_KEY |
| **Qwen** | qwen3.5-plus, qwen3-max-instruct | `qwen` | DASHSCOPE_API_KEY |
| **Meta Llama** | meta-llama/llama-4-maverick, meta-llama-3.3-70b-instruct | `meta-llama/`, `llama-` | OPENROUTER_API_KEY |

### 已知的定价（每100万个令牌）

| 模型 | 输入令牌 | 输出令牌 | 成本 |
|-------|-------|--------|
| claude-opus-4-6 | 15.00美元 | 75.00美元 |
| claude-sonnet-4-6 | 3.00美元 | 15.00美元 |
| claude-haiku-4-5-20251001 | 1.00美元 | 5.00美元 |
| gpt-5.2-pro | 21.00美元 | 168.00美元 |
| gpt-5.2 | 1.75美元 | 14.00美元 |
| gpt-5.1 | 2.00美元 | 8.00美元 |
| gemini-2.5-pro | 1.25美元 | 10.00美元 |
| gemini-2.5-flash | 0.30美元 | 2.50美元 |
| gemini-2.5-flash-lite | 0.10美元 | 0.40美元 |
| mistral-large-latest | 2.00美元 | 6.00美元 |
| mistral-small-latest | 0.10美元 | 0.30美元 |
| deepseek-chat | 0.27美元 | 1.10美元 |
| deepseek-reasoner | 0.55美元 | 2.19美元 |
| grok-4-1-fast | 5.00美元 | 25.00美元 |
| grok-3-beta | 3.00美元 | 15.00美元 |
| MiniMax-M2.1 | 0.40美元 | 1.60美元 |
| qwen3.5-plus | 0.57美元 | 2.29美元 |
| qwen3-max-instruct | 1.60美元 | 6.40美元 |
| meta-llama/llama-4-maverick | 0.20美元 | 0.60美元 |
| meta-llama/llama-3.3-70b-instruct | 0.59美元 | 0.79美元 |

> **注意：** 未列出的模型仍然可以测试，但系统会显示成本为0.00并给出警告。定价表仅供参考，不作为验证依据。

### 性能指标
每次测试都会记录以下指标：
- ⚡ **延迟** — 响应时间（毫秒）
- 💰 **成本** — 每次请求的API费用（输入令牌 + 输出令牌）
- 🎯 **质量** — 响应质量得分（0–100）
- 📊 **令牌使用量** — 输入和输出令牌的数量
- 🔄 **一致性** — 多次测试结果的一致性
- ❌ **错误跟踪** — API错误、超时、速率限制

### 智能建议
您可以立即获得以下信息：
- 哪个模型对您的提示响应**最快**？
- 哪个模型最**经济实惠**？
- 哪个模型产生的响应**质量最高**？
- 更换提供商后可以**节省**多少成本？

---

## 📊 实际应用示例

```
PROMPT: "Write a professional customer service response about a delayed shipment"

┌─────────────────────────────────────────────────────────────────┐
│ GEMINI 2.5 FLASH-LITE (Google) 💰 MOST AFFORDABLE              │
├─────────────────────────────────────────────────────────────────┤
│ Latency:  523ms                                                 │
│ Cost:     $0.000025                                             │
│ Quality:  65/100                                                │
│ Tokens:   28 in / 87 out                                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ DEEPSEEK CHAT (DeepSeek) 💡 BUDGET PICK                        │
├─────────────────────────────────────────────────────────────────┤
│ Latency:  710ms                                                 │
│ Cost:     $0.000048                                             │
│ Quality:  70/100                                                │
│ Tokens:   28 in / 92 out                                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ CLAUDE HAIKU 4.5 (Anthropic) 🚀 BALANCED PERFORMER             │
├─────────────────────────────────────────────────────────────────┤
│ Latency:  891ms                                                 │
│ Cost:     $0.000145                                             │
│ Quality:  78/100                                                │
│ Tokens:   28 in / 102 out                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ GPT-5.2 (OpenAI) 💡 EXCELLENT QUALITY                          │
├─────────────────────────────────────────────────────────────────┤
│ Latency:  645ms                                                 │
│ Cost:     $0.000402                                             │
│ Quality:  88/100                                                │
│ Tokens:   28 in / 98 out                                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ CLAUDE OPUS 4.6 (Anthropic) 🏆 HIGHEST QUALITY                 │
├─────────────────────────────────────────────────────────────────┤
│ Latency:  1,234ms                                               │
│ Cost:     $0.001875                                             │
│ Quality:  94/100                                                │
│ Tokens:   28 in / 125 out                                       │
└─────────────────────────────────────────────────────────────────┘

🎯 RECOMMENDATIONS:
1. Most cost-effective: Gemini 2.5 Flash-Lite ($0.000025/request) — 99.98% cheaper than Opus
2. Budget pick: DeepSeek Chat ($0.000048/request) — strong quality at low cost
3. Best quality: Claude Opus 4.6 (94/100) — state-of-the-art reasoning & analysis
4. Smart pick: Claude Haiku 4.5 ($0.000145/request) — 81% cheaper, 83% quality match
5. Speed + Quality: GPT-5.2 ($0.000402/request) — excellent quality at mid-range cost

💡 Potential monthly savings (10,000 requests/day, 28 input + 115 output tokens avg):
   - Using Gemini 2.5 Flash-Lite vs Opus: $903/month saved ($1.44 vs $904.50)
   - Using DeepSeek Chat vs Opus: $899/month saved ($4.50 vs $904.50)
   - Using Claude Haiku vs Opus: $731/month saved ($173.40 vs $904.50)
```

---

## 使用场景

### 生产环境部署
- 在选择模型之前进行评估
- 比较不同提供商的成本与质量
- 基于提供商测试API的延迟

### 提示开发
- 在不同模型上测试提示变体
- 持续测量质量得分
- 比较性能指标

### 成本分析
- 分析每种模型的LLM API使用成本
- 比较不同提供商的定价结构
- 寻找更经济的替代方案

### 性能测试
- 测量延迟和响应时间
- 测试多次运行的结果一致性
- 评估质量得分

---

## 🚀 快速入门

### 1. 订阅该工具
在ClawhHub上点击“Subscribe”以获取访问权限。

### 2. 设置API密钥
添加您想要测试的提供商的密钥：

```bash
# Anthropic (Claude models)
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI (GPT models)
export OPENAI_API_KEY="sk-..."

# Google (Gemini models)
export GOOGLE_API_KEY="AI..."

# DeepSeek
export DEEPSEEK_API_KEY="..."

# xAI (Grok models)
export XAI_API_KEY="..."

# MiniMax
export MINIMAX_API_KEY="..."

# Alibaba (Qwen models)
export DASHSCOPE_API_KEY="..."

# OpenRouter (Meta Llama models)
export OPENROUTER_API_KEY="..."

# Mistral
export MISTRAL_API_KEY="..."
```

您只需要为计划测试的提供商设置密钥。

### 3. 安装依赖项

```bash
# Install only what you need
pip install anthropic          # Claude
pip install openai             # GPT, DeepSeek, xAI, MiniMax, Qwen, Llama
pip install google-generativeai  # Gemini
pip install mistralai          # Mistral

# Or install everything
pip install anthropic openai google-generativeai mistralai
```

### 4. 运行首次测试

**选项A：Python**
```python
import os
from prompt_performance_tester import PromptPerformanceTester

tester = PromptPerformanceTester()  # reads API keys from environment

results = tester.test_prompt(
    prompt_text="Write a professional email apologizing for a delayed shipment",
    models=[
        "claude-haiku-4-5-20251001",
        "gpt-5.2",
        "gemini-2.5-flash",
        "deepseek-chat",
    ],
    num_runs=3,
    max_tokens=500
)

print(tester.format_results(results))
print(f"🏆 Best quality:  {results.best_model}")
print(f"💰 Cheapest:      {results.cheapest_model}")
print(f"⚡ Fastest:       {results.fastest_model}")
```

**选项B：CLI**
```bash
# Test across multiple models
prompt-tester test "Your prompt here" \
  --models claude-haiku-4-5-20251001 gpt-5.2 gemini-2.5-flash deepseek-chat \
  --runs 3

# Export results
prompt-tester test "Your prompt here" --export results.json
```

---

## 🔒 安全性与隐私

### API密钥安全
- 密钥仅存储在环境变量中，从不硬编码或记录
- 绝不会传输到UnisAI服务器
- 所有提供商的API调用都使用HTTPS加密

### 数据隐私
- 您的提示仅发送到您选择用于测试的AI提供商
- 每个提供商都有自己的数据保留政策（请参阅其隐私政策）
- 数据不会存储在UnisAI的基础设施上

## 📚 技术细节

### 系统要求
- **Python**：3.9及以上版本
- **依赖项**：`anthropic`, `openai`, `google-generativeai`, `mistralai`（仅安装实际需要的依赖项）
- **平台**：macOS、Linux、Windows

### 架构
- **懒加载客户端** — 仅加载实际测试的提供商的SDK
- **基于前缀的路由** — `PROVIDER_MAP`根据模型名称自动检测提供商；没有硬编码的白名单
- **兼容OpenAI的路径** — DeepSeek、xAI、MiniMax、Qwen和OpenRouter都使用`openai` SDK，并带有自定义的`base_url`
- **定价表** — 仅用于成本计算；未知模型的成本显示为0.00并带有警告

### 收集的指标
每次测试都会记录以下数据：
- **延迟**：总响应时间（毫秒）
- **成本**：基于已知定价的输入和输出令牌费用
- **质量**：基于长度和完整性的响应质量得分（0–100）
- **令牌**：每个提供商的输入和输出令牌数量
- **一致性**：多次测试结果的标准差
- **错误**：超时、速率限制、API错误

---

## ❓ 常见问题

**Q：我需要所有9个提供商的API密钥吗？**
A：不需要。您只需要为想要测试的提供商设置密钥。如果只测试Claude模型，只需`ANTHROPIC_API_KEY`即可。

**Q：API费用由谁支付？**
A：由您支付。您需要提供自己的API密钥，并直接支付给每个提供商。此工具不收取每次请求的费用。

**Q：成本计算准确吗？**
A：费用是根据已知定价表和实际令牌数量计算的。未在定价表中的模型显示成本为0.00，但模型仍然可以运行。

**Q：我可以测试未在定价表中的模型吗？**
A：可以。任何名称以受支持前缀开头的模型都可以测试。未列出的模型的成本将显示为0.00。

**Q：我可以测试非英语语言的提示吗？**
A：可以。所有支持的提供商都支持多种语言。

**Q：我可以在生产环境/持续集成/持续部署（CI/CD）中使用这个工具吗？**
A：可以。可以直接从Python导入`PromptPerformanceTester`，或通过CLI调用它。

**Q：如果我的提示很长怎么办？**
A：适当设置`max_tokens`参数。该工具会原样将您的提示发送给每个提供商的API。

---

## 🗺️ 路线图

### ✅ 当前版本（v1.1.8）
- 支持模型无关性架构 — 任何模型ID都可以通过前缀检测
- 支持9个提供商和20个已知模型及其定价
- DeepSeek、xAI Grok、MiniMax、Qwen、Meta Llama作为一级提供商
- 支持Claude 4.6系列（opus-4-6、sonnet-4-6）
- 实现懒加载客户端初始化 — 仅加载实际使用的提供商的SDK
- 修复了UnisAI的品牌标识

### 🚧 即将推出（v1.3）
- **批量测试**：同时测试100多个提示
- **历史数据跟踪**：记录模型性能的变化
- **Webhook集成**：Slack、Discord、电子邮件通知

### 🔮 未来版本（v1.3+）
- **A/B测试框架**：科学地进行提示实验
- **微调建议**：根据您的需求推荐适合的模型
- **自定义基准测试**：创建自己的评估标准
- **自动优化**：基于AI的提示优化建议

---

## 📞 支持

- **电子邮件**：support@unisai.vercel.app
- **网站**：https://unisai.vercel.app
- **问题报告**：support@unisai.vercel.app

---

## 📝 许可证与条款

此工具通过ClawhHub提供，遵循以下条款。

### ✅ 您可以：
- 用于自己的业务和项目
- 为内部应用程序测试提示
- 为个人用途修改源代码

### ❌ 您不可以：
- 将工具分发到ClawhHub注册表之外
- 转售或再许可
- 未经许可使用UnisAI的商标

**完整条款**：请参阅[LICENSE.md]

---

## 📝 更新日志

### [1.1.8] - 2026-02-27

#### 修复与优化
- 版本更新至1.1.8
- 重新编写了SKILL.md文件，优化了格式，删除了过时的内容
- 移除了旧的IP水印（`PROPRIETARY_SKILL_VEDANT_2024`）
- 将水印统一为`PROPRIETARY_SKILL_UNISAI_2026_MULTI_PROVIDER`
- 修复了所有UnisAI的品牌标识（在v1.1.0的更新日志中为UniAI）
- 更新了定价表，包含了所有20个已知模型
- 优化了FAQ、快速入门和使用场景部分

### [1.1.6] - 2026-02-27

#### 🏗️ 模型无关性架构
- 根据模型名称前缀自动检测提供商
- 无需修改代码即可支持新模型
- 新增了DeepSeek、xAI Grok、MiniMax、Qwen、Meta Llama作为一级提供商（共9个）
- 更新了Claude到4.6系列（claude-opus-4-6、claude-sonnet-4-6）
- 实现了懒加载客户端初始化
- 为DeepSeek、xAI、MiniMax、Qwen、OpenRouter统一了OpenAI兼容的路径

### [1.1.5] - 2026-02-01

#### 最新模型更新
- 添加了GPT-5.2系列的Instant、Thinking和Pro版本
- Gemini 2.5系列更新为2.5 Pro、Flash和Flash-Lite
- 更新了Claude 4.5的定价
- 共支持3个提供商的10个模型

### [1.1.0] - 2026-01-15

#### ✨ 主要功能
- 支持多个提供商（Claude、GPT、Gemini）
- 跨提供商的成本比较
- 强化的推荐系统
- 更换了品牌名称为UnisAI

### [1.0.0] - 2024-02-02

#### 初始版本
- 仅支持Claude模型的提示测试（Haiku、Sonnet、Opus）
- 提供性能指标：延迟、成本、质量、一致性
- 基本的推荐系统

---

**最后更新时间**：2026年2月27日
**当前版本**：1.1.8
**状态**：活跃且持续维护中

© 2026 UnisAI. 保留所有权利。