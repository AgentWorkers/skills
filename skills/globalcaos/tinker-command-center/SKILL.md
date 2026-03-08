---
name: tinker-command-center
description: "别再猜测你的人工智能系统到底花了多少钱了。Tinker 可以实时显示每一个代币（token）、每一美元的花费，以及所有与系统运行相关的成本数据（包括存储、计算等资源消耗）。"
metadata:
  openclaw:
    requires:
      bins: [node, pnpm]
    notes:
      security: "Read-only dashboard. Connects to your local OpenClaw gateway WebSocket. No data leaves your machine."
---
# Tinker 命令中心

> **其实，你本不必花费 200 美元的 Opus 会话费用。** Tinker 会实时显示每个令牌的去向——在账单生成之前。

## 问题所在

你之所以切换到 Claude API，是因为 Anthropic 的表现确实非常出色（值得尊敬）。但现在，当你通过 OpenClaw 使用 Opus 时，一次深度对话就会消耗 **20 多美元的令牌**，而且没有任何预警。三天后你查看仪表盘时，才会疑惑到底发生了什么。

这其实不是计费问题，而是信息透明度的问题。

## Tinker 的功能

Tinker 是一个 **实时命令中心**，它直接集成在你的 OpenClaw 网关之上。它可以实时显示填充在你的上下文窗口中的内容、每个响应的成本，以及你的预算使用情况。

### 🗺️ 上下文信息树状图

这是一个交互式的树状图，用于展示你的上下文窗口中的各项内容：系统提示、对话历史、工具结果等。你可以从类别、消息到原始文本逐层深入查看。当你想知道“为什么我的上下文信息会消耗 180,000 个令牌”时，这个工具能立刻为你解答。

### 📊 响应信息树状图

同样的可视化方式用于展示模型的输出结果：文本部分占多少成本、模型推理部分占多少成本、工具调用部分又占多少成本？它会详细列出每次 LLM 调用的具体费用，让你清楚地看到那个包含 8 个步骤的工具循环的实际成本。

### 💰 实时成本追踪

它会显示每个提供者的令牌使用情况，提供每日和每月的估算数据。同时还会显示 Claude 的 5 小时速率限制窗口，并带有倒计时功能。这样你就再也不会意外超出速率限制了。

### ⚠️ 预算警报

你可以设置每月的预算限制。当预算使用达到 70%、90% 或 100% 时，系统会立即发出警报。再也不用说“我稍后再查看”了——对于 Opus 来说，等到“稍后”可能已经太晚了。

### 🔄 多次调用视图

当你的代理依次使用多个工具（搜索 → 阅读 → 编辑 → 测试 → 提交）时，每个工具调用的上下文和成本都会被单独显示出来。你可以清楚地看到哪些工具调用消耗了大量令牌，哪些工具调用较为经济。

### 💬 完整的聊天界面

Tinker 不只是一个简单的仪表盘，它还是一个功能齐全的网页聊天工具：支持会话切换、工具调用详细查看（可以在线展开任何工具的详细信息），以及实时数据流。你可以将其作为日常工作的辅助工具，也可以仅用于监控使用情况。

## 定价参考

以下是 Tinker 监控的 API 成本：

| 模型                | 输入（每百万令牌） | 输出（每百万令牌） | 需要注意的事项？                |
| --------------------- | -------------- | --------------- | ------------------------------- |
| Claude Opus 4 / 4.5   | **15.00 美元**     | **75.00 美元**      | ⚠️ 一次深度对话费用超过 20 美元         |
| Claude Sonnet 4 / 3.5 | 3.00 美元          | 15.00 美元          | 性价比最高的模型                |
| Claude Haiku 3.5      | 0.80 美元          | 4.00 美元          | 适用于后台任务                |
| Gemini 3 Pro          | 1.25 美元          | 5.00 美元          | 优秀的备用模型                |
| Gemini 2 Flash        | 0.10 美元          | 0.40 美元          | 几乎免费的使用体验               |

## 安装方法

Tinker 是一个 **集成在 OpenClaw 中的插件**，位于 [globalcaos 分支](https://github.com/globalcaos/tinkerclaw) 中。它随 OpenClaw 的构建过程一起提供。

```bash
# Clone the fork
git clone https://github.com/globalcaos/tinkerclaw.git openclaw
cd openclaw

# Build (includes Tinker UI)
pnpm install
pnpm build

# Access
# Production: http://localhost:18789/tinker/
# Development: cd tinker-ui && pnpm dev → http://localhost:18790/tinker/
```

## 架构说明

```
tinker-ui/                ← Standalone Vite + Lit app (zero upstream conflicts)
├── src/
│   ├── app.ts            ← Main shell: sidebar + panels + WebSocket client
│   └── panels/
│       ├── context-treemap.ts    ← What fills your context window
│       ├── response-treemap.ts   ← What each response costs
│       └── context-timeline.ts   ← Context usage over time
├── index.html
└── vite.config.ts

extensions/tinker/        ← OpenClaw plugin (serves UI from gateway)
├── index.ts
└── openclaw.plugin.json
```

- Tinker 与上游的 `ui/` 模块 **完全独立**，因此永远不会产生合并冲突。
- 代码量约为 3,300 行，主要使用 TypeScript 编写，并结合了 Lit 组件。
- Tinker 不依赖任何外部服务，它直接通过本地网关的 WebSocket 端口（18789）与 OpenClaw 连接。

## 为什么现在需要这个工具？

Anthropic 拒绝了五角大楼的合同（这很值得尊敬）。本周末，Claude 在 App Store 的排名超过了 ChatGPT，大量用户开始转向 Claude API。不过，通过 OpenClaw 使用 Claude API 是 **免计费的**，没有每月 20 美元的费用上限。不过，Opus 的输入费用为每百万令牌 15 美元，输出费用为每百万令牌 75 美元。一次使用多个工具的会话很容易就会消耗 200,000 多个令牌。算一下成本吧！

如果你因为相信 Anthropic 的理念而选择使用 Claude API，那么你也应该清楚自己实际花费了多少钱。这并不是为了省钱，而是为了做到心中有数。Tinker 就能帮助你做到这一点。

→ **[下载 Tinker](https://github.com/globalcaos/tinkerclaw)**

---

_由 [globalcaos](https://github.com/globalcaos) 开发 · 属于 [The Tinker Zone](https://github.com/globalcaos/tinkerclaw) 项目的一部分_