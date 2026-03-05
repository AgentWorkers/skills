---
name: metrillm
description: 为您的机器找到最适合的本地大型语言模型（LLM）。该工具会测试模型的运行速度、质量以及与系统内存（RAM）的兼容性，然后告诉您该模型是否适合在您的硬件上运行。
argument-hint: "[model-name]"
author: MetriLLM
source: https://github.com/MetriLLM/metrillm
license: MIT
allowed-tools: Bash, Read
---
# MetriLLM — 本地大语言模型（LLM）的基准测试工具

您可以直接通过您的AI编程助手来对任何本地大语言模型进行基准测试，从而判断该模型是否适合您的硬件配置。

## 设置

1. 安装并启动 [Ollama](https://ollama.com)。
2. 下载一个模型：`ollama pull llama3.2:3b`

## 使用方法

### 列出可用模型

```bash
ollama list
```

### 运行完整的基准测试

```bash
metrillm bench --model $ARGUMENTS --json
```

该测试会评估以下方面：
- **性能**：每秒生成的令牌数、生成第一个令牌所需的时间、内存使用情况
- **质量**：推理能力、数学运算能力、代码执行能力、指令遵循能力、输出结构化程度以及多语言支持能力
- **适用性评估**：优秀 / 良好 / 一般 / 不推荐

完整的基准测试根据模型大小的不同，耗时1到5分钟。

### 仅评估性能的快速测试

```bash
metrillm bench --model $ARGUMENTS --perf-only --json
```

该测试仅耗时约30秒，不包含质量评估。

### 查看之前的测试结果

```bash
ls ~/.metrillm/results/
```

您可以读取任何JSON文件以获取完整的测试详细信息。

### 将测试结果分享到公开排行榜

```bash
metrillm bench --model $ARGUMENTS --share
```

## 解读测试结果

| 评估结果 | 分数 | 含义 |
|---|---|---|
| 优秀 | >= 80 | 性能快速且准确——非常适合您的硬件 |
| 良好 | >= 60 | 性能稳定——适用于大多数任务 |
| 一般 | >= 40 | 可以使用，但存在某些局限性 |
| 不推荐 | < 40 | 性能太慢或准确性不足 |

需要重点关注的指标：
- `tokensPerSecond`（每秒生成的令牌数）> 30：适合交互式使用
- `ttft`（生成第一个令牌所需的时间）< 500毫秒：响应速度快
- `memoryUsedGB`（使用的内存大小）与可用RAM的对比：模型是否能在您的系统上正常运行？

## 使用技巧

- 使用 `--perf-only` 选项进行快速测试
- 较小的模型（10亿到30亿参数）测试时间约为30秒，较大的模型（70亿参数以上）测试时间约为2到5分钟
- 在进行基准测试前，请关闭那些对GPU资源要求较高的应用程序
- 某些高级模型（如Qwen3）会生成大量令牌，因此测试时间较长