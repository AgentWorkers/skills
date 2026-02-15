---
name: jb-omnichain-payout-limits
description: |
  Omnichain projects have per-chain payout limits, not aggregate limits. This is a fundamental
  constraint with no perfect solution. Use when: (1) user wants a fixed total fundraising cap
  across chains, (2) asking about aggregate payout limits on omnichain projects, (3) designing
  omnichain projects with payout constraints, (4) exploring oracle or monitoring solutions for
  cross-chain state. Covers the limitation, why it exists, and practical approaches with tradeoffs.
---

# Omnichain 支付限额限制

> **注意**：本内容适用于使用支付限额的项目（即标准 Juicebox 项目，这些项目具有资金库分配功能）。Revnet 并不使用支付限额——它们通过 REVLoans 使用无限制的剩余额度进行贷款，因此此限制不适用于 Revnet。

## 问题所在

**Juicebox V5 中的支付限额是针对每个链设置的，而非所有链的总额。**

当你部署一个多链项目（通过 Suckers 连接）时，每个链都有自己独立的支付限额。例如，如果你为一个包含 5 个链的项目设置了 10 ETH 的支付限额，那么你最多只能支付 50 ETH（10 ETH × 5 个链），而不是 10 ETH。

```
┌─────────────────────────────────────────────────────────────────────┐
│  Omnichain Project with 10 ETH "Payout Limit"                       │
│                                                                     │
│  Chain 1 (Ethereum):  Limit = 10 ETH  →  Can pay out 10 ETH        │
│  Chain 2 (Optimism):  Limit = 10 ETH  →  Can pay out 10 ETH        │
│  Chain 3 (Base):      Limit = 10 ETH  →  Can pay out 10 ETH        │
│  Chain 4 (Arbitrum):  Limit = 10 ETH  →  Can pay out 10 ETH        │
│                                          ─────────────────         │
│                                          TOTAL: 40 ETH possible    │
│                                                                     │
│  User expectation: 10 ETH max                                       │
│  Reality: 40 ETH max                                                │
└─────────────────────────────────────────────────────────────────────┘
```

## 为何这本质上是难以解决的

跨链状态是**异步的**。目前没有一种原子级的方法可以实时了解所有链上的总筹集或支付金额。

任何尝试协调跨链状态的解决方案都会带来以下问题：
- **延迟**：无法实现实时更新（可能存在几秒到几分钟的延迟）
- **信任问题**：谁来运行预言机？谁能够操纵预言机？
- **攻击机会**：攻击者可以利用同步延迟进行攻击
- **高昂的成本**：跨链通信费用较高
- **复杂性**：更多的组件意味着更多的故障可能性

这不是 Juicebox 的漏洞，而是多链系统固有的特性。

## 解决方案

### 方法 1：接受并围绕这一限制进行设计

**适用场景**：能够接受近似限额的项目

为每个链设置限额，使这些限额之和达到你的目标金额，同时接受实际分配可能与预期不符的情况。

```solidity
// Goal: ~100 ETH total across 5 chains
// Strategy: 20 ETH limit per chain

// Each chain's ruleset config:
fundAccessLimitGroups: [{
    terminal: MULTI_TERMINAL,
    token: NATIVE_TOKEN,
    payoutLimits: [{
        amount: 20 ether,  // Per-chain limit
        currency: 1        // ETH
    }],
    surplusAllowances: []
}]
```

**权衡**：
- 可能某个链会达到其限额，而其他链仍有剩余额度
- 如果分配不均，实际筹集的金额可能低于预期
- 无需协调——最简单的方法

**使用时机**：
- 对于设定软性上限的项目（非强制性要求）
- 对于目标金额的 80-120% 可以接受的项目
- 处于早期阶段的多链项目

---

### 方法 2：监控 + 手动暂停

**适用场景**：有活跃运营者且能够快速响应的项目

使用 Bendystraw 监控总筹集金额，在接近限额时手动暂停支付。

**手动暂停操作**：
```typescript
// Project owner calls on each chain
await controller.queueRulesetsOf(projectId, [{
  // ... existing config
  metadata: {
    // ... existing metadata
    pausePay: true  // Disable new payments
  }
}]);
```

