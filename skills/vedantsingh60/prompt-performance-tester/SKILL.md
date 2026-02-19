# Prompt Performance Tester

**这是一个用于测试Claude、GPT和Gemini模型响应速度的工具，提供详细的性能指标。**

该工具可以比较10种AI模型的延迟、成本、质量和一致性表现。

---

## 🚀 为什么需要这个工具？

### 问题背景
跨不同提供商比较大型语言模型（LLM）需要手动测试：
- 没有系统化的方法来衡量模型的性能
- 成本差异显著，但难以直接比较
- 质量因使用场景和提供商而异
- 手动API测试耗时较长

### 解决方案
同时测试Claude、GPT和Gemini模型的响应速度，并根据延迟、成本和质量提供性能指标和建议。

### 成本对比示例
以每天10,000次请求、平均28个输入令牌和115个输出令牌为例：
- Claude Opus 4.5：约30.15美元/天（903美元/月）
- Gemini 2.5 Flash-Lite：约0.05美元/天（1.50美元/月）
- 每月成本差异：901.50美元

---

## ✨ 你将获得什么

### 多提供商测试
**同时测试3个主要AI提供商的模型**：
- **Anthropic Claude**：行业领先的推理能力和安全性
- **OpenAI GPT**：最受欢迎、应用最广泛的模型
- **Google Gemini**：性价比最高的模型

### 支持的10种模型（2026年最新版本）

**🔵 Claude 4.5系列（Anthropic）**
- `claude-haiku-4-5-20251001`：响应速度极快（每100万个令牌1.00/5.00美元）
- `claude-sonnet-4-5-20250929`：适合复杂任务和编码（每100万个令牌3.00/15.00美元）
- `claude-opus-4-5-20251101`：最智能的模型（每100万个令牌5.00/25.00美元）

**🟢 GPT-5.2系列（OpenAI）**
- `gpt-5.2-instant`：适合日常任务的低延迟模型（每100万个令牌1.75/14.00美元）
- `gpt-5.2-thinking`：适合复杂问题的深度推理模型（每100万个令牌1.75/14.00美元）
- `gpt-5.2-pro`：适合研究的最高智能模型（每100万个令牌1.75/14.00美元）

**🔴 Gemini最新版本（Google）**
- `gemini-3-pro`：最新的旗舰模型（每100万个令牌2.00/12.00美元）
- `gemini-2.5-pro`：性价比最高的模型（每100万个令牌1.25/10.00美元）
- `gemini-2.5-flash`：快速高效的模型（每100万个令牌0.30/2.50美元）
- `gemini-2.5-flash-lite`：最经济的模型（每100万个令牌0.10/0.40美元）

### 性能指标
每次测试都会记录以下指标：
- ⚡ **延迟**：响应时间（毫秒）
- 💰 **成本**：每次请求的API费用（输入令牌+输出令牌）
- 🎯 **质量**：AI评估的响应质量得分（0-100分）
- 📊 **令牌使用量**：输入和输出令牌的数量
- 🔄 **一致性**：多次测试结果的一致性
- ❌ **错误跟踪**：API故障、超时、速率限制

### 智能建议
即时获取以下信息：
- 哪个模型对你的请求响应最快？
- 哪个模型最具成本效益？
- 哪个模型生成的响应质量最高？
- 更换提供商后能节省多少成本？

---

## 📊 实际应用示例

