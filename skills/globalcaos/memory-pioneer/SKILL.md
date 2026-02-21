---
name: memory-pioneer
version: 1.0.2
description: "对您的代理程序的内存使用情况进行基准测试，并将匿名化的测试结果贡献给开放性的研究项目。这属于人工智能领域中的“公民科学”（citizen science）实践——即让普通用户也能为相关研究提供数据支持。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🗺️",
        "os": ["linux", "darwin"],
        "requires":
          {
            "skills": ["agent-memory-ultimate"],
          },
        "notes":
          {
            "security": "Benchmark scores (recall %, precision %, hallucination rate) are optionally shared with our open research dataset. OPT-IN ONLY: no data is sent without explicit user consent. NEVER SENT: conversation content, memory content, personal data. Users can review every data point before submission and opt-out anytime.",
          },
      },
  }
---
# Memory Pioneer

### 探索未知领域。你运行的每一个基准测试都在推动代理记忆相关研究的发展。

代理记忆是人工智能领域尚未解决的问题之一：代理能多好地回忆起它所学到的内容？它在哪些方面会出现记忆错觉？目前还没有足够的数据来回答这些问题。

这就是你发挥作用的地方。

**memory-pioneer** 会测试代理的记忆能力——包括回忆能力、精确度以及记忆错觉的检测能力——如果你选择参与，你的匿名测试结果将被贡献到一个开放的研究数据集中。你不仅仅是在进行测试，更是在开拓新的研究方向。

### 测试内容：

- 🧪 **回忆能力**：代理能否记住它存储的信息？
- 🎯 **精确度**：代理能否准确地检索到所需的信息？
- 🚨 **记忆错觉率**：代理是否会编造出它从未经历过的记忆？
- 📈 在调整参数后重新运行测试，以评估实际的改进效果。

### 数据共享情况：

我们坚信透明度的重要性——因为我们非常重视这一点。

**共享的数据（仅限自愿提供）：** 匿名的测试结果：回忆率%、精确度%、记忆错觉率。仅此而已。

**绝不共享的数据：** 你的对话内容、代理的记忆数据以及任何个人信息。绝不会泄露任何信息。

**你的控制权：**
- 首次运行时可以选择是否参与测试（非自动默认设置）。
- 在数据提交前可以随时查看每个数据点。
- 你可以随时选择退出测试，没有任何麻烦或责任。

**数据去向：** 这些数据会被汇总到我们的开放研究数据集中（位于 GitHub 上），用于支持 [**ENGRAM**](https://github.com/globalcaos/clawdbot-moltbot-openclaw/blob/main/docs/papers/context-compaction.md) 和 [**CORTEX**](https://github.com/globalcaos/clawdbot-moltbot-openclaw/blob/main/docs/papers/cortex.md) 等研究论文的撰写。所有数据都将公开共享。

### 为什么这很重要：

代理记忆是一个尚未被充分探索的领域。我们收集到的数据点越多，涵盖不同的代理、配置和使用场景，就越接近解决这个问题的目标。这对所有人来说都至关重要。

你运行的每一个基准测试都像是在未知领域里插下的一面旗帜。仅仅凭“我大概记得用户曾经提到过某个重要的事情”这样的主观判断，是无法构成有效的信息检索策略的。

## 与以下工具搭配使用效果更佳：

- [**agent-memory-ultimate**](https://clawhub.com/globalcaos/agent-memory-ultimate) —— 该工具用于测试代理的记忆系统。安装这两个工具，可以在同一过程中同时进行测试和优化。

👉 **探索完整项目：** [github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)

你可以克隆这个项目，对其进行修改，然后让它成为你自己的工具。