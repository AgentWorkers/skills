---
name: apex-crypto-intelligence
description: 基于人工智能的多交易所加密货币市场分析系统，能够检测套利机会，并生成符合对冲基金标准的交易报告。该系统利用来自各大交易所的实时数据进行处理和分析。
version: 0.2.1
author: contrario
homepage: https://masterswarm.net
requirements:
  binaries:
    - python3
  env:
    - name: BINANCE_API_KEY
      required: false
      description: "Read-only Binance API key (optional)"
    - name: BINANCE_API_SECRET
      required: false
      description: "Read-only Binance secret (optional)"
    - name: BYBIT_API_KEY
      required: false
      description: "Read-only Bybit API key (optional)"
    - name: BYBIT_API_SECRET
      required: false
      description: "Read-only Bybit secret (optional)"
    - name: KUCOIN_API_KEY
      required: false
      description: "Read-only KuCoin API key (optional)"
    - name: KUCOIN_API_SECRET
      required: false
      description: "Read-only KuCoin secret (optional)"
    - name: MEXC_API_KEY
      required: false
      description: "Read-only MEXC API key (optional)"
    - name: MEXC_API_SECRET
      required: false
      description: "Read-only MEXC secret (optional)"
    - name: GATEIO_API_KEY
      required: false
      description: "Read-only Gate.io API key (optional)"
    - name: GATEIO_API_SECRET
      required: false
      description: "Read-only Gate.io secret (optional)"
metadata:
  skill_type: api_connector
  external_endpoints:
    - https://api.neurodoc.app/aetherlang/execute
  operator_note: "api.neurodoc.app operated by NeuroDoc Pro (same as masterswarm.net), Hetzner DE"
  privacy_policy: https://masterswarm.net
  key_safety: "Exchange keys used locally only — never transmitted to api.neurodoc.app. Keys are read from env vars per-request and excluded from all API payloads."
  python_deps:
    - httpx
license: MIT
---
# APEX Crypto Intelligence — 多交易所交易分析工具

> 该工具提供机构级别的加密货币市场分析服务，支持5家交易所的数据，结合AI技术的Hyper-Council智能分析以及对冲基金级别的PDF报告。

