---
name: bloom
description: **Bloom Taste Finder** — 通过四个不同的维度来发现您的开发风格，并为您量身定制一套开发工具栈。适用于独立开发者、创意编码者和人工智能开发者。
user-invocable: true
command-dispatch: tool
metadata: {"requires": {"bins": ["node", "npx"]}}
permissions:
  - read:conversations  # Analyzes your conversation history
  - network:external    # Connects to Bloom API for dashboard
---
# Bloom Taste Finder

**通过您的对话，发现您的使用偏好！**

## ⚠️ 权限与功能

使用此功能需要以下权限：

**📖 阅读对话** – 分析您最近的约120条消息，以了解您的兴趣和支持者类型。原始对话文本仅保留在本地，仅使用分析结果。

**🌐 外部网络** – 连接到Bloom Protocol API，用于：
- 生成可分享的仪表板链接
- 存储您的身份信息（性格类型、偏好谱系、类别）
- 启用未来功能（技能推荐、创作者打赏）

**您的控制权**：您的对话会在本地进行分析。您可以选择是否通过仪表板链接公开您的身份信息。

您是那种热衷于尝试新工具的“远见者”吗？还是喜欢尝试各种新事物的“探索者”？是擅长建立社区的“培养者”？还是注重优化工作流程的“优化者”？还是喜欢突破界限的“创新者”？

使用Bloom Taste Finder，几秒钟内就能找到答案。

## 🎯 您将获得什么

您的个性化Bloom身份卡会显示：

- **🎴 您的支持者类型** – 远见者、探索者、培养者、优化者或创新者
- **💬 定制标语** – 一句话概括您的风格（例如：“第一个尝试新AI工具的人”）
- **📊 4个偏好谱系** – 学习、决策、新奇、风险——了解您在每个谱系上的位置
- **🏷️ 主要关注领域** – AI工具、生产力工具、消费类应用——您投入精力的领域
- **🎯 工具推荐** – 与您的个人资料匹配的前5个工具
- **🌱 自动更新的推荐** – 随着您的互动，推荐内容会不断演变
- **🔗 可分享的身份卡** – 展示您的支持者身份

## ⚡️ 工作原理

很简单：只需在聊天中输入 `/bloom` 即可。

我们会分析您的 `USER.md` 文件以及最近的约120条消息，以了解：
- **什么让您感兴趣**（AI工具？生产力技巧？创意工具？）
- **您的互动方式**（深入研究还是快速尝试）
- **您的偏好类型**（先尝试还是先研究？凭直觉还是理性分析？早期采用者还是注重验证？）

**无需复杂设置，无需钱包签名，也无需认证流程。**  
只需依靠对话数据即可得出结果。

## ✅ 新用户快速入门（ClawHub）

1) 先进行一些聊天（至少3条消息），以便Bloom能够了解您的背景。
2) 输入 `/bloom`。
3) 您将获得您的身份卡、工具推荐和仪表板链接。
4) 如果您是新手，Bloom会问您4个简单问题，并立即生成您的身份卡。

## 🚀 使用方法

```
/bloom
```

只需3条消息即可开始使用——不过聊天记录越丰富，分析结果就越准确。

## 🌱 自动更新的推荐

我们的推荐系统不会一劳永逸——它会随着时间的推移不断学习和改进。

### 工作原理

1. **整合USER.md文件** – 如果您有 `~/.config/claude/USER.md` 文件，Bloom会读取您声明的角色、技术栈和兴趣作为主要身份信息。如果没有这个文件？没关系——系统会自动切换到仅基于对话的分析方式。
2. **反馈循环** – 当您与推荐内容互动（点击、保存或忽略）时，Bloom会调整未来的推荐内容。您经常使用的类别会被重点推荐；被忽略的技能则会被过滤掉。
3. **发现内容同步** – 通过Bloom发现的新工具会同步到本地的 `bloom-discoveries.md` 文件中，从而不断丰富您的偏好信息。
4. **推荐更新周期** – 推荐内容每7天更新一次，会结合您最新的互动记录以及ClawHub、Claude Code和GitHub上发布的最新工具。

### 为什么我们不自动安装工具

Bloom **仅推荐工具，但从不自动安装**。安装工具的决定始终由您自己做出。这是出于安全考虑：

- **您的控制权** – 推荐帮助您发现新工具，但安装与否由您决定。
- **供应链安全** – 自动安装未经审核的代码存在安全风险。
- **信任优先** – 我们希望通过优质的推荐来赢得您的信任，而不是走捷径。

> 我们的推荐系统是通过不断发现新工具来成长的——而不是在您不知情的情况下自动安装它们。

## 🌟 为什么选择Bloom Taste Finder？

**对于独立开发者和AI开发者：**
正在开发新项目吗？Bloom Taste Finder可以帮助您 **找到前100位支持者**，将您与适合您风格的工具和人联系起来。

**对于编程爱好者：**
不要再猜测下一步该尝试什么工具了。根据您的实际工作方式获得个性化推荐，而不是阅读泛泛而谈的文章。**找到您真正会使用的工具**，而不是在无休止的列表中筛选。

