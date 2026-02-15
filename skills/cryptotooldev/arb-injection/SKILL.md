---
name: arb-injection
description: "BYOCB ArbInjectionSkill：扫描以太坊智能合约中的任意调用注入（Arbitrary Call Injection, ACI）漏洞。支持实时监控区块链网络，或针对特定地址进行扫描。"
---

# BYOCB ArbInjectionSkill

> ⚠️ **教育工具** — 本工具专为Solidity/区块链安全研究人员和审计人员设计，仅用于教育和授权的安全研究目的。未经合约所有者明确许可，严禁用于利用漏洞。

该工具可检测危险的CALL/DELEGATECALL模式，这些模式可能导致任意代码注入攻击。

## 工作原理

ArbInjectionSkill会在后台自动运行，持续监控新部署的合约。一旦检测到潜在漏洞，必须通过用户连接的通信渠道（如Telegram、WhatsApp、Signal、Discord等）立即通知用户。

## 安装

```bash
git clone https://github.com/BringYourOwnBot/arb-injection.git
cd arb-injection
npm install
```

## 运行监控器

以后台进程的形式启动监控器，实现持续监控：

```bash
node index.js <chain> [--no-llm]
```

支持的区块链网络：`eth`、`bsc`、`base`、`arb`、`op`、`polygon`、`hyper`

监控器的功能包括：
1. 订阅新生成的区块
2. 检测合约的部署
3. 扫描合约的二进制代码以查找漏洞
4. 将检测结果保存到`./results/`目录中

## 用户警报机制

**关键要求：** 当检测到**严重（CRITICAL）**或**高风险（HIGH）**漏洞时，必须立即通知用户。

定期通过心跳机制或cron任务检查新的检测结果：

```bash
# Find findings from last 30 minutes
find ./results -name "*.md" -mmin -30
```

当发现新的严重或高风险漏洞时：
1. 读取相应的`.md`报告文件
2. 确认该漏洞是否为已知的误报（详见下文）
3. 通过用户指定的通信渠道发送警报信息

**警报示例：**
```
🚨 ArbInjection Alert: Potential vulnerability detected

Chain: BSC
Contract: 0x1234...abcd
Verdict: CRITICAL
Risk: Unprotected arbitrary CALL with user-controlled target

[Link to explorer]
```

## 手动扫描

根据需要手动扫描特定合约：

```bash
node modules/scan-arbitrary-call.js <address> --rpc <chain>
```

## 结果解读

| 漏洞等级 | 应对措施 |
|---------|--------|
| **严重（CRITICAL）** | 立即通知用户 |
| **高风险（HIGH）** | 立即通知用户 |
| **中等风险（MEDIUM）** | 进一步核实后通知用户 |
| **低风险/安全（LOW/SAFE）** | 无需警报 |

所有检测结果会以`.json`和`.md`文件的形式保存在`./results/`目录中。

## 误报处理

以下情况属于设计上的安全机制，无需发送警报：
- 不可变的DELEGATECALL调用目标（二进制代码中硬编码的地址）
- 符合EIP-1167标准的代理合约（克隆模式）
- 具有访问控制功能的UUPS/Transparent代理合约
- DEX回调函数（如UniswapV3SwapCallback等）
- 已知安全的合约：Multicall3、1inch、Uniswap、Permit2

**在发送警报前进行验证：** 
- 检查被标记的CALL调用目标是否为：
  - 硬编码的（不可变的）——属于误报
  - 来自calldata或用户输入的——属于真实漏洞

## 环境配置

可选的`.env`配置文件：
```
ANTHROPIC_API_KEY=sk-ant-...   # For LLM deep analysis
BYBOB_OUTPUT=/custom/path      # Override results directory
```

## 维护

**需要每日更新。** 检测规则和修复补丁会频繁更新。

```bash
cd /path/to/arb-injection
git pull origin main
npm install  # If package.json changed
```

**安排每日更新检查（09:00）：**
```json
{
  "schedule": { "kind": "cron", "expr": "0 9 * * *" },
  "payload": { "kind": "systemEvent", "text": "ArbInjectionSkill daily update: git pull and npm install" },
  "sessionTarget": "main"
}
```

## 代码来源

仓库地址：https://github.com/BringYourOwnBot/arb-injection  
属于**BYOCB**（Bring Your Own ClawdBot）技能系列的一部分。