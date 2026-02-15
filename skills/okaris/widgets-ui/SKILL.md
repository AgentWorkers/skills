---
name: widgets-ui
description: |
  Declarative UI widgets from JSON for React/Next.js from ui.inference.sh.
  Render rich interactive UIs from structured agent responses.
  Capabilities: forms, buttons, cards, layouts, inputs, selects, checkboxes.
  Use for: agent-generated UIs, dynamic forms, data display, interactive cards.
  Triggers: widgets, declarative ui, json ui, widget renderer, agent widgets,
  dynamic ui, form widgets, card widgets, shadcn widgets, structured output ui
---

# Widget Renderer

通过 [ui.inference.sh](https://ui.inference.sh) 从 JSON 文件中生成声明式用户界面（Declarative UI）。

## 快速入门

```bash
npx shadcn@latest add https://ui.inference.sh/r/widgets.json
```

## 基本用法

```tsx
import { WidgetRenderer } from "@/registry/blocks/widgets/widget-renderer"
import type { Widget, WidgetAction } from "@/registry/blocks/widgets/types"

const widget: Widget = {
  type: 'ui',
  title: 'My Widget',
  children: [
    { type: 'text', value: 'Hello World' },
    { type: 'button', label: 'Click me', onClickAction: { type: 'click' } },
  ],
}

<WidgetRenderer
  widget={widget}
  onAction={(action, formData) => console.log(action, formData)}
/>
```

## 组件类型

### 布局（Layout）

```json
{ "type": "row", "gap": 2, "children": [...] }
{ "type": "col", "gap": 2, "children": [...] }
{ "type": "box", "background": "gradient-ocean", "padding": 4, "radius": "lg", "children": [...] }
```

### 字体样式（Typography）

```json
{ "type": "title", "value": "Heading", "size": "2xl", "weight": "bold" }
{ "type": "text", "value": "Body text", "variant": "bold" }
{ "type": "caption", "value": "Small text" }
{ "type": "label", "value": "Field label", "fieldName": "email" }
```

### 交互式组件（Interactive Components）

```json
{ "type": "button", "label": "Submit", "variant": "default", "onClickAction": { "type": "submit" } }
{ "type": "input", "name": "email", "placeholder": "Enter email" }
{ "type": "textarea", "name": "message", "placeholder": "Your message" }
{ "type": "select", "name": "plan", "options": [{ "value": "pro", "label": "Pro" }] }
{ "type": "checkbox", "name": "agree", "label": "I agree", "defaultChecked": false }
```

### 显示方式（Display Methods）

```json
{ "type": "badge", "label": "New", "variant": "secondary" }
{ "type": "icon", "iconName": "check", "size": "lg" }
{ "type": "image", "src": "https://...", "alt": "Image", "width": 100, "height": 100 }
{ "type": "divider" }
```

## 示例：飞行信息卡片（Flight Card Example）

```tsx
const flightWidget: Widget = {
  type: 'ui',
  children: [
    {
      type: 'box', background: 'gradient-ocean', padding: 4, radius: 'lg', children: [
        {
          type: 'row', justify: 'between', children: [
            {
              type: 'col', gap: 1, children: [
                { type: 'caption', value: 'departure' },
                { type: 'title', value: 'SFO', size: '2xl', weight: 'bold' },
              ]
            },
            { type: 'icon', iconName: 'plane', size: 'lg' },
            {
              type: 'col', gap: 1, align: 'end', children: [
                { type: 'caption', value: 'arrival' },
                { type: 'title', value: 'JFK', size: '2xl', weight: 'bold' },
              ]
            },
          ]
        },
      ]
    },
  ],
}
```

## 示例：表单（Form Example）

```tsx
const formWidget: Widget = {
  type: 'ui',
  title: 'Contact Form',
  asForm: true,
  children: [
    {
      type: 'col', gap: 3, children: [
        { type: 'input', name: 'name', placeholder: 'Your name' },
        { type: 'input', name: 'email', placeholder: 'Email address' },
        { type: 'textarea', name: 'message', placeholder: 'Message' },
        { type: 'button', label: 'Send', variant: 'default', onClickAction: { type: 'submit' } },
      ]
    },
  ],
}
```

## 渐变效果（Gradient Effects）

| 名称 | 描述 |
|------|-------------|
| `gradient-ocean` | 蓝绿色渐变 |
| `gradient-sunset` | 橙粉色渐变 |
| `gradient-purple` | 紫色渐变 |
| `gradient-cool` | 冷蓝色渐变 |
| `gradient-midnight` | 深蓝色渐变 |

## 动作处理（Action Handling）

```tsx
const handleAction = (action: WidgetAction, formData?: WidgetFormData) => {
  switch (action.type) {
    case 'submit':
      console.log('Form data:', formData)
      break
    case 'click':
      console.log('Button clicked')
      break
  }
}
```

## 相关技能（Related Skills）

```bash
# Full agent component
npx skills add inference-sh/agent-skills@agent-ui

# Chat UI blocks
npx skills add inference-sh/agent-skills@chat-ui

# Tool UI
npx skills add inference-sh/agent-skills@tools-ui
```

## 文档资料（Documentation）

- [组件概述](https://inference.sh/docs/agents/widgets/overview) - 了解组件功能 |
- [组件 JSON 结构](https://inference.sh/docs/agents/widgets/schema) - 组件的 JSON 格式 |
- [生成用户界面的代理（Agents That Generate UI）](https://inference.sh/blog/ux/generative-ui) - 如何构建自动生成用户界面的系统 |

组件文档：[ui.inference.sh/blocks/widgets](https://ui.inference.sh/blocks/widgets)