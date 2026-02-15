---
name: a2a-shib-payments
description: 一个与框架无关的代理间支付系统，支持在 Polygon 上使用 SHIB（Solana 的代币）进行交易。该系统提供了无需信任的托管服务、价格协商功能以及基于声誉的信任机制。与传统托管服务相比，其成本降低了 9,416 倍（每笔交易所需的 gas 费用约为 0.003 美元）。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node", "npm"] },
        "install":
          [
            {
              "id": "node-deps",
              "kind": "node",
              "package": ".",
              "label": "Install dependencies (npm install)",
            },
          ],
        "tags": ["payments", "blockchain", "polygon", "shib", "escrow", "a2a", "agent-to-agent", "crypto", "web3"],
      },
  }
---

# A2A SHIB支付系统 - OpenClaw技能  
这是一个基于Polygon网络的、跨框架的代理间支付解决方案。  

## 概述  
该技能使AI代理能够：  
- 💰 在Polygon网络上发送/接收SHIB支付（手续费约为0.003美元）  
- 🔒 创建无需信任的托管合约  
- 💬 自动进行多轮价格谈判  
- ⭐ 通过评分建立声誉  
- 🌐 通过A2A协议发现其他代理  

与传统托管服务相比，该系统的成本低9,416倍（Escrow.com每100美元收取28.25美元，而本系统仅需0.003美元）。  

## 主要功能  

### 支付系统  
- 直接在Polygon网络上进行SHIB转账  
- 手续费极低（约0.003美元）  
- 可查询账户余额  
- 提供交易历史记录  

### 托管系统  
- 实现时间锁定的无信任支付  
- 需要多方共同批准  
- 支持提交交易完成证明  
- 条件满足后自动释放资金  
- 提供仲裁机制解决争议  
- 支持6种状态：待处理 → 已支付 → 被锁定 → 已释放/退款/争议中  

### 价格谈判  
- 生成服务报价  
- 支持多轮还价  
- 具有接受/拒绝交易的工作流程  
- 自动集成托管功能  
- 提供服务交付跟踪  

### 声誉系统  
- 提供0-5星的评分和评论  
- 动态信任评分（0-100分）  
- 信任等级：新用户 → 青铜 → 银 → 金 → 白金  
- 为优秀代理颁发徽章  
- 支持代理身份验证  

### 安全性  
- 使用API密钥进行身份验证（64字节密钥）  
- 实施请求/支付量限制  
- 日志记录不可篡改（采用哈希链技术）  
- 为每个代理设置权限和交易限额  

## 安装  
（具体安装步骤请参考**```bash
# Via ClawHub
clawhub install a2a-shib-payments

# Or manual clone
cd ~/clawd/skills
git clone https://github.com/marcus20232023/a2a-shib-payments.git
cd a2a-shib-payments
npm install
```**）  

## 配置  
创建`.env.local`文件：  
（具体配置内容请参考**```bash
cp .env.example .env.local
nano .env.local
```**）  

**必需的环境变量：**  
- `WALLET_PRIVATE_KEY`：您的Polygon钱包私钥  
- `RPC_URL`：Polygon的RPC端点（默认：https://polygon-rpc.com）  
- `SHIB_CONTRACT_ADDRESS`：SHIB代币合约地址（默认：0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce）  

## 使用方法  
（具体使用步骤请参考**```bash
node a2a-agent-full.js
```**）  
代理默认运行在8003端口。  

### 与OpenClaw的集成  
该代理提供了A2A协议接口，OpenClaw可以通过以下方式与其交互：  
**代理信息文件：** `http://localhost:8003/.well-known/agent-card.json`  
**OpenClaw示例命令：**  
（具体命令请参考**```javascript
// Check balance
const result = await fetch('http://localhost:8003/a2a/jsonrpc', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    jsonrpc: '2.0',
    method: 'message/send',
    params: {
      message: {
        kind: 'message',
        messageId: '1',
        role: 'user',
        parts: [{kind: 'text', text: 'balance'}]
      }
    },
    id: 1
  })
});

// Send payment
// text: 'send 100 SHIB to 0x...'

// Create escrow
// text: 'escrow create 500 SHIB for data purchase payee data-agent'

// Check reputation
// text: 'reputation check data-agent'
```**）  