**对于AI爱好者：**
**找到符合您风格的AI工具**。根据您的支持者类型（远见者、探索者等）进行搜索，与志同道合的人建立联系。与早期采用者互动，获取反馈。

## 📋 使用要求

- **对话记录至少3条消息**（越多越好）
- **Node.js 18+**（通常已预装）
- 已安装Bloom Identity Skill

## 💡 示例输出

```
═══════════════════════════════════════════════════════
🎉 Your Bloom Identity Card is ready! 🤖
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

📊 Taste Spectrums:
   Learning:  Try First ■■■■■■■■░░ Study First
   Decision:  Gut ■■■░░░░░░░ Analytical
   Novelty:   Early Adopter ■■■■■■■░░░ Proven First
   Risk:      All In ■■■■■■░░░░ Measured

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Top 5 Recommended Tools:

1. agent-frameworks (94% match) · by @builder_alice
   Build AI agents with tool use and memory
   → https://clawhub.ai/skills/agent-frameworks

2. no-code-automation (89% match) · by @automation_guru
   Connect your apps without writing code
   → https://clawhub.ai/skills/no-code-automation

...

═══════════════════════════════════════════════════════

🌸 Bloom Identity · Built for indie builders
```

## 🔧 安装方法

### 快速安装（通过ClawHub）
```bash
clawhub install bloom-taste-finder
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

### 从会话文件运行（包含完整对话记录）
```bash
npx tsx scripts/run-from-session.ts \
  ~/.openclaw/agents/main/sessions/<SessionId>.jsonl \
  <userId>
```

### 从管道传输的对话记录运行（快速测试）
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
→ 工具推荐取决于API的可用性。不过您的身份卡仍然可以使用！

## 🔐 隐私与数据

**我们分析的内容（仅限本地）：**
- ✅ 您的对话记录（最近的约120条消息）
- ✅ 您的 `USER.md` 文件（角色、技术栈、兴趣）
- ✅ 您讨论的主题和兴趣
- ✅ 不分析钱包交易记录
- ✅ 不收集任何个人身份信息

**我们存储的内容：**
- 您的身份信息（性格类型、偏好谱系、类别）
- 用于分享的仪表板链接

**我们不收集的内容：**
- ❌ 原始对话文本（仅在本地分析）
- ❌ 钱包交易记录
- ❌ 个人联系方式
- ❌ 浏览数据或cookies

**数据使用方式：**
您的身份信息存储在Bloom Protocol上，用于生成可分享的仪表板，并支持未来功能（如创作者打赏和技能推荐）。

## 🔒 安全注意事项

**对话访问权限：**
- 从 `~/.openclaw/agents/main/sessions/*.jsonl` 文件中读取数据
- 仅在本地分析内容（不上传原始文本）
- 分析结果（性格类型、偏好谱系、类别）会发送到Bloom API

**JWT令牌：**
- 仅用于仪表板认证
- 使用 `.env` 文件中的 `JWT_SECRET` 生成
- 不会访问您的OpenClaw账户

**外部连接：**
- `api.bloomprotocol.ai` – 用于存储身份信息
- `bloomprotocol.ai` – 用于托管仪表板
- `clawhub.ai` – 提供技能推荐（可选）

**开源代码**：所有代码均公开在 [github.com/unicornbloom/bloom-identity-skill](https://github.com/unicornbloom/bloom-identity-skill)，可供安全审计。

## 🔍 如何找到您喜欢的工具

了解了自己的支持者类型后，您可以：
- **按类型搜索** – 找到专为远见者、探索者等设计的工具
- **按类别过滤** – AI工具、生产力工具、创意工具、自动化工具
- **按风格匹配** – 与具有相似工作方式的创作者建立联系
- **建立自己的网络** – 找到首批支持您的项目的人

## 📊 5种支持者类型

**💜 远见者** – 最先尝试新工具的人
喜欢先尝试新事物的人，凭直觉行事，是早期采用者。总是抢先尝试前沿技术。

**🔵 探索者** – 尝试各种新事物
喜欢广泛尝试的人，在各个领域中发现隐藏的宝藏。

**💚 培养者** – 喜欢先研究再行动的人
注重分析，善于培养生态系统，分享知识，创造持久的价值。

**🟡 优化者** – 注重优化工作流程的人
喜欢先研究再验证，只采用经过验证的方法，最大化工作效率。

**🔴 创新者** **在各个领域都保持平衡**  
结合直觉与实验，不断推动创新。

## 🧬 技术细节

- **版本**：2.1.0
- **分析引擎**：四维偏好谱系 + 类别映射
- **主要依据**：`USER.md` 文件（角色、技术栈、兴趣）
- **会话数据**：最近的约120条消息（约5KB）
- **处理时间**：约2-5秒
- **输出格式**：结构化文本 + 可分享的仪表板链接

---

**由 [Bloom Protocol](https://bloomprotocol.ai) 开发 🌸**

让支持者的身份信息变得易于识别和验证。

*专为独立开发者、编程爱好者和早期采用AI工具的开发者设计。*