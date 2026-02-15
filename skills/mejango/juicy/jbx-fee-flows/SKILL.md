---
name: jbx-fee-flows
description: |
  JBX ecosystem fee flows and revenue streams for investor understanding.
  Use when: (1) explaining how JBX captures ecosystem value, (2) describing protocol
  fee flows, (3) showing revenue streams to JBX holders, (4) explaining NANA and REV
  relationships, (5) explaining layered fees on revnet cash outs and loans. Covers
  V5 protocol fees, revnet external protocol fees, the NANA-REV feedback loop, and
  JBX ownership stakes across ecosystem tokens.
---

# JBX费用结构：费用如何为JBX持有者创造价值

## 问题

JBX投资者需要了解Juicebox生态系统中的费用是如何通过NANA和REV的分层所有权结构回流到JBX代币持有者手中的。

## 背景/触发条件

- 用户询问“JBX是如何盈利的？”
- 需要解释JBX作为一个“基金中的基金”（fund-of-funds）的运作模式
- 需要描述生态系统的费用流动机制
- 用户可能对NANA或REV与JBX之间的关系有疑问
- 投资者需要了解JBX如何捕获价值

## 解决方案

### 协议栈（Protocol Stack）

要理解费用结构，首先需要了解各个层次之间的关系：

```
┌─────────────────────────────────────────────────────────────────┐
│                     PROTOCOL STACK                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   LAYER 3: Individual Revnets                                   │
│   ─────────────────────────────                                 │
│   Any project using the Revnet framework                        │
│   (including NANA and REV themselves!)                          │
│                    │                                             │
│                    │ built on                                    │
│                    ▼                                             │
│   LAYER 2: Revnet Framework                                     │
│   ─────────────────────────                                     │
│   Adds loans, bonding curves, external protocol fees            │
│   REV collects fees from all revnet cash outs & loans           │
│   (REV is itself a Revnet!)                                     │
│                    │                                             │
│                    │ built on                                    │
│                    ▼                                             │
│   LAYER 1: Juicebox V5 Protocol                                 │
│   ─────────────────────────────                                 │
│   Base protocol for all projects                                │
│   NANA (Project #1) collects 2.5% on all outbound funds         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

KEY INSIGHT: Both NANA and REV are themselves Revnets!
This creates a powerful compounding feedback loop.
```

### Revnet操作中的分层费用

当revnet执行取款或贷款操作时，**两个层次的费用都会被收取**：