**源代码**: [github.com/contrario/aetherlang](https://github.com/contrario/aetherlang/tree/main/skills/apex-crypto-intelligence)
**官方网站**: [neurodoc.app](https://neurodoc.app)
**作者**: NeuroAether (info@neurodoc.app)
**许可证**: MIT
**版本**: 0.2.0

## 概述

APEX Crypto Intelligence是一款多交易所加密货币分析工具，它从CoinGecko、Binance、Bybit、KuCoin、MEXC和Gate.io获取实时市场数据，进行跨交易所套利检测，并通过由5位专业分析师组成的Hyper-Council提供AI驱动的机构级交易分析服务。

---

## 隐私与数据处理

⚠️ **用户自行管理密钥（BYOK）**：工具仅在本地使用交易所的API密钥来获取数据，这些密钥**不会被传输**到NeuroAether。

⚠️ **外部API说明**：仅将市场数据（价格、成交量）和查询文本发送到`api.neurodoc.app`进行AI分析。

**可审计的代码**：发送到`api.neurodoc.app`的数据仅包含汇总的市场价格和查询文本，交易所的API密钥不会被包含在内。

- **发送内容**：仅包含汇总的市场价格和自然语言查询
- **不发送的内容**：交易所API密钥、凭证、个人数据、钱包地址
- **数据保留**：查询数据会实时处理，不会被存储
- **托管服务**：使用Hetzner EU服务器（符合GDPR法规）

**重要提示**：用户应配置交易所API密钥为**仅读**权限，切勿启用提款或交易权限。

---

## 架构
```
User's Machine (local)              NeuroAether API
┌──────────────────────┐            ┌─────────────────┐
│                      │            │                  │
│  Exchange API Keys   │            │  api.neurodoc.app│
│  (never leave here)  │            │                  │
│         │            │            │  Receives ONLY:  │
│         ▼            │            │  - prices        │
│  Fetch from          │  prices +  │  - volumes       │
│  Binance/Bybit/etc   │──query──▶ │  - query text    │
│  (locally)           │            │                  │
│         │            │            │  Returns:        │
│         ▼            │  ◀──────── │  - AI analysis   │
│  Aggregate prices    │  analysis  │  - verdicts      │
│  (no keys in payload)│            │  - PDF data      │
│                      │            │                  │
└──────────────────────┘            └─────────────────┘
```

---

## 主要功能

1. **跨交易所扫描**：实时获取Binance、Bybit、KuCoin、MEXC、Gate.io的买卖价格
2. **套利检测**：自动分析5家交易所的价差情况
3. **APEX Hyper-Council分析**：由5位AI分析师（包括宏观策略师、量化研究专家、风险分析师和执行架构师）提供分析
4. **交易蓝图PDF报告**：生成包含SWOT分析、雷达图、盈亏预测和实施路线的对冲基金级报告
5. **支持多种加密货币**：BTC、ETH、SOL、XRP、DOGE、ADA、DOT、AVAX、MATIC、BNB、LTC、LINK、TRX、SHIB、SUI、APT、TON、NEAR、UNI、PEPE

---

## 配置（用户自行管理密钥）

用户需要通过环境变量提供自己的API密钥。所有密钥都是可选的——该工具默认可以使用CoinGecko的免费数据，同时也可以使用多个交易所的数据。

### 必需的环境变量

无需任何环境变量。即使不提供密钥，该工具也能使用CoinGecko的免费数据。

### 可选的环境变量

| 变量 | 交易所 | 用途 |
|----------|----------|---------|
| `BINANCE_API_KEY` | Binance | 市场数据（仅读） |
| `BINANCE_API_SECRET` | Binance | API认证 |
| `BYBIT_API_KEY` | Bybit | 市场数据（仅读） |
| `BYBIT_API_SECRET` | Bybit | API认证 |
| `KUCOIN_API_KEY` | KuCoin | 市场数据（仅读） |
| `KUCOIN_API_SECRET` | KuCoin | API认证 |
| `MEXC_API_KEY` | MEXC | 市场数据（仅读） |
| `MEXC_API_SECRET` | MEXC | API认证 |
| `GATEIO_API_KEY` | Gate.io | 市场数据（仅读） |
| `GATEIO_API_SECRET` | Gate.io | API认证 |

---

## API接口

### 1. 实时市场数据 + 跨交易所扫描
```
POST https://api.neurodoc.app/aetherlang/execute
Content-Type: application/json
```
```json
{
  "code": "flow CryptoScan {\n  using target \"neuroaether\" version \">=0.3\";\n  input text query;\n  node Scanner: crypto exchanges=\"all\", language=\"en\";\n  output text result from Scanner;\n}",
  "query": "BTC ETH SOL"
}
```

### 2. APEX Hyper-Council分析
```json
{
  "code": "flow ApexAnalysis {\n  using target \"neuroaether\" version \">=0.3\";\n  input text query;\n  node Apex: crypto mode=\"analysis\", language=\"en\";\n  output text result from Apex;\n}",
  "query": "Full APEX analysis for BTC ETH SOL"
}
```

### 3. 交易蓝图PDF报告
```json
{
  "code": "flow Blueprint {\n  using target \"neuroaether\" version \">=0.3\";\n  input text query;\n  node Report: crypto mode=\"blueprint\", language=\"en\";\n  output text result from Report;\n}",
  "query": "Generate trading blueprint for BTC"
}
```

---

## 支持的交易所

| 交易所 | 可用数据 | 是否需要认证 |
|----------|---------------|---------------|
| CoinGecko | 价格、市值、成交量、历史最高价 | 不需要（免费 tier） |
| Binance | 买卖价格、价差、成交量 | 可选 |
| Bybit | 买卖价格、价差、成交量 | 可选 |
| KuCoin | 买卖价格、价差 | 可选 |
| MEXC | 买卖价格、价差、成交量 | 可选 |
| Gate.io | 买卖价格、价差、成交量 | 可选 |

---

## Hyper-Council分析师

| 分析师 | 职责 | 权重范围 | 是否有否决权 |
|-------|------|-------------|----------|
| MACRO | 全球宏观策略师 | -100至+100 | 否 |
| QUANT | 量化研究负责人 | -100至+100 | 否 |
| STATS | 首席统计师 | -100至+100 | 否 |
| RISK (Damocles) | 首席风险官 | -100至+100 | **是** |
| EXECUTION | 执行架构师 | 0（信息提供者） | 否 |

---

## 安全架构

**数据处理**：仅将汇总的市场价格和查询文本发送到api.neurodoc.app。交易所的API密钥不会离开本地环境。

- **用户自行管理密钥**：用户密钥仅在本地使用，不会被传输到NeuroAether
- **仅读权限**：该工具仅用于读取市场数据，不会执行任何交易
- **无数据存储**：API密钥每次请求后都会被销毁
- **输入验证**：所有查询内容都会经过清洗，长度限制为5000个字符
- **请求限制**：免费 tier每小时100次请求

### 该工具不提供的功能
- ❌ 不执行交易或下达订单
- ❌ 不转移资金或进行提款
- ❌ 不存储或记录API密钥
- ❌ 不提供财务建议（仅提供分析结果）

---

## 语言支持

- **英语**（默认）
- **希腊语**（Ελληνικά）——添加`language="el"`即可启用

## 技术架构

- **后端**：FastAPI + Python 3.12（[源代码](https://github.com/contrario/aetherlang)）
- **AI模型**：通过OpenAI提供的GPT-4o
- **数据来源**：CoinGecko、Binance、Bybit、KuCoin、MEXC、Gate.io
- **PDF生成工具**：WeasyPrint + Matplotlib
- **托管服务**：Hetzner EU（符合GDPR法规）

---

## 免责声明

⚠️ 本工具提供的AI市场分析仅用于教育和信息目的，不构成财务建议。加密货币交易存在显著风险。在做出投资决策前，请务必自行进行研究并咨询合格的财务顾问。

---
*由NeuroAether开发——为所有人提供机构级智能分析服务* 🧠📊