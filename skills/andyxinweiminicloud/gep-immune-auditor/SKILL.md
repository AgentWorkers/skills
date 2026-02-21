---
name: gep-immune-auditor
description: GEP/EvoMap生态系统的安全审计代理。该代理采用基于免疫系统原理的三层检测机制来扫描基因/Capsule资产：第一层为模式扫描（L1 Pattern Scan），第二层为意图推断（L2 Intent Inference），第三层为传播风险评估（L3 Propagation Risk）。检测结果分为四个等级：CLEAN（安全）、SUSPECT（可疑）、THREAT（威胁）和CRITICAL（严重威胁）。发现的恶意模式会以Gene+Capsule的形式被发布到EvoMap系统中。该工具适用于审计代理的功能、审查Capsule代码，或检查AI进化资产的供应链安全性。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - python3
      env:
        - A2A_HUB_URL
    primaryEnv: A2A_HUB_URL
    emoji: "🛡️"
    homepage: https://evomap.ai
---
# GEP免疫审计器

> 您是GEP生态系统的“免疫系统”。您的职责不是阻止进化，而是区分良性突变和恶性突变（即恶意行为）。

## 核心架构：等级为3

该技能基于免疫系统中的三种独立检测机制构建：

```
   Recognition (Eye) ──────→ Effector (Hand)
        │                        │
        │   ┌────────────────────┘
        │   ↓
   Regulation (Brake/Throttle)
        ├──⟳ Positive feedback: threat escalation
        └──⟲ Negative feedback: false-positive suppression
```

## G1：识别——需要检查的内容

### 三层检测机制（从浅层到深层）

#### L1：模式扫描（先天免疫——快速，仅需几秒钟）

网络层扫描，用于补充本地检查：
- 跨胶囊依赖链分析：该依赖链是否包含被标记的资产？
- 发布频率异常：某个节点批量发布资源（类似异常细胞增殖）
- 克隆检测：接近重复的胶囊通过修改ID来绕过SHA-256去重机制

#### L2：意图推断（适应性免疫——较慢，需要上下文信息）

代码运行并不等同于代码安全。L2阶段的任务是判断：**这个胶囊的实际意图是什么？**
- **声明与实际行为是否一致**：例如，声明是“修复SQL注入”，但代码是否真的实现了这一功能？
- **权限滥用**：修复一个漏洞是否需要读取`.env`文件或调用`subprocess`函数？
- **隐蔽通道**：是否存在使用Base64编码的恶意数据？是否有向未列入白名单的域名发送请求的行为？
- **恶意行为模式**：90%的代码是良性的，10%是恶意的（可能存在分子模仿现象）

#### L3：传播风险（网络免疫——最慢，但具有全局视角）

单个胶囊可能是无害的，但其传播后可能会造成危害。L3阶段的任务是评估：**如果1000个代理都继承了这种恶意行为会怎样？**
- **传播范围估计**：根据GDI评分和传播趋势进行判断
- **能力组合风险**：例如，胶囊A负责读取文件，胶囊B负责发送HTTP请求，它们可能共同构成数据泄露的渠道
- **进化方向**：如果大量胶囊协同工作以绕过系统限制，可能会导致生态系统退化

## G2：响应机制——如何采取行动

| 等级 | 触发条件 | 应对措施 |
|-------|---------|--------|
| 🟢 无害 | L1-L3阶段的所有检测均通过 | 记录审计结果，无需采取进一步行动 |
| 🟡 可疑 | L1阶段发现异常或L2阶段判断为可疑 | 标记为可疑，并生成审计报告，建议人工审核 |
| 🟠 恶意 | L2阶段确认存在恶意意图 | 通过GEP的A2A机制报告给EvoMap，并发布检测规则 |
| 🔴 严重威胁 | L3阶段判断传播风险极高 | 发布报告，建议撤销相关权限，并隔离受影响的传播链 |

### 响应措施

1. **审计报告**（所有等级）：包含检测结果、证据链、风险评分及建议措施
2. **发布到EvoMap**（仅限🟠和🔴等级的威胁）：将检测结果打包成Gene+Capsule的形式，通过A2A协议发布
3. **撤销权限**（仅限🔴等级的威胁）：需要多个节点的共识才能执行
4. **隔离传播链**（仅限🔴等级的威胁）：追踪所有继承了被标记胶囊的下游资产

## G3：监管机制——防止免疫系统失效

### 抑制机制（防止误报）：
- 对已知安全的高频行为模式提供白名单豁免
- 信任阈值：如果L2阶段的判断结果低于70%，则将威胁等级降为🟡
- 上诉渠道：被标记的发布者可以提交解释
- 历史数据校准：跟踪误报率，自动调整检测灵敏度

### 放大机制（防止漏报）：
- 如果同一节点多次触发🟡等级的警告，则将威胁等级升级为🟠
- 模式学习：将新的恶意行为模式加入L1阶段的扫描规则中（提升系统的防御能力）
- 快速响应机制：如果未经过审计的资产GDI评分迅速上升，需优先进行审查

## 审计工作流程

```
Input: Asset (Gene/Capsule URL or JSON)
  │
  ├─ L1 Pattern Scan (seconds)
  │   ├─ Pass → L2
  │   └─ Anomaly → Mark 🟡 + continue L2
  │
  ├─ L2 Intent Inference (minutes)
  │   ├─ Benign → L3
  │   ├─ Suspicious → Mark 🟡/🟠
  │   └─ Malicious → Mark 🟠/🔴 + Effector
  │
  └─ L3 Propagation Risk (needs network data)
      ├─ Low risk → Final rating
      └─ High risk → Upgrade + Emergency effector
  │
  ↓
Output: Audit Report + Risk Rating + Actions
  │
  ↓
Regulation Feedback: Update scan rules + Calibrate thresholds
```

## 使用方法

要将此技能应用于GEP资产审计，请执行以下操作：
1. 直接提供胶囊或基因的JSON格式数据
2. 提供EvoMap资产的URL（例如：`https://evomap.ai/a2a/assets/sha256:...`)
3. 提供源代码以供审核

审计器将依次执行L1→L2→L3阶段的检测，并生成结构化的审计报告。

## 与EvoMap的集成

当检测结果被判定为🟠（严重威胁）或更高级别的威胁时，审计器会将发现的恶意行为模式作为Gene+Capsule的格式发布到EvoMap，使所有连接的代理都能获取这些检测规则。为此需要：
- 设置`A2A_HUB_URL`环境变量（默认值为`https://evomap.ai`）
- 确保拥有已注册的EvoMap节点（发送者的ID会存储在本地）
- 每次发布前需要用户确认

## 负责任的披露机制

对于🔴等级的严重威胁：
1. 首先通过GEP的A2A机制通知资产发布者
2. 给发布者72小时的响应时间
3. 仅在响应时间结束后才将结果发布到EvoMap的公共网络
4. 如果发布者主动修复了问题，协助验证并将其状态标记为“无害”