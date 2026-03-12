---
name: Facebook Marketplace
slug: facebook-marketplace
version: 1.0.0
homepage: https://clawic.com/skills/facebook-marketplace
description: 在 Facebook Marketplace 上进行买卖时，您可以享受到价格管理的便利性、更安全的消息交流、完善的运输保障机制、欺诈检测功能以及保护账户安全的工作流程。
changelog: Initial release with buyer, seller, shipping, policy, and interface guidance for Facebook Marketplace.
metadata: {"clawdbot":{"emoji":"🛍️","requires":{"bins":[]},"os":["darwin","linux","win32"],"configPaths":["~/facebook-marketplace/"]}}
---
## 使用场景

当用户需要实时获得Facebook Marketplace的实际帮助时，例如寻找优质的本地商品、筛选欺诈性商品信息、撰写或修改商品信息、处理买家消息、安排取货、决定运输方式，或解决账户警告问题时，可以使用此技能。需要注意的是，所提供的建议必须符合Facebook Marketplace在公共网页、登录网页和移动端上的实际运作规则，而不能采用通用的电子商务建议。

## 架构

相关数据存储在`~/facebook-marketplace/`目录下。如果该目录不存在，请运行`setup.md`文件进行初始化。具体目录结构请参考`memory-template.md`文件。

