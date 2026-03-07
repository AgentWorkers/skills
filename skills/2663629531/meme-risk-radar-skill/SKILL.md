---
name: meme-risk-radar-skill
description: >
  **Binance Web3数据的双语表情包代币风险雷达**：  
  该工具能够扫描来自“Meme Rush”平台的新上线或快速增长的表情包代币，结合代币审计和代币信息进行深度分析，生成标准化的风险报告（支持中文或英文格式）。同时，该工具还支持与SkillPay平台的集成，以便用户通过付费方式调用扫描和审计服务。
---
# 技能：meme-risk-radar-skill

## 目的  
该技能可将 Binance Web3 的 meme 发现数据转化为可交易的风险分析工具。它适用于那些希望快速获取 meme 信息，但在进一步研究之前需要先进行结构化筛选的用户。  
默认输出支持中文（zh）和英文（en）两种语言。  

## 产品定位  
- 专为交易者、研究人员、测试小组以及内容创作者设计，帮助他们更快地对 meme 代币进行分类和评估。  
- 强调“风险优先”的发现策略：首先筛选出潜在的候选项目，再排除明显的高风险选项，然后再进行深入研究。  
- 适合在 ClawHub 平台上使用（需付费），因为其价值体现在每次可执行的扫描结果上，而非原始的静态内容上。  

## 信任机制  
- 默认情况下，该技能仅提供数据读取功能，不会执行任何交易操作或请求交易所的交易密钥。  
- 所有敏感信息（如 API 密钥）均从环境变量中读取，绝不会被硬编码。  
- 输出结果具有可解释性：每个项目的评分都基于可查看的指标（如持有者集中度、开发者持股比例、流动性、审计记录和税收状态等）。  
- 面向用户的语言必须保持中立，不得承诺盈利或保证投资安全。  

## 命令  
通过该技能的根目录运行相关命令：  
```bash
python3 scripts/meme_risk_radar.py scan --chain solana --stage new --limit 10 --lang zh
python3 scripts/meme_risk_radar.py scan --chain bsc --stage finalizing --limit 5 --lang en --min-liquidity 10000
python3 scripts/meme_risk_radar.py audit --chain bsc --contract 0x1234... --lang en
python3 scripts/meme_risk_radar.py health
```  

## 输出格式  
每次扫描会返回以下信息：  
- `chain`（区块链）  
- `stage`（扫描阶段）  
- `lang`（语言）  
- `generated_at_utc`（生成时间）  
- `tokens[]`（扫描到的代币列表）  

每个代币条目包含以下信息：  
- `symbol`（代币符号）  
- `name`（代币名称）  
- `contract_address`（合约地址）  
- `score`（评分）  
- `risk_level`（风险等级）  
- `summary`（简要概述）  
- `signals`（风险信号）  
- `metrics`（相关指标）  
- `audit`（审计结果）  
- `links`（相关链接）  

## 计费机制（SkillPay）  
- 仅对“scan”和“audit”操作进行计费。  
- API 密钥从 `SKILLPAY_APIKEY` 变量中读取。  
- 默认计费价格为 `SKILLPAY_PRICE_USDT`（当前值为 0.002 美元）。  
- 确保敏感信息不会被硬编码。  

## 建议的盈利模式  
- 可按每次扫描和每次审计操作收费，基础功能免费提供。  
- 建议的起步价格为每次调用 0.002 美元；根据使用数据稳定后，可逐步提高价格。  
- 向用户传达的核心价值是：“付费获取经过筛选的候选列表，而非原始的代币信息。”  
- 如果后续添加高级功能（如高级筛选、观察列表、数据导出或警报通知），可针对这些功能额外收费。  

## 必需/有用的环境变量  
- `SKILLPAY_APIKEY`（付费模式所需）  
- `SKILLPAY_BASE_URL`（可选，默认为 `https://skillpay.me`）  
- `SKILLPAY_CHARGE_URL`（可选，用于自定义计费页面）  
- `SKILLPAY_CHARGE_PATH`（可选，用于指定计费路径）  
- `SKILLPAY_USER_REF`（可选，默认为 `anonymous`）  
- `SKILLPAY_PRICE_USDT`（可选，默认为 0.002 美元）  
- `SKILLPAY_BILLING_MODE`（可选，设置为 `skillpay` 或 `noop`）  
- `BINANCE_WEB3_BASE_URL`（可选，默认为 `https://web3.binance.com`）  
- `BINANCE_HTTP_TIMEOUT_SEC`（可选，默认为 12 秒）  

## 注意事项  
- 该技能仅用于风险筛选，不用于直接执行交易操作。  
- 即使评分显示为“LOW”（低风险），也不代表绝对安全；报告结果仅为实时快照。  
- 面向用户的语言必须保持中立，不得提供交易保证或盈利承诺。