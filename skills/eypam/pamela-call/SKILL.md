---
name: pamela-call
description: 立即通过 AI 进行电话通话。无延迟，无需设置，可无限扩展。
homepage: https://docs.thisispamela.com
metadata:
  {"openclaw":{"requires":{"env":["PAMELA_API_KEY"]},"primaryEnv":"PAMELA_API_KEY","homepage":"https://docs.thisispamela.com"}}
---
# Pamela Calls  
立即发起人工智能电话呼叫，无延迟、无需设置，可无限扩展。**[ThisIsPamela](https://thisispamela.com)** 是一个用于外拨电话、电话树导航以及通过 SDK、Webhook 和 MCP 进行集成的语音 AI 平台。  

**跳转至：** [安装](#installation) · [快速入门](#quick-start) · [示例](#examples) · [SDK 参考](#sdk-reference)  

**ClawHub 技能版本：** `v1.1.12`  

## 先决条件  
- API 订阅（API 访问所需）  
- 来自您的 API 账户的 API 密钥  
- Node.js 18+、Bun 或 Python 3.8+（适用于 Python）  

## 安装  

**JavaScript/TypeScript：** (使用 npm、yarn 或 bun)  
```bash
npm install @thisispamela/sdk
# or: yarn add @thisispamela/sdk
# or: bun add @thisispamela/sdk
```  

**Python：**  
```bash
pip install thisispamela
```  

**React：** (使用 npm、yarn 或 bun)  
```bash
npm install @thisispamela/react @thisispamela/sdk
# or: bun add @thisispamela/react @thisispamela/sdk
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

最新版本：SDK / CLI / 插件 / MCP / Python / React `1.2.0`  

## 获取 API 密钥  
1. 在 [developer.thisispamela.com](https://developer.thisispamela.com) 注册 API 订阅。  
2. 转到“设置” → “API 访问”。  
3. 通过 Stripe 设置计费。  
4. 点击“创建 API 密钥”。  
5. 立即保存密钥——完整的密钥（以 `pk_live_` 开头）仅显示一次。  

## 安全性与信任  
- **官方包：** npm [@thisispamela](https://www.npmjs.com/org/thisispamela)、PyPI [thisispamela](https://pypi.org/project/thisispamela/) —— 请确保使用这些官方名称以避免拼写错误。  
- **上线前测试：** 在使用该功能时，请使用受限或测试 API 密钥；在账户中启用计费提醒；切勿将生产密钥（`pk_live_...`）放入公共配置文件或日志中。  
- **Webhook：** 始终验证 `X-Pamela-Signature` 标头并保护您的端点；详情请参阅 [SDK 文档](https://docs.thisispamela.com/sdk/javascript#verifywebhooksignature)。  
- **数据：** 通话音频和文字记录会发送给 Pamela，并可能被存储或转发到您的 Webhook；请查阅 [隐私政策与数据使用规定](https://thisispamela.com)（或联系 support@thisispamela.com）。  
- **费用：** 启用后监控使用情况并计费；仅按实际通话时长收费，费用为 $0.10/分钟。  

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

## 示例  
| 场景 | 示例任务 |  
|----------|--------------|  
| 预约安排 | “致电牙医并预约下周的清洁服务” |  
| 订单状态 | “致电药店查询我的处方是否准备好” |  
| 客户服务 | “通过 IVR 菜单联系客服部门” |  
| 信息收集 | “致电餐厅询问素食选项” |  
| 回访 | “致电确认明天下午 2 点的预约” |  
| IVR 导航 | “通过电话菜单联系人工客服” |  

## 主要功能  
- **电话树导航**：自动导航 IVR 菜单，处理通话暂停和转接操作。  
- **自定义工具**：允许 AI 在通话过程中调用自定义功能。  
- **实时文字记录**：通话过程中通过 Webhook 实时更新文字记录。  
- **React 组件**：提供用于显示通话状态和文字记录的预构建用户界面。  

## SDK 参考  
详细 SDK 文档请参阅：  
- **[JavaScript SDK](https://docs.thisispamela.com/sdk/javascript)** — 完整的 JavaScript/TypeScript 参考文档。  
- **[Python SDK](https://docs.thisispamela.com/sdk/python)** — 完整的 Python 参考文档。  
- **[React 组件](https://docs.thisispamela.com/sdk/react)** — 组件库（版本 1.1.5）。  
- **[插件](https://docs.thisispamela.com/sdk/widget)**：适用于任何网站的嵌入式插件。  
- **[MCP 服务器](https://docs.thisispamela.com/sdk/mcp)**：用于 AI 助手的 MCP 工具。  
- **[CLI](https://docs.thisispamela.com/sdk/cli)**：命令行参考文档。  

## Webhook  
Pamela 会在通话生命周期事件发生时发送 Webhook：  
- `call.queued`：通话创建并排队。  
- `callstarted`：通话连接成功。  
- `call_completed`：通话顺利完成。  
- `call.failed`：通话失败。  
- `call.transcript_update`：新增文字记录。  

所需凭证仅为您的 API 密钥。使用 Webhook 时，请务必验证 `X-Pamela-Signature` 标头；详情请参阅 SDK 文档。  

## 计费  
- **API 使用费用：** $0.10/分钟。  
- **每次通话至少计费 1 分钟。**  
- **仅计费实际通话时长。**  
- 需要 API 订阅。  

## 故障排除  
- **“无效的 API 密钥”**：确认密钥是否以 `pk_live_` 开头，并检查其在 API 设置面板中是否处于激活状态。  
- **“403 Forbidden”**：需要 API 订阅，请在 developer.thisispamela.com 查看订阅状态。  
- **“无效的电话号码”**：请使用带有国家代码的 E.164 格式（例如：`+1234567890`）。  

## 资源  
- **官方网站：** https://thisispamela.com  
- **文档：** https://docs.thisispamela.com  
- **演示：** https://demo.thisispamela.com  
- **API：** https://api.thisispamela.com  
- **Discord（实时支持）：** https://discord.gg/cJj5CK8V  
- **邮箱：** support@thisispamela.com