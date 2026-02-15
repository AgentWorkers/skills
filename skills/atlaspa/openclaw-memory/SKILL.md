---
name: openclaw-memory
user-invocable: true
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["node"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw 内存系统

**支持跨会话的持久化存储，并提供语义搜索和 x402 支付功能。**

## 什么是 OpenClaw 内存系统？

这是 OpenClaw 的首个功能，它为代理提供了 **持久化存储**——代理能够在所有会话中记住事实、偏好设置、模式以及对话历史，从而避免重复提及相同的内容。

## 主要特性

- 🧠 **持久化存储**：在所有会话中保存所有数据
- 🔍 **语义搜索**：根据内容含义进行搜索，而不仅仅是关键词
- 🤖 **自动学习**：自动提取事实和偏好设置
- 💾 **本地存储**：使用 SQLite 数据库进行存储，并支持向量嵌入
- 💰 **x402 支付**：代理可以按月支付费用（0.5 美元）来使用无限存储空间

## 免费版与专业版

**免费版：**
- 最多支持 100 条记忆记录
- 数据保留 7 天
- 基本的语义搜索功能

**专业版（每月 0.5 美元）：**
- 无限条记忆记录
- 数据永久保存
- 高级语义搜索功能
- 能够建立记忆记录之间的关联关系

## 安装

```bash
claw skill install openclaw-memory
```

## 命令

```bash
# Search memories
claw memory search "What does user prefer?"

# List recent memories
claw memory list --limit=10

# Show stats
claw memory stats

# Open dashboard
claw memory dashboard

# Subscribe to Pro
claw memory subscribe
```

## 工作原理

1. **自动提取关键信息**：在处理请求时自动提取重要数据
2. **生成嵌入向量**：为搜索创建语义向量
3. **本地存储**：数据存储在 SQLite 数据库中，确保隐私安全
4. **按需检索**：在处理请求前显示相关的记忆记录
5. **管理存储配额**：当达到免费版的存储限制时，系统会自动删除旧记录

## 使用场景

- 记录用户偏好和编码风格
- 保存项目背景和需求信息
- 从重复的交互中学习模式
- 在不同会话中保持对话历史记录
- 随时间积累知识库

## 代理经济模型

代理可以自主判断是否值得升级到专业版：
- **费用：**每月 0.5 美元
- **价值：**通过避免重复提及相同内容来节省代币
- **投资回报：**如果持久化存储功能每月节省的代币超过 0.5 美元，那么这个功能就具有成本效益

有关 x402 支付的详细信息，请参阅 [AGENT-PAYMENTS.md](AGENT-PAYMENTS.md)。

## 隐私保护

- 所有数据均存储在 `~/.openclaw/openclaw-memory/` 目录下
- 无需依赖外部服务器或遥测数据
- 嵌入向量可以使用本地模型（无需调用 API）
- 代码开源，可自行审核

## 仪表盘

通过 `http://localhost:9091` 访问 Web 用户界面：
- 浏览和搜索记忆记录
- 查看记忆记录的时间线
- 检查存储配额和统计信息
- 管理专业版订阅

## 未来工具的基础

该内存系统是以下功能的基础：
- **上下文优化器**：利用记忆记录来压缩对话内容
- **智能路由器**：学习对话路由模式
- **速率限制管理器**：监控使用情况

## 系统要求

- Node.js 18 及以上版本
- OpenClaw v2026.1.30 及以上版本
- 操作系统：Windows、macOS、Linux

## 链接

- [官方文档](README.md)
- [代理支付指南](AGENT-PAYMENTS.md)
- [GitHub 仓库](https://github.com/yourusername/openclaw-memory)
- [ClawHub 页面](https://clawhub.ai/skills/openclaw-memory)

---

**由 OpenClaw 社区开发** | 首个支持 x402 支付的内存系统