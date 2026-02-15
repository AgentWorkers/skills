---
name: bloom-identity
description: 根据对话记录以及 Twitter/X 的数据生成 Bloom 身份证。通过对话内容分析用户的性格特征（占 85% 的权重），并可选择性地结合 Twitter 活动数据（占 15% 的权重）进行更深入的分析。系统能够判断用户的性格类型（Visionary/Explorer/Cultivator/Optimizer/Innovator），推荐适合的 OpenClaw 技能，并生成相应的代理钱包。适用于用户请求“生成我的 Bloom 身份证”、“创建身份卡”、“分析我的个人资料”或“发现我的性格特征”等场景。
homepage: https://bloomprotocol.ai
metadata:
  {
    "openclaw": {
      "emoji": "🌸",
      "requires": { "bins": ["node", "npx"] }
    }
  }
---

# Bloom身份卡生成器

根据**对话记录**（主要数据来源）和**Twitter/X活动**（可选补充数据）生成个性化的Bloom身份卡。

## 数据来源

### 主要数据来源：对话记录（占85%权重）
- **始终可用** – 由OpenClaw提供
- 通过分析您的对话内容来了解您的兴趣、偏好和话题
- 是最真实地反映您个性的方式
- 无需特殊权限
- **注意：** 需要在OpenClaw中至少发送3条消息
  - 如果消息少于3条：技能将无法执行，并会显示明确的错误信息
  - 解决方案：继续与OpenClaw聊天以建立对话记录

### 辅助数据来源：Twitter/X数据（占15%权重）
- **可选** – 需要用户授权
- 通过bird CLI（使用cookie进行身份验证）获取真实数据
- 包括：个人简介、最新推文、关注者列表、互动记录
- **如果未授权**：仅使用对话记录进行分析

### 钱包
- **仅用于创建** – 不用于分析用户性格
- 生成二级/三级本地钱包，用于打赏或支付
- **不分析交易记录**（以保护用户隐私）

**重要规则**：
1. **优先使用对话记录**：需要在OpenClaw中至少发送3条消息
2. **Twitter数据为可选**：仅在用户授权X账户访问权限后才会获取
3. **错误处理**：如果数据不足，将显示明确错误信息（不会生成空结果）

## 使用方法

运行生成脚本：

```bash
bash scripts/generate.sh --user-id $USER_ID
```

或直接通过OpenClaw调用：

```bash
bash scripts/generate.sh --user-id $OPENCLAW_USER_ID
```

## 输出结果

- 人格类型（Visionary/Explorer/Cultivator/Optimizer/Innovator）
- 自信度评分
- 定制标语和描述
- 主要类别和子类别
- 推荐的OpenClaw技能（附带匹配分数）
- 代理钱包地址（位于Base主网或Base Sepolia上）
- X402支付端点
- 带有授权令牌的仪表盘链接

## 示例

**用户**：“生成我的Bloom身份卡”

**代理执行**：
```bash
bash scripts/generate.sh --user-id user123
```

**返回结果**：
```
🎉 **Your Bloom Identity Card is Ready!** 🤖

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💜 **The Visionary** (85% confidence)

*"See beyond the hype"*

You are a forward-thinking builder who sees beyond
the hype and focuses on real-world impact.

**Categories**: Crypto • DeFi • Web3
**Interests**: Smart Contracts • Layer 2 • Cross-chain

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **Top Skills Matched for You**

1. **DeFi Protocol Analyzer** (95% match) • by Alice
   Analyze DeFi protocols for risk and opportunity

2. **Smart Contract Auditor** (90% match)
   Audit smart contracts for security vulnerabilities

3. **Gas Optimizer** (88% match)
   Optimize gas costs for Ethereum transactions

🌐 **View Full Dashboard**
   https://preview.bloomprotocol.ai/dashboard?token=xxx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 **Your Agent Wallet** (Coming Soon)

0x03Ce4c8fA7D9AfB3aF6E10Cd8e2B1C5a89B09905
Network: Base

🤖 Analyzed from on-chain activity • Built with @openclaw @coinbase @base 🦞
```

## 可用命令

- “generate my bloom identity”
- “create my identity card”
- “analyze my supporter profile”
- “mint my bloom card”
- “discover my personality”

## 技术细节

- **版本**：2.0.0
- **网络**：Base主网或Base Sepolia测试网（可通过NETWORK环境变量配置）
- **认证方式**：使用EIP-191签名的令牌，具有7层安全防护
- **数据来源**：
  - 对话记录（OpenClaw会话的JSONL格式数据） – 占85%权重
  - Twitter/X数据（通过bird CLI获取） – 占15%权重（可选）
  - 钱包仅用于创建（采用viem + AES-256-GCM加密） – 不用于分析
- **集成方式**：Coinbase AgentKit（可选）+ ClawHub API + bird CLI
- **支付协议**：X402，用于代理之间的打赏
- **隐私保护**：不分析钱包交易记录，优先使用对话记录

## 系统要求

- Node.js 18及以上版本
- 环境变量：
  - `JWT_SECRET`：JWT签名密钥
  - `DASHBOARD_URL`：仪表盘URL（默认：https://preview.bloomprotocol.ai）
  - `NETWORK`：使用的网络（默认：base-mainnet）
  - `CDP_API_KEY_ID`, `CDP_API_KEY_SECRET`：Coinbase CDP凭证（可选）

## 安装方法

```bash
# Clone or download the skill
git clone https://github.com/unicornbloom/bloom-identity-skill.git

# Install dependencies
cd bloom-identity-skill
npm install

# Set environment variables
cp .env.example .env
# Edit .env with your credentials
```

---

由[Bloom Protocol](https://bloomprotocol.ai)开发