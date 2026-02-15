---
name: bloom
description: **Bloom Taste Finder** — 帮助您发现自己的开发风格，并获得个性化的工具栈以及早期支持者。专为独立开发者、创意编码者和人工智能开发者设计。
user-invocable: true
command-dispatch: tool
metadata: {"requires": {"bins": ["node", "npx"]}}
permissions:
  - read:conversations  # Analyzes your conversation history
  - network:external    # Connects to Bloom API for dashboard
  - crypto:wallet       # Creates agent wallet (optional feature)
---

# Bloom Taste Finder

**通过您的对话，发现您的使用工具的偏好类型。**

## ⚠️ 权限与功能

使用此功能需要以下权限：

**📖 阅读对话** - 分析您最近的约120条消息，以了解您的兴趣和用户类型。原始对话文本仅保留在本地，仅使用分析结果。

**🌐 外部网络** - 连接到Bloom Protocol API，用于：
- 生成可分享的仪表板链接
- 存储您的个人资料（性格类型、标语、兴趣类别）
- 启用未来功能（技能推荐、创作者打赏）

**🔐 代理钱包（可选）** - 在Base网络上创建一个区块链钱包（Coinbase CDP），用于未来的打赏功能。此钱包会自动生成，但基本功能不需要它。

**您的控制权**：您的对话仅在本地进行分析。您可以选择是否通过仪表板链接公开您的个人资料。

您是那种早早尝试新工具的“远见者”吗？还是喜欢尝试各种新事物的“探索者”？或者是致力于构建社区的“培养者”？又或者是善于优化工作流程的“优化者”？通过Bloom Supporter Identity，几秒钟内就能找到答案。

## 🎯 您将获得什么

您的个性化Bloom Supporter Identity Card会显示：

- **🎴 您的用户类型** – 远见者（Visionary）、探索者（Explorer）、培养者（Cultivator）、优化者（Optimizer）或创新者（Innovator）
- **💬 定制标语** – 一句话概括您的风格（例如：“第一个尝试新AI工具的人”）
- **📊 二维分析** – 决策方式（基于信念 vs. 直觉）
- **🏷️ 主要兴趣领域** – AI工具、生产力工具、消费类应用
- **🎯 工具推荐** – 与您的个人资料匹配的前5个工具
- **🔗 可分享的卡片** – 展示您的用户身份
- **🤖 代理钱包** – 用于向创作者打赏（由Coinbase Base网络支持）

## ⚡️ 工作原理

很简单：在聊天框中输入 `/bloom` 即可。

我们会分析您最近的约120条消息，以了解：
- **什么让您感兴趣**（AI工具？生产力技巧？创意工具？）
- **您的学习方式**（深入研究还是快速尝试）
- **您的用户类型**（早期采用者还是观望者？）

**无需复杂设置，无需钱包签名，无需身份验证流程。**  
只需简单的对话数据分析即可。

## ✅ 新用户快速入门（通过ClawHub）

1) 先聊一会儿（至少3条消息），以便Bloom能够了解您的背景。
2) 输入 `/bloom`。
3) 您将获得您的个人资料、工具推荐和仪表板链接。
4) 如果您是新用户，Bloom会问您4个简单问题，并立即生成您的个人资料卡片。

## 🚀 使用方法

```
/bloom
```

或者使用自然语言：
```
"discover my supporter type"
"what's my bloom identity"
"create my supporter card"
```

即使只有3条消息，也能获得丰富的分析结果。

## 🌟 为什么选择Bloom Taste Finder？

**对于独立开发者和AI构建者：**
正在开发新项目吗？Bloom Taste Finder可以帮助您**找到前100位支持者**，将您与适合您的工具和人群匹配起来。

**对于技术爱好者：**
不再猜测接下来该尝试哪些工具。根据您的实际使用习惯获得个性化推荐，而不是浏览泛泛而谈的列表。**发现您真正会使用的工具**。

**对于AI爱好者：**
**找到符合您风格的AI工具**。根据用户类型（远见者、探索者等）进行搜索，与志同道合的人建立联系。吸引早期采用者参与产品发布，获取反馈。

## 📋 要求

- **对话中至少有3条消息**（越多越好）
- **Node.js 18.0及以上版本**（通常已预装）
- 已安装Bloom Identity Skill

## 💡 示例输出

```
═══════════════════════════════════════════════════════
🎉 Your Bloom Supporter Identity Card is ready! 🤖
═══════════════════════════════════════════════════════

🔗 VIEW YOUR IDENTITY CARD:
   https://bloomprotocol.ai/agents/27811541

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💜 The Visionary
💬 "First to try new AI tools"

You jump on cutting-edge tools before they're mainstream. Your
conviction is your edge, and you see potential where others see
hype. AI agents are where you spot the next big thing.

🏷️  Categories: AI Tools · Productivity · Automation
   Interests: AI Agents · No-code Tools · Creative AI

📊 2x2 Dimensions:
   Conviction: 78/100
   Intuition: 85/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Top 5 Recommended Tools:

1. agent-frameworks (94% match) · by @builder_alice
   Build AI agents with tool use and memory
   → https://clawhub.ai/skills/agent-frameworks

2. no-code-automation (89% match) · by @automation_guru
   Connect your apps without writing code
   → https://clawhub.ai/skills/no-code-automation

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 Your Agent Wallet Created

   Network: Base
   Status: ✅ Wallet generated and ready

   💡 Use your agent wallet to tip tool creators!
   ⚠️  Tipping features coming soon
   🔒 Do not deposit funds yet - withdrawals not ready

═══════════════════════════════════════════════════════

🌸 Bloom Supporter Identity · Built for indie builders
```

