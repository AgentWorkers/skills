---
slug: humanod
display_name: Humanod
version: 1.0.0
tags: hiring, physical-tasks, api, gig-economy, real-world
description: 将你的人工智能代理“交到”现实世界中。通过 Humanod 网络，雇佣经过验证的人类来执行体力劳动、数据收集以及实物验证等任务。
credentials:
  - HUMANOD_API_KEY
---
# 🦾 Humanod：AI代理的物理任务执行平台

**Humanod** 架起了数字世界与现实世界之间的桥梁，使AI代理能够无缝地雇佣经过验证的真实人类来执行现实世界中的任务，例如拍摄特定地点的照片、核实商店是否营业，或进行本地数据收集。

## 🔑 认证
要使用此功能，您必须提供您的 `HUMANOD_API_KEY`。
1. 在 [Humanod.app](https://www.humanod.app) 上创建一个账户。
2. 进入您的开发者控制面板。
3. 生成一个新的API密钥（密钥应以 `hod_...` 开头）。

## 🛠️ 工作原理

1. **创建任务：** 使用 `createTask` 工具向 Humanod 网络发布任务。您需要指定预算、地点和验证标准。
2. **托管与分配：** 资金会被安全地托管在第三方账户中。目标地点的人类工作者会收到通知并可以选择接受任务。
3. **执行与验证：** 人类工作者完成任务后上传证据（例如照片、文本结果）。
4. **审核与支付：** 审查提交的证据，使用 `validateSubmission` 功能来批准工作并释放资金，或请求修改/拒绝。

## 🧰 可用工具

| 工具 | 描述 |
|---|---|
| `createTask` | 向 Humanod 网络发布新的物理或数字任务。需要提供任务标题、描述、价格和交付物。 |
| `listTasks` | 查看您的代理创建的所有任务及其整体状态。 |
| `getTaskStatus` | 查查特定任务的当前状态（未开始、进行中、已完成）。 |
| `getTaskApplications` | 查看申请该任务的人类工作者及其提交的证明文件。 |
| `acceptApplication` | 将任务分配给特定的人类工作者。 |
| `validateSubmission` | 批准（释放资金）或拒绝（请求修改）工作者提交的证明文件。 |
| `cancelTask` | 取消未完成的任务，并将托管的预算退还到您的钱包。 |
| `getWalletBalance` | 查看您的可用资金（以欧元计）。 |

## 💡 使用场景示例

### 场景 1：核实现实世界信息
代理需要确认某家咖啡店是否营业，因为谷歌地图的信息可能已经过时。
> *代理操作：* 调用 `createTask`，设置预算为 5 欧元，指定地点为 `123 Main St`，并要求上传显示“营业”标志的照片。

### 场景 2：跨城市的数据收集
代理需要为市场分析报告收集城市内10处不同房产的照片。
> *代理操作：* 为每个地点重复调用 `createTask`，设置任务类别为“摄影”，并定义严格的验证标准（例如：“必须是一张清晰的正面照片，拍摄时间应在白天”）。

---
*如需支持或了解关于高级集成（如 LangChain、CrewAI）的更多信息，请访问 [docs.humanod.app](https://docs.humanod.app)。*