**权衡**：
- 需要持续监控（需要有人负责）
- 反应时间很重要——如果在延迟期间进行支付可能会出问题
- 存在人为错误的风险（可能忘记暂停或暂停错误的链）
- 不适用于无需信任机制/自动化的项目

**使用时机**：
- 有专职运营者的项目
- 风险较低的项目，允许短暂超出限额
- 在构建自动化系统过程中的过渡阶段

---

### 方法 3：自动化 Cron 任务 + Relayr

**适用场景**：希望实现自动化但不想使用复杂预言机的项目

通过 Cron 任务使用 Bendystraw 监控总余额，在接近限额时使用 Relayr 在所有链上暂停支付。

**实施要求**：
1. **运营者地址**：需要在每个链的项目上拥有 `QUEUE_RULESETS` 权限
2. **Cron 任务执行环境**：可靠的执行服务（如 AWS Lambda、Cloudflare Workers 或专用服务器）
3. **Bendystraw API 密钥**：用于查询总余额
4. **Relayr 集成**：用于多链交易打包

**权衡**：
- **延迟**：Cron 任务的执行时间加上 Relayr 的处理时间可能导致实际支付超过限额
- **信任问题**：运营者可能单方面操作
- **基础设施成本**：需要维护相关服务
- **费用**：Relayr 的费用以及所有链上的交易手续费
- **可靠性**：Cron 任务失败可能导致错过限额

**使用时机**：
- 对指定运营者有一定信任的项目
- 可以接受 5-10% 超出限额的软性上限的项目
- 没有资源来构建完整预言机系统的项目

---

### 方法 4：在支付钩子中集成预言机

**适用场景**：需要严格限制且需要强保障的项目

在允许支付之前，通过支付钩子查询预言机的总余额。预言机由监控所有链的中间件更新。

**实施概要**：
```solidity
// Oracle contract
contract AggregateBalanceOracle {
    uint256 public aggregateBalance;
    uint256 public threshold;
    uint256 public lastUpdate;
    address public relayer;

    function updateBalance(uint256 newBalance) external {
        require(msg.sender == relayer, "UNAUTHORIZED");
        aggregateBalance = newBalance;
        lastUpdate = block.timestamp;
    }

    function wouldExceedThreshold(uint256 additionalAmount) external view returns (bool) {
        return aggregateBalance + additionalAmount > threshold;
    }
}

// Pay hook that checks oracle
contract AggregateLimitPayHook is IJBPayHook {
    AggregateBalanceOracle public oracle;
    uint256 public maxStaleness = 5 minutes;

    function beforePayRecordedWith(JBBeforePayRecordedContext calldata context)
        external view override returns (uint256, uint256, uint256, JBPayHookSpecification[] memory)
    {
        // Check oracle freshness
        require(
            block.timestamp - oracle.lastUpdate() <= maxStaleness,
            "Oracle stale"
        );

        // Check aggregate limit
        require(
            !oracle.wouldExceedThreshold(context.amount.value),
            "Aggregate limit exceeded"
        );

        // Allow payment
        return (context.weight, context.newlyIssuedTokenCount, context.totalSupply, new JBPayHookSpecification[](0));
    }
}
```

**权衡**：
- **复杂性**：需要多个合约和中间件服务
- **延迟**：预言机的更新可能会滞后于实际情况
- **延迟期间可能发生支付**：如果在预言机更新期间进行支付，可能会导致超出限额
- **依赖中间件**：中间件是单点故障风险
- **成本**：需要持续运行中间件以及支付预言机的费用
- **用户体验**：如果预言机数据过时或接近限额，支付可能会失败

**使用时机**：
- 需要严格遵守监管规定的项目
- 风险较高的项目，不允许超出限额
- 有资源来构建和维护基础设施的项目

**当前状态**：目前尚无现成的实现方案，需要定制开发。

---

### 方法 5：单链资金库

**适用场景**：能够集中管理资金库操作的项目

在所有链上接受支付，但将所有资金汇总到一条“主链”上进行资金库操作。只有主链上的支付限额才具有约束力。

