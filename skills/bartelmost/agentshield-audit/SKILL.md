# AgentShield 审计技能

这是一个用于 AI 代理的安全评估工具，通过静态模式分析来识别系统提示和代理代码中的漏洞。

## 安装

```bash
clawhub install agentshield-audit
```

## 使用方法

### 基本审计（模式扫描）

```bash
# Scan a local agent configuration
agentshield-audit scan --prompt "Your system prompt here"

# Scan code for vulnerabilities
agentshield-audit scan --code-file ./agent.py

# Full audit with certificate
agentshield-audit audit --prompt-file ./prompt.txt --code-file ./agent.py
```

### 实时测试（真实代理）

若要使用真实代理和实际的攻击尝试进行测试，请执行以下操作：

```bash
python scripts/demo_real_integration.py
```

该操作会生成真实的 OpenClaw 代理，每次测试的费用约为 0.01 至 0.10 美元。

## ⚠️ 重要限制

该工具仅执行 **静态模式分析**，不提供实时渗透测试功能：

### 功能概述：
- ✅ 扫描代理的代码和提示，查找已知的漏洞模式
- ✅ 通过签名匹配来识别潜在的安全风险
- ✅ 在本地机器上运行（不会向外部服务发送任何数据）
- ✅ 生成 PDF 报告以供查阅

### 功能限制：
- ❌ 不会对正在运行的代理执行真正的越狱攻击
- ❌ 不会测试代理的实际运行时行为
- ❌ 无法保证绝对的安全性（因为某些新型攻击可能无法被检测到）

### 功能对比：

| 功能        | 模式扫描      | 实时测试     |
|------------|-----------|-----------|
| 方法        | 静态分析     | 实际代理交互   |
| 成本        | 免费        | 约 0.01–0.10 美元 |
| 速度        | 即时        | 10–60 秒     |
| 覆盖范围      | 已知漏洞模式   | 实际攻击途径  |
| 适用场景    | 持续集成/持续交付（CI/CD）、快速检查 | 安全性验证   |

## API 集成

```python
import requests

# Code scan
response = requests.post(
    'https://agentshield-api-bartel-fe94823ceeea.herokuapp.com/api/code-scan',
    json={'code': 'your code here', 'promo_code': 'BETA5'}
)
print(response.json())
```

## 证书验证

AgentShield 为通过验证的代理颁发基于 Ed25519 的证书：

```bash
# Verify a certificate
agentshield-audit verify --certificate ./agent_certificate.json
```

## 隐私保护：
- 私钥存储在本地路径 `~/.openclaw/workspace/.agentshield/` 中
- API 调用仅使用公开端点
- 在本地扫描过程中，代理的代码和提示数据不会离开您的机器

## 支持资源：
- 文档：https://agentshield.live/docs
- 代码仓库：https://github.com/bartelmost/agentshield
- 问题反馈：https://github.com/bartelmost/agentshield/issues