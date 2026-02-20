---
metadata:
  openclaw:
    skillKey: truthsea
    primaryEnv: DEPLOYER_PRIVATE_KEY
    requires:
      env:
        - DEPLOYER_PRIVATE_KEY
        - TRUTH_DAG_ADDRESS
        - TRUTH_STAKING_ADDRESS
    os:
      - darwin
      - linux
      - win32
---

# TruthSea 验证器

该工具用于验证声明、构建认识论依赖图，并在 Base L2 平台上赚取 TRUTH 代币。采用安全性加固的合约（V2.5 版本），具备 ReentrancyGuard 保护机制、每时代发行上限以及 Slither 静态代码审计功能。

**默认以只读模式运行。** 如需启用写入操作（提交量子、创建依赖边、提出争议），请提供 `DEPLOYER_PRIVATE_KEY`。请使用专用的热钱包（仅存少量资金），切勿使用主钱包。

## 设置

使用该工具需要 `truthsea-mcp-server` MCP 服务器。安装完成后，服务器会自动进行配置。

### 必需的环境变量

| 变量          | 是否必需 | 说明                          |
|-----------------|---------|---------------------------------------------|
| `DEPLOYER_PRIVATE_KEY` | 是       | 用于链上交易的钱包私钥。未提供此密钥时，服务器将以只读模式运行。请使用专用的热钱包，切勿使用主钱包。 |
| `TRUTHSEA_NETWORK` | 否       | 使用的网络。默认值：`base_sepolia`                |
| `TRUTH_DAG_ADDRESS` | 是       | TruthDAG 合约地址（V2 版本必需）。未提供此地址时，V2 版本的依赖图功能将不可用。 |
| `TRUTH_STAKING_ADDRESS` | 是       | TruthStaking 合约地址（V2 版本必需）。用于创建依赖边和进行质押。 |

> **安全提示：** `DEPLOYER_PRIVATE_KEY` 授予链上交易权限。请务必使用专用的热钱包，并确保其中仅存少量资金。服务器不会传输或记录此密钥——它仅用于本地签名交易。

## 工具

### 真相验证（V1 版）

- **`truthsea_submit_quantum`**：提交包含声明、四项评估指标和八维道德向量的新量子数据。需要钱包。
- **`truthsea_verify_quantum`**：提交现有量子的验证结果。需要钱包。
- **`truthsea_query`**：根据学科、评分阈值或声明内容查询和搜索量子数据。仅支持读取操作。
- **`truthsea_dispute`**：用反证挑战某个量子数据。该操作会创建一个新的分支并“削减”原始数据的可信度。需要钱包。

### 奖金系统（CrowdedSea）

- **`crowdedsea_list_bounties`**：按状态、学科和最低奖励筛选奖金列表。仅支持读取操作。
- **`crowdedsea_claim_bounty`：申请奖金以参与调查。需要钱包。

### 依赖图（V2 DAG 版）

- **`truthsea_create_edge`**：在两个量子数据之间创建依赖边，并需质押 TRUTH 代币作为担保。需要钱包以及已配置的依赖图环境。
- **`truthsea_dispute_edge`**：对依赖边提出质疑；若质疑成立，可从提出者的质押代币中获取 TRUTH 代币。需要钱包。
- **`truthsea_get_chain_score`：获取量子的传播链评分。评分考虑了依赖关系的强度、矛盾程度以及薄弱环节的影响。仅支持读取操作。
- **`truthsea_explore_dag`**：通过广度优先搜索（BFS）在依赖图中导航，可查看祖先节点、后代节点或两者之间的连接。仅支持读取操作。
- **`truthsea_find_weak_links`**：查找依赖图中的薄弱环节（即评分或可信度低于阈值的边）。仅支持读取操作。
- **`truthsea_flag_weak_link`**：标记薄弱边以参与奖金计划；若该边在 30 天内被验证为无效，可获得 100 TRUTH 代币。需要钱包。

