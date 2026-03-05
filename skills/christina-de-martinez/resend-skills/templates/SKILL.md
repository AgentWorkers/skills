---
name: templates
description: >
  **使用场景：**  
  - 通过 API 创建、更新、发布、删除或列出邮件发送模板；  
  - 定义模板变量；  
  - 理解模板的草稿状态与已发布状态；  
  - 以编程方式管理模板的生命周期。
---
# 重新发送模板

## 概述

模板是存储在 Resend 中的可重用电子邮件结构。只需定义一次 HTML 内容和变量，在发送邮件时引用相应的模板 ID 或别名即可。

**在以下情况下使用模板：**  
- 当多个邮件需要使用相同的结构时；  
- 当非技术人员需要编辑邮件内容而无需修改代码时；  
- 当您希望保留邮件的版本历史记录时。

**在以下情况下使用内联 HTML：**  
- 当每次发送邮件的结构都发生变化时；  
- 当您需要使用 50 个以上的动态变量时；  
- 当您希望更精确地控制邮件的渲染效果时。

## 模板生命周期

```
Create (draft) → Publish → Send
      ↑ edit                 |
      └─────────────────────┘
```

编辑已发布的模板会创建一个新的草稿版本——已发布的模板会继续被用于发送，直到您再次将其发布。

| 状态 | 是否可以发送？ |
|-------|-----------|
| **草稿** | 不可以 |
| **已发布** | 可以 |

## SDK 方法（Node.js）

| 操作       | 方法                |
|-----------|-------------------|
| 创建       | `resendtemplates.create(params)`     |
| 获取       | `resendtemplates.get(id)`       |
| 列出       | `resendtemplates.list(params)`     |
| 更新       | `resendtemplates.update(id, params)`    |
| 删除       | `resendtemplates.remove(id)`      | （注意：使用 `remove()` 而不是 `.delete()`） |
| 发布       | `resendtemplates.publish(id)`     |
| 复制       | `resendtemplates.duplicate(id)`     |

### 可链式操作的 `create` 和 `publish` 方法

SDK 支持在调用 `.create()` 或 `.duplicate()` 后立即调用 `.publish()`：

```typescript
const { data, error } = await resend.templates.create({
  name: 'Welcome',
  html: '<p>Hi {{{NAME}}}</p>',
}).publish();
// Template is created AND published in one call
```

## 别名

别名是一个在创建模板时设置的、稳定且易于阅读的标识符。您可以在任何需要使用自动生成的模板 ID 的地方，通过 `id` 字段传递该别名。

```typescript
// Set alias at create time
await resend.templates.create({
  name: 'Order Confirmation',   // display-only
  alias: 'order-confirmation',  // referenceable slug
  html: '<p>Hi {{{CUSTOMER_NAME}}}</p>',
});

// Reference by alias — no need to store the generated tmpl_ ID
template: { id: 'order-confirmation', variables: { CUSTOMER_NAME: 'Alice' } }
```

## 变量语法

在 HTML 和邮件主题中，使用 `{{{VARIABLE_NAME}}}` 来引用变量。

```html
<!-- ✅ Correct -->
<p>Hi {{{CUSTOMER_NAME}}}, your order #{{{ORDER_ID}}} has shipped!</p>

<!-- ❌ Wrong — double braces don't render in Resend -->
<p>Hi {{CUSTOMER_NAME}}</p>
```

请注意：只能进行简单的变量替换，不能使用 `{{#each}}`、`{{#if}}` 等 Handlebars 控制结构。动态列表需要在服务器端预先渲染成单个 HTML 变量。

变量的命名规则比较灵活（例如 `ORDER_ID`、`orderId`、`order_id` 都可以），但必须保持一致：在模板定义中使用的变量命名方式必须与发送邮件时的调用方式完全匹配。

## 使用模板发送邮件

```typescript
const { data, error } = await resend.emails.send(
  {
    from: 'Acme <orders@acme.com>',
    to: ['customer@example.com'],
    template: {
      id: 'order-confirmation',  // alias or auto-generated ID
      variables: { CUSTOMER_NAME: 'Alice', ORDER_ID: '12345' },
    },
  },
  { idempotencyKey: `order-confirm/${orderId}` }
);
```

不能同时使用 `template`、`html`、`text` 或 `react`——这些功能是互斥的。模板中的 `subject` 和 `from` 可以在每次发送邮件时进行自定义。

有关变量限制、保留名称、完整的 CRUD 操作示例、分页功能以及版本历史记录的详细信息，请参阅 [reference.md](reference.md)。