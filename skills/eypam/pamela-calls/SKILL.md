---
name: pamela-calls
description: 使用 Pamela 的语音 API 进行人工智能驱动的电话通话。您可以发起外拨电话、注册自定义的通话中操作功能、处理 Webhook 事件，并构建 React 用户界面。该 API 非常适用于用户需要拨打电话、集成语音人工智能、构建交互式语音应答（IVR）系统、导航电话菜单或自动化电话任务的场景。
---

# Pamela语音API技能

使用原生电话菜单导航功能，实现基于AI的电话通话。

**跳转至：** [安装](#installation) · [快速入门](#quick-start) · [使用场景](#use-cases) · [SDK参考](#sdk-reference)

## 先决条件

- API订阅（访问API所需）
- 来自您的开发者账户的API密钥
- Node.js 18+（适用于JavaScript/React）或Python 3.8+（适用于Python）

## 安装

**JavaScript/TypeScript：**
```bash
npm install @thisispamela/sdk
```

**Python：**
```bash
pip install thisispamela
```

**React：**
```bash
npm install @thisispamela/react @thisispamela/sdk
```

**命令行界面（CLI）：**
```bash
npm install -g @thisispamela/cli
```

## 获取API密钥

1. 在 [developer.thisispamela.com](https://developer.thisispamela.com) 注册API订阅。
2. 进入API设置面板。
3. 通过Stripe设置账单支付。
4. 点击“创建API密钥”。
5. 立即保存密钥——完整的密钥（以 `pk_live_` 开头）仅显示一次。

## 快速入门

**注意：** 电话号码必须采用E.164格式（例如：`+1234567890`）。

### JavaScript
```typescript
import { PamelaClient } from '@thisispamela/sdk';

const client = new PamelaClient({ apiKey: 'pk_live_...' });

const call = await client.createCall({
  to: '+1234567890',
  task: 'Call the pharmacy and check if my prescription is ready',
  voice: 'female',
  agent_name: 'Pamela',
});

const status = await client.getCall(call.id);
console.log(status.transcript);
```

### Python
```python
from pamela import PamelaClient

client = PamelaClient(api_key="pk_live_...")

call = client.create_call(
    to="+1234567890",
    task="Call the pharmacy and check if my prescription is ready",
    voice="female",
    agent_name="Pamela",
)

status = client.get_call(call["id"])
print(status["transcript"])
```

### 命令行界面（CLI）
```bash
export PAMELA_API_KEY="pk_live_..."

thisispamela create-call \
  --to "+1234567890" \
  --task "Call the pharmacy and check if my prescription is ready"
```

## 使用场景

| 使用场景 | 示例任务 |
|----------|--------------|
| 预约安排 | “致电牙医，预约下周的清洁服务” |
| 订单状态查询 | “致电药店，查询我的处方是否已准备好” |
| 客户服务 | “通过IVR菜单导航至账单部门” |
| 信息收集 | “致电餐厅，询问是否有素食选项” |
| 回访确认 | “致电确认明天下午2点的预约” |
| IVR导航 | “通过电话菜单导航至人工客服” |

## 主要特性

- **电话菜单导航**：自动导航IVR菜单，处理等待和转接操作。
- **自定义工具**：允许AI在通话过程中调用自定义功能。
- **实时转录**：通话进行时通过Webhook实时更新转录内容。
- **React组件**：提供用于显示通话状态和转录内容的预构建用户界面。

## SDK参考

有关详细的SDK文档，请参阅：

- **[JavaScript SDK](../../../sdk/javascript.md)** - 完整的JavaScript/TypeScript参考文档。
- **[Python SDK](../../../sdk/python.md)** - 完整的Python参考文档。
- **[React组件](../../../sdk/react.md)** - 组件库指南。

## Webhook

Pamela会为通话生命周期事件发送Webhook：

- `call.queued`：通话创建并排队。
- `callstarted`：通话开始。
- `call_completed`：通话成功结束。
- `call.failed`：通话失败。
- `call.transcript_update`：新增转录内容。

请使用`X-Pamela-Signature`头部验证Webhook签名。

## 账费

- API使用费用：每分钟0.10美元。
- 每次通话至少计费1分钟。
- 仅对已连接的通话计费。
- 需要API订阅。

## 故障排除

- **“API密钥无效”**：确认密钥以 `pk_live_` 开头，并检查其在API设置面板中是否处于激活状态。
- **“403 Forbidden”**：需要API订阅，请在 [developer.thisispamela.com](https://developer.thisispamela.com) 查看订阅状态。
- **“电话号码无效”**：请使用带有国家代码的E.164格式（例如：`+1234567890`）。

## 资源

- 文档：https://docs.thisispamela.com/
- 示范：https://demo.thisispamela.com/
- API：https://api.thisispamela.com
- 技术支持：support@thisispamela.com