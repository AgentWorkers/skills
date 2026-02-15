---
name: polymarket-auto-trader
description: **自主型 Polymarket 预测市场交易代理**  
该代理能够自动扫描市场，利用大型语言模型（LLM）评估交易概率，根据 Kelly 准则确定交易头寸，并通过 CLOB API 执行交易。适用于用户希望在 Polymarket 上进行交易、设置自动化预测市场交易系统或构建交易机器人的场景。支持基于 Cron 表达式的自动运行机制，具备盈亏（P&L）跟踪和预算管理功能。
metadata: {"openclaw": {"requires": {"env": ["PRIVATE_KEY", "LLM_API_KEY"]}, "primaryEnv": "LLM_API_KEY", "homepage": "https://github.com/srikanthbellary"}}
---

# Polymarket自动交易系统

这是一个完全自主的预测市场交易代理，专为Polymarket设计。该系统利用大型语言模型（LLM）进行市场评估，根据Kelly准则确定交易头寸大小，并通过Polymarket的CLOB API在非美国地区的VPS上执行交易。

## 先决条件

- **非美国地区的VPS**：Polymarket禁止美国IP地址的使用。建议使用DigitalOcean Amsterdam、Hetzner EU等提供商的VPS。
- **Polygon钱包**，并绑定USDC.e（这是一种桥接后的USDC形式，而非原生USDC）。
- **MATIC**作为交易手续费（大约0.1 MATIC即可支持数百次交易）。
- **Anthropic API密钥**（使用Haiku服务，每次评估费用约为0.001美元）。

## 设置

### 1. VPS环境

通过SSH连接到你的非美国VPS，并运行以下命令：
```bash
python3 {baseDir}/scripts/setup_vps.sh
```

或者手动配置：
```bash
apt update && apt install -y python3 python3-venv
python3 -m venv /opt/trader
/opt/trader/bin/pip install py-clob-client python-dotenv web3 requests
```

### 2. 配置文件

创建`/opt/trader/app/.env`文件，并配置相关环境变量：
```
PRIVATE_KEY=<your-polygon-wallet-private-key>
LLM_API_KEY=<your-anthropic-api-key>
```

### 3. 区块链权限审批

在开始交易之前，需要为Polymarket的合约审批USDC.e和CTF代币的交易权限。运行以下命令：
```bash
python3 {baseDir}/scripts/approve_contracts.py
```

所需审批的权限（共6项）：
- USDC.e → CTF交易所、Neg Risk交易所、Neg Risk适配器
- CTF → CTF交易所、Neg Risk交易所、Neg Risk适配器

### 4. 部署交易脚本

将交易脚本部署到相应的位置：
```bash
cp {baseDir}/scripts/run_trade.py /opt/trader/app/
cp {baseDir}/scripts/pnl_tracker.py /opt/trader/app/
```

### 5. 定时任务自动化

设置定时任务以自动执行交易逻辑：
```bash
crontab -e
# Add: */10 * * * * cd /opt/trader/app && /opt/trader/bin/python3 run_trade.py >> cron.log 2>&1
```

## 工作原理

1. **市场扫描**：从Gamma API获取活跃市场列表，并根据流动性及时间范围进行筛选。
2. **LLM评估**：使用Claude Haiku模型估算每个市场的真实概率。
3. **价格检测**：比较LLM预测的公允价值与市场价格（最低价格差异阈值为5%）。
4. **头寸调整**：根据Kelly准则确定交易规模，同时设置最大头寸为25%。
5. **订单执行**：通过CLOB API以GTC（Good-Till-Cancelled）方式下达限价单。
6. **去重处理**：将所有交易记录保存在`trades.jsonl`文件中，并跳过已交易过的市场。
7. **预算管理**：将LLM推理成本与交易资金分开管理。

## 交易参数

这些参数可以在`run_trade.py`文件中进行配置：
- `EDGE_THRESHOLD`：最低可交易的价格差异阈值（默认值：0.05，即5%）。
- `MINSHARES`：最小订单数量（Polymarket要求至少5个份额）。
- 资金分配：80%可用于交易，每次交易最多使用25%，单个头寸不超过30%。
- 交易时间范围：优先考虑30天内到期的市场。

## 监控

- 随时查看盈亏情况：```bash
python3 /opt/trader/app/pnl_tracker.py
```
- 查看近期交易活动：```bash
tail -50 /opt/trader/app/cron.log
```

## 关键技术细节

- **钱包类型**：使用EOA（Externally Owned Account，signature_type=0），而非代理钱包。
- **交易代币**：使用USDC.e（地址：`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生USDC。
- **高风险市场**（如选举相关市场或体育联赛）需要使用USDC.e进行Neg Risk Adapter的权限审批（地址：`0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296`）。
- **地理限制**：所有API请求必须来自非美国地区的IP地址。使用VPN无法绕过这一限制，必须使用实际的非美国VPS。

## 成本

- LLM推理费用：每次市场评估约0.001美元（使用Haiku服务）。
- 整个交易周期（包含40次评估）的总成本约为0.04美元。
- Polygon平台的交易手续费：每次交易约0.001美元。

## ⚠️ 安全注意事项

- **使用专用钱包并仅投入少量资金**：切勿使用你的主钱包的私钥。请创建一个新的钱包，并仅投入你能承受的风险金额。
- **私钥存储方式**：私钥存储在`.env`文件中。确保VPS的安全性（设置严格的文件权限`chmod 600 .env`），禁止共享访问，并使用SSH密钥进行连接。
- **权限设置**：虽然DeFi平台通常允许广泛的交易权限，但此处授予的权限较为广泛。在运行前请仔细检查`references/contract-addresses.md`文件中的合约地址。
- **先从小额资金开始测试**（建议5-10美元），再逐步增加交易金额。
- **持续监控**：定期检查`cron.log`日志，并运行`pnl_tracker.py`程序。
- **费用问题**：每次使用Anthropic API的费用约为0.04美元。请在Anthropic账户中设置费用提醒。
- **本系统为自动交易工具**：可能存在漏洞或市场风险，使用前请自行承担风险。

## 参考资料

- 详细了解CLOB API的文档：`references/polymarket-api.md`
- 查看所有Polygon合约的地址：`references/contract-addresses.md`