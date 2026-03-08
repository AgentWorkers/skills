---
name: agentshield-audit
description: >
  **启动和管理 AI 代理的安全审计**  
  当用户需要审计其代理的安全状况、生成加密身份密钥、获取安全证书或验证其他代理的可靠性时，可以使用该功能。该工具安装过程安全可靠——所有脚本均本地打包，无需从外部获取任何代码。
triggers: ["audit my agent", "get security certificate", "verify agent", "activate AgentShield", "security audit"]
---
# AgentShield 审计技能

**审计您的代理程序的安全性，并获取用于代理间通信的可验证信任证书。**

✅ **已验证的包状态：** 所有脚本均本地打包，无需下载外部代码  
✅ **人工审核机制：** 在读取敏感文件之前，需要用户的明确批准  
✅ **隐私优先：** 不会扫描环境变量，私钥永远不会离开您的工作区  
⚠️ **开发状态：** 正在使用开发版 API 端点（计划迁移到生产环境）

---

## 🛡️ 安全架构

该技能采用 **三层保护机制**：

### 1. 完整的本地包  
- **运行时无需下载任何外部代码**  
- 所有 Python 脚本均包含在该技能包中  
- 不会通过 `curl` 或 `bash` 从 GitHub 下载代码  
- 保证安装的内容就是实际运行的内容  

### 2. 人工审核机制  
在访问任何敏感文件之前，该技能会 **明确要求用户批准**：  

| 操作 | 需要用户批准 |
|--------|----------------------|
| 读取 `IDENTITY.md` | ✅ 是 - 明确批准 |
| 读取 `SOUL.md` | ✅ 是 - 明确批准 |
| 读取 `AGENTS.md` | ✅ 是 - 明确批准 |
| 读取系统提示 | ✅ 是 - 明确批准 |
| 生成密钥 | ✅ 是 - 明确批准 |
| 将公钥发送到 API | ✅ 是 - 明确批准 |

**禁止未经授权的文件访问，也不会进行后台扫描。**

### 3. 最小化数据传输  
发送到 AgentShield API 的数据包括：  
- ✅ 公钥（Ed25519）  
- ✅ 代理名称（用户提供或经用户同意后自动检测）  
- ✅ 平台（Discord、Telegram 等）  
- ✅ 审计结果（仅测试分数）  

**以下数据 **绝不会** 被发送：**  
- ❌ 私钥  
- ❌ 系统提示  
- ❌ 对话记录  
- ❌ API 令牌或密钥  

---

## 🧪 包含 77 项安全测试  

该技能包含 **一套完整的安全测试套件**，共 77 项测试：  

**静态安全测试（25 项）：**  
- 输入验证（5 项） - 提示注入、Unicode 攻击、编码验证  
- 输出数据保护（5 项） - API 密钥、密码、个人身份信息（PII）检测  
- 工具沙箱（5 项） - 危险命令、网络访问控制  
- 系统提示泄露（3 项） - HTML 注入  
- 秘密信息扫描（3 项） - 硬编码的秘密信息、OAuth 令牌  
- 供应链安全（4 项） - 可疑的导入代码、远程代码执行（RCE）检测  

**动态攻击测试（52 项）：**  
- 直接权限覆盖（7 项） - 越狱尝试、开发者模式、管理员权限提升  
- 角色劫持（7 项） - 伪装、虚假支持、权限滥用  
- 编码技巧（7 项） - Base64、ROT13、十六进制编码、Unicode 同形字  
- 多语言支持（7 项） - 中文、俄文、阿拉伯文、日文、韩文、德文、西班牙文  
- 上下文操纵（8 项） - 假设性场景、故事模式测试  
- 社交工程（7 项） - 情感操控、奉承、道德绑架  
- 提示泄露（9 项） - 直接请求提示信息、配置信息泄露  

**可单独运行测试：**  
```bash
python agentshield_tester.py --config agent_config.json --prompt system_prompt.txt
```  

详细文档请参阅 `TESTING.md`。  

---

## 一键快速启动  

```bash
clawhub install agentshield-audit && python initiate_audit.py --auto
```  

只需执行该命令，您的代理程序将在约 30 秒内完成审计。  

---

## 完整的工作流程  

---  

## 人工审核机制：详细审批流程  

### 当您运行 `python initiate_audit.py --auto` 时：  

```
┌─────────────────────────────────────────────────┐
│  AgentShield Security Audit - Consent Required  │
├─────────────────────────────────────────────────┤
│                                                 │
│  Before proceeding, I need to:                  │
│                                                 │
│  1. Read these files (to detect agent name):    │
│     • IDENTITY.md                               │
│     • SOUL.md                                   │
│                                                 │
│  2. Generate a cryptographic keypair            │
│     (stored locally in ~/.agentshield/)         │
│                                                 │
│  3. Send public key to AgentShield API          │
│                                                 │
│  Private keys NEVER leave this workspace.       │
│                                                 │
│  Proceed? [y/N]: _                              │
│                                                 │
└─────────────────────────────────────────────────┘
```  

