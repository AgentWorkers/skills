---
name: tax
description: **XPR网络的加密税务报告功能（支持多地区）**  

**概述：**  
XPR网络提供了加密资产的税务报告功能，帮助用户根据所在地区的法规要求，准确申报与加密货币交易相关的税务。该功能支持多地区设置，用户可以根据自己的实际居住地或业务所在地进行配置。  

**主要特点：**  
1. **多地区支持**：用户可以根据自己的居住地或业务所在地，选择相应的税务报告设置。  
2. **自动计算**：系统会根据用户的交易记录，自动计算应缴纳的税款。  
3. **详细报告**：生成的税务报告包含所有相关的交易信息，便于用户进行税务申报。  
4. **合规性保障**：确保用户的税务报告符合所在地区的法律法规要求。  

**使用步骤：**  
1. **登录XPR网络**：使用您的用户名和密码登录XPR网络。  
2. **进入设置页面**：点击个人账户页面，找到“税务设置”选项。  
3. **选择地区**：根据您的居住地或业务所在地，选择相应的地区设置。  
4. **配置报告参数**：根据当地税法要求，配置报告的相关参数（如税率、免税额度等）。  
5. **生成报告**：系统会自动生成税务报告。  
6. **下载报告**：将报告下载并保存，以便用于税务申报。  

**注意事项：**  
- 请确保您的交易记录完整且准确，以便税务报告的生成。  
- 如有疑问，请咨询专业的税务顾问。  

