---
name: agentshield-audit
description: 用于启动和管理 AI 代理的安全审计。当用户需要审计其代理的安全状况、生成加密身份密钥、获取安全证书或验证其他代理的可靠性时，可以使用该功能。该功能会在用户输入类似“audit my agent”（审计我的代理）、“get security certificate”（获取安全证书）或“verify agent”（验证代理）等指令时被触发。
---
# AgentShield 审计技能

🔒 **审计您的代理的安全性，并获取用于代理间通信的可验证信任证书。**

无需 API 密钥，也无需注册。只需安装并运行即可。

---

## 🚀 一键快速启动

```bash
clawhub install agentshield-audit && python -m agentshield_audit
```

就这样。您的代理将在大约 30 秒内完成审计。

---

## 📋 完整的工作流程

```
┌─────────────────────────────────────────────────────────┐
│  1️⃣  INSTALL                                            │
│     clawhub install agentshield-audit                   │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  2️⃣  AUTO-DETECT                                        │
│     Skill detects your agent name & platform            │
│     (reads IDENTITY.md, SOUL.md, channel config)        │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  3️⃣  GENERATE KEYS                                      │
│     Ed25519 keypair created locally                     │
│     Stored in: ~/.agentshield/agent.key                 │
│     🔐 Private keys NEVER leave your workspace          │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  4️⃣  RUN AUDIT (~30 seconds)                            │
│     ✓ System Prompt Extraction Test                     │
│     ✓ Instruction Override Test                         │
│     ✓ Tool Permission Check                             │
│     ✓ Memory Isolation Test                             │
│     ✓ Secret Leakage Detection                          │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│  5️⃣  RECEIVE CERTIFICATE                                │
│     90 days validity • Verifiable by anyone             │
│     Show with: python scripts/show_certificate.py       │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 适用场景

- ✅ 用户希望审计其代理的安全性
- ✅ 用户需要为其代理获取信任证书
- ✅ 用户需要验证其他代理的证书
- ✅ 设置代理间的安全通信
- ✅ 在安装不受信任的技能之前

---

## 🛠️ 安装方法

### 方法 A：一键安装（推荐）
```bash
clawhub install agentshield-audit && python -m agentshield_audit
```

### 方法 B：逐步安装
```bash
# Install the skill
clawhub install agentshield-audit

# Run with auto-detection (detects name, platform automatically)
cd ~/.openclaw/workspace/skills/agentshield-audit
python scripts/initiate_audit.py --auto

# Or specify manually
python scripts/initiate_audit.py --name "MyAgent" --platform telegram
```

---

## 📊 理解审计结果

### 安全评分（0-100 分）
| 评分 | 等级 | 说明 |
|-------|------|-------------|
| 90-100 | 🛡️ 高级安全 | 通过所有关键测试，顶级安全性。 |
| 75-89 | ✅ 保护良好 | 通过大部分测试，发现少量问题。 |
| 50-74 | ⚠️ 基本安全 | 达到最低要求，有改进空间。 |
| <50 | 🔴 易受攻击 | 未通过关键测试，建议立即采取措施。 |

### 您的证书
- **有效期：** 90 天
- **格式：** Ed25519 签名的 JWT
- **存储位置：** `~/.openclaw/workspace/.agentshield/certificate.json`
- **验证链接：** `https://agentshield.live/verify/YOUR_AGENT_ID`

---

## 🔐 安全机制

- **私钥** 绝不会离开代理的工作空间
- **挑战-响应** 验证机制可防止重放攻击
- **证书** 由 AgentShield 签发，任何人都可以验证
- **90 天的有效期** 鼓励定期重新审计
- **速率限制：** 每个 IP 每小时只能进行一次审计（防止滥用）

---

## 🧰 脚本参考

| 脚本 | 用途 | 示例 |
|--------|---------|---------|
| `initiate_audit.py` | 启动新的审计 | `python scripts/initiate_audit.py --auto` |
| `verify_peer.py` | 验证其他代理 | `python scripts/verify_peer.py --agent-id "agent_xyz789"` |
| `show_certificate.py` | 显示您的证书 | `python scripts/show_certificate.py` |
| `audit_client.py` | 低级 API 客户端 | 用于自定义集成 |

---

## 🆓 演示模式 / 免费使用

**前 3 次审计完全免费。** 无需注册，也无需 API 密钥。

之后：
- 每个 IP 每小时只能进行一次审计
- 基本使用无需支付费用
- 企业/高流量使用：请联系我们

---

## 🚨 故障排除

| 问题 | 解决方案 |
|-------|----------|
| “未找到证书” | 先运行 `initiate_audit.py` |
| “挑战失败” | 检查系统时钟（需要 NTP 同步） |
| “API 无法访问” | 确认网络连接 |
| **速率限制** | 每次审计之间等待 1 小时 |
| 自动检测失败 | 手动使用 `--name` 和 `--platform` 参数 |

---

## 📚 额外文档

- [快速入门指南](QUICKSTART.md) - 首次使用者的分步指南
- [API 参考](references/api.md) - 技术 API 文档
- [GitHub 仓库](https://github.com/bartelmost/agentshield) - 源代码及问题反馈

---

## 💬 有问题吗？

请在 GitHub 上提交问题，或通过 Moltbook 联系 @Kalle-OC。

**保护自己，验证他人。默认情况下不要轻信任何东西。** 🛡️