```
┌─────────────────────────────────────────────────────────────────┐
│           LAYERED FEES ON REVNET CASH OUT                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   User cashes out $1000 from a Revnet                           │
│                    │                                             │
│                    ▼                                             │
│   ┌────────────────────────────────────────┐                    │
│   │  LAYER 2 FEE: REV External Protocol    │                    │
│   │  2.5% = $25 ──▶ Goes to REV            │                    │
│   └────────────────────────────────────────┘                    │
│                    │                                             │
│                    │ $975 remaining                              │
│                    ▼                                             │
│   ┌────────────────────────────────────────┐                    │
│   │  LAYER 1 FEE: V5 Protocol Fee (2.5%)   │                    │
│   │  ~$24 ──▶ Goes to NANA                 │                    │
│   └────────────────────────────────────────┘                    │
│                    │                                             │
│                    ▼                                             │
│   User receives ~$951 (5% total)                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│           LAYERED FEES ON REVNET LOAN                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   User takes $1000 loan from a Revnet                           │
│                    │                                             │
│                    ▼                                             │
│   ┌────────────────────────────────────────┐                    │
│   │  INTERNAL FEE: 2.5% = $25              │                    │
│   │  (Stays in revnet treasury)            │                    │
│   └────────────────────────────────────────┘                    │
│                    │                                             │
│                    ▼                                             │
│   ┌────────────────────────────────────────┐                    │
│   │  LAYER 2 FEE: REV External Protocol    │                    │
│   │  1% = $10 ──▶ Goes to REV              │                    │
│   └────────────────────────────────────────┘                    │
│                    │                                             │
│                    │ $965 remaining                              │
│                    ▼                                             │
│   ┌────────────────────────────────────────┐                    │
│   │  LAYER 1 FEE: V5 Protocol Fee (2.5%)   │                    │
│   │  ~$24 ──▶ Goes to NANA                 │                    │
│   └────────────────────────────────────────┘                    │
│                    │                                             │
│                    ▼                                             │
│   User receives ~$941 (3.5% external + 2.5% internal)           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### NANA-REV的反馈循环

NANA和REV本身都是revnets，这形成了一个强大的复利反馈循环：

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE FEEDBACK LOOP                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐                      ┌─────────────┐          │
│   │             │   V5 fees (2.5%)     │             │          │
│   │  ALL V5     │ ─────────────────▶   │    NANA     │          │
│   │  PROJECTS   │                      │  (Revnet)   │          │
│   │             │                      │      │      │          │
│   └─────────────┘                      └──────┼──────┘          │
│                                               │      ▲          │
│                                               │      │          │
│                                               │      │ 2.5%     │
│                                               │      │ V5 fee   │
│                                               ▼      │          │
│   ┌─────────────┐                      ┌──────┴──────┐          │
│   │             │   2.5% cash outs     │             │          │
│   │  ALL        │   1% loans           │    REV      │          │
│   │  REVNETS    │ ─────────────────▶   │  (Revnet)   │          │
│   │ (inc NANA   │   (+ 2.5% NANA fee)  │             │          │
│   │  and REV!)  │                      └─────────────┘          │
│   └─────────────┘                                               │
│                                                                  │
│   REV is also a Revnet! When REV does cash outs or loans,       │
│   it pays 2.5% V5 fee back to NANA, completing the loop.        │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                         │   │
│   │   NANA ──── 62% issuance ────▶ JBX                     │   │
│   │                                  ▲                      │   │
│   │   REV ───── >30% ownership ──────┘                     │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   JBX captures value from BOTH layers!                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 完整的费用流动图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     JBX ECOSYSTEM FEE FLOWS                                  │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────┐
                    │          JUICEBOX V5                │
                    │        All Projects                 │
                    │   (Payouts, Surplus Allowance,      │
                    │         Cash Outs)                  │
                    └─────────────────┬───────────────────┘
                                      │
                                      │ 2.5% Protocol Fee
                                      │ (on ALL outbound funds)
                                      ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                              NANA                                        │
    │                     (Project ID 1 - A REVNET)                           │
    │                                                                          │
    │   Receives: 2.5% of all V5 outbound funds                               │
    │                                                                          │
    │   Issuance split:  ┌───────────┬───────────────┐                        │
    │                    │    62%    │      38%      │                        │
    │                    │   ──▶     │     ──▶       │                        │
    │                    │   JBX     │   Fee Payer   │                        │
    │                    └───────────┴───────────────┘                        │
    │                                                                          │
    │   As a Revnet, NANA also pays REV fees on its own cash outs & loans!   │
    └─────────────────────────────────┬───────────────────────────────────────┘
                                      │
                                      │ REV fees when NANA
                                      │ does cash outs/loans
                                      ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                               REV                                        │
    │                      (Revnet Protocol Layer)                            │
    │                                                                          │
    │   Receives: External protocol fees from ALL revnets (including NANA)   │
    │   • 2.5% on cash outs (+ 2.5% NANA = 5% total to user)                 │
    │   • 1% on loans (+ 2.5% NANA = 3.5% total external to user)            │
    │                                                                          │
    │   NEW ISSUANCE    ┌───────────┬───────────────┐                         │
    │   (when fees      │    32%    │      68%      │                         │
    │    are paid):     │   ──▶     │     ──▶       │                         │
    │                   │ team.rev  │   Fee Payer   │                         │
    │                   │   .eth    │               │                         │
    │                   └───────────┴───────────────┘                         │
    │                                                                          │
    │   EXISTING OWNERSHIP: JBX CURRENTLY owns >30% of all REV tokens        │
    └─────────────────────────────────────────────────────────────────────────┘
```

### 收入流1：Juicebox V5协议费用

**来源：**所有Juicebox V5项目
**费用率：**对外部资金收取2.5%
**收款方：**NANA revnet（项目ID 1）
**JBX收益：**NANA代币发行量的62%

**费用适用情况：**
- 向非项目地址的支付
- 剩余津贴的使用
- 取款（当取款税率<100%时）

**免费用情况：**
- 项目之间的支付
- 免费的终端地址
- 内部转账

**费用计算方式：**
```
feeAmount = amount × 25 / (1000 + 25)
         ≈ 2.44% of gross amount
```

### 收入流2：Revnet外部协议费用

**来源：**所有使用revnet框架的项目
**收款方：**REV revnet
**JBX收益：**持有REV代币总量的30%以上

**费用构成：**

