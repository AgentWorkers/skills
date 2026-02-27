# 🛡️ AgentShield 审计

> **以隐私为核心的安全评估，配备公共信任注册系统**

---

## 🔒 以隐私为核心的安全评估

**您的系统中没有任何数据会被泄露。所有测试都在本地执行。**

✅ **您的系统中没有任何数据会被泄露**  
✅ **52 种以上的安全测试在您的代理程序中本地执行**  
✅ **仅共享证书的公钥**  
✅ **开源代码——您可以自行验证每一项测试**

**AgentShield 无法看到您的提示信息、代码或代理程序的行为。**

---

## 🚀 快速入门

### 安装

```bash
clawhub install agentshield-audit
```

### 使用方法

告诉您的代理程序：

```
"Run a security assessment with AgentShield"
```

或者手动操作：

```bash
cd ~/.openclaw/skills/agentshield-audit
python scripts/initiate_audit.py --auto --yes
```

**所需时间：**约 2-5 分钟

---

## 🔍 开发者的透明度

### 基础设施的透明度

**⚠️ 开发者需要注意：**

> **当前的注册服务器：** Heroku（开发环境）  
> - **状态：** 将在 2026 年第二季度更换为专用基础设施  
> **用途：** 仅存储证书 ID 和信任评分  
> **不存储敏感数据：** 提示信息、代码和测试结果永远不会离开您的系统

**服务器会看到以下内容：**
✅ 证书 ID（公钥哈希）——用于注册查询  
✅ 挑战-响应签名——用于身份验证  
✅ 时间戳——用于审计追踪

**服务器绝对看不到以下内容：**
🚫 代理程序的提示信息或对话内容  
🚫 您的内部代码  
🚫 测试结果（PDF 文件保留在本地）  
🚫 系统日志或配置信息

**数据流：**
```
Your Agent → Local Tests → Ed25519 Signing → Public Certificate → Registry
   (Code)      (52+ Tests)    (Private Key)      (Public Key)    (ID Only)
                                                     👆
                                              Only this goes to server!
```

**详细信息：** 请参阅 `DEVELOPER_TRANSPARENCY.md`

---

## ✨ 功能

### 🔐 以隐私为核心的安全性
- ✅ **52 种以上的本地安全测试** —— 全部在您的环境中执行  
- ✅ **零数据泄露** —— 仅共享公钥  
- ✅ **开源测试** —— 您可以自行验证每一项测试  
- ✅ **挑战-响应协议** —— 使用加密技术进行身份验证

### 📜 证书系统
- ✅ **Ed25519 签名** —— 行业标准的加密算法  
- ✅ **公共信任注册系统** —— 可以验证任何代理程序的状态  
- ✅ **CRL 支持** —— 需要时可立即撤销证书  
- ✅ **防篡改的 PDF 报告** —— 本地生成报告