**难点**：Suckers 需要用户明确操作才能完成资金转移。项目无法自动将资金从其他链转移到主链。用户必须：
1. 在源链上调用 `prepare()` 函数
2. 等待资金转移
3. 在目标链上调用 `claim()` 函数

**潜在的解决方法**：
- 通过奖励机制激励用户进行资金转移（例如提供奖励代币或降低主链的费用）
- 构建一个代表用户进行资金转移的自动化脚本（但这需要用户的信任以及额外的交易费用）
- 接受部分资金会分散在各个链上的情况

**权衡**：
- **用户操作不便**：用户需要额外步骤来转移资金
- **资金分散**：资金会在转移前分散在多个链上
- **复杂性**：用户需要理解资金转移的流程
- **强制措施**：无法强制用户进行资金转移

**使用时机**：
- 大部分活动集中在某一个链上的项目
- 愿意接受资金分散的项目
- 在向单链系统过渡的项目中使用的临时方案

## 对比矩阵

| 方法 | 执行方式 | 延迟 | 是否需要信任 | 复杂性 | 适用场景 |
|----------|-------------|---------|----------------|------------|----------|
| 接受并设计 | 软性限制 | 无需 | 低 | 适用于设定软性上限的项目 |
| 手动监控 | 软性限制 | 需要人工监控 | 需要运营者参与 | 适用于活跃团队 |
| Cron + Relayr | 软性限制 | 延迟约 5-10 分钟 | 需要运营者参与 | 适用于需要自动化的场景 |
| 在支付钩子中集成预言机 | 需要严格限制 | 实时性较低 | 需要依赖中间件 | 适用于需要合规性的项目 |
| 单链模式 | 中等复杂度 | 无需额外信任 | 适用于集中管理的项目 |

*注：在预言机更新期间，存在一定的延迟窗口*

## 根据使用场景的建议

### “我们需要一个严格的限额以满足监管要求”
**建议**：在多链系统中实现这一点非常困难。可以考虑以下方案：
1. 仅使用单链模式（不使用多链功能）
2. 使用支付钩子与预言机结合（实现方式复杂，需要定制开发）
3. 接受支付限额只能是近似的这一事实

### “我们设定了筹款目标，但该目标不具有法律约束力”
**建议**：使用方法 1（接受并设计）或方法 2（手动监控）：
- 为每个链设置合计达到目标金额 80% 的限额
- 使用 Bendystraw 监控筹集情况
- 在接近目标金额时手动暂停支付

### “我们有能够管理这些操作的运营者”
**建议**：使用方法 3（Cron + Relayr）：
- 自动化监控和暂停支付
- 接受 5-10% 的潜在超出限额
- 确保运营者的密钥安全

### “我们正在构建一个 Revnet”
**建议**：此限制不适用于 Revnet：
- Revnet 不使用支付限额——它们通过 REVLoans 使用剩余额度进行贷款
- 设计上，剩余额度是无限的（用于贷款抵押）
- 如果需要在 Revnet 上设置总筹款限额，请参考上述关于预言机或监控的方法

## 未来考虑

### Juicebox 能否原生支持总限额？

理论上可以，但这需要：
1. **跨链通信协议**：与跨链桥接机制的集成
2. **关于总余额的共识机制**：如何确定哪个链的数据是最准确的？
3. **对延迟的容忍度**：用户需要接受同步过程中的支付失败
4. **费用分配**：谁来承担跨链通信的费用？

这是一个重大的协议级变更，不是简单的功能添加。

### 是否可以存在共享的预言机服务？

可以——一个由社区运营的预言机服务可以：
- 监控所有 Juicebox 项目
- 提供总余额查询功能
- 更新链上的预言机数据

这样的服务可以作为基础设施的一部分，但需要：
- 持续的资金支持
- 对服务运营者的信任
- 与支付钩子的集成

## 相关技能

- `/jb-omnichain-ui`：构建多链前端界面
- `/jb-suckers`：实现跨链代币桥接功能
- `/jb-bendystraw`：查询项目的总余额数据
- `/jb-relayr`：实现多链交易打包
- `/jb-fund-access-limits`：配置每个链的支付限额