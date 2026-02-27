---
name: shieldapi
description: "**ShieldAPI** — 专为AI代理设计的x402安全情报服务。提供7个主要功能端点：  
1. 密码泄露检测（涵盖超过9亿条HIBP哈希值）；  
2. 电子邮件泄露信息查询；  
3. 域名信誉评估（包括DNS、黑名单、SSL、SPF、DMARC等）；  
4. IP地址信誉评估（包括Tor网络及黑名单信息）；  
5. URL安全检测（识别钓鱼网站、恶意软件及品牌仿冒行为）；  
6. 全面安全扫描。  
采用按请求计费的模式，支持USDC微支付（费用范围：0.001美元至0.01美元）。  
无需注册账户、无需API密钥，也无需订阅服务。所有功能端点均支持演示模式。"
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["curl"] }
    }
  }
---
# 🛡️ ShieldAPI — 为AI代理提供的安全情报服务

ShieldAPI是一款按请求计费的安全情报服务，基于**x402**协议（HTTP 402 “需要支付”）构建。它允许任何AI代理执行全面的安全检查——无需账户、API密钥或订阅。只需调用API、支付费用，即可获取结果。

所有费用均以USDC在Base Sepolia平台上结算。所有端点都支持免费试用模式。

**基础URL：** `https://shield.vainplex.dev/api`

**状态/信息查询：** `GET /api/health` （免费，列出所有端点及价格）

---

## 端点介绍

### 1. `check-password` — 密码泄露检测
将用户的SHA1哈希值与超过9亿条泄露的密码进行比对（来自HIBP数据库）。
- **费用：** 0.001 USDC
- **请求方式：** `GET /api/check-password?hash=<40字符的sha1哈希值>`
- **返回结果：** `{ found: true/false, count: 3861493 }`

### 2. `check-password-range` — 基于前缀的密码哈希范围查询
返回与前缀匹配的所有哈希值（保护用户隐私）。
- **费用：** 0.001 USDC
- **请求方式：** `GET /api/check-password-range?prefix=<5字符的前缀>`
- **返回结果：** `{ prefix, total_matches, results: [{ suffix, count }] }`

### 3. `check-domain` — 域名信誉检查
检查DNS记录、SPF/DMARC设置、SSL证书，并查询Spamhaus/SpamCop/SORBS黑名单。
- **费用：** 0.003 USDC
- **请求方式：** `GET /api/check-domain?domain=<域名>`
- **返回结果：** `{ domain, dns, blacklists, ssl, risk_score, risk_level }`

### 4. `check-ip` — IP地址信誉检查
检查IPv4地址是否在黑名单中，检测是否为Tor出口节点，并解析反向DNS。
- **费用：** 0.002 USDC
- **请求方式：** `GET /api/check-ip?ip=<IPv4地址>`
- **返回结果：** `{ ip, blacklists, is_tor_exit, reverse_dns, risk_score, risk_level }`

### 5. `check-email` — 邮箱泄露检测
检查该邮箱所属域名是否涉及数据泄露事件，提供泄露详情、泄露的数据类型及风险建议。
- **费用：** 0.005 USDC
- **请求方式：** `GET /api/check-email?email=<邮箱地址>`
- **返回结果：** `{ breaches: [...], domain_breach_count, risk_score, risk_level, recommendations }`
- **示例：** `test@linkedin.com` → 涉及3次数据泄露（2012年：1.64亿个账户；2021年：1.25亿个账户；2023年：1900万个账户）

### 6. `check-url` — URL安全与钓鱼检测
检查URL是否包含恶意代码，进行启发式分析（如品牌仿冒、可疑顶级域名、重定向链），并探测HTTP请求。
- **费用：** 0.003 USDC
- **请求方式：** `GET /api/check-url?url=<URL地址>`
- **返回结果：** `{ url, checks: { urlhaus, heuristics, http }, threats, risk_score, risk_level }`
- **检测内容：** 恶意软件传播、品牌仿冒（如PayPal、Google等）、可疑顶级域名（.tk、.ml）、过多的子域名、包含登录路径的URL等）

### 7. `full-scan` — 综合安全扫描
并行执行所有适用的安全检查。
- **费用：** 0.01 USDC
- **请求方式：** `GET /api/full-scan?email=<邮箱地址>&password_hash=<sha1哈希值>&domain=<域名>&ip=<IP地址>&url=<URL地址>`
- **返回结果：** 综合扫描结果及整体风险评分，附带易于理解的摘要
- **示例：** `?email=test@linkedin.com&password_hash=5BAA61...` → “⚠️ 该密码在5200万次数据泄露事件中被发现；该域名涉及3次数据泄露”

---

## 免费试用模式

所有7个端点都支持`?demo=true`参数——返回模拟数据，无需支付费用。非常适合在正式上线前测试您的集成。

```bash
# Try it now:
curl -s "https://shield.vainplex.dev/api/check-url?demo=true"
curl -s "https://shield.vainplex.dev/api/full-scan?demo=true"
curl -s "https://shield.vainplex.dev/api/check-email?demo=true"
```

---

## x402支付流程

当您尝试调用任何需要付费的端点但未完成支付时，ShieldAPI会返回`HTTP 402`响应，并提供机器可识别的支付指令：

```json
{
  "x402Version": 1,
  "error": "X-PAYMENT header is required",
  "accepts": [{
    "scheme": "exact",
    "network": "base-sepolia",
    "maxAmountRequired": "3000",
    "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
    "payTo": "0x...",
    "resource": "https://shield.vainplex.dev/api/check-domain?domain=example.com",
    "description": "Domain reputation & security check"
  }]
}
```

支持x402协议的客户端（使用`@coinbase/x402`、`@x402/core`或任何x402相关库）将：
1. 读取402响应
2. 在Base Sepolia平台上完成USDC支付
3. 重新发送请求，并在请求头中添加`X-PAYMENT`字段
4. 接收安全检查结果

---

## 使用场景

- **密码轮换系统** — 在设置新密码前检查其是否存在于泄露数据库中
- **邮箱验证** — 确认新用户的邮箱地址是否来自高风险域名
- **URL安全检查** — 在代理点击或用户访问链接前进行安全筛查
- **IP地址审核** — 检查IP地址是否为Tor出口节点、代理或黑名单中的地址
- **安全审计** — 一次性扫描整个组织的域名、IP地址及常用密码

---

## 来源与链接

- **实时API接口：** `https://shield.vainplex.dev/api/health`
- **项目源代码：** https://github.com/alberthild/shieldapi （即将发布）
- **协议文档：** https://x402.org
- **数据来源：** HIBP（CC-BY许可）、PhishTank、URLhaus（abuse.ch）、Spamhaus