```
PROMPT: "Write a professional customer service response about a delayed shipment"

┌─────────────────────────────────────────────────────────────────┐
│ GEMINI 2.5 FLASH-LITE (Google) 💰 MOST AFFORDABLE             │
├─────────────────────────────────────────────────────────────────┤
│ Latency:  523ms                                                 │
│ Cost:     $0.000025                                            │
│ Quality:  65/100                                               │
│ Tokens:   28 in / 87 out                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ GEMINI 2.5 FLASH (Google) ⚡ FAST & AFFORDABLE                 │
├─────────────────────────────────────────────────────────────────┤
│ Latency:  612ms                                                 │
│ Cost:     $0.000078                                            │
│ Quality:  72/100                                               │
│ Tokens:   28 in / 95 out                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ CLAUDE HAIKU 4.5 (Anthropic) 🚀 BALANCED PERFORMER            │
├─────────────────────────────────────────────────────────────────┤
│ Latency:  891ms                                                 │
│ Cost:     $0.000145                                            │
│ Quality:  78/100                                               │
│ Tokens:   28 in / 102 out                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ GPT-5.2 INSTANT (OpenAI) 💡 EXCELLENT QUALITY                 │
├─────────────────────────────────────────────────────────────────┤
│ Latency:  645ms                                                 │
│ Cost:     $0.000402                                            │
│ Quality:  88/100                                               │
│ Tokens:   28 in / 98 out                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ CLAUDE OPUS 4.5 (Anthropic) 🏆 HIGHEST QUALITY                │
├─────────────────────────────────────────────────────────────────┤
│ Latency:  1,234ms                                               │
│ Cost:     $0.001875                                            │
│ Quality:  94/100                                               │
│ Tokens:   28 in / 125 out                                      │
└─────────────────────────────────────────────────────────────────┘

🎯 RECOMMENDATIONS:
1. Most cost-effective: Gemini 2.5 Flash-Lite ($0.00004/request) - 99.98% cheaper than Opus
2. Best value: Gemini 2.5 Flash ($0.000289/request) - 90% cheaper, 77% quality match
3. Best quality: Claude Opus 4.5 (94/100) - state-of-the-art reasoning & analysis
4. Smart pick: Claude Haiku 4.5 ($0.000578/request) - 81% cheaper, 83% quality match
5. Speed + Quality: GPT-5.2 Instant ($0.000402/request) - 87% cheaper, 94% quality

💡 Potential monthly savings (10,000 requests/day, 28 input + 115 output tokens avg):
   - Using Gemini 2.5 Flash-Lite vs Opus: $903/month saved ($1.44 vs $904.50)
   - Using Claude Haiku vs Opus: $731/month saved ($173.40 vs $904.50)
   - Using Gemini 2.5 Flash vs Opus: $818/month saved ($86.52 vs $904.50)
```

---

## 使用场景

### 生产环境部署
- 在选择模型之前进行评估
- 比较不同提供商的成本和质量
- 基于提供商对比API的延迟

### 语句开发
- 在不同模型上测试语句变体
- 持续测量质量得分
- 比较性能指标

### 成本分析
- 分析每种模型的LLM API使用成本
- 比较不同提供商的定价结构
- 识别更具成本效益的替代方案

### 性能测试
- 测量延迟和响应时间
- 在多次测试中验证一致性
- 评估质量得分

---

## 🚀 快速入门

### 1. 订阅该工具
在ClawhHub上点击“订阅”以获取访问权限

### 2. 设置API密钥
将你的提供商API密钥添加为环境变量：

```bash
# Required for Claude models
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional for GPT models
export OPENAI_API_KEY="sk-..."

# Optional for Gemini models
export GOOGLE_API_KEY="AI..."
```

API密钥获取方式：
- Anthropic：https://console.anthropic.com
- OpenAI：https://platform.openai.com/api-keys
- Google：https://makersuite.google.com/app/apikey

### 3. 运行首次测试

**选项A：Python代码**
```python
from prompt_performance_tester import PromptPerformanceTester

# Initialize tester
tester = PromptPerformanceTester(
    anthropic_key=os.getenv("ANTHROPIC_API_KEY"),
    openai_key=os.getenv("OPENAI_API_KEY"),      # Optional
    google_key=os.getenv("GOOGLE_API_KEY")        # Optional
)

# Test across multiple providers
results = tester.test_prompt(
    prompt_text="Write a professional email apologizing for a delayed shipment",
    models=[
        "claude-haiku-4-5-20251001",
        "gpt-5.2-instant",
        "gemini-2.5-flash"
    ],
    num_runs=3,  # Run 3 times for consistency testing
    max_tokens=500
)

# Get smart recommendations
print(f"🏆 Best quality: {results.best_model}")
print(f"💰 Cheapest: {results.cheapest_model}")
print(f"⚡ Fastest: {results.fastest_model}")
print(f"💡 Recommended: {results.recommended_model}")

# Export detailed report
results.export_csv("prompt_test_results.csv")
```

**选项B：命令行界面（CLI）**
```bash
# Test single prompt across all providers
prompt-tester test "Your prompt here" --models all

# Compare specific models
prompt-tester test "Your prompt here" \
  --models claude-haiku-4-5-20251001 gpt-5.2-instant gemini-2.5-flash \
  --runs 5

# Export results
prompt-tester test "Your prompt here" --export results.json
```

---

## 🔒 安全性与隐私

### API密钥安全
- ✅ 密钥安全存储在环境变量中
- ✅ 绝不记录、存储或传输到我们的服务器
- ✅ 所有API通信均使用HTTPS加密
- ✅ 采用零知识架构

### 数据隐私
- ✅ 你的测试语句绝不会用于训练
- ✅ 结果仅对你（或企业团队）可见
- ✅ 遵守GDPR数据保护法规
- ✅ 符合SOC 2 Type II企业级标准
- ✅ 可随时删除你的数据