### 🏆 信任评分
- ✅ **分级系统** —— 未验证 → 基础级 → 已验证 → 可信赖  
- ✅ **公共注册系统** —— [agentshield.live/registry](https://agentshield.live/registry)  
- ✅ **建立信誉** —— 通过多次验证提升信任度

### 🇪🇺 合规性
- ✅ **符合欧盟 AI 法规** —— 支持风险分类  
- ✅ **遵守 GDPR** —— 不存储个人数据  
- ✅ **RFC 5280 CRL** —— 标准的证书撤销格式  
- ✅ **审计追踪** —— 所有验证操作都会被记录

---

## 📊 工作原理

**步骤说明：**

1. **在本地安装 Skill：** `clawhub install agentshield-audit`  
2. **生成子代理程序** —— 测试在隔离的会话中执行（在您的环境中！）  
3. **执行 52 种以上的安全测试** —— 所有测试都在本地完成，不会上传任何数据  
4. **生成 Ed25519 密钥** —— 私钥保留在您的机器上  
5. **挑战-响应** —— 使用签名来验证身份（在本地完成！）  
6. **颁发证书** —— 提供公共注册信息和防篡改的 PDF 报告  
7. **信任评分** —— 通过多次验证提升信任度

**我们能看到以下内容：**
- ✅ 您的 Ed25519 **公钥**（证书）  
- ✅ 挑战过程中的 **签名**（身份验证的证明）

**我们绝对看不到以下内容：**
- ❌ 您的提示信息或对话内容  
- ❌ 您的代码或代理程序的行为  
- ❌ 您的 API 密钥或敏感信息  
- ❌ 您的测试结果（PDF 文件保留在本地）

---

## 🔍 安全测试

**52 种测试，涵盖 5 个类别：**

### 1. 输入清理
- 检测提示信息注入  
- 模板注入测试  
- SQL 注入攻击  
- 命令注入尝试  
- XSS 漏洞扫描

### 2. EchoLeak 测试
- 零点击数据泄露检测  
- 恶意工具调用  
- 上下文污染检测  
- 内存隔离检查

### 3. 工具沙箱
- 权限边界控制  
- 文件系统访问测试  
- 网络隔离检查  
- 权限提升尝试

### 4. 输出数据保护
- 个人身份信息（PII）检测（电子邮件、社会安全号码、信用卡信息）  
- API 密钥模式匹配  
- 防止秘密信息泄露  
- 数据清理检查

### 5. 供应链扫描
- 依赖项完整性检查  
- 包含恶意代码的库扫描  
- 过时库的警告

**所有测试代码均为开源：** [github.com/bartelmost/agentshield](https://github.com/bartelmost/agentshield)

---

## 🏆 信任评分解释

### 评分计算

您的信任评分（0-100 分）基于以下因素计算：

- **40%** 验证次数（一致性）  
- **30%** 证书使用时间（信誉）  
- **30%** 测试成功率（可靠性）

### 分级系统

| 分级 | 评分 | 标志 | 要求 |
|------|-------|-------|--------------|
| 🔴 **未验证** | 0 | ❌ | 无证书 |
| 🟡 **基础级** | 1-49 | 🆔 | 初始评估 |
| 🟢 **已验证** | 50-79 | ✅ | 多次验证 |
| 🔵 **可信赖** | 80-100 | 🛡️ | 有良好的验证记录 |

### 查看注册信息

**浏览所有已认证的代理程序：**  
👉 [agentshield.live/registry](https://agentshield.live/registry)

**检查任何代理程序的状态：**  
👉 [agentshield.live/verify](https://agentshield.live/verify)

---

## 🛡️ 安全架构（以隐私为核心）

```
┌──────────────────────────────────────────────────────────────┐
│                   YOUR AGENT ENVIRONMENT                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ 52+ Tests   │  │  Code Scan  │  │  Token Opt  │  ◄─ Local │
│  │  (Local)    │  │  (Local)    │  │   (Local)   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         └────────────────┴────────────────┘                 │
│                          │                                   │
│                    Ed25519 Sign                              │
│                  (Private Key Never Leaves)                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                  Challenge Response
                  (Public Cert Only)
                           ▼
               ┌───────────────────────┐
               │  AgentShield Registry │
               │  (Public Trust DB)    │
               └───────────────────────┘
```

**关键隐私保障措施：**

- ✅ **所有测试都在您的代理程序会话中执行**  
- ✅ **子代理程序在本地生成（不在我们的服务器上）**  
- ✅ **私钥在本地生成并存储**  
- ✅ **PDF 报告在您的机器上生成**  
- ❌ **我们永远不会收到您的代码或提示信息**  
- ❌ **我们永远不会看到您的测试结果**  
- ❌ **我们仅存储您的公钥和信任评分**

**验证我们的声明：** 所有测试代码均为开源，可在 [github.com/bartelmost/agentshield](https://github.com/bartelmost/agentshield) 查看

---

## 📖 命令

### 启动审计

```bash
# Auto-detect agent details
python scripts/initiate_audit.py --auto --yes

# Manual mode
python scripts/initiate_audit.py \
  --name "MyAgent" \
  --platform openclaw \
  --environment production
```

### 验证其他代理程序

```bash
# Check another agent's certificate
python scripts/verify_peer.py agent_abc123

# Output example:
# ✅ Agent Verified
# Trust Score: 85/100 (TRUSTED)
# Verifications: 12
# Last Verified: 2026-02-26
# CRL Status: Valid
```

### 检查速率限制

```bash
curl https://agentshield.live/api/rate-limit/status
```

---

## 🔗 API 端点

### 公共端点（无需认证）

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/api/registry/agents` | GET | 列出所有已认证的代理程序 |
| `/api/registry/search?q=...` | GET | 搜索代理程序 |
| `/api/verify/:agent_id` | GET | 检查证书状态 |
| `/api/crl/check/:id` | GET | 检查证书撤销状态 |
| `/api/crl/download` | GET | 下载 CRL（RFC 5280 格式） |
| `/api/challenge/create` | POST | 生成挑战随机数 |
| `/api/challenge/verify` | POST | 验证签名 |

**完整的 API 文档：** [github.com/bartelmost/agentshield/docs/API.md](https://github.com/bartelmost/agentshield/blob/main/docs/API.md)

---

## ⚙️ 系统要求

- **Python：** >= 3.10  
- **OpenClaw：** >= 2026.2.15  
- **依赖库：**  
  - `cryptography >= 41.0.0`  
  - `requests >= 2.31.0`  
  - `PyNaCl >= 1.5.0`（用于 Ed25519 签名）

### 安装说明

```bash
# Install dependencies
pip install cryptography requests PyNaCl

# Or use requirements.txt
pip install -r requirements.txt
```

---

## 📚 文档资料

- **安全架构：** [SECURITY.md](https://github.com/bartelmost/agentshield/blob/main/SECURITY.md)  
- **API 参考：** [docs/API.md](https://github.com/bartelmost/agentshield/blob/main/docs/API.md)  
- **技术细节：** [docs/ARCHITECTURE.md](https://github.com/bartelmost/agentshield/blob/main/docs/ARCHITECTURE.md)  
- **更新日志：** [CHANGELOG.md](https://github.com/bartelmost/agentshield/blob/main/CHANGELOG.md)

---

## 🌐 链接

- **官方网站：** [agentshield.live](https://agentshield.live)  
- **注册系统：** [agentshield.live/registry](https://agentshield.live/registry)  
- **验证代理程序：** [agentshield.live/verify](https://agentshield.live/verify)  
- **GitHub 仓库：** [github.com/bartelmost/agentshield](https://github.com/bartelmost/agentshield)  
- **ClawHub 上的相关技能：** [clawhub.ai/skills/agentshield-audit](https://clawhub.ai/skills/agentshield-audit)

---

## 🤝 支持方式

- **电子邮件：** ratgeberpro@gmail.com  
- **GitHub 问题反馈：** [github.com/bartelmost/agentshield/issues](https://github.com/bartelmost/agentshield/issues)  
- **文档资料：** [github.com/bartelmost/agentshield](https://github.com/bartelmost/agentshield)

---

## 📜 许可证

MIT 许可证 —— 详情请参阅 [LICENSE](https://github.com/bartelmost/agentshield/blob/main/LICENSE)

---

## 🌟 为什么选择 AgentShield？

**1. **开源代码**  
所有测试过程都是公开透明的，没有隐藏的部分。  

**2. **以隐私为核心**  
我们永远不会看到您的任何数据，仅处理加密后的验证结果。  

**3. **符合行业标准**  
使用 Ed25519 算法和 RFC 5280 标准，同时遵守 GDPR 规定。  

**4. **公共信任注册系统**  
提供透明的信任评分，您可以随时验证任何代理程序的状态。  

**5. **符合欧盟 AI 法规**  
从项目初期就遵循了相关的合规性要求。  

**由代理程序开发者专为代理程序设计** 🤖🛡️

*最后更新时间：2026-02-26*  
*版本：v6.4*  
*维护者：Kalle-OC*