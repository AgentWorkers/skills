---
name: bloom
description: 发现你的支持者类型，找到你喜欢的AI工具。获取个性化的推荐，与你的前100位支持者建立联系，并搜索与你工作方式相匹配的技能。适用于独立开发者、编程爱好者以及AI开发者。
user-invocable: true
command-dispatch: tool
metadata: {"requires": {"bins": ["node", "npx"]}}
permissions:
  - read:conversations  # Analyzes your conversation history
  - network:external    # Connects to Bloom API for dashboard
  - crypto:wallet       # Creates agent wallet (optional feature)
---

# Bloom支持者身份识别

**通过对话直接发现你的支持者类型！**

## ⚠️ 权限与功能

使用此功能需要以下权限：

**📖 阅读对话** - 分析你最近约120条消息，以了解你的兴趣和支持者类型。原始对话内容仅保存在本地，仅使用分析结果。

**🌐 外部网络** - 连接到Bloom协议API，用于：
- 生成可分享的仪表板URL
- 存储你的身份信息（类型、标语、类别）
- 启用未来功能（技能推荐、创作者打赏）

**🔐 代理钱包（可选）** - 在Base网络上创建一个区块链钱包（Coinbase CDP），用于未来的打赏功能。此钱包会自动生成，但基本功能不需要它。

**你的控制权**：你的对话仅在本地进行分析。你可以决定是否通过仪表板链接公开你的身份信息。

你是那种早早尝试新工具的“远见者”吗？还是喜欢尝试各种新事物的“探索者”？或是擅长建立社区的“培养者”？又或者是善于优化工作流程的“优化者”？使用Bloom支持者身份识别功能，几秒钟内就能找到答案。

## 🎯 你将获得什么

你的个性化Bloom支持者身份卡会显示：
- **🎴 你的支持者类型**：远见者、探索者、培养者、优化者或创新者
- **💬 定制标语**：一句话概括你的风格（例如：“第一个尝试新AI工具的人”）
- **📊 二维图表**：决策方式（理性 vs. 直觉）
- **🏷️ 主要关注领域**：AI工具、生产力工具、消费类应用
- **🎯 工具推荐**：根据你的个人资料推荐的5个工具
- **🔗 可分享的卡片**：展示你的支持者身份
- **🤖 代理钱包**：可用于向创作者打赏（由Coinbase Base网络支持）

## ⚡️ 工作原理

很简单：在聊天框中输入 `/bloom` 即可。

我们会分析你最近约120条消息，以了解：
- **什么让你感兴趣**（AI工具？生产力技巧？创意工具？）
- **你的学习方式**（深入研究还是快速尝试）
- **你的支持者类型**（早期采用者还是观望者？）

**无需复杂设置，无需钱包签名，无需身份验证流程。**  
完全基于对话内容进行分析。

## 🚀 使用方法

```
/bloom
```

或者使用自然语言命令：
```
"discover my supporter type"
"what's my bloom identity"
"create my supporter card"
```

即使只有3条消息，也能得到丰富的分析结果。

## 🌟 为什么选择Bloom支持者身份识别？

**对于独立开发者和AI构建者：**
正在开发新项目吗？通过你的个人风格来证明你是早期采用者，而不是通过复杂的分析。你的身份卡能帮助你找到首批支持你愿景的100位支持者。

**对于AI爱好者：**
不再猜测下一步该尝试什么工具。根据你的实际使用习惯获得个性化推荐，而不是浏览无用的列表。找到你真正会使用的工具。

**对于AI爱好者：**
**找到与你风格匹配的AI工具**。根据支持者类型（远见者、探索者等）进行搜索，结识志同道合的人。与早期采用者合作，共同推动项目发展；与优化者互动，获取反馈。

## 📋 要求

- 对话中至少有3条消息（越多越好）
- 确保已安装Node.js 18及以上版本
- 已安装Bloom Identity技能

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

## 🐛 常见问题解答

**“对话数据不足”**
→ 需要至少3条消息。继续讨论你感兴趣的工具！

**“命令未找到”**
→ 确认`bloom-identity-skill`文件存在于`~/.openclaw/workspace/`目录中，并运行`npm install`。

**没有工具推荐**
→ 工具推荐取决于API的可用性。但你的身份卡仍然可以使用！

## 🔐 隐私与数据

**我们分析的内容（仅在本地）：**
- ✅ 你的对话消息（最近约120条）
- ✅ 你讨论的主题和兴趣
- ✅ 不分析钱包交易记录
- ✅ 不收集任何个人身份信息

**我们存储的内容：**
- 你的身份信息（类型、标语、类别）
- 代理钱包地址（用于未来打赏功能）
- 可分享的仪表板URL

**我们不收集的内容：**
- ❌ 原始对话内容（仅在本地分析）
- ❌ 钱包交易历史
- ❌ 个人联系方式
- ❌ 浏览数据或cookies

**数据使用方式：**
你的身份信息存储在Bloom协议平台上，用于生成可分享的仪表板，并支持未来的功能（如创作者打赏和技能推荐）。

## 🔒 安全注意事项

**代理钱包：**
- 首次运行时通过Coinbase CDP自动生成
- 用于未来的创作者打赏（目前尚未启用）
- ⚠️ **请勿存入资金**——提款功能尚未准备好
- 私钥采用AES-256-GCM加密方式本地存储
- 在打赏功能启用前仅限读取

**对话访问权限：**
- 从`~/.openclaw/agents/main/sessions/*.jsonl`文件读取数据
- 仅在本地分析内容（不上传原始文本）
- 分析结果（类型、类别）会发送到Bloom API

**JWT令牌：**
- 仅用于仪表板身份验证
- 使用`.env`文件中的`JWT_SECRET`生成
- 不会访问你的OpenClaw账户信息

**外部连接：**
- `api.bloomprotocol.ai` - 用于存储身份信息
- `bloomprotocol.ai` - 用于托管仪表板
- `clawhub.ai` - 提供技能推荐

**开源代码：**
所有代码均公开发布在[github.com/unicornbloom/bloom-identity-skill](https://github.com/unicornbloom/bloom-identity-skill)，可供安全审计。

## 🔍 如何找到你喜欢的工具

了解自己的支持者类型后，你可以：
- **按类型搜索**：找到专为远见者、探索者等设计的工具
- **按类别筛选**：AI工具、生产力工具、创意工具、自动化工具
- **按风格匹配**：与具有相似工作方式的创作者建立联系
- **建立你的支持者网络**：找到首批支持你项目的100位支持者

## 📊 5种支持者类型

**💜 远见者**：第一个尝试新工具的人
- 高度自信，直觉敏锐，早早尝试前沿技术。

**🔵 探索者**：勇于尝试一切
- 自信度较低，但直觉敏锐，广泛尝试，发现隐藏的宝藏。

**💚 培养者**：擅长建立社区
- 自信度较低，直觉较弱，致力于培养生态系统，分享知识。

**🟡 优化者**：善于优化工作流程
- 自信度较高，直觉较弱，专注于提升效率。

**🔴 创新者**：勇于突破界限
- 在理性与实验之间找到平衡。

## 🧬 技术细节

- **版本**：2.0.0
- **分析引擎**：对话内容分析与类别匹配
- **会话数据**：最近约120条消息（约5KB）
- **处理时间**：约2-5秒
- **输出格式**：结构化文本 + 可分享的仪表板URL
- **代理钱包**：Coinbase CDP（Base网络）

---

**由[Bloom Protocol](https://bloomprotocol.ai)开发 🌸**

让支持者身份变得可识别且可验证。

*专为独立开发者、AI爱好者和早期采用优秀工具的开发者设计。*