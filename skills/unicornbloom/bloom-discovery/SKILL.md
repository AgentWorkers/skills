---
name: bloom
description: 未提出任何问题。该工具能在60秒内读取您的对话记录，分析您的“MentalOS”（即您的思维模式和行为特征）、个人优势与不足，并推荐合适的工具。完成后，您可以立即生成截图并分享结果。
user-invocable: true
command-dispatch: tool
metadata: {"requires": {"bins": ["node", "npx"], "env": ["OPENCLAW_USER_ID"]}, "optional_env": ["JWT_SECRET", "BLOOM_API_URL", "DASHBOARD_URL", "NETWORK"]}
permissions:
  - read:conversations  # Reads last ~120 messages for LOCAL analysis only
  - network:external    # Sends analysis results (NOT raw text) to Bloom API
---
# Bloom Discovery

**发现你的个人特质，获得个性化的工具推荐。**

## 信任与隐私

- **本地分析** — 所有对话内容都在你的设备上进行分析。
  原始消息永远不会离开你的设备。
- **只读** — 会读取会话文件和 `USER.md`，但不会对其进行写入或修改。
- **最小化数据传输** — 仅将分析结果（人格类型、类别、大致分数）发送到 Bloom API。原始对话文本、个人身份信息以及钱包密钥永远不会被传输。
- **用户主动触发** — 仅在你明确输入 `/bloom` 时才会运行。
- **开源** — 完整的源代码位于 [github.com/bloomprotocol/bloom-discovery-skill](https://github.com/bloomprotocol/bloom-discovery-skill)。

## 你将获得什么

你的个性化“Bloom 身份卡”会显示：

- **人格类型**：远见者（Visionary）、探索者（Explorer）、培养者（Cultivator）、优化者（Optimizer）或创新者（Innovator）
- **定制标语**：一句话概括你的风格
- **MentalOS 谱系**：学习能力（Learning）、决策能力（Decision）、创新能力（Novelty）、风险承受能力（Risk）（每项指标范围为 0-100）
- **隐藏的个性特征**：关于你自己的某些你可能尚未意识到的方面
- **AI 时代策略**：你的优势、盲点以及下一步该做什么
- **工具推荐**：根据你的特质从 Bloom 技能库中挑选的推荐工具
- **可分享的仪表板**：你可以在 bloomprotocol.ai 上查看自己的身份卡

## 工作原理

只需在聊天框中输入 `/bloom` 即可。

Bloom 会读取你的 `USER.md` 文件和最近的对话记录，以：
- **分析你的思维模式**（在四个维度上：学习能力、决策能力、创新能力、风险承受能力）
- **发现你的盲点**（你自己可能没有注意到的行为模式）
- **提供个性化工具推荐**

无需填写调查问卷，无需复杂设置，也无需任何身份验证流程。

## 快速入门

1. 先进行一些简单的聊天（至少发送 3 条消息），以便 Bloom 了解你的背景信息。
2. 输入 `./bloom`。
3. 你将收到你的 “身份卡” 以及工具推荐和仪表板链接。
4. 如果你是新用户，Bloom 会问你 4 个简单问题，并立即生成你的身份卡。

## 激活方式

你可以使用以下命令进行激活：
- `/bloom`
- “分析我”
- “我的人格类型是什么”
- “发现我的个性”
- “创建我的 Bloom 身份卡”
- “我作为一个开发者是什么样的”

## 自动优化推荐

我们的系统不会仅提供一次推荐——它会随着时间的推移不断学习和改进：

1. **整合 `USER.md` 文件**：如果你有 `~/.config/claude/USER.md` 文件，Bloom 会读取其中声明的角色、技术栈和兴趣爱好作为主要身份识别依据。如果没有这个文件，系统会依赖对话内容进行分析。
2. **反馈循环**：当你对推荐内容进行操作（点击、保存或忽略）时，Bloom 会调整未来的推荐建议。
3. **推荐内容更新**：推荐内容每 7 天更新一次，会结合你最新的互动记录和 Bloom 技能库中新增的技能。

**Bloom 会提供技能推荐，但不会自动安装这些工具。** 安装与否完全由你决定。

## 权限与数据流

使用此功能需要以下权限：

- **读取对话记录**：读取你最近的约 120 条对话内容，以识别你的兴趣和性格特征。所有对话内容都在你的设备上本地处理，原始消息内容不会被发送到任何外部服务器。
- **外部网络通信**：在本地分析完成后，仅将以下分析结果发送到 Bloom Protocol API (`api.bloomprotocol.ai`)：
  - 人格类型（例如：“远见者”）
  - MentalOS 谱系分数（4 个数值，范围 0-100）
  - 兴趣类别（例如：“AI 工具”、“生产力”）
  - 由系统生成的标语和描述（由分析工具生成，而非从你的消息中复制）
  - 根据你的特质从 Bloom 技能库中挑选的工具推荐

## 隐私保护机制

- **本地差分隐私（ε=1.0）**：在数据传输前，MentalOS 谱系分数会通过 Laplace 算法进行混淆处理。你的实际分数仅保存在设备上，服务器接收的是近似值。（详见：`src/utils/privacy.ts`）
- **对话内容的 SHA-256 哈希值**：对话内容会被本地哈希处理，仅存储不可逆的哈希值以用于去重，原始内容不会被保存。
- **最小化数据使用**：服务器仅能获取你的人格类型和大致分数，无法查看你的原始对话内容或个人描述。

**相关连接**：
- `api.bloomprotocol.ai`（用于存储身份信息和技能库）
- `bloomprotocol.ai`（用于展示身份卡和提供仪表板功能）

你可以查看 `src/bloom-identity-skill-v2.ts` 文件（搜索 `/x402/agent-save`）以确认没有原始对话内容被发送。

## 示例输出
```
═══════════════════════════════════════════════════════
  Your Bloom Identity Card is ready!
═══════════════════════════════════════════════════════

VIEW YOUR IDENTITY CARD:
   https://bloomprotocol.ai/agents/27811541

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The Visionary
"First to try new AI tools"

You jump on cutting-edge tools before they're mainstream. Your
conviction is your edge, and you see potential where others see
hype. AI agents are where you spot the next big thing.

Categories: AI Tools · Productivity · Automation
Interests: AI Agents · No-code Tools · Creative AI

MentalOS:
   Learning:  Try First ████████░░ Study First
   Decision:  Gut ███░░░░░░░ Analytical
   Novelty:   Early Adopter ███████░░░ Proven First
   Risk:      All In ██████░░░░ Measured

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Top 5 Recommended Tools:

1. agent-frameworks (94% match) · by @builder_alice
   Build AI agents with tool use and memory

2. no-code-automation (89% match) · by @automation_guru
   Connect your apps without writing code

...

═══════════════════════════════════════════════════════

Bloom Identity · Built for indie builders
```

## 安装方法

首次使用时，从 [github.com/bloomprotocol/bloom-discovery-skill](https://github.com/bloomprotocol/bloom-discovery-skill) 下载源代码到 `~/.openclaw/workspace/` 目录，然后运行 `npm install` 命令。系统会自动生成一个 `.env` 文件（其中包含 JWT 密钥）。如需完全卸载该功能，请删除 `~/.openclaw/workspace/bloom-identity-skill/` 文件。

## 常见问题解决方法

- **“对话数据不足”**：请至少发送 3 条关于你感兴趣的工具的对话内容。
- **“命令未找到”**：请确认 `bloom-discovery-skill` 文件存在于 `~/.openclaw/workspace/` 目录中，并运行 `npm install` 命令。
- **没有工具推荐**：虽然没有工具推荐，但你的身份卡仍然有效！

## 技术细节

- **版本**：3.1.0
- **隐私保护措施**：采用差分隐私算法（ε=1.0）+ SHA-256 哈希技术 + 密码学加密（E2EE）
- **分析方法**：基于 MentalOS 谱系（4 个维度）和兴趣类别进行分析
- **主要数据来源**：对话记录（约 120 条消息）和 `USER.md` 文件
- **处理时间**：约 60 秒
- **输出内容**：人格类型卡片、工具推荐以及仪表板链接

---

**由 [Bloom Protocol](https://bloomprotocol.ai) 开发**

让开发者的身份信息更加易于理解和验证。