---
name: clawchain
description: **ClawChain RPC客户端（适用于EvoClaw代理）**  
该客户端用于连接基于Substrate的区块链，查询链上的代理数据、提交交易，并支持代理参与链上的治理活动及声誉管理系统。适用于需要处理ClawChain L1区块链、代理DID（Digital Identity Documents）、代币经济模型或代理声誉系统的场景。
---

# ClawChain RPC客户端

该客户端用于将EvoClaw代理连接到ClawChain区块链，以实现链上的声誉跟踪、代币经济机制以及治理参与功能。

## 快速入门

```rust
use clawchain::ClawChainClient;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Connect to local node
    let client = ClawChainClient::new("ws://127.0.0.1:9944").await?;
    
    // Query agent reputation
    let did = "did:claw:1a2b3c4d...";
    let reputation = client.get_agent_reputation(did).await?;
    println!("Reputation score: {}", reputation);
    
    // Check token balance
    let balance = client.get_token_balance(did).await?;
    println!("CLAW tokens: {}", balance);
    
    Ok(())
}
```

## 先决条件

1. **ClawChain节点正在运行：**
   ```bash
   clawchain-node --dev --rpc-external --ws-external
   ```

2. **Rust项目的Cargo.toml文件中已添加以下依赖：**
   ```toml
   [dependencies]
   clawchain = { path = "/path/to/clawchain-skill" }
   ```

## 架构

```
┌─────────────────────────────────────────────────┐
│              EvoClaw Edge Agent                │
├─────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────┐   │
│  │  ClawChain Skill (this skill)         │   │
│  │  └─ Substrate RPC client              │   │
│  └────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
          ↓ WebSocket
┌─────────────────────────────────────────────────┐
│         ClawChain Node (Substrate)             │
│  ┌───────────────────────────────────────────┐  │
│  │ AgentRegistry Pallet                      │  │
│  │ ClawToken Pallet                           │  │
│  │ Governance Pallet                           │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## 关键概念

### 代理DID（Agent DID）

代理的标识符遵循以下格式：
```
did:claw:<hash>
```

其中 `<hash>` 是代理元数据与所有者地址的SHA-256哈希值。

### 声誉分数（Reputation Scores）

声誉分数的计算方式如下：
```rust
score = (commits * 1000) + (pull_requests * 5000) + (docs * 2000)
```

### 代币经济机制（Token Economics）

- **总供应量：** 10亿个$CLAW
- **分配方式：** 40%通过空投发放，30%分配给验证者，20%存入储备金，10%归团队所有
- **通货膨胀率：** 年度5%（最低不低于2%），用于补贴交易手续费

## API参考

### 连接（Connection）

```rust
let client = ClawChainClient::new("ws://localhost:9944").await?;
```

**参数：**
- `url`：WebSocket地址（格式为ws://或wss://）
- **返回值：** 连接成功的客户端对象

### 查询代理信息（Query Agent）

```rust
let agent = client.get_agent("did:claw:...").await?;
```

**返回值：`AgentInfo`结构体，包含以下字段：**
- `did`：代理的DID
- `owner`：代理的所有者地址
- `metadata`：代理的IPFS哈希值
- `reputation`：代理的声誉分数
- `verifications`：代理获得的验证次数

### 获取代理的代币余额（Get Token Balance）

```rust
let balance = client.get_token_balance("did:claw:...").await?;
```

**返回值：** 代理的代币余额（类型为u128）

### 注册新代理（Register Agent）

```rust
let did = client.register_agent(metadata_ipfs_hash).await?;
```

**返回值：** 新创建的代理DID

### 对提案进行投票（Vote on Proposal）

```rust
client.vote(proposal_id, true).await?;
```

**参数：**
- `proposal_id`：提案的标识符
- `approve`：true（批准）或false（拒绝）

### 提交交易（Submit Transaction）

```rust
let tx_hash = client.submit_extrinsic(call_data).await?;
```

**参数：**
- `call_data`：需要提交的交易数据（已编码）
- **返回值：** 交易的哈希值

## 错误处理（Error Handling）

```rust
use clawchain::ClawChainError;

match client.get_agent(did).await {
    Ok(agent) => println!("Agent: {:?}", agent),
    Err(ClawChainError::NotFound) => println!("Agent not found"),
    Err(e) => eprintln!("Error: {:?}", e),
}
```

## 示例：代理的完整集成流程（Example: Full Agent Integration）

```rust
use clawchain::ClawChainClient;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let client = ClawChainClient::new("ws://127.0.0.1:9944").await?;
    
    // 1. Register this agent
    let metadata = b"{\"name\":\"pi1-edge\",\"type\":\"edge\"}";
    let did = client.register_agent(metadata).await?;
    println!("Registered: {}", did);
    
    // 2. Check reputation
    let rep = client.get_agent_reputation(&did).await?;
    println!("Reputation: {}", rep);
    
    // 3. Vote on governance proposal
    if rep > 1000 {
        client.vote(123, true).await?;
        println!("Voted on proposal #123");
    }
    
    Ok(())
}
```

## 监控（Monitoring）

可以订阅链上的事件以获取实时信息：

```rust
client.subscribe_events(|event| {
    match event {
        ChainEvent::Block(block) => println!("New block: {}", block.number),
        ChainEvent::AgentRegistered(did) => println!("Agent: {}", did),
        ChainEvent::ProposalPassed(id) => println!("Proposal {} passed", id),
    }
}).await?;
```

## 测试（Testing）

可以使用模拟的RPC服务器进行测试：

```rust
let mock = MockServer::new().await?;
let client = mock.client().await?;
```

## 安全注意事项（Security Notes）

- **切勿在代理代码中暴露私钥**  
- 对于自主运行的代理，应使用**程序化签名**机制进行安全验证  
- 需要对所有RPC响应进行验证  
- 对公共RPC接口实施速率限制（防止恶意请求）

## 参考资料（References）

- [ClawChain架构文档](https://github.com/clawinfra/claw-chain/blob/main/docs/architecture/overview.md)  
- [Substrate RPC文档](https://docs.substrate.io/)  
- [代理注册库](https://github.com/clawinfra/claw-chain/blob/main/pallets/agent-registry)