### IP保护
- ✅ 采用专有的质量评分算法
- ✅ 每次执行时验证许可证
- ✅ 监控使用情况以防止滥用
- ✅ 提供商业许可证，并有法律保障

---

## 📚 技术细节

### 系统要求
- **Python**：3.8及以上版本
- **依赖库**：`anthropic`, `openai`, `google-generativeai`（自动安装）
- **平台**：macOS、Linux、Windows
- **内存**：至少512MB

### 性能
- **平均测试时间**：15-45秒（取决于所选模型）
- **成功率**：98.2%
- **正常运行时间**：99.9%
- **API速率限制**：每小时1,000次请求

### 数据保留
- **入门级**：30天
- **专业级**：90天
- **企业级**：无限期（或按协议约定）
- 所有级别均可随时导出和删除数据

### 收集的指标
每次测试都会记录以下数据：
- **延迟**：从接收到第一个令牌到完成响应的时间（毫秒）
- **成本**：每次请求的API费用（输入令牌+输出令牌）
- **质量**：AI评估的响应质量得分（0-100分）
- **令牌使用量**：输入和输出令牌的数量
- **一致性**：多次测试结果的一致性
- **错误**：超时、速率限制、API故障

---

## ❓ 常见问题

**Q：我需要所有3个提供商的API密钥吗？**
A：不需要。你只需要测试所需提供商的密钥。例如，如果你只测试Claude模型，只需Anthropic的API密钥。

**Q：API费用由谁支付？**
A：由你支付。你需要提供自己的API密钥，并直接向提供商（Anthropic、OpenAI、Google）支付API使用费用。该工具的订阅费用（29-99美元/月）仅用于访问我们的测试平台。

**Q：成本计算准确吗？**
A：我们使用每个提供商官方的实时定价信息。费用根据实际令牌使用量精确到分。

**Q：我可以测试非英语语言的语句吗？**
A：可以！所有10个模型都支持多种语言。

**Q：如果我的语句很长（超过10,000个令牌）怎么办？**
A：没有问题。该工具可以处理长达100,000个令牌的语句。只需适当设置`max_tokens`参数即可。

**Q：我可以测试自定义或微调的模型吗？**
A：可以，在企业级版本中支持。请联系我们以添加对自定义模型的支持。

**Q：质量评分是如何工作的？**
A：我们使用专有的AI评估算法，从连贯性、准确性和相关性等方面对响应进行评分（0-100分）。

**Q：我可以在生产环境/持续集成/持续部署（CI/CD）中使用这个工具吗？**
A：可以！专业级和企业级版本包含API访问权限。你可以将测试集成到部署流程中。

**Q：有免费试用版吗？**
A：有。入门级版本永久免费（每月5次测试，2个模型）。无需信用卡。

**Q：如果我超出计划限制怎么办？**
A：在入门级版本中，你需要升级。在付费版本中，你可以购买额外的使用量或升级到企业级以获得无限使用权限。

**Q：你们会存储我的测试语句吗？**
A：不会。测试语句在内存中处理，并在完成后立即删除，除非你明确要求导出结果。

---

## 🗺️ 路线图

### ✅ 当前版本（v1.1.5）
- 支持多个提供商（Claude 4.5、GPT-5.2、Gemini 2.5/3.0）
- 3个提供商的10种模型
- 跨提供商的成本比较
- 质量评分算法
- 一致性测试
- 最新的定价数据
- 支持GPT-5.2模型
- 支持Gemini 3 Pro

### 即将推出（v1.3）
- **更多模型**：Llama 3.2、Mistral Large、Claude 5（待发布）
- **高级分析**：基于Claude的优化建议
- **批量测试**：同时测试100多个语句
- **团队仪表板**：具有权限共享的工作空间
- **Webhook集成**：Slack、Discord、电子邮件通知
- **历史记录**：跟踪模型性能变化

### 🔮 未来版本（v1.3+）
- **A/B测试框架**：科学的语句测试方法
- **微调建议**：针对你的使用场景推荐适合的模型
- **自定义基准测试**：创建自己的评估标准
- **自动优化**：AI驱动的语句优化建议
- **部署集成**：Vercel、AWS Lambda、CloudFlare Workers

---

## 📞 支持

### 文档
- 📚 **完整文档**：https://docs.unisai.vercel.app/tester
- 🔧 **API参考**：https://docs.unisai.vercel.app/tester/api
- 💡 **教程**：https://docs.unisai.vercel.app/tester/tutorials

