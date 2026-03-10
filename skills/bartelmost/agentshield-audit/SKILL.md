# AgentShield Audit - OpenClaw Skill v1.4.0  
**为AI代理提供信任基础设施**

---

## 描述  
AgentShield为AI代理提供加密安全审计和信任验证服务。  

**v1.4的新功能：**  
- 引入了代理间相互验证的信任握手协议（Trust Handshake Protocol）。  

**主要特性：**  
- 安全审计（涵盖77种攻击途径）  
- Ed25519证书（有效期为90天）  
- 信任握手协议（实现相互验证）  
- 公共信任注册表  
- 证书吊销列表（CRL）  

**使用场景：**  
- 部署前验证代理的安全性  
- 建立代理间的信任关系  
- 建立代理的声誉  
- 识别可信赖的代理  
- 取消被泄露的证书  

---

## 快速入门  

### 1. 安全审计（一次性设置）  
```bash
# Initialize audit
openclaw run agentshield-audit --agent-id your_agent_id

# Follow prompts to:
# 1. Generate Ed25519 keypair
# 2. Submit system prompt
# 3. Sign challenge
# 4. Receive certificate
```  
**结果：** 证书有效期为90天，并已发布到注册表中。  

---

### 2. 验证其他代理  
```bash
openclaw run agentshield-audit --verify agent_xyz
```  
**返回信息：**  
- 安全评分（0-100分）  
- 信任等级（未验证 → 基础 → 已验证 → 可信赖）  
- 证书有效期  
- 证书吊销状态  

---

### 3. 信任握手（v1.4的新功能！）  
```bash
# Quick trust check
openclaw run agentshield-audit --verify-peer agent_b --min-score 70

# Full mutual handshake
openclaw run agentshield-audit --handshake agent_b
```  
**操作流程：**  
1. 双方代理均完成验证（包括安全评分和信任评分）  
2. 交换Ed25519签名  
3. 生成用于加密通信的会话密钥  
4. 双方代理各获得+5点信任分  
5. 握手过程被记录在历史记录中  

**优势：**  
- 代理间基于加密技术的信任机制  
- 帮助建立代理的声誉（跟踪成功率）  
- 为加密通信奠定基础  

---

## 命令说明  

### 审计命令  
- `--audit`：执行全面的安全审计  
- `--verify <agent_id>`：验证其他代理的证书  
- `--status`：查看自己的证书状态  

### 信任握手命令（新功能！）  
- `--verify-peer <agent_id>`：快速进行信任验证  
- `--handshake <agent_id>`：实现相互验证  
- `--history`：查看自己的握手历史记录  

### 注册表命令  
- `--search <query>`：在注册表中搜索代理  
- `--list`：列出最受信任的代理  

---

## 使用的API端点  

### 信任握手（v1.4）  
- `GET /api/verify-peer/:agent_id`：快速进行信任验证  
- `POST /api/trust-handshake/initiate`：启动相互握手  
- `POST /api/trust-handshake/complete`：提交Ed25519签名  
- `GET /api/trust-handshake/status/:id`：查看握手进度  
- `GET /api/trust-handshake/history/:id`：查看代理的历史记录  

### 安全审计  
- `POST /api/agent-audit/initiate`：开始审计  
- `POST /api/agent-audit/challenge`：提交挑战响应  
- `POST /api/agent-audit/complete`：提交测试结果  
- `GET /api/verify/:agent_id`：验证证书  

### 注册表与证书吊销列表  
- `GET /api/registry/agents`：列出所有代理  
- `GET /api/registry/search`：按关键词搜索  
- `GET /api/crl`：获取证书吊销列表  

---

## 安装说明  
**无需安装！** 该功能通过使用AgentShield的公共API实现。  
**建议：** 为增强安全性，可进行本地测试：  
```bash
pip install cryptography requests
```  
**必备条件：** 需准备Ed25519密钥对（首次审计时生成）。  

## 配置  
创建`~/.agentshield/config.json`文件：  
```json
{
  "agent_id": "agent_your_unique_id",
  "private_key_path": "~/.agentshield/private_key.pem",
  "api_base": "https://agentshield.live/api"
}
```  

---

## 示例  
### 示例1：首次审计  
```bash
$ openclaw run agentshield-audit --audit

AgentShield Security Audit v1.4.0
=================================

Agent ID: agent_abc123def456
Status: No certificate found

Generating Ed25519 keypair...
✓ Keys saved to ~/.agentshield/

Submitting audit request...
Challenge received: a85dc6ca8ca2f980f07d...

Signing challenge...
✓ Challenge verified

Running 77 security tests...
✓ Prompt injection: PASS
✓ Data exfiltration: PASS
✓ Token flooding: PASS
... (72 more tests)

Results:
- Security Score: 85/100
- Tier: VERIFIED
- Tests Passed: 72/77

Certificate issued!
Expires: 2026-06-07
Verify: https://agentshield.live/api/verify/agent_abc123
```  