```text
~/facebook-marketplace/
|-- memory.md          # Core profile, area, goals, and durable operating rules
|-- saved-searches.md  # Buyer watchlists, search specs, and go/no-go filters
|-- inventory.md       # Seller inventory, ask prices, floor prices, and stale listing notes
|-- message-lab.md     # Reusable reply patterns, offer rules, and no-show handling
|-- incident-log.md    # Scams, disputes, cancellations, and blocked patterns
`-- account-health.md  # Warnings, listing removals, appeals, and stop conditions
```

## 快速参考

仅加载当前操作过程中所需的文件：

| 主题 | 文件名 |
|-------|------|
| 设置指南 | `setup.md` |
| 内存结构与状态模型 | `memory-template.md` |
| 买家搜索、筛选与取货流程 | `buyer-flow.md` |
| 商品信息质量、定价与销售策略 | `listing-and-pricing.md` |
| 买家与卖家之间的消息交流 | `messages-and-negotiation.md` |
| 运输、证据收集与交易保护 | `shipping-and-protection.md` |
| 政策、警告与账户健康状态 | `policy-and-account-health.md` |
| 界面与自动化限制 | `interface-and-automation.md` |

## 操作范围

此技能整合了四个核心层面：
- **买家层面**：包括搜索条件、商品价值评估、卖家资质审核、谈判以及安全的取货计划。
- **卖家层面**：涉及商品信息创建、定价、买家筛选、商品保留政策以及销售时机决策。
- **保护层面**：包括欺诈检测、支付安全机制、证据收集以及问题升级流程。
- **账户健康层面**：涵盖政策检查、违规行为规避，以及在商品被删除或出现警告时的应对措施。

## 数据存储

`~/facebook-marketplace/`目录下的本地数据可能包含以下内容：
- 买家搜索的地理位置范围、类别偏好及预算信息；
- 卖家库存信息、商品底价、更新规则及默认取货选项；
- 可复用的消息模板、报价阈值以及未到场的处理规则；
- 欺诈行为指标、商品被删除的原因以及申诉流程的相关证据。

## 核心规则

### 1. 先明确操作对象
在提供任何建议之前，首先要确定当前的操作对象（买家、普通本地卖家、频繁交易的卖家，或是处于账户恢复/安全模式中的卖家）。不同的操作对象可能需要不同的处理策略。

### 2. 区分公共网页、登录网页和移动端
Facebook Marketplace在不同界面上的行为有所不同：
- 公共网页提供浏览、分类、搜索和商品展示功能；
- 登录网页处理活跃用户的交易流程；
- 移动端可能具备桌面端未有的功能。

切勿假设所有功能在三个平台上都通用。

### 3. 根据实际情况定价
定价时应参考周边类似商品的价格、商品状况、完整性、季节性因素以及取货的便利程度。对于体积大或价值低的商品，运输距离和取货难度可能比价格更为重要。

### 4. 以证据为基础进行沟通
在推进交易前，务必确认关键细节（如商品状况、完整性、具体型号/尺寸、是否可用以及取货/运输限制）。切勿仅依赖模糊的卖家或买家回复作为决策依据。

### 5. 有意识地选择取货方式
对于体积大、易碎、紧急或利润空间小的商品，通常建议选择本地取货。只有在考虑过运输成本、包装风险以及平台提供的保护措施后，才考虑使用运输方式。

### 6. 安全优先于速度
如果出现欺诈迹象、压力、平台外的支付请求、虚假的紧急情况或身份信息不匹配等问题，应暂停优化流程，评估风险并推荐最安全的下一步行动。

### 7. 禁止使用未经授权的自动化工具或规避账户限制
不得自行开发用于消费者买卖的API、命令行工具（CLI）或图谱（Graph）接口。也不得推荐使用机器人、登录后进行数据抓取的行为、批量发送消息的操作，或任何反检测策略。

## Facebook Marketplace 的常见陷阱
- 将所有商品都视为当前库存进行管理会导致资源浪费并影响定价准确性；
- 对仅限本地销售的商品使用全国范围内的价格参考会导致商品无法在本地售出；
- 允许买家或卖家过早将支付或证据信息移出平台会增加欺诈风险；
- 撰写含糊不清的商品描述会降低买家信任度；
- 接受不准确的运输信息会导致利润大幅减少；
- 在收到警告后随意重新发布、复制或编辑商品信息会加剧账户风险；
- 误以为Meta提供了支持这些操作的API或CLI接口会导致自动化方案失效。

## 外部接口
仅允许使用以下接口：
| 接口地址 | 发送的数据 | 用途 |
|------------|-----------|---------|
| https://www.facebook.com | 用户授权的搜索词、商品浏览记录、商品草稿、消息内容及交易相关操作 | 用于市场浏览、商品管理和账户操作 |
| https://www.messenger.com | 用户授权的市场消息内容和对话记录 | 通过Messenger继续市场交易 |
| https://www.facebook.com/help | 用户授权的文章查询和政策咨询 | 用于验证功能可用性、政策信息及支持指南 |

其他数据不会被发送到外部。

## 安全与隐私
- 本技能默认不会向外部发送任何数据；
- 仅在用户明确授权的情况下，才会通过Facebook或Messenger传输相关数据。

**存储的数据**：
- 存储在`~/facebook-marketplace/`目录下的本地数据包括：操作上下文、内存信息、搜索参数、库存记录、消息模板、事件日志以及账户健康状态信息。

**注意事项**：
- 本技能不会要求用户提供密码、一次性验证码、银行卡信息或身份证明文件；
- 不会为了方便而将支付、押金或争议处理流程转移到平台外；
- 未经用户明确授权，不会自动执行高风险操作或绕过平台限制；
- 不会提供任何绕过限制、规避检测或创建虚假账户的机制。

## 信任机制
使用本技能时，数据可能会通过Facebook Marketplace和Messenger传输给Meta。请确保您信任Meta来处理您的商品信息、消息和交易数据。

## 技能范围
- 本技能仅用于规范Facebook Marketplace上的买卖流程，明确下一步操作；
- 帮助用户合理定价、沟通、筛选商品信息、记录交易过程，并确保操作的安全性；
- 通过本地数据存储和专注的操作流程保持操作的连贯性。

**注意事项**：
- 本技能不保证一定能促成交易、确保商品售出或满足运输条件，也不保证能使用未经授权的API或CLI；
- 不会帮助用户规避平台限制或冒充他人；
- 不会协助用户进行高风险操作。

## 相关技能
如用户同意，可使用以下命令进行安装：
- `clawhub install marketplace`：用于比较不同平台（包括Facebook Marketplace）上的买家/卖家操作流程；
- `clawhub install buy`：在需要更严格买家审核的情况下优化购买决策；
- `clawhub install sell`：加强商品信息管理、定价策略以及跨渠道的成交流程；
- `clawhub install pricing`：设置商品底价、谈判范围及基于利润空间的折扣规则；
- `clawhub install ecommerce`：将本地市场操作扩展到更广泛的电子商务系统中。

## 用户反馈
- 如觉得本技能有用，请给`clawhub facebook-marketplace`打星评价；
- 如需获取最新更新，请使用`clawhub sync`命令。