---
name: agentshield
version: 1.0.22
description: AI代理的信任基础设施——类似于用于代理间通信的SSL/TLS协议。通过77项安全测试、加密证书以及信任握手协议（Trust Handshake Protocol），确保代理之间的通信通道安全可靠。
triggers: ["audit my agent", "get security certificate", "verify agent", "activate AgentShield", "security audit", "trust handshake", "verify peer agent"]
---
# AgentShield - 为AI代理提供信任基础设施

**这是代理经济中的信任层。就像SSL/TLS，但专为AI代理设计。**

🔐 **加密身份验证** - 使用Ed25519签名密钥  
🤝 **信任握手协议** - 通信前的相互验证  
📋 **公共信任注册表** - 信誉评分和交易记录  
✅ **77项安全测试** - 全面的漏洞评估

**🔒 隐私政策：** 详细的数据处理信息请参阅[PRIVACY.md]。**

---

## 🎯 问题所在

代理需要与其他代理进行通信（API调用、数据共享、任务委托）。但**如何判断另一个代理是否可信呢？**

- 它是否已被入侵？
- 是否在泄露数据？
- 你能信任它的响应吗？

如果没有信任层，代理之间的通信就如同没有SSL保护的HTTP协议一样——**不安全且无法验证**。

---

## 💡 解决方案：信任基础设施

AgentShield为代理之间的通信提供了**信任层**：

### 1. 加密身份验证
- **Ed25519密钥对** - 行业标准的加密技术
- **私钥始终保存在本地** - 从不传输
- **公钥证书** - 由AgentShield签名

### 2. 安全审计（77项测试）
**52种实时攻击方式：**
- 提示注入（15种变体）
- 编码攻击（Base64、ROT13、Hex、Unicode）
- 多语言攻击（中文、俄文、阿拉伯文、日文、德文、韩文）
- 社会工程学攻击（情感诉求、权威压力、奉承话术）
- 系统提示提取尝试

**25项静态安全检查：**
- 输入内容清洗
- 输出数据泄露防护（DLP）
- 工具沙箱测试
- 供应链安全检查

**结果：** 安全评分（0-100分）+ 安全等级（VULNERABLE → HARDENED）

### 3. 信任握手协议
**代理A希望与代理B通信：**

```bash
# Step 1: Both agents get certified
python3 initiate_audit.py --auto

# Step 2: Agent A initiates handshake with Agent B
python3 handshake.py --target agent_B_id

# Step 3: Both agents sign challenges
# (Automatic in v1.0.13+)

# Step 4: Receive shared session key
# → Now you can communicate securely!
```

**你会得到：**
- ✅ 双方身份的相互验证
- ✅ 共享的会话密钥（用于加密通信）
- ✅ 信任评分提升（握手成功后增加5分）
- ✅ 公开的交易记录

### 4. 公共信任注册表
- 所有经过认证的代理的查询数据库
- 基于审计结果、握手记录和活跃时间的信誉评分
- **信任等级：** 未验证 → 基础 → 已验证 → 可信赖
- **撤销列表（CRL）** - 被入侵的代理会被标记出来

---

## 🚀 快速入门

### 安装
```bash
clawhub install agentshield
cd ~/.openclaw/workspace/skills/agentshield*/
```

### 获取认证（通过77项安全测试）
```bash
# Auto-detect agent name from IDENTITY.md/SOUL.md
python3 initiate_audit.py --auto

# Or manual:
python3 initiate_audit.py --name "MyAgent" --platform telegram
```

**输出结果：**
- ✅ 代理ID：`agent_xxxxx`
- ✅ 安全评分：XX/100
- ✅ 安全等级：PATTERNS_CLEAN / HARDENED等
- ✅ 证书（有效期90天）

### 验证其他代理
```bash
python3 verify_peer.py agent_yyyyy
```

### 与其他代理进行信任握手
```bash
# Initiate handshake
python3 handshake.py --target agent_yyyyy

# Result: Shared session key for encrypted communication
```

---

## 📋 使用场景

### 1. 代理之间的API调用
**之前：** 代理A调用代理B的API时无法验证B的可靠性  
**使用AgentShield后：** 代理A会检查代理B的证书并进行握手验证 → 确保通信安全

### 2. 多代理任务委托
**之前：** 调度器创建子代理时无法确认它们的安全性  
**使用AgentShield后：** 所有子代理都经过认证 → 调度器可以确保它们的可靠性

### 3. 代理市场
**之前：** 从互联网上随机选择代理时无法保证其安全性  
**使用AgentShield后：** 可在信任注册表中筛选 → 只雇佣经过认证的代理

### 4. 代理之间的数据共享
**之前：** 与代理共享敏感数据时担心数据泄露  
**使用AgentShield后：** 通过握手协议和加密会话密钥确保数据传输安全

---

## 🛡️ 安全架构

### 首先考虑隐私

✅ **所有77项测试都在本地执行** - 系统提示内容永远不会离开用户的设备  
✅ **私钥始终保存在本地** - 仅传输公钥  
✅ 需要用户明确同意才能读取IDENTITY.md/SOUL.md文件  
✅ **不进行环境扫描** - 不会扫描API令牌

**上传到服务器的内容：**
- 公钥（Ed25519格式）
- 代理名称及平台信息
- 测试结果（通过/失败总结）