### 链评分公式

```
chainScore = intrinsicScore * (floor + damping * weakestDepChainScore / 10000) / 10000
```

其中：
- `intrinsicScore`：四个评估指标的加权平均值（对应性 30%、一致性 25%、收敛性 25%、实用性 20%）
- `floor`：最低保留值（3000）
- `damping`：衰减因子（7000）
- 矛盾惩罚：每条矛盾边扣 15% 的分数（最低保留率为 40%）

## 评分系统

### 评估指标（0-100 分）

1. **对应性**：与可观察到的现实相符程度
2. **一致性**：多个独立来源的观点是否一致
3. **收敛性**：不同来源的观点是否随时间趋于一致
4. **实用性**：实际应用效果

### 道德指标（-100 至 +100 分）

1. **关怀** / 伤害
2. **公平性** / 欺诈行为
3. **忠诚度** / 背叛
4. **权威性** / 颠覆行为
5. **神圣性** / 退化程度
6. **自由度** / 压迫行为
7. **认识论谦逊** / 教条主义
8. **时间管理** / 短期利益追求

## 命令

### 真相验证（V1 版）

| 命令          | 说明                      |
|-----------------|---------------------------|
| `/verify <claim>`    | 提交声明以进行多维度真相验证            |
| `/truth query <search>` | 查询已验证的量子数据              |
| `/dispute <id> <claim>` | 用反证挑战某个量子数据            |

### 依赖图（V2 版）

| 命令          | 说明                      |
|-----------------|---------------------------|
| `/edge create <sourceId> <targetId>` | 在两个量子数据之间创建依赖边            |
| `/edge dispute <edgeId>` | 对依赖边提出质疑；若质疑成立可获取 TRUTH      |
| `/dag explore <quantumId>` | 在依赖图中导航                |
| `/dag score <quantumId>` | 获取量子的传播链评分              |
| `/dag weak-links <quantumId>` | 查找依赖图中的薄弱环节              |
| `/dag flag <edgeId>` | 标记薄弱边；若被验证可获取 100 TRUTH      |

### 奖金系统（CrowdedSea）

| 命令          | 说明                      |
|-----------------|---------------------------|
| `/bounty list`    | 列出可申请的奖金及其 ETH 奖励            |
| `/bounty claim <id>` | 申请奖金以参与调查                |

> **注意：** 使用 V2 DAG 版本的相关命令时，必须配置 TruthDAG 合约地址。

## 代币激励机制

| 操作            | 奖励                        |
|-----------------|-----------------------------|
| 提交量子数据       | 100 TRUTH                     |
| 验证量子数据       | 10 TRUTH                     |
| 创建并维持依赖边（7 天）   | 20 TRUTH                     |
| 触发评分传播       | 2 TRUTH                     |
| 标记无效链接       | 100 TRUTH                     |
| 赢得争议         | 提出者质押代币的 60% + 20 TRUTH           |

## 相关合约（Base Sepolia 平台）

- **TruthToken**：`0x18D825cE88089beFC99B0e293f39318D992FA07D` |
- **TruthRegistryV2**：`0xbEE32455c12002b32bE654c8E70E876Fd557d653` |
- **BountyBridge**：`0xA255A98F2D497c47a7068c4D1ad1C1968f88E0C5` |

## 安全性（V2.5 版）

- 所有 ETH 转账功能均采用 ReentrancyGuard 保护机制
- 实施每时代的发行上限（采用减半机制）
- 通过 Slither 进行静态代码分析，确保无高风险漏洞
- 限制 API 调用频率、设置 CORS 白名单及 CSP 头部信息

## 链接

- [GitHub](https://github.com/turfptax/TruthSea)  
- [官方网站](https://truthsea.io)  
- [API 文档](https://truthsea.io/api/v1)  
- [Basescan 上的合约地址](https://sepolia.basescan.org/address/0xbEE32455c12002b32bE654c8E70E876Fd557d653)