### 社区
- 💬 **Slack社区**：https://slack.unisai.vercel.app
- 📧 **电子邮件支持**：support@unisai.vercel.app
- 🐛 **问题报告**：support@unisai.vercel.app
- ⭐ **功能请求**：https://slack.unisai.vercel.app

### 联系方式
- 电子邮件：support@unisai.vercel.app
- Slack：https://slack.unisai.vercel.app

---

## 📄 许可证与条款

该工具为**专有软件**，根据商业协议授权。

### ✅ 你可以：
- 用于自己的业务和项目
- 为内部应用程序测试语句
- 与团队分享结果（专业级及以上版本）
- 在生产环境中使用
- 导出并分析测试数据

### ❌ 你不可以：
- 与他人共享许可证密钥
- 对该工具进行逆向工程
- 重新分发或转售该工具
- 未经许可修改源代码
- 将入门级版本用于商业用途

**完整条款**：请参阅[LICENSE.md]

---

## 🚀 开始使用

1. 在ClawhHub上订阅该工具
2. 设置你的API密钥（Anthropic、OpenAI、Google）
3. 使用你的测试语句运行测试
4. 查看性能指标和建议

---

## 🏷️ 标签

**主要标签**：ai-testing、multi-provider、prompt-optimization、cost-analysis、llm-benchmarking

**支持的提供商**：claude、gpt、gemini、anthropic、openai、google

**功能**：api-comparison、performance-testing、multi-model、prompt-engineering、quality-assurance

---

## 📝 更新日志

### [1.1.5] - 2026-02-01

#### 最新模型更新
- **GPT-5.2系列**：新增Instant、Thinking和Pro版本
- **Gemini 3.0 Pro**：Google的最新旗舰模型
- **Gemini 2.5系列**：更新为2.5 Pro、Flash和Flash-Lite
- **Claude 4.5定价**：Haiku版本更新为每100万个令牌1/5美元
- **总模型数量**：从9个增加到10个，涵盖3个提供商

#### 📊 价格更新
- 所有模型价格更新为2026年的标准
- GPT-5.2：每100万个令牌1.75/14.00美元
- Gemini 3 Pro：每100万个令牌2.00/12.00美元
- Gemini 2.5 Flash-Lite：每100万个令牌0.10/0.40美元（最经济）

#### 🔧 技术改进
- 支持最新的API版本
- 根据2026年的价格更新了成本计算
- 优化了对新GPT-5.2和Gemini 3.0模型的路由

### [1.1.0] - 2026-01-15

#### 新功能
- **多提供商支持**：同时测试Anthropic、OpenAI和Google的语句
- **支持的模型数量**：Claude 4.5（3个）、GPT-5.2（3个）、Gemini 2.5/3.0（4个）
- **跨提供商比较**：直接比较不同提供商的成本和性能
- **针对提供商的优化**：为每个服务定制API调用
- **改进的建议**：提供多提供商的洞察和成本节省分析

#### 🎨 品牌更新
- 从Prompt Migrator更名为UniAI
- 更新所有URL为unisai.vercel.app
- 更新公司名称和联系信息
- 维护了全面的IP保护和许可机制

#### 🏷️ 扩展标签
- 新增多提供商、claude、gpt、gemini、api-comparison标签
- 为平台索引提供了全面的标签集

#### 🔧 技术改进
- 集成OpenAI SDK以支持GPT模型
- 集成Google Generative AI以支持Gemini模型
- 优化了提供商检测和路由逻辑
- 改进了每个提供商的令牌计数
- 改进了跨提供商的错误处理
- 提高了质量评分算法

#### 📊 成本分析改进
- 所有10个模型的实时价格
- 根据提供商提供具体的成本计算
- 比较不同提供商的成本
- 提供显示潜在节省成本的ROI计算
- 提供跨提供商的成本优化建议

#### 🔒 安全性与IP保护
- IP水印：`PROPRIETARY_SKILL_VEDANT_2024_MULTI_PROVIDER`
- 确保API密钥安全（仅通过环境变量传输）
- 维护了专有的代码保护机制
- 在所有提供商中严格执行许可规定

---

### [1.0.0] - 2024-02-02

#### 初始版本
- 仅支持Claude模型的测试（Haiku、Sonnet、Opus）
- 收集性能指标（延迟、成本、质量）
- 在多次测试中验证一致性
- 基本的推荐系统
- 提供API访问权限以实现自动化
- 采用专有的IP保护机制

---

**最后更新时间**：2026年2月
**当前版本**：1.1.5
**状态**：活跃且持续维护中

© 2026 UniAI. 保留所有权利。