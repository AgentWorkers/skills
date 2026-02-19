# TruthSea 验证器

该工具用于验证各种声明，构建认识论依赖图，并通过 Base L2 上的链上评分系统获得 TRUTH 代币。所有合约均经过安全加固，采用了 ReentrancyGuard 技术，同时设置了每个时代的发行上限，并通过了 Slither 的代码审计。

## 设置

使用该工具需要 `truthsea-mcp-server` 这个 MCP 服务器。安装完成后，服务器会自动进行配置。

### 环境变量

| 变量          | 是否必填 | 说明                          |
|-----------------|---------|--------------------------------------|
| `DEPLOYER_PRIVATE_KEY` | 是      | 用于写入操作；缺少此密钥时，服务器将以只读模式运行。         |
| `TRUTHSEA_NETWORK` | 否       | 使用的网络；默认值为 `base_sepolia`                |
| `TRUTH_DAG_ADDRESS` | 是      | V2 DAG 合约地址；缺少此地址时，V2 DAG 功能将被禁用。         |
| `TRUTH_STAKING_ADDRESS` | 是      | V2 DAG 合约地址；创建依赖边时需要此地址。           |

## 工具

### 真相验证（V1）

- **`truthsea_submit_quantum`**：提交一个新的真相声明，包括声明内容、四项评估指标的得分以及八维的道德向量。需要钱包。  
- **`truthsea_verify_quantum`**：提交现有声明的验证结果。需要钱包。  
- **`truthsea_query`**：根据学科、得分阈值或声明内容查询和搜索声明。仅支持读取操作。  
- **`truthsea_dispute`**：用反证来挑战现有的声明；该操作会创建一个新的分支并削减原始声明的得分。需要钱包。  

### Bounty Bridge（CrowdedSea）

- **`crowdedsea_list_bounties`**：按状态、学科和最低奖励筛选赏金列表。仅支持读取操作。  
- **`crowdedsea_claim_bounty`：申请赏金以进行调查。需要钱包。  

### 依赖图（V2 DAG）

- **`truthsea_create_edge`**：在两个声明之间创建依赖关系；需要投入 TRUTH 代币作为抵押。需要钱包以及配置好的 DAG。  
- **`truthsea_dispute_edge`**：对依赖关系提出挑战；如果挑战成功，可以从提出者被削减的代币中获利。需要钱包。  
- **`truthsea_get_chain_score`**：获取声明的链上得分；该得分反映了依赖关系的强度、矛盾程度以及薄弱环节对得分的影响。仅支持读取操作。  
- **`truthsea_explore_dag`**：通过广度优先搜索（BFS）在祖先节点、后代节点或两者之间导航认识论依赖图。仅支持读取操作。  
- **`truthsea_find_weak_links`**：查找依赖图中的薄弱环节（即得分低于预设阈值的边）。仅支持读取操作。  
- **`truthsea_flag_weak_link`**：标记出需要奖励的薄弱环节；如果该环节在 30 天内被证明无效，可获得 100 TRUTH 代币。需要钱包。  

### 链上得分公式

```
chainScore = intrinsicScore * (floor + damping * weakestDepChainScore / 10000) / 10000
```

其中：  
- `intrinsicScore` = 四项评估指标的加权平均值（对应性 30%、一致性 25%、收敛性 25%、实用性 20%）  
- `floor` = 3000（最低保留分数）  
- `damping` = 7000（衰减因子）  
- 矛盾惩罚：每条矛盾边扣 15% 的分数（最低保留分数为 40%）  

## 评分系统

### 真相评估指标（0-100 分）

1. **对应性**：与可观察到的现实相符的程度  
2. **一致性**：多个独立来源的观点是否随时间保持一致  
3. **收敛性**：不同来源的观点是否逐渐趋于一致  
4. **实用性**：该观点在实践中是否有效  

### 道德向量（-100 到 +100 分）

1. **关怀** / 伤害  
2. **公平性** / 欺诈  
3. **忠诚度** / 背叛  
4. **权威性** / 颠覆  
5. **神圣性** / 退化  
6. **自由** / 压迫  
7. **认识论谦逊** / 教条主义  
8. **时间管理** / 短期利益追求  

## 命令

### 真相验证（V1）

| 命令        | 说明                                      |
|-------------|-----------------------------------------|
| `/verify <claim>`   | 提交一个声明以进行多维度验证                |
| `/truth query <search>` | 查询已验证的真相声明                    |
| `/dispute <id> <claim>` | 用反证挑战现有的声明                    |

### 依赖图（V2）

| 命令        | 说明                                      |
|-------------|-----------------------------------------|
| `/edge create <sourceId> <targetId>` | 在两个声明之间创建依赖关系                |
| `/edge dispute <edgeId>` | 对依赖关系提出挑战；成功时可获利                |
| `/dag explore <quantumId>` | 导航依赖图                          |
| `/dag score <quantumId>` | 获取声明的链上得分                    |
| `/dag weak-links <quantumId>` | 查找依赖图中的薄弱环节                    |
| `/dag flag <edgeId>` | 标记薄弱环节；若被验证可获 100 TRUTH 代币奖励         |

### 赏金系统（CrowdedSea）

| 命令        | 说明                                      |
|-------------|-----------------------------------------|
| `/bounty list`   | 列出可获得的真相赏金列表（以 ETH 为奖励单位）          |
| `/bounty claim <id>` | 申请赏金以进行调查                          |

> **注意：** 使用 V2 DAG 相关命令前，请确保已配置 `TruthDAG` 合约地址。  

## 代币激励机制

| 操作        | 奖励                                    |
|-------------|-----------------------------------------|
| 提交声明      | 100 TRUTH                                |
| 验证声明      | 10 TRUTH                                |
| 创建依赖关系（持续 7 天） | 20 TRUTH                                |
| 触发得分传播    | 2 TRUTH                                |
| 标记薄弱环节    | 100 TRUTH                                |
| 赢得争议      | 提出者代币的 60% + 20 TRUTH                     |

## 相关合约（基于 Sepolia）

- **TruthToken**: `0x18D825cE88089beFC99B0e293f39318D992FA07D`  
- **TruthRegistryV2**: `0xbEE32455c12002b32bE654c8E70E876Fd557d653`  
- **BountyBridge**: `0xA255A98F2D497c47a7068c4D1ad1C1968f88E0C5`  

## 安全措施（V2.5）

- 所有 ETH 转账功能均采用了 ReentrancyGuard 技术  
- 实施了每个时代的发行上限（遵循减半机制）  
- 代码经过了 Slither 的静态分析，未发现高风险问题  
- 提供 API 速率限制、CORS 白名单和 CSP 头部信息  

## 链接

- [GitHub](https://github.com/turfptax/TruthSea)  
- [官方网站](https://truthsea.io)  
- [API 文档](https://truthsea.io/api/v1)  
- [Basescan 上的合约地址](https://sepolia.basescan.org/address/0xbEE32455c12002b32bE654c8E70E876Fd557d653)