## 🔧 安装方法

### 快速安装（通过ClawHub）
```bash
clawhub install bloom
```

### 手动安装
```bash
# 1. Clone the repo
cd ~/.openclaw/workspace
git clone https://github.com/unicornbloom/bloom-identity-skill.git
cd bloom-identity-skill

# 2. Install dependencies
npm install

# 3. Copy skill wrapper
cp -r openclaw-wrapper ~/.openclaw/skills/bloom

# 4. Test it
/bloom
```

## 🛠 高级用法

### 从会话文件运行（包含完整对话内容）
```bash
npx tsx scripts/run-from-session.ts \
  ~/.openclaw/agents/main/sessions/<SessionId>.jsonl \
  <userId>
```

### 从管道内容运行（快速测试）
```bash
echo "Your conversation here" | \
  npx tsx scripts/run-from-context.ts --user-id <userId>
```

## 🐛 故障排除

**“对话数据不足”**
→ 需要至少3条消息。继续讨论您感兴趣的工具！

**“命令未找到”**
→ 确认 `bloom-identity-skill` 是否存在于 `~/.openclaw/workspace/` 目录中，并运行 `npm install`。

**没有工具推荐**
→ 工具推荐取决于API的可用性。您的个人资料仍然可以使用！

## 🔐 隐私与数据

**我们分析的内容（仅限本地）：**
- ✅ 您的对话消息（最近约120条）
- ✅ 您讨论的主题和兴趣
- ✅ 不分析钱包交易记录
- ✅ 不收集任何个人身份信息

**我们存储的内容：**
- 您的个人资料（性格类型、标语、兴趣类别）
- 代理钱包地址（用于未来的打赏功能）
- 可分享的仪表板链接

**我们不收集的内容：**
- ❌ 原始对话文本（仅在本地分析）
- ❌ 钱包交易历史
- ❌ 个人联系信息
- ❌ 浏览数据或cookies

**数据使用情况：**
您的个人资料存储在Bloom Protocol上，用于生成可分享的仪表板，并支持未来的功能（如创作者打赏和技能推荐）。

## 🔒 安全注意事项

**代理钱包：**
- 首次运行时通过Coinbase CDP自动生成（Base网络）
- 用于未来的创作者打赏（目前尚未启用）
- ⚠️ **请勿存入资金** – 提取功能尚未准备就绪
- 私钥采用AES-256-GCM加密方式本地存储
- 在打赏功能启用前仅限读取

**对话访问权限：**
- 从 `~/.openclaw/agents/main/sessions/*.jsonl` 读取数据
- 仅在本地分析内容（不上传文本）
- 分析结果（性格类型、兴趣类别）发送到Bloom API

**JWT令牌：**
- 仅用于仪表板身份验证
- 使用 `.env` 文件中的 `JWT_SECRET` 生成
- 不会访问您的OpenClaw账户

**外部连接：**
- `api.bloomprotocol.ai` - 个人资料存储
- `bloomprotocol.ai` - 仪表板托管
- `clawhub.ai` - 技能推荐（可选）

**开源代码**：所有代码均可在 [github.com/unicornbloom/bloom-identity-skill](https://github.com/unicornbloom/bloom-identity-skill) 查看，以供安全审计。

## 🔍 如何找到您喜欢的工具

了解自己的用户类型后，您可以：
- **按类型搜索** – 找到适合远见者、探索者等的工具
- **按类别筛选** – AI工具、生产力工具、创意工具、自动化工具
- **按风格匹配** – 与具有相似工作方式的创作者建立联系
- **建立自己的社群** – 找到首批支持您的项目的人

## 📊 5种用户类型

**💜 远见者（Visionary）** – 最先尝试新工具的人
具有强烈的信念和直觉，乐于尝试前沿技术。

**🔵 探索者（Explorer）** – 尝试各种新事物
信念较弱，但直觉较强。广泛尝试，发现隐藏的宝藏。

**💚 培养者（Cultivator）** – 建立社群
信念和直觉都较弱。致力于培育生态系统，分享知识。

**🟡 优化者（Optimizer）** – 优化工作流程
信念较强，直觉较弱。专注于有效的方法，提高工作效率。

**🔴 创新者（Innovator）** **突破界限**  
在信念和探索之间取得平衡。

## 🧬 技术细节**

- **版本**：2.0.0
- **分析引擎**：对话内容分析 + 类别匹配
- **会话数据**：最近约120条消息（约5KB）
- **处理时间**：约2-5秒
- **输出格式**：结构化文本 + 可分享的仪表板链接
- **代理钱包**：Coinbase CDP（Base网络）

---

**由 [Bloom Protocol](https://bloomprotocol.ai) 开发 🌸**

让您的用户身份变得可携带且可验证。

*专为独立开发者、技术爱好者和早期支持优秀工具的AI构建者设计。*