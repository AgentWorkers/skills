---
name: pamela-call
version: 1.1.4
description: 使用 Pamela 即刻发起由 AI 驱动的电话通话。无需等待、无需设置电话设备，也无需支付高额的前期费用——只需简单点击即可自动拨打电话。您可以创建外拨电话、注册自定义的通话中操作工具、处理 Webhook 事件，并构建 React 用户界面。无论用户需要拨打电话、集成语音 AI、构建交互式语音应答（IVR）系统、导航电话菜单，还是自动化电话任务，P Pamela 都能满足您的需求。
---

# Pamela Calls – 即时进行人工智能电话通话

使用原生电话导航功能，实现人工智能驱动的电话通话。**[ThisIsPamela](https://thisispamela.com)** 是一个语音人工智能平台，能够处理外拨电话、导航电话菜单，并通过 SDK、Webhook 和 MCP 与您的应用程序集成。

**跳转至：** [安装](#installation) · [快速入门](#quick-start) · [用例](#use-cases) · [SDK 参考](#sdk-reference)

## 先决条件

- API 订阅（API 访问所需）
- 来自您的 API 账户的 API 密钥
- Node.js 18+（适用于 JavaScript/React）或 Python 3.8+（适用于 Python）

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

**CLI：**
```bash
npm install -g @thisispamela/cli
```

**MCP（适用于基于 MCP 的代理）：**
```bash
npm install @thisispamela/mcp
```

**插件（可嵌入，无需框架）：**
```bash
npm install @thisispamela/widget
```

最新版本：SDK / CLI / 插件 / MCP / Python `1.1.3`，React `1.1.4`。

## 获取 API 密钥

1. 在 [developer.thisispamela.com](https://developer.thisispamela.com) 注册 API 订阅。
2. 进入“设置” → “API 访问”。
3. 通过 Stripe 设置账单。
4. 点击“创建 API 密钥”。
5. 立即保存密钥——完整的密钥（以 `pk_live_` 开头）仅显示一次。

## 快速入门

**注意：** 电话号码必须采用 E.164 格式（例如：`+1234567890`）。

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

### CLI
```bash
export PAMELA_API_KEY="pk_live_..."

thisispamela create-call \
  --to "+1234567890" \
  --task "Call the pharmacy and check if my prescription is ready"
```

## 用例

| 用例 | 示例任务 |
|----------|--------------|
| 预约安排 | “打电话给牙医，预约下周的洁牙服务” |
| 订单状态 | “打电话给药店，查询我的处方是否已准备好” |
| 客户服务 | “导航 IVR 菜单，联系账单部门” |
| 信息收集 | “打电话给餐厅，询问是否有素食选项” |
| 回访 | “打电话确认明天下午 2 点的预约” |
| IVR 导航 | “导航电话菜单，联系人工客服” |

## 主要功能

- **电话菜单导航** – 自动导航 IVR 菜单，处理等待和转接操作
- **自定义工具** – 在通话过程中注册 AI 可以使用的自定义功能
- **实时转录** – 通话进行时通过 Webhook 更新转录内容
- **React 组件** – 提供用于显示通话状态和转录内容的预构建用户界面

## SDK 参考

有关详细的 SDK 文档，请参阅：

- **[JavaScript SDK](https://docs.thisispamela.com/sdk/javascript)** – 完整的 JavaScript/TypeScript 参考文档
- **[Python SDK](https://docs.thisispamela.com/sdk/python)** – 完整的 Python 参考文档
- **[React 组件](https://docs.thisispamela.com/sdk/react)** – 组件库（v1.1.4）
- **[插件](https://docs.thisispamela.com/sdk/widget)** – 适用于任何网站的嵌入式插件
- **[MCP 服务器](https://docs.thisispamela.com/sdk/mcp)** – 用于 AI 助手的 MCP 工具
- **[CLI](https://docs.thisispamela.com/sdk/cli)** – 命令行参考

## Webhook

Pamela 会为通话生命周期事件发送 Webhook：

- `call.queued` – 通话创建并排队
- `callstarted` – 通话开始
- `call_completed` – 通话成功完成
- `call.failed` – 通话失败
- `call.transcript_update` – 新的转录内容更新

使用 `X-Pamela-Signature` 标头验证 Webhook 签名。

## 账费

- **API 使用费用：0.10 美元/分钟**
- **每次通话至少计费 1 分钟**
- **仅对已连接的通话计费**
- 需要 API 订阅

## 故障排除

- **“无效的 API 密钥”**：确认密钥以 `pk_live_` 开头，并检查其在 API 设置面板中是否有效。
- **“403 禁止访问”**：需要 API 订阅，请在 developer.thisispamela.com 检查订阅状态。
- **“无效的电话号码”**：使用带有国家代码的 E.164 格式，例如：`+1234567890`。

## 资源

- **网站：** https://thisispamela.com
- **文档：** https://docs.thisispamela.com
- **演示：** https://demo.thisispamela.com
- **API：** https://api.thisispamela.com
- **Discord（实时支持）：** https://discord.gg/cJj5CK8V
- **电子邮件：** support@thisispamela.com