**了解更多：**  
- [访问XPR网络官网了解更多关于税务报告的详细信息](https://www.xprnetwork.com/support/tax-reporting)  

**技术支持：**  
如在使用过程中遇到任何问题，请联系XPR网络的客服团队或技术支持团队。  

---  

（翻译说明：  
1. 保持原文的格式和结构，包括标题、段落和列表。  
2. 使用中文术语替换英文术语（如“crypto tax reporting”译为“加密税务报告”，“API”译为“API”等）。  
3. 对技术细节进行准确翻译，如“auto-compute taxes”译为“自动计算税款”。  
4. 对长句进行适当拆分，以便阅读更加流畅。）
---

## 加密货币税务报告

您可以使用相关工具根据XPR网络的链上交易记录生成加密货币税务报告。该工具支持**新西兰**（NZ）和**美国**（US）的税务报告生成。

### 主要信息

- **新西兰的纳税年度：**4月1日至3月31日（例如，“2025”表示2024年4月1日至2025年3月31日）
- **美国的纳税年度：**1月1日至12月31日（按日历年份计算，例如，“2024”表示2024年1月1日至12月31日）
- **新西兰没有资本利得税**——对于普通交易者而言，所有加密货币收益均按**收入**征税
- **美国有资本利得税**：短期（<1年）收益按普通收入征税，长期收益按较低税率征税。使用2024年的联邦税率等级。报告不包含州税或NIIT（国家所得税）。
- **成本计算方法：**先进先出（FIFO）或平均成本法
- **所有工具均为只读模式**——它们仅用于查询API和计算数据，不进行任何交易操作
- **默认地区为新西兰**——如需生成美国税务报告，请设置`region: "US"`

### 典型工作流程

为了生成完整的税务报告，建议按照以下顺序执行步骤：

1. `tax_get_balances`：获取纳税年度初和年末的账户余额
2. `tax_get_dex_trades`：获取该期间的所有Metal X DEX交易记录
3. `tax_get_transfers`：获取链上转账记录（自动分类，包括质押奖励、借贷、交换、NFT销售等）
4. `tax_get_rates`：获取每种代币的本地货币兑换率
5. `tax_calculate_gains`：使用FIFO或平均成本法计算应纳税收益/损失
6. `tax_generate_report`：生成包含税率等级和预估税额的完整报告

或者直接使用`tax_generate_report`来一次性完成所有步骤的自动报告生成。

### 数据来源（仅限主网）

- **Saltant API**：获取历史账户余额快照（包括流动性资产、质押资产、借贷资产）
- **Metal X API**：以CSV格式提供DEX交易记录
- **Hyperion API**：提供原始的链上转账/操作记录
- **CoinGecko API**：提供历史和当前的加密货币价格（在`.env`文件中设置`COINGECKO_API_KEY`以获取完整的历史数据）

### 转账类别

转账记录会根据发送方/接收方自动分类：

| 类别 | 识别依据 |
|----------|-----------|
| `staking_reward` | 来自`eosio`或`eosio.vpay`的转账 |
| `lendingdeposit` | 转入`lending.loan` |
| `lending_withdrawal` | 从`lending.loan`取出 |
| `lending_interest` | 来自`lending.loan`且带有利息信息的转账 |
| `swap_deposit` | 转入`proton.swaps` |
| `swap_withdrawal` | 从`proton.swaps`取出 |
| `long_stake` | 转入`longstaking`（XPR长期质押） |
| `long_unstake` | 从`longstaking`取出 |
| `loan_stake` | 转入`lock.token`或`yield.farms`（贷款/质押） |
| `loan_unstake` | 从`lock.token`或`yield.farms`取出 |
| `dexdeposit` | 转入`dex`或`metalx` |
| `dex_withdrawal` | 从`dex`或`metalx`取出 |
| `nft_sale` | 来自`atomicmarket`的NFT销售记录 |
| `nft_purchase` | 转入`atomicmarket`的NFT购买记录 |
| `burn` | 转入`eosio.null`（代币销毁即视为损失） |
| `escrow` | 转入/转出`agentescrow` |
| `transfer` | 其他所有类型的转账 |

### 质押收益规则

- **区块生产者奖励（`staking_reward`）**：收到奖励时全额计入收入
- **长期质押（`longstaking`）**：仅超出质押数量的收益计入收入。例如：质押100 XPR，取出150 XPR，则收入为50 XPR
- **贷款质押（`lock.token`/`yield.farms`）**：同样适用超出质押数量的收益规则
- **借贷利息**：`lending.loan`中带有利息信息的全部金额计入收入

### 安定币处理

XUSDC和XMD与美元挂钩——它们的本地货币价值直接使用外汇汇率（USD/NZD）进行转换，不依赖CoinGecko的价格数据。这种方法比基于市场的定价更准确。

### 汇率来源（优先级顺序）

1. **DEX交易**：根据TOKEN/XMD的交易比率获取代币价格（最准确，无API使用限制）
2. **前向填充（Forward-fill）**：在DEX交易日期之间使用最近的可用汇率
3. **CoinGecko**：在没有DEX数据的日期时作为备用来源。如果没有`COINGECKO_API_KEY`，则数据覆盖范围为365天；使用`COINGECKO_API_KEY`可获取无限历史数据
4. **外汇汇率**：用于稳定币的USD→NZD转换

### 报告交付方式

`tax_generate_report`函数返回一个`report_markdown`字段，该字段是一个预格式化的Markdown文档，包含资产负债表、交易摘要、收入明细、税率等级和免责声明。交付方式如下：

1. 通过`store_deliverable`上传`report_markdown`文件，设置`content_type: "application/pdf"`——这是主要的交付文件
2. 通过`store_deliverable`上传`csv_exports.disposals`文件，设置`content_type: "text/csv"`——包含交易明细的CSV文件
3. 通过`store_deliverable`上传`csv_exports.income`文件，设置`content_type: "text/csv"`——包含收入明细的CSV文件
4. 调用`xpr_deliver_job`函数，并传入所有文件的URL（以逗号分隔，PDF文件优先）：`"https://ipfs.io/ipfs/QmPDF...,https://ipfs.io/ipfs/QmDisposals...,https://ipfs.io/ipfs/QmIncome..."`

**重要提示：**您必须一次性完成所有步骤（上传文件和交付报告）。上传PDF文件后不要停止操作，还需上传CSV文件并调用`xpr_deliver_job`函数。只有当`xpr_deliver_job`被调用后，任务才算完成。

前端会突出显示主要报告文件（PDF格式），并列出其他可下载文件的链接。

### 已知的限制

- 仅包含**已完成的DEX交易**（不包括待处理的订单）
- NFT仅支持买入/卖出操作（不支持拍卖）
- 不支持Metal Lending的清算交易
- 虽然会追踪托管支付记录，但未对其进行详细分类
- 历史价格的准确性取决于DEX的交易活跃度和CoinGecko的数据可用性

### 重要注意事项

- 请务必在报告中包含免责声明——本工具提供的信息不构成税务建议
- 建议用户保存CSV文件，以满足IRD（Income Tax Return，所得税申报）的7年记录要求
- 所有工具的默认地区设置为“新西兰”；如需生成其他地区的报告，请指定相应的地区代码
- 为获取最准确的历史价格，请在`.env`文件中设置`COINGECKO_API_KEY`（免费试用密钥的使用期限为365天）
- 对于CoinGecko未收录的代币，工具会根据Metal X DEX的交易比率来计算价格