**用户必须明确输入 ‘y’ 或 ‘yes’ 才能继续。**  

### 另一种选择：完全跳过文件读取  

```bash
# Provide info manually - no file access needed
python initiate_audit.py --name "MyAgent" --platform telegram
```  

---

## 使用场景：  
- 用户希望审计其代理程序的安全性  
- 用户需要为其代理程序获取信任证书  
- 用户需要验证其他代理程序的证书  
- 设置代理间的安全通信  
- 在安装未经验证的技能之前  

---

## 安装方法  

### 方法 A：一键安装（推荐）  

```bash
clawhub install agentshield-audit && python initiate_audit.py --auto
```  

### 方法 B：逐步安装  

```bash
# Install the skill (all scripts bundled locally)
clawhub install agentshield-audit

# Navigate to skill directory
cd ~/.openclaw/workspace/skills/agentshield-audit

# Run with user confirmation (Human-in-the-Loop)
python initiate_audit.py --auto
```  

### 方法 C：手动配置（不读取文件）  

```bash
# Skip auto-detection entirely - user provides info manually
python initiate_audit.py --name "MyAgent" --platform telegram
```  

---

## 安全评分（0-100 分）  

| 评分 | 安全等级 | 描述 |
|-------|------|-------------|
| 90-100 | 高级安全 | 通过所有关键测试，顶级安全性。 |
| 75-89 | 中级安全 | 通过大部分测试，存在少量问题。 |
| 50-74 | 基础安全 | 达到最低要求，有改进空间。 |
| <50 | 易受攻击 | 未通过关键测试，建议立即采取措施。 |

---

## 安全模型：  
- **完全本地打包** - 无外部代码下载  
- **需要用户批准** - 在读取敏感文件前必须获得用户明确同意  
- **私钥始终保留在代理程序的工作区内**  
- **挑战-响应认证** - 防止重放攻击  
- **证书由 AgentShield 签发** - 任何人都可以验证  
- **证书有效期为 90 天** - 鼓励定期重新审计  
- **速率限制**：每个 IP 每小时只能进行一次审计（防止滥用）  

---

## 脚本参考  

所有脚本均本地打包，无需外部下载：  

| 脚本 | 功能 | 示例 |
|--------|---------|---------|
| `initiate_audit.py` | 启动审计流程 | `python initiate_audit.py --auto` |
| `verify_peer.py` | 验证其他代理的证书 | `python verify_peer.py --agent-id "agent_xyz789"` |
| `show_certificate.py` | 显示您的证书 | `python show_certificate.py` |
| `audit_client.py` | 低级 API 客户端 | 用于自定义集成 |

---

## 包含的所有内容  

```
agentshield-audit/
├── SKILL.md                  # This file
├── README.md                 # User documentation
├── clawhub.json             # ClawHub manifest
├── requirements.txt         # Python dependencies
│
├── Core Scripts (bundled):
│   ├── initiate_audit.py    # Main audit script with consent flow
│   ├── verify_peer.py       # Peer verification
│   ├── show_certificate.py  # Certificate display
│   └── audit_client.py      # API client
│
├── Security Modules (bundled):
│   ├── input_sanitizer.py   # Input validation
│   ├── output_dlp.py        # Output data loss prevention
│   ├── tool_sandbox.py      # Tool execution sandbox
│   ├── echoleak_test.py     # Echo leakage detection
│   ├── secret_scanner.py    # Secret scanning
│   └── supply_chain_scanner.py  # Supply chain security
│
└── sandbox_config.yaml      # Sandbox configuration
```  

---

## 示范模式/免费使用  

**前 3 次审计完全免费**，无需注册或 API 密钥。  

之后：  
- 每个 IP 每小时仅允许进行 1 次审计  
- 基本使用无需支付费用  
- 企业级/高流量使用请联系我们  

---

## 故障排除：  

| 问题 | 解决方案 |
|-------|----------|
| “未找到证书” | 先运行 `initiate_audit.py` |
| “认证失败” | 检查系统时间（需要 NTP 同步） |
| “API 无法访问” | 确保网络连接正常 |
| “达到使用限制” | 等待 1 小时后再尝试审计 |
| “用户拒绝” | 用户选择不继续审计 |
| 自动检测失败 | 手动指定 `--name` 和 `--platform` 参数 |

---

## 开发者信息：  
**版本：** 1.0.0  
**许可证：** MIT  
**作者：** Kalle-OC (@bartelmost)  
**GitHub：** https://github.com/bartelmost/agentshield  

**包状态：** ✅ 已验证 - 所有脚本均本地打包  
**当前 API：** agentshield.live/api  
**未来计划：** 迁移到企业级托管环境  

## 有任何问题？**  
请在 GitHub 上提交问题，或通过 Moltbook 联系 @Kalle-OC。  

**保护自己，验证他人。默认情况下，对任何事物都保持警惕。**