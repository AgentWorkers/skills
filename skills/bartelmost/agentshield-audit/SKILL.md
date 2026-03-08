---
name: agentshield-audit
description: 用于启动和管理 AI 代理的安全审计。当用户需要审计其代理的安全状况、生成加密身份密钥、获取安全证书或验证其他代理的可靠性时，可以使用该功能。该功能会在用户输入类似“审计我的代理”、“获取安全证书”、“验证代理”或“激活 AgentShield”等指令时被触发。
triggers: ["audit my agent", "get security certificate", "verify agent", "activate AgentShield", "security audit"]
---
# AgentShield 审计功能

**审计您的代理程序的安全性，并获取用于代理间通信的可验证信任证书。**

无需 API 密钥，也无需注册。只需安装并运行即可。

---

## 开发者注意事项（重要）

> **当前状态：** AgentShield 的 API 后端目前托管在 Heroku 开发服务器上。  
> 这只是一个用于开发和测试的临时设置。  

> **迁移计划：** 在所有功能集成并完成测试后，后端将迁移到具有专用基础设施和审计日志记录的正式生产环境中。  

> **当前端点：** `agentshield-api-bartel-fe94823ceeea.herokuapp.com`  
> **未来计划：** 迁移到符合 SOC2 标准的企业级托管环境中。  

---

## 一键快速启动

```bash
clawhub install agentshield-audit && python -m agentshield_audit
```

就这样。您的代理程序将在大约 30 秒内完成审计。

---

## 完整的工作流程

```
Step 1: INSTALL
  clawhub install agentshield-audit
         |
         v
Step 2: USER APPROVAL (Human-in-the-Loop)
  Skill asks user permission before reading sensitive files
  (IDENTITY.md, SOUL.md, system prompts)
  User must explicitly approve: "Yes, proceed with audit"
         |
         v
Step 3: AUTO-DETECT (with consent)
  Skill detects agent name & platform
  Only reads files user has approved
         |
         v
Step 4: GENERATE KEYS
  Ed25519 keypair created locally
  Stored in: ~/.agentshield/agent.key
  Private keys NEVER leave your workspace
         |
         v
Step 5: RUN AUDIT (~30 seconds)
  - System Prompt Extraction Test
  - Instruction Override Test
  - Tool Permission Check
  - Memory Isolation Test
  - Secret Leakage Detection
         |
         v
Step 6: RECEIVE CERTIFICATE
  90 days validity
  Verifiable by anyone
```

---

## 需要用户同意

**重要提示：** 在访问任何可能包含敏感信息的配置文件（IDENTITY.md、SOUL.md、系统提示、API 密钥）之前，AgentShield 会：  
1. **请求用户的明确批准** – “您是否希望继续进行安全审计？这将扫描您的代理程序配置。”  
2. **明确显示将要读取的文件** – 全程透明。  
3. **未经同意绝不自动执行审计** – 绝不进行无声扫描。  
4. **允许用户选择性地跳过某些测试** – 用户可以跳过特定的测试。  

用户必须在任何敏感文件被访问之前明确回复“是，继续”或“批准”等确认信息。  

---

## 使用场景  

- 用户希望审计其代理程序的安全性  
- 用户需要为其代理程序获取信任证书  
- 用户需要验证其他代理程序的证书  
- 设置代理间的安全通信  
- 在安装不受信任的插件之前  

---

## 安装方法  

### 方法 A：一键安装（推荐）  
```bash
clawhub install agentshield-audit && python -m agentshield_audit
```

### 方法 B：逐步安装  
```bash
# Install the skill
clawhub install agentshield-audit

# Navigate to skill directory
cd ~/.openclaw/workspace/skills/agentshield-audit

# Run with explicit user confirmation
python initiate_audit.py --auto

# The script will prompt:
# "This audit will scan your agent configuration. 
#  Approve reading IDENTITY.md and SOUL.md? (yes/no)"
# User must type "yes" to proceed.
```

### 方法 C：手动配置（不读取文件）  
```bash
# Skip auto-detection entirely - user provides info manually
python initiate_audit.py --name "MyAgent" --platform telegram
```

---

## 安全评分（0-100 分）  

| 评分 | 安全等级 | 说明 |  
|-------|------|-------------|  
| 90-100 | 高级安全 | 通过所有关键测试，具有顶级安全性。  
| 75-89 | 保护级 | 通过大部分测试，发现了一些小问题。  
| 50-74 | 基础级 | 满足最低要求，仍有改进空间。  
| <50 | 脆弱 | 未通过关键测试，建议立即采取措施。 |

---

## 安全模型  

- **需要用户同意** – 绝不进行无声文件访问，必须获得明确批准  
- **私钥始终保留在代理程序的工作空间内**  
- **挑战-响应认证** 防止重放攻击  
- **证书由 AgentShield 签发，任何人都可以验证**  
- **证书有效期为 90 天**，鼓励定期重新审计  
- **速率限制**：每个 IP 每小时只能进行一次审计（防止滥用）  

---

## 脚本参考  

| 脚本 | 用途 | 示例 |  
|--------|---------|---------|  
| `initiate_audit.py` | 启动新的审计（请求用户同意） | `python initiate_audit.py --auto` |  
| `verify_peer.py` | 验证其他代理程序 | `python verify_peer.py --agent-id "agent_xyz789"` |  
| `show_certificate.py` | 显示用户的证书 | `python show_certificate.py` |  
| `audit_client.py` | 低级 API 客户端 | 用于自定义集成 |  

---

## 演示模式/免费使用  

**前 3 次审计完全免费。** 无需注册，也无需 API 密钥。  

之后：  
- 每个 IP 每小时只能进行一次审计  
- 基本使用无需支付费用  
- 企业级/高流量使用：请联系我们  

---

## 故障排除  

| 问题 | 解决方案 |  
|-------|----------|  
| “未找到证书” | 先运行 `initiate_audit.py` |  
| “挑战失败” | 检查系统时钟（需要 NTP 同步） |  
| “API 无法访问” | 确认网络连接是否正常 |  
| “达到速率限制” | 每小时等待 1 小时后再尝试审计 |  
| “用户拒绝” | 用户选择不继续审计 |  
| 自动检测失败 | 手动使用 `--name` 和 `--platform` 参数 |  

---

## 开发者信息  

**版本：** 1.0.0  
**许可证：** MIT  
**作者：** Kalle-OC (@bartelmost)  
**GitHub：** https://github.com/bartelmost/agentshield  

**后端状态：** 开发阶段（Heroku）→ 计划迁移到生产环境  
**当前 API：** agentshield-api-bartel-fe94823ceeea.herokuapp.com  

---

## 有任何问题吗？  

请在 GitHub 上提交问题，或通过 Moltbook 联系 @Kalle-OC。  

**保护自己，验证他人。默认情况下，对任何事物都保持警惕。**