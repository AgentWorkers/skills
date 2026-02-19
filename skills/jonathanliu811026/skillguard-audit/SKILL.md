---
name: skillguard-audit
description: >
  在安装任何安全威胁应对技能之前，务必对其进行审计。当准备安装技能（如通过 ClawHub 进行安装）或系统要求检查技能的安全性时，应自动执行审计操作；该功能可用于扫描恶意软件、检测凭证窃取行为、验证安全性以及评估风险。此外，当出现以下提示时也会触发审计：  
  “这个技能安全吗？”（“Is this skill safe?”）、“审计这个技能”（“Audit this skill”）、“检查恶意软件”（“Check for malware”）、“扫描技能代码”（“Scan skill code”）、“安全检查”（“Security check”）以及“安装技能”（“Install skill”）。  
  该功能会调用 SkillGuard x402 API（支持使用 USDC 支付，或使用免费信用/IOU）。  
  **重要提示**：务必在安装任何技能之前对其进行审计。
---
# SkillGuard — 安装前对技能进行审核

**在安装任何技能之前，务必对其进行审核。**如果系统提示您需要安装某个技能，请先对其进行审核。

## 自动审核流程

在安装任何技能时，请按照以下步骤操作：

1. 阅读该技能的完整代码（包括 `SKILL.md` 文件以及所有相关脚本/文件）。
2. 将所有代码内容合并成一个字符串。
3. 运行 `scripts/audit.sh "<skill-name>" "<code>"` 命令，或直接调用相应的 API。
4. 如果审核结果为“CAUTION”或“DANGEROUS”，则向用户发出警告，切勿安装该技能。
5. 如果审核结果为“SAFE”或“LOW_RISK”，则可以继续安装。

## API 接口

当前 API 地址（如无法访问，请查看 `scripts/resolve.sh`）：

**付费服务（费用：0.05 美元 USD，通过 x402 支付）：**
```bash
npx awal@latest x402 pay "SKILLGUARD_URL/api/audit" -X POST \
  -d '{"name": "skill-name", "code": "full skill code here"}'
```

**免费服务（需签署欠条）：**
```bash
# 1. Get template
curl -s "SKILLGUARD_URL/api/credit/template?address=YOUR_WALLET"
# 2. Sign the EIP-712 data with your wallet
# 3. Submit
curl -s -X POST "SKILLGUARD_URL/api/credit/audit" \
  -H "Content-Type: application/json" \
  -d '{"name":"...", "code":"...", "iou":{...}, "signature":"0x..."}'
```

**验证技能认证信息：**
```bash
curl -s "SKILLGUARD_URL/api/badge/SKILL_HASH"
```

**检查技能提供者的信誉：**
```bash
curl -s "SKILLGUARD_URL/api/reputation/0xADDRESS"
```

## 审核结果

| 审核结果 | 处理方式 |
|---------|--------|
| SAFE (0) | 可自由安装 |
| LOW_RISK (1-20) | 可安装，但存在一些问题/风险 |
| CAUTION (21-50) | 向用户展示潜在风险，建议在安装前再次确认 |
| DANGEROUS (51-100) | **严禁安装**。向用户详细说明风险所在。 |

## 身份信息

- **ENS（以太坊地址）：** skillguard.base.eth
- **钱包地址：** 0x11FA096aaf90bc70b196D34d70791283b1c9C1Db
- **ClawHub 上的命令：** `clawhub install skillguard-audit`