| 操作 | 内部费用 | REV费用 | NANA费用（V5） | 总费用 |
|--------|-------------|---------|---------------|-------|
| 取款 | 无 | **2.5%** | **2.5%** | 5% |
| 贷款发放 | 2.5%（归库） | **1%** | **2.5%** | 6% |
| 贷款偿还 | 利息（归库） | 无 | 无 | 变动 |

**分层费用的工作原理：**
- REV费用：取款时收取2.5%，贷款时收取1% → 收入归REV
- NANA费用：所有对外部资金的V5协议费用 → 收入归NANA
- 用户需支付REV费用和NANA费用

**JBX和REV的所有权结构：**
- JBX目前持有**现有REV总量的30%以上**（由于早期投资）
- 新发行的REV代币中，32%归team.rev.eth，68%归费用支付方

### 收入流3：JBX的投资收益

JBX的储备金持有来自生态系统的投资代币：
- **NANA：**V5协议费用发行量的62%
- **REV：**总发行量的30%以上
- **其他代币：**战略性的生态系统投资

这形成了一个“基金中的基金”结构，使JBX能够从多个层面获取价值。

---

## Revnet费用详情（来自Revnet Planner）

### 贷款系统费用

1. **2.5%的预付内部费用**
   - 收入归revnet储备金
   - 按照阶段分配新代币
2. **1%的外部协议费用（支付给REV）**
   - 收入归REV（外部实体）
   - 不会在revnet系统中生成新的代币
3. **2.5%的V5协议费用（支付给NANA）**
   - 从贷款发放金额中收取
   - 62%的收入归JBX

### 取款系统费用

1. **2.5%的外部协议费用（支付给REV）**
   - 从取款金额中收取
   - 收入归REV（外部实体）
2. **2.5%的V5协议费用（支付给NANA）**
   - 从取款金额中收取
   - 62%的收入归JBX

**关键区别：**
- 内部费用：归revnet储备金，同时生成新的代币
- 外部协议费用：不进入revnet系统，因此不会生成新的代币

**用户需支付的总费用：**
- 取款：2.5%（REV）+ 2.5%（NANA）= **5%**
- 贷款：2.5%（内部费用）+ 1%（REV）+ 2.5%（NANA）= **6%**

---

## 价值流动总结

JBX通过以下方式捕获生态系统价值：
1. 直接持有NANA（发行量的62%）
2. 持有大量REV（超过30%）
3. REV的活动通过反馈循环将价值返还给NANA
4. 持有其他生态系统代币

---

## 验证方式

- 检查NANA的所有权结构：JBX在NANA规则集中的分配比例
- 检查REV的所有权结构：JBX代币在REV项目中的持有情况
- 费用率：在协议合同（JBFees, REVLoans）中明确规定

## 示例

向投资者解释分层费用结构：

> “Juicebox生态系统具有分层费用结构，这有利于JBX持有者。在最底层，Juicebox V5对所有对外部资金的支付收取2.5%的费用——这部分费用归NANA，JBX从这些费用中获得62%的NANA代币。
> 
> 此外，Revnet框架还会对取款和贷款行为收取额外的外部协议费用——这些费用归REV，而JBX持有REV超过30%的股份。
> 
> 关键在于：NANA本身也是一个revnet！因此，当有人使用NANA代币进行取款或贷款时，两个层次的费用都会被收取——REV获得其费用，同时这笔支付也会促进NANA代币的发行。这种机制形成了一个反馈循环，使生态系统的价值在多个层面为JBX创造价值。”

**解释revnet取款费用：**

> “当你从任何revnet中取款时，会依次收取两层费用：
> 首先是REV的外部协议费用，然后是对支付金额的V5协议费用（2.5%）。这两部分费用最终都会通过用户持有的NANA和REV股份惠及JBX持有者。”

## 注意事项

- 费用百分比可能会根据治理结构的变化而调整
- JBX的所有权比例基于当前的分配配置
- 外部协议费用可以根据不同的revnet部署进行配置
- 2.5%的V5协议费用是固定的（FEE = 25/1000）
- NANA和REV都是revnets，这形成了一个复利反馈循环：
  - 当NANA持有者取款或贷款时，NANA需要支付REV费用
  - 当REV持有者取款或贷款时，REV需要支付NANA费用（V5协议费用）
  - 这种循环机制使JBX在多个层面捕获价值
- 分层费用结构意味着revnet用户需要同时支付V5费用（给NANA）和revnet费用（给REV）