### 兼容性  
该系统可与以下框架配合使用：  
- ✅ **OpenClaw**（作为技能或独立代理）  
- ✅ **LangChain**（通过A2A工具）  
- ✅ **AWS Bedrock**（通过代理调用）  
- ✅ **AutoGen**（通过A2A消息传递）  
- ✅ 任何支持A2A协议的系统  

详细集成指南请参阅[INTEGRATION-EXAMPLES.md]。  

## 应用场景  
- **数据市场**  
- **AI模型训练**  
（具体应用场景请参考相应代码块。）  

## API接口  
- `/.well-known/agent-card.json`：代理功能信息  
- `/a2a/jsonrpc`：JSON-RPC通信接口  
- `/a2a/rest/*`：REST API接口  

### 常用命令  
- `balance`：查询SHIB余额  
- `send [amount] SHIB to [address]`：发送SHIB支付  
- `escrow create [amount] SHIB for [purpose] payee [agent]`：创建托管合约  
- `escrow fund [id]`：为托管合约充值  
- `escrow release [id]`：释放托管资金  
- `quote create [service] [price]`：生成服务报价  
- `reputation check [agentId]`：查询代理声誉  
- `rate [agentId] [1-5] [review]`：对代理进行评分  

## 测试说明  
（具体测试步骤请参考**```bash
# Run all tests
npm test

# Individual test suites
npm run test:security
npm run test:escrow
npm run test:reputation
```**）  

## 文件结构  
- `a2a-agent-full.js`：功能齐全的代理程序（运行在8003端口）  
- `index.js`：支付代理核心代码  
- `escrow.js`：托管系统代码  
- `payment-negotiation.js`：谈判流程代码  
- `reputation.js`：声誉管理代码  
- `auth.js`：API身份验证代码  
- `rate-limiter.js`：请求/支付量限制代码  
- `audit-logger.js`：日志记录代码  

**文档资料：**  
- `README.md`：项目概述  
- `INTEGRATION-EXAMPLES.md`：框架集成指南  
- `ESCROW-NEGOTIATION-GUIDE.md`：API参考手册  
- `PRODUCTION-HARDENING.md`：安全加固指南  
- `DEPLOYMENT.md`：部署指南  

## 安全措施  
- ✅ API密钥认证  
- ✅ 请求/支付量限制  
- 日志记录不可篡改  
- 为每个代理设置权限  
- 支持托管合约的时间锁定机制  
- 需要多方共同批准  

**生产环境推荐措施：**  
- 使用多签名钱包  
- 使用HTTPS（如Cloudflare/Let’s Encrypt）  
- 配置防火墙规则  
- 自动化数据备份  
- 实施监控和警报机制  

完整的安全指南请参阅[PRODUCTION-HARDENING.md]。  

## 部署方式  
- **快速本地测试：** （具体步骤请参考**```bash
./deploy-local.sh
```**）  
- **生产环境选项：**  
  - systemd服务（系统启动时自动运行）  
  - Cloudflare Tunnel（免费HTTPS服务）  
  - Docker容器  
  - VPS（每月6美元）  

详细部署指南请参阅[DEPLOYMENT.md]。  

## 成本对比  
| 系统 | 费用 | 结算时间 | 信任机制 |  
|--------|-----|-----------|-------|  
| **Escrow.com** | 28.25美元 | 5-7天 | 集中式 |  
| **PayPal** | 3.20美元 | 1-3天 | 集中式 |  
| **本系统** | 0.003美元 | 几秒内 | 去中心化 |  
（每100美元交易可节省99.99%的费用）  

## 链接  
- **GitHub仓库：** https://github.com/marcus20232023/a2a-shib-payments  
- **最新版本：** https://github.com/marcus20232023/a2a-shib-payments/releases/tag/v2.0.0  
- **A2A协议官网：** https://a2a-protocol.org  
- **问题反馈：** https://github.com/marcus20232023/a2a-shib-payments/issues  

## 许可证  
MIT许可证——商业和个人使用均免费  

## 版本信息  
v2.0.0——已准备好投入生产环境  

---

**专为代理经济而打造！**