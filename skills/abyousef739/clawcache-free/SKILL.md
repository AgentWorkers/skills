---
name: ClawCache Free
description: Python语言实现的智能大型语言模型（LLM）成本跟踪与缓存系统
version: 0.2.0
author: ClawCache Team
category: Developer Tools
license: MIT
---
# ClawCache Free – LLM（大型语言模型）成本跟踪与缓存工具

**ClawCache** 是一个适用于生产环境的 Python 库，可帮助您精确追踪在 LLM（大型语言模型）API 上的所有支出，并自动缓存响应结果，从而有效降低使用成本。

## 🎯 主要功能

### 💰 成本跟踪
- **自动记录** 每次 LLM API 调用的详细信息（包括使用的令牌数量）
- **每日 CLI 报告**：显示支出、节省的费用以及缓存效率
- **支持多种 LLM 服务提供商**：OpenAI、Anthropic、Mistral、Ollama 等
- **内置 2026 年度收费标准**，确保成本计算的准确性

### ⚡ 智能缓存
- **基于 SQLite 的精确匹配缓存**：速度快、可靠性高、数据存储在本地
- **实际使用场景中缓存命中率高达 58.3%**
- **自动节省费用**：缓存后的响应无需额外付费
- **复合缓存键**：提高缓存命中率（结合模型名称、参数等信息）

## 📊 实际性能测试

通过 48 次 API 调用（涵盖 4 种常见使用场景）进行的综合测试结果显示：

| 指标 | 值       |
|--------|---------|
| **缓存命中率** | 58.3%     |
| **总成本** | 0.0062 美元 |
| **节省的 API 调用次数** | 28 次（共 48 次） |
| **测试场景** | 代码审查、数据分析、内容生成、质量保证支持 |

### 场景示例

| 场景       | 调用次数 | 缓存命中次数 | 命中率    |
|------------|---------|-----------|---------|
| 代码审查     | 12       | 7        | 58.3%     |
| 数据分析     | 12       | 8        | 66.7%     |
| 内容生成     | 12       | 7        | 58.3%     |
| 质量保证支持 | 12       | 6        | 50.0%     |

## 🚀 快速入门

### 安装

```bash
pip install clawcache
```

### 基本用法

```python
from clawcache.free.cost import async_monitor_cost
from clawcache.free.cache_basic import BasicCache

# Initialize cache
cache = BasicCache()

# Decorate your LLM function
@async_monitor_cost
async def my_llm_call(prompt, model="gpt-4-turbo"):
    # Check cache first
    cached = await cache.aget(prompt, model=model)
    if cached:
        return cached.content
    
    # Make actual API call
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Cache the response
    await cache.aset(prompt, response, model=model)
    return response

# Use it
result = await my_llm_call("Explain quantum computing")
```

### 查看成本报告

ClawCache 会自动记录您的所有 LLM 使用成本：

```bash
# See today's detailed cost report
clawcache --report

# Output shows:
# - Money spent today
# - Money saved via cache
# - Total API calls
# - Cache hit rate
# - Efficiency metrics
```

## ✨ 主要特性

### 成本跟踪与监控
- ✅ **自动记录成本**：每次 API 调用都会记录时间戳、使用的模型、令牌数量及费用
- ✅ **每日 CLI 报告**：提供支出、节省费用及效率数据
- ✅ **精确的令牌计数**：支持使用 `tiktoken` 工具进行计数
- ✅ **支持多种 LLM 服务提供商**：OpenAI、Anthropic、Mistral、Ollama 等

### 智能缓存
- ✅ **基于 SQLite 的精确匹配缓存**：快速且可靠
- ✅ **复合缓存键**：根据提示内容、模型名称及参数生成缓存键
- ✅ **异步支持**：完全兼容异步/await 编程模式
- ✅ **自动节省费用**：缓存后的响应无需额外付费

### 安全性与可靠性
- ✅ **安全性**：支持启用或禁用数据序列化功能（默认禁用，以防 RCE 攻击）
- ✅ **并发安全性**：采用 SQLite 的 WAL 模式确保数据安全
- ✅ **跨平台兼容性**：支持 Windows、macOS、Linux

## 🔒 安全措施

ClawCache 非常重视安全性：
- **数据序列化功能可选**：默认禁用以防止 RCE（远程代码执行）攻击
- **SQLite WAL 模式**：确保多线程访问时的数据安全
- **文件锁定**：跨平台文件锁定机制，保证日志文件完整性

## 📖 配置选项

您可以通过环境变量自定义 ClawCache 的行为：

```bash
export CLAWCACHE_HOME=/path/to/cache  # Default: ~/.clawcache
```

### 缓存键设计

ClawCache 支持使用复合缓存键以提高缓存命中率：

```python
# Cache by prompt + model + temperature
await cache.aset(
    prompt, 
    response, 
    model="gpt-4-turbo",
    temperature=0.7
)
```

### 支持的模型及收费标准（2026 年度）

| 模型        | 输入费用（每百万令牌） | 输出费用（每百万令牌） |
|-------------|----------------|-------------------|
| GPT-4 Turbo   | 10.00 美元       | 30.00 美元       |
| GPT-3.5 Turbo   | 0.50 美元       | 1.50 美元       |
| Claude 3.5 Sonnet | 3.00 美元       | 15.00 美元       |
| Claude 3 Haiku    | 0.25 美元       | 1.25 美元       |

## 💡 使用场景

- **代码审查辅助**  
- **数据分析**  
- **内容生成**  

## 📈 成本节省预测

根据典型使用模式：
- **未使用 ClawCache 时**：48 次调用总成本为 0.0062 美元
- **使用 ClawCache 时**：首次调用成本仍为 0.0062 美元，后续调用成本约为 0.0026 美元（节省 58%）
- **年度预测**：每月 10,000 次调用可节省 3,600 美元

## ⭐ 即将推出的 Pro 版本

想要更多节省和功能吗？ClawCache Pro 版本将提供：
- 🔮 **语义缓存**：自动匹配相似查询，提高缓存命中率
- 📊 **高级分析**：详细成本统计与趋势分析
- 📈 **可视化报告**：美观的图表展示
- 🚀 **社交分享**：支持在 Twitter、LinkedIn、Molbook 上分享节省的费用及图表
- ☁️ **云同步**：支持跨设备同步缓存数据
- 🎯 **团队分析**：支持团队成员间的成本监控

**免费版本**：提供成本跟踪功能及 CLI 报告、精确匹配缓存服务  
**Pro 版**：增加社交分享、语义缓存及高级分析功能

[了解更多信息](https://www.clawcache.com/pro)

## 🤝 贡献方式

欢迎贡献代码！请按照以下步骤参与开发：
1. 克隆仓库
2. 创建新功能分支
3. 为新功能编写测试用例
4. 提交 Pull Request

## 📄 许可证

ClawCache 使用 MIT 许可证，详细信息请参阅 [LICENSE](LICENSE)

## 🔗 相关链接

- **官方网站**：[clawcache.com](https://clawcache.com)
- **GitHub 仓库**：[github.com/AbYousef739/-clawcache-free](https://github.com/AbYousef739/-clawcache-free)
- **文档**：[docs.clawcache.com](https://docs.clawcache.com)

---

**专为 AI 社区精心打造**  
*节省成本，精准追踪使用情况，助力更高效的工作流程。*