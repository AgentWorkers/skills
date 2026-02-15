# APEX Crypto Intelligence — 多交易所交易分析工具

> 该工具提供机构级别的加密货币市场分析服务，支持5家交易所的数据，结合AI驱动的Hyper-Council智能分析以及对冲基金级别的PDF报告。

**源代码**: [github.com/contrario/aetherlang](https://github.com/contrario/aetherlang/tree/main/skills/apex-crypto-intelligence)
**官方网站**: [neurodoc.app](https://neurodoc.app)
**作者**: NeuroAether (info@neurodoc.app)
**许可证**: MIT
**版本**: 0.1.0

## 概述

APEX Crypto Intelligence是一款多交易所加密货币分析工具，能够从CoinGecko、Binance、Bybit、KuCoin、MEXC和Gate.io获取实时市场数据，进行跨交易所套利检测，并通过由5位专业分析师组成的Hyper-Council提供AI驱动的机构级交易分析服务。

---

## 隐私与数据处理

⚠️ **用户自行管理密钥（BYOK, Bring Your Own Keys）**：工具仅在本机使用交易所API密钥来获取数据，这些密钥**不会被传输**到NeuroAether。

⚠️ **外部API说明**：仅将市场数据（价格、成交量）和查询文本发送到`api.neurodoc.app`进行AI分析。

**可审计的代码**：请查看[`client.py`](https://github.com/contrario/aetherlang/blob/main/skills/apex-crypto-intelligence/client.py)文件中的`build_api_request()`函数，该函数展示了发送给API的**确切数据内容**。在发送请求前，请运行`python client.py`来检查数据内容。

- **发送内容**：仅包含聚合的市场价格和自然语言查询（详见`client.py`文件第109行）。
- **不发送的内容**：交易所API密钥、凭证、个人数据、钱包地址。
- **数据存储**：查询数据会实时处理，不会被保存。
- **托管服务**：使用Hetzner EU服务器（符合GDPR法规）。

**重要提示**：用户必须将交易所API密钥设置为**仅读**权限，切勿启用任何交易相关权限。

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

1. **跨交易所扫描器**：实时获取Binance、Bybit、KuCoin、MEXC、Gate.io的买卖价格。
2. **套利检测**：自动分析所有5家交易所的价差情况。
3. **APEX Hyper-Council分析**：由5位AI分析师（包括宏观策略师、量化研究员、风险主管、执行架构师和监管分析师）提供分析意见。
4. **交易分析报告**：生成包含SWOT分析、雷达图、盈亏预测和实施路线的PDF报告。
5. **多币种支持**：支持BTC、ETH、SOL、XRP、DOGE、ADA、DOT、AVAX、MATIC、BNB、LTC、LINK、TRX、SHIB、SUI、APT、TON、NEAR、UNI、PEPE等币种。

---

## 配置（用户自行管理密钥）

用户需要通过环境变量提供自己的API密钥。所有密钥都是可选的——该工具默认使用CoinGecko的免费数据，同时也可以使用多个交易所的数据。

### 必需的环境变量

无需额外环境变量。该工具在使用CoinGecko的免费数据时即可正常运行。

### 可选的环境变量

| 变量          | 交易所        | 用途                |
|---------------|-----------------|-------------------|
| `BINANCE_API_KEY`    | Binance       | 市场数据（仅读）          |
| `BINANCE_API_SECRET`    | Binance       | API认证              |
| `BYBIT_API_KEY`    | Bybit        | 市场数据（仅读）          |
| `BYBIT_API_SECRET`    | Bybit        | API认证              |
| `KUCOIN_API_KEY`    | KuCoin        | 市场数据（仅读）          |
| `KUCOIN_API_SECRET`    | KuCoin        | API认证              |
| `MEXC_API_KEY`    | MEXC        | 市场数据（仅读）          |
| `MEXC_API_SECRET`    | MEXC        | API认证              |
| `GATEIO_API_KEY`    | Gate.io       | 市场数据（仅读）          |
| `GATEIO_API_SECRET`    | Gate.io       | API认证              |

---

## API接口

### 1. 实时市场数据 + 跨交易所扫描器
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

### 3. 交易分析报告PDF
```json
{
  "code": "flow Blueprint {\n  using target \"neuroaether\" version \">=0.3\";\n  input text query;\n  node Report: crypto mode=\"blueprint\", language=\"en\";\n  output text result from Report;\n}",
  "query": "Generate trading blueprint for BTC"
}
```

---

## 支持的交易所

| 交易所        | 可获取的数据        | 是否需要认证           |
|--------------|-----------------|----------------------|
| CoinGecko     | 价格、市值、成交量、历史最高价 | 不需要（免费 tier）         |
| Binance      | 买卖价格、价差、成交量    | 可选                 |
| Bybit        | 买卖价格、价差、成交量    | 可选                 |
| KuCoin        | 买卖价格、价差        | 可选                 |
| MEXC        | 买卖价格、价差、成交量    | 可选                 |
| Gate.io       | 买卖价格、价差、成交量    | 可选                 |

---

## Hyper-Council分析师

| 分析师角色      | 职责                | 权重范围            | 是否有否决权           |
|--------------|------------------|------------------|----------------------|
| MACRO        | 全球宏观策略师       | -100至+100            | 否                    |
| QUANT        | 量化研究负责人       | -100至+100            | 否                    |
| STATS        | 首席统计师         | -100至+100            | 否                    |
| RISK (Damocles)   | 首席风险官         | -100至+100            | 是                    |
| EXECUTION    | 执行架构师         | 0（信息提供者）          | 否                    |

---

## 安全架构

**可审计的代码**：请查看[`client.py`](https://github.com/contrario/aetherlang/blob/main/skills/apex-crypto-intelligence/client.py)文件中的`build_api_request()`函数，以验证发送给API的数据内容。

- **用户密钥仅在本机使用，不会被传输**。
- **工具仅读取市场数据，不执行任何交易操作**。
- **API密钥按请求使用，不会被保存**。
- **输入验证**：所有查询内容都会被净化处理，长度限制为5000个字符。
- **免费 tier下的请求限制**：每小时100次请求。

### 该工具不提供的功能
- ❌ 不执行任何交易或下达订单。
- ❌ 不进行资金转移或提取。
- ❌ 不存储或记录API密钥。
- ❌ 不提供财务建议（仅提供分析结果）。

---

## 语言支持

- **英语**（默认）
- **希腊语（Ελληνικά）**：通过设置`language="el"`启用

## 技术架构

- **后端**：FastAPI + Python 3.12（[源代码](https://github.com/contrario/aetherlang)）
- **AI模型**：使用OpenAI的GPT-4o模型
- **数据来源**：CoinGecko、Binance、Bybit、KuCoin、MEXC、Gate.io
- **PDF生成工具**：WeasyPrint + Matplotlib
- **托管服务**：Hetzner EU（符合GDPR法规）

---

## 免责声明

⚠️ 本工具提供的市场分析结果由AI生成，仅用于教育和信息参考目的，不构成任何财务建议。加密货币交易存在显著风险。在做出投资决策前，请务必自行进行充分研究并咨询专业金融顾问。

---
*由NeuroAether开发——为所有人提供机构级智能分析服务* 🧠📊