**保留在本地的内容：**
- 私钥
- 系统提示内容
- 配置文件
- 详细的测试结果

### 环境变量（可选）
```bash
AGENTSHIELD_API=https://agentshield.live  # API endpoint
AGENT_NAME=MyAgent                        # Override auto-detection
OPENCLAW_AGENT_NAME=MyAgent               # OpenClaw standard
```

---

## 📊 你将获得的内容

### 证书（有效期90天）
```json
{
  "agent_id": "agent_xxxxx",
  "public_key": "...",
  "security_score": 85,
  "tier": "PATTERNS_CLEAN",
  "issued_at": "2026-03-10",
  "expires_at": "2026-06-08"
}
```

### 信任注册表条目
- ✅ 公共验证链接：`agentshield.live/verify/agent_xxxxx`
- ✅ 信任评分（0-100分，依据以下因素：
  - 使用时长（使用时间越长，信任度越高）
  - 验证次数
  - 握手成功率
  - 活跃天数
- ✅ 安全等级：未验证 → 基础 → 已验证 → 可信赖

### 握手验证证明
```json
{
  "handshake_id": "hs_xxxxx",
  "requester": "agent_A",
  "target": "agent_B",
  "status": "completed",
  "session_key": "...",
  "completed_at": "2026-03-10T20:00:00Z"
}
```

---

## 🔧 随附脚本

| 脚本 | 用途 |
|--------|---------|
| `initiate_audit.py` | 运行77项安全测试并获取认证 |
| `handshake.py` | 与其他代理进行信任握手 |
| `verify_peer.py` | 检查其他代理的证书 |
| `show_certificate.py` | 显示你的证书 |
| `agentshield_tester.py` | 独立测试套件（高级功能） |

---

## 🌐 信任握手协议（技术细节）

### 流程
1. **发起请求：** 代理A向服务器发送“我想与代理B握手”的请求
2. **生成挑战：** 服务器为双方生成随机挑战
3. **签名：** 双方使用私钥对挑战内容进行签名
4. **验证：** 服务器使用公钥验证签名
5. **完成握手：** 服务器生成共享的会话密钥
6. **信任提升：** 双方的信任评分各增加5分

### 加密技术
- **算法：** Ed25519（curve25519）
- **密钥长度：** 256位
- **签名：** 确定性签名（相同消息产生相同签名）
- **会话密钥：** 兼容AES-256加密算法

---

## 🚀 发展计划

**当前版本（v1.0.13）：**
- ✅ 77项安全测试
- ✅ Ed25519证书
- ✅ 信任握手协议
- ✅ 公共信任注册表
- ✅ 证书撤销列表（CRL）

**即将推出：**
- ⏳ 自动重新审计（当提示内容发生变化时）
- ⏳ 负面事件报告功能
- ⏳ 多代理管理界面
- ⏳ 适用于消息平台的信任徽章

---

## 📖 更多信息

- **官方网站：** https://agentshield.live
- **GitHub仓库：** https://github.com/bartelmost/agentshield
- **API文档：** https://agentshield.live/docs
- **ClawHub集成：** https://clawhub.ai/bartelmost/agentshield

---

## 🎯 总结

**AgentShield就是为AI代理设计的SSL/TLS。**

获取认证 → 验证对方 → 建立信任关系 → 安全通信。

```bash
# 1. Get certified
python3 initiate_audit.py --auto

# 2. Handshake with another agent
python3 handshake.py --target agent_xxxxx

# 3. Verify others
python3 verify_peer.py agent_yyyyy
```

**为代理经济建立信任基础。** 🛡️

---

## 🔒 数据传输透明度

### 上传到AgentShield API的内容

**在提交审计信息时：**
```json
{
  "agent_name": "YourAgent",
  "platform": "telegram",
  "public_key": "base64_encoded_ed25519_public_key",
  "test_results": {
    "score": 85,
    "tests_passed": 74,
    "tests_total": 77,
    "tier": "PATTERNS_CLEAN",
    "failed_tests": ["test_name_1", "test_name_2"]
  }
}
```

**不上传的内容：**
- ❌ 完整的测试结果或日志
- ❌ 用户的提示信息或系统消息
- ❌ IDENTITY.md或SOUL.md文件的内容
- ❌ 私钥（保存在`~/.agentshield/agent.key`文件中）
- ❌ 工作区文件或内存中的数据

**API接口：**
- 主接口：`https://agentshield.live/api`（通过Heroku后端代理）
- 所有流量均使用HTTPS（TLS 1.2+协议）

---

## 🛡️ 同意与隐私保护

**文件读取权限：**
1. 在读取IDENTITY.md/SOUL.md之前，系统会请求用户授权
2. 用户会看到提示：“是否要读取代理的名称？[是/否]”
3. 如果用户拒绝：系统将进入手动模式（使用`--name`参数）
4. 如果用户同意：仅提取代理名称和平台信息（不读取完整文件内容）

**隐私优先模式：**
```bash
export AGENTSHIELD_NO_AUTO_DETECT=1
python initiate_audit.py --name "MyBot" --platform "telegram"
```
→ 完全不读取文件内容，仅通过手动输入获取信息

详细的数据处理政策请参阅[PRIVACY.md]。