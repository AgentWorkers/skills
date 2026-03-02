---
name: openclaw-tally
description: "“Token”显示了您支付的费用；“Task”则展示了您完成的工作内容。“Tally”会记录每个 OpenClaw 任务的完整过程，包括成本、复杂度以及效率评分。"
metadata:
  {"openclaw": {"emoji": "📊", "runtime": "node", "requires": {"anyBins": ["node", "npm"]}}}
---
# OpenClaw Tally

该工具将AI的使用方式从简单的“计数令牌”转变为关注“任务完成的经济性”。它不再关注“有多少令牌”，而是关注“完成某项任务需要多少资源，以及这样做是否值得”。

## 安全与隐私声明

- **钩子（Hook）**：该技能会注册一个`message-post`钩子，并处理**所有消息**。
- **仅限本地处理**：所有处理操作都在本地完成，不会向任何外部服务器发送数据。
- **消息内容**：任务检测器会读取消息文本，通过正则表达式匹配来识别任务的开始/完成/失败信号。**消息文本本身不会被存储**，只有元数据（令牌数量、使用的模型、会话ID、复杂度得分）会被保存到数据库中。
- **存储方式**：默认使用SQLite数据库（路径为`~/.openclaw/tally/tally.db`），也可以为测试指定自定义路径。
- **依赖库**：需要`better-sqlite3`（Node.js的原生插件）。安装过程会通过`npm install`触发原生构建步骤。
- **权限要求**：无网络访问权限，也无执行权限；文件系统访问范围仅限于`~/.openclaw/tally/`。

## 功能概述

- **自动从消息流中检测任务**（第一层：任务检测器）
- **记录不同会话、子代理及定时任务的相关成本**（第二层：任务记录器）
- **计算每个任务、模型及定时任务的效率得分（Task Efficiency Score, TES）**（第三层：分析引擎）

## 命令行接口

- `/tasks list`：显示最近的任务列表，包括状态、成本及效率得分（TES）
- `/tasks stats`：显示指定时间段的统计信息
- `/tasks this-week`：显示本周的任务概览
- `/tasks show <task_id>`：显示特定任务的详细信息
- `/tasks report --dimension model`：生成模型的效率报告
- `/tasks cron-health`：检查定时任务的执行效率和健康状况

## 复杂度等级

- **L1（Reflex）**：单轮处理，仅使用文本，无需任何工具
- **L2（Routine）**：多轮处理或使用1–3个工具
- **L3（Mission）**：使用多个工具、进行文件读写操作及调用外部API
- **L4（Campaign）**：涉及子代理、定时任务以及跨会话的处理

## TES（Task Efficiency Score，任务效率得分）

```
TES = quality_score / (normalized_cost × complexity_weight)
```

- **> 2.0** 🟢 优秀
- **1.0–2.0** 🟡 良好
- **0.5–1.0** 🟠 低于平均水平
- **< 0.5** 🔴 较差
- **0.0** ⚫ 失败

## 使用方法

安装该技能后，它会自动连接到`message-post`事件。可以使用上述命令行接口查询相关数据。所有数据均存储在`~/.openclaw/tally/tally.db`文件中。

完整的产品规格请参阅[PRD.md](./PRD.md)。