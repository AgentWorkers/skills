---
name: trustlog-guard
description: >
  OpenClaw代理的财务治理机制：  
  - 监控API的使用情况；  
  - 强制执行预算限制；  
  - 检测可能导致系统失控的异常行为（如无限循环）；  
  - 提供成本报告；  
  - 在本地读取会话相关的.jsonl日志文件。  
  该系统完全采用私有化部署方式（100% private）。
version: 1.1.0
author: Anouar
tags: [finance, spending, budget, cost-tracking, governance]
---
# TrustLog Guard — OpenClaw的财务治理工具

TrustLog Guard是一款专为OpenClaw代理设计的财务治理工具，其主要功能包括监控API使用情况、执行预算控制、检测异常行为以及清晰地报告各项费用。

## 核心原则

每个代币都有其对应的价格，每次会话都会产生相应的费用。用户有权了解这两项信息。

我们的目标不是限制AI的使用，而是通过揭示隐藏的成本数据，让AI的使用更加智能、高效。

## 数据来源

会话日志存储在以下路径：`~/.openclaw/agents/{agent}/sessions/*.jsonl`  
每个文件都包含JSON格式的记录。需要查找`type`字段值为`"assistant"`或`"message"`的记录，并且这些记录中必须包含`cost`对象。

`cost`对象的结构如下：  
```json
{
  "cost": {
    "input": 0.00003,
    "output": 0.00786,
    "cacheRead": 0,
    "cacheWrite": 0.0541,
    "total": 0.0620
  }
}
```

`cost.total`字段表示每条消息的花费（单位：美元）。

同时，还需要关注`model`字段，以确定使用了哪种AI模型（例如：`claude-opus-4-6`、`claude-sonnet-4.5`、`claude-haiku-4.5`）。

此外，`timestamp`或`createdAt`字段可用于确定消息的发送时间。

如果在指定路径下找不到会话日志，请告知用户，并请他们确认OpenClaw代理的目录位置。

---

## 命令

### /spend — 花费汇总

读取所有`.jsonl`格式的会话文件，找出包含`cost.total`字段的记录，并按时间段和模型对费用进行分类。  
**输出格式如下：**  
```
💰 TrustLog Guard — Spend Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Today:       $X.XX  (N messages)
This week:   $X.XX  (N messages)
This month:  $X.XX  (N messages)
All time:    $X.XX  (N messages)

Avg cost/message: $X.XXXX

Cost by model:
  model-name-1    $X.XX (XX%) ⚠️  ← add ⚠️ if over 60% of total
  model-name-2    $X.XX (XX%)
  model-name-3    $X.XX (XX%)

Top sessions by cost:
  1. session-name — $X.XX (N messages)
  2. session-name — $X.XX (N messages)
  3. session-name — $X.XX (N messages)
```

**报告结束后，提供以下优化建议：**  
- 如果使用最昂贵模型的消息占比超过50%，计算将简单任务（输出代币数少于200的消息）切换到更便宜模型后能节省的费用：  
  `💡 共有N条消息使用[昂贵模型]完成简单任务，切换到[便宜模型]后每月可节省约$X`  
- 如果平均每条消息的费用超过0.05美元，请提醒用户检查模型选择是否合理。  
- 如果某次会话的花费占总费用的30%以上，请标记该会话为异常。

---

### /budget — 预算管理

**设置预算：**  
用户可以执行命令`/budget set daily $5`或`/budget set monthly $50`来设置每日/每月的预算。  
预算信息将保存在文件`~/.openclaw/workspace/trustlog-guard/budgets.json`中。  
**文件格式如下：**  
```json
{
  "daily": 5.00,
  "monthly": 50.00,
  "currency": "USD"
}
```

如果文件不存在，则创建新文件；如果文件已存在，仅更新相应的预算值。  
**检查预算状态：**  
用户执行命令`/budget`时，系统会读取当前的花费情况（与/spend命令的逻辑相同），并与预设的预算进行对比。  
**输出格式如下：**  
```
📊 TrustLog Guard — Budget Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Daily:   $X.XX / $X.XX [██████░░░░] XX%  ← status emoji
Monthly: $X.XX / $X.XX [██░░░░░░░░] XX%  ← status emoji
```

**进度条显示规则：**  
- 使用`█`表示已使用的预算比例，`░`表示未使用的预算比例  
- 比例低于60%时显示`✅`  
- 60%-79%时显示`⚡`  
- 80%-99%时显示`⚠️`  
- 超过100%时显示`🚨`  

**预算预测：**  
计算当前的消耗速度（今天的花费除以今天的总时长），并预测：  
  `⏱️ 以当前速度，每日预算将在X小时/分钟后耗尽。`  
**仅在该情况下显示预测结果。**  

**警告提示：**  
- 当预算使用率达到80%时显示`⚠️ 警告：即将超出每日预算限制。`  
- 当预算使用率达到100%时显示`🚨 警报：每日预算已超出！当前花费：$X.XX`  

---

### /trustlog — 全面财务报告（含异常检测）

此命令会执行全面的费用分析。  
**输出格式如下：**  
```
🛡️ TrustLog Guard — Full Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SPENDING OVERVIEW
Today:       $X.XX  (N messages)
This week:   $X.XX  (N messages)
This month:  $X.XX  (N messages)

💳 COST BY MODEL
  model-name    $X.XX (XX%) — bar visual
  model-name    $X.XX (XX%) — bar visual

📂 TOP SESSIONS
  1. session-name — $X.XX (N msgs, Xm duration)
  2. session-name — $X.XX (N msgs, Xm duration)
  3. session-name — $X.XX (N msgs, Xm duration)

🔍 ANOMALY SCAN
  ✅ No anomalies detected.
  OR
  🚨 X anomalies detected — see below.

💡 OPTIMIZATION TIPS
  1. tip text
  2. tip text
```

**如果检测到异常行为，会显示具体的异常情况：**  
```
🚨 ANOMALY DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 Rapid-fire loop detected
   Session:    session-name
   Messages:   N in X minutes
   Burn rate:  $X.XX/min (normal: $X.XX/min)
   Spent:      $X.XX
   Status:     ⚠️ Investigate immediately
```

---

## 异常检测规则

每当执行/trustlog命令时，都会自动运行这些检测规则。如果在/spend或/budget命令执行过程中检测到异常，也会在报告底部添加相应的警告信息。

### 规则1：消耗速度骤增  
- 比较最后5条消息的费用与之前20条消息的平均费用  
- 如果最后5条消息的平均费用是之前20条消息平均费用的5倍以上，则触发警告  
- 标签：`🔥 消耗速度骤增`  
- 显示当前消耗速度与正常水平的对比情况，以及受影响的会话信息。

### 规则2：单次会话费用过高  
- 如果某次会话的总费用超过5.00美元，则触发警告  
- 标签：`💥 费用过高的会话`  
- 显示会话名称、总费用及消息数量。  

### 规则3：快速连续发送行为  
- 如果在10分钟内发送超过20条消息，则触发警告  
- 标签：`🔄 快速连续发送行为`  
- 显示消息数量、时间窗口及每分钟的消耗速度。  

### 规则4：模型切换行为  
- 如果会话开始时使用的是较便宜的模型（如Haiku或Sonnet），但在会话中途切换到了更昂贵的模型（如Opus），则触发警告  
- 标签：`📈 模型切换`  
- 显示切换发生的模型、切换时间以及费用差异。  

### 规则5：缓存效率低下  
- 如果后续会话中`cacheWrite`的值持续高于0，而`cacheRead`的值为0或接近0，则触发警告  
- 标签：`💾 缓存效率低下`  
- 显示因缓存写入而产生的总费用（但这些数据从未被读取）。  

---

## 优化建议

在/spend和/trustlog报告中提供针对性的优化建议，仅展示适用的建议，避免提供泛化的建议：  
1. **模型降级建议**：如果使用Opus或昂贵模型的消息中，有超过30%的输出代币数少于200个，建议切换到更便宜的模型，并计算具体的节省金额。  
2. **缓存优化**：如果`cacheRead`的值持续低于`cacheWrite`的值，建议用户延长会话时长或合并相关会话以重用缓存内容。  
3. **会话整合**：如果存在大量耗时少于5分钟的会话，建议将相关任务合并为次数较少、时长较长的会话，以降低上下文构建的成本。  
4. **消费高峰时段**：如果发现消费集中在特定时间段（例如凌晨2-4点），请记录这一现象（可能是自动化任务导致的）。  
5. **按任务类型分类费用**：如果会话名称能反映任务类型，建议按任务类型对费用进行分类，并显示各类型的费用占比。  

---

## 格式规范  

以下格式规范适用于TrustLog Guard的所有输出内容：  
1. 标题后必须使用`━━━━`作为分隔符。  
2. 显示货币金额时，各列中的金额要对齐。  
3. 对于模型费用的细分，必须同时显示金额和百分比。  
4. 为便于理解，费用信息应附带消息数量。  
5. 一致使用表情符号进行状态提示：✅ 表示正常，⚡ 表示需要关注，⚠️ 表示警告，🚨 表示紧急情况。  
6. 货币金额保留2位小数（格式为$X.XX）。  
7. 百分比四舍五入为整数。  
8. 预算进度条使用`██████░░░░`的格式进行显示。  
9. 保持输出简洁易读，避免过多的文字内容。  
10. 每份报告结尾应提供至少一个可操作的优化建议（如可能的话）。  

---

## 错误处理  
- 如果未找到会话文件：`📂 未在指定路径下找到会话日志。请先运行一些OpenClaw会话，或提供代理的目录位置。`  
- 如果会话文件存在但未包含费用数据：`📂 找到了会话文件，但未检测到费用数据。可能是您的OpenClaw版本不支持费用记录，或者某些会话为空。`  
- 在检查预算时如果预算文件不存在：`📊 未设置预算。可以执行命令 `/budget set daily $X` 来设置预算。`  

## 隐私政策  
- 100%数据仅存储在用户本地。  
- 仅读取用户机器上的`.jsonl`文件，绝不修改或删除会话日志。  
- 无需使用API密钥，系统会直接读取OpenClaw已计算好的费用数据。  
- 不涉及任何外部服务器或数据传输，也不会发送任何遥测信息。  
- 预算配置信息保存在`~/.openclaw/workspace/trustlog-guard/budgets.json`文件中。