---
name: creating-inline-actions
description: 基于按钮的交互式用户界面（UI），适用于遵循 XIP-67 协议的 XMTP 代理。可用于创建菜单、确认对话框、选择选项或任何基于按钮的交互功能。该界面可通过内联操作、按钮、菜单或 ActionBuilder 来触发。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP内联操作

基于交互式按钮的UI，用于遵循XIP-67规范的XMTP代理。用户可以通过点击按钮来执行操作，而无需输入命令。

## 适用场景

在以下情况下，请参考这些指南：
- 创建交互式按钮菜单
- 构建确认对话框
- 实现选择选项
- 设置多菜单导航
- 处理操作回调

## 规则类别（按优先级排序）

| 优先级 | 类别 | 影响程度 | 前缀 |
|----------|----------|--------|--------|
| 1 | ActionBuilder | 关键性 | `builder-` |
| 2 | Helpers | 高度重要 | `helpers-` |
| 3 | App Config | 中等重要 | `config-` |
| 4 | Validators | 中等重要 | `validators-` |

## 快速参考

### ActionBuilder（关键性）
- `builder-create` - 使用ActionBuilder创建操作菜单
- `builder-send` - 向对话框发送操作

### Helpers（高度重要）
- `helpers-confirmation` - 显示确认对话框
- `helpers-selection` - 显示选择菜单
- `helpers-navigation` - 显示导航选项

### App Config（中等重要）
- `config-menus` - 配置多菜单应用程序
- `config-initialize` - 根据配置初始化应用程序

### Validators（中等重要）
- `validators-inbox-id` - 验证收件箱ID格式
- `validators-ethereum-address` - 验证以太坊地址

## 快速入门

```typescript
// 1. Add middleware to handle intent messages
agent.use(inlineActionsMiddleware);

// 2. Register action handlers
registerAction("my-action", async (ctx) => {
  await ctx.conversation.sendText("Action executed!");
});

// 3. Send interactive buttons
await ActionBuilder.create("my-menu", "Choose an option:")
  .add("my-action", "Click Me")
  .add("other-action", "Cancel")
  .send(ctx);
```

## 实现示例

**操作注册表和处理器：**

```typescript
import type { AgentMiddleware, MessageContext } from "@xmtp/agent-sdk";
import type { Intent } from "@xmtp/node-sdk";

type ActionHandler = (ctx: MessageContext) => Promise<void>;
const actionHandlers = new Map<string, ActionHandler>();

const registerAction = (id: string, handler: ActionHandler) => {
  actionHandlers.set(id, handler);
};
```

**内联操作中间件：**

```typescript
const inlineActionsMiddleware: AgentMiddleware = async (ctx, next) => {
  if (ctx.message.contentType?.typeId === "intent") {
    const intent = ctx.message.content as Intent;
    const handler = actionHandlers.get(intent.actionId);
    if (handler) await handler(ctx);
    else await ctx.conversation.sendText(`Unknown action: ${intent.actionId}`);
    return;
  }
  await next();
};
```

**ActionBuilder类：**

```typescript
import { ActionStyle } from "@xmtp/node-sdk";

class ActionBuilder {
  private actions: { id: string; label: string; style?: ActionStyle }[] = [];
  constructor(private id: string, private description: string) {}
  
  static create(id: string, description: string) {
    return new ActionBuilder(id, description);
  }
  
  add(id: string, label: string, style?: ActionStyle) {
    this.actions.push({ id, label, style });
    return this;
  }
  
  async send(ctx: MessageContext) {
    await ctx.conversation.sendActions({
      id: this.id,
      description: this.description,
      actions: this.actions,
    });
  }
}
```

**确认辅助功能：**

```typescript
const sendConfirmation = async (
  ctx: MessageContext, message: string,
  onYes: ActionHandler, onNo?: ActionHandler
) => {
  const ts = Date.now();
  registerAction(`yes-${ts}`, onYes);
  registerAction(`no-${ts}`, onNo || (async (c) => c.conversation.sendText("Cancelled")));
  await ActionBuilder.create(`confirm-${ts}`, message)
    .add(`yes-${ts}`, "Yes").add(`no-${ts}`, "No", ActionStyle.Danger).send(ctx);
};
```

## 使用方法

有关详细说明，请阅读相应的规则文件：

```
rules/builder-create.md
rules/helpers-confirmation.md
rules/config-menus.md
```