### 示例2：执行信任握手  
```bash
$ openclaw run agentshield-audit --handshake agent_b

Trust Handshake with agent_b
============================

Step 1: Verifying peer...
✓ agent_b found (Trust: 78, Tier: VERIFIED)

Step 2: Initiating handshake...
✓ Handshake ID: hs_xyz789

Step 3: Signing challenges...
✓ Your signature: base64_abc123...
✓ Peer signature: base64_def456...

Step 4: Completing handshake...
✓ Signatures verified!

Session Key: base64_session_key_ghi789...

Results:
- Your trust: 72 → 77 (+5 points)
- Peer trust: 78 → 83 (+5 points)
- Success rate: 95.2% (40/42 handshakes)

✓ Handshake complete! Use session key for encrypted communication.
```  

### 示例3：在注册表中搜索代理  
```bash
$ openclaw run agentshield-audit --search "customer support"

AgentShield Registry Search
===========================

Query: "customer support"
Found: 3 agents

1. SupportBot Pro
   - Trust: 92 (TRUSTED)
   - Platform: openclaw
   - Verified: 45 times
   - Last audit: 2026-03-01

2. HelpDesk AI
   - Trust: 78 (VERIFIED)
   - Platform: langchain
   - Verified: 12 times
   - Last audit: 2026-02-28

3. CustomerCare Agent
   - Trust: 65 (BASIC)
   - Platform: autogpt
   - Verified: 3 times
   - Last audit: 2026-03-05
```  

---

## 安全性说明  

### 数据隐私  
- **不存储系统提示信息**：仅保存哈希值  
- **不保存对话数据**：仅保存安全相关元数据  
- **不提交API密钥**：绝不向AgentShield传输  

### 加密技术  
- 使用Ed25519签名（256位安全性）  
- 证书采用SHA-256哈希算法  
- 采用“挑战-响应”（Challenge-Response）协议进行身份验证  

### 信任评分  
- 评分算法透明（详见文档/TRUST_ALGORITHM.md）  
- 抗作弊机制：服务器会对评分进行验证  
- 证书可吊销（支持CRL机制）  

---

## 常见问题及解决方法  

### “证书过期”  
**解决方法：** 重新执行审计（证书有效期为90天）。  
```bash
openclaw run agentshield-audit --audit
```  

### “签名无效”  
**问题原因：** 私钥不匹配  
**解决方法：** 确保`~/.agentshield/private_key.pem`文件存在且与公钥匹配。  

### “找不到代理”  
**问题原因：** 目标代理尚未进行审计  
**解决方法：** 要求其先运行AgentShield审计。  

### “握手失败”  
**问题原因：** 握手超时（默认为1小时）  
**解决方法：** 重新执行握手操作，并设置更长的超时时间。  
```bash
openclaw run agentshield-audit --handshake agent_b --ttl 3600
```  

---

## 更新日志  

### v1.4.0（2026-03-09）  
- 新增信任握手协议：  
  - 新增5个API端点  
  - 支持代理间相互验证  
  - 记录握手历史  
  - 生成会话密钥  
  - 每次握手后增加5点信任分  

**测试情况：**  
- 10项测试全部通过（My1stBot验证）  
- 已具备生产环境适用性  

### v1.2.1（2026-03-07）  
- 修复问题：  
  - 服务器开始尊重客户端提交的评分结果  
  - 解决评分不一致的问题  

### v1.2.0（2026-02-26）  
- 新增证书吊销列表（RFC 5280标准）  
- 引入公共信任注册表  
- 支持“挑战-响应”协议  

### v1.0.0（2026-02-19）  
- **初始版本：**  
  - 提供安全审计功能（涵盖77项测试）  
  - 使用Ed25519证书  
  - 支持PDF格式的报告生成  

---

## 资源链接  
- **官方网站：** https://agentshield.live  
- **API文档：** https://agentshield.live/docs  
- **GitHub仓库：** https://github.com/bartelmost/agentshield  
- **支持邮箱：** ratgeberpro@gmail.com  

---

## 许可证  
**MIT-0许可证**：免费使用、修改和分发，无需署名。  

---

**AgentShield v1.4.0——为AI代理提供信任基础设施**  
**由Kalle和Bartel共同开发。**