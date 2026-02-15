---
name: tg-miniapp
description: 轻松构建 Telegram Mini 应用程序。提供针对安全区域、全屏模式、BackButton 处理程序、内联分享功能、position:fixed 属性相关问题的解决方案，以及 React 开发中常见的问题解决方法。适用于构建或调试 Telegram Mini 应用程序时，或在遇到 WebApp API、安全区域或分享功能相关问题时使用。
---

# Telegram Mini App 开发

针对 Telegram Mini App 常见问题的经过实践验证的解决方案。

## 快速参考

### 安全区域（全屏模式）
```typescript
// Use reactive hook - values are async and context-dependent
const safeArea = useSafeAreaInset(); // from references/hooks.ts
<div style={{ paddingTop: safeArea.top }}>Header</div>
```

### `position:fixed` 出现问题
Telegram 会对容器应用 `transform` 动作。请使用 `createPortal` 方法：
```tsx
import { createPortal } from 'react-dom';
createPortal(<Modal />, document.body);
```

### 返回按钮（BackButton）无法正常使用
请使用 `@telegram-apps/sdk`，而不是原始的 WebApp：
```typescript
import { onBackButtonClick, showBackButton } from '@telegram-apps/sdk';
onBackButtonClick(handleBack);
```

### 使用内联模式（Inline Mode）进行分享
1. 启用内联模式：通过 `@BotFather` 发送 `/setinline` 命令，然后选择目标机器人。
2. 后端调用 `savePreparedInlineMessage` 方法，该方法会返回 `prepared_message_id`。
3. 前端调用 `WebApp.shareMessage(prepared_message_id)` 方法进行分享。

**注意：** `prepared_message_id` 是 **一次性使用的**——每次分享时都需要重新生成。
对于静态内容，可以考虑将图片缓存到 R2/CDN 并为每次分享重新生成图片。

### React “0” 渲染模式
```tsx
// WRONG: renders literal "0"
{count && <span>{count}</span>}

// CORRECT
{count > 0 && <span>{count}</span>}
```

## 详细指南

- **[references/KNOWLEDGE.md](references/KNOWLEDGE.md)** — 包含所有注意事项和解决方案的完整知识库。
- **[references/hooks.ts](references/hooks.ts)** — 可复用的 React 钩子函数（如 `useSafeAreaInset`、`useFullscreen` 等）。
- **[references/components.tsx](references/components.tsx)** — 可直接使用的组件（如 `SafeAreaHeader`、`DebugOverlay`）。

## 测试清单

在发布之前，请进行以下测试：
- [ ] 从文件夹中打开应用
- [ ] 从直接与机器人对话的界面中打开应用
- [ ] 在 iOS 设备上测试
- [ ] 在 Android 设备上测试
- [ ] 测试分享流程（点击 → 关闭 → 再次点击）
- [ ] 测试向不同类型的聊天对象（用户、群组、频道）分享
- [ ] 测试返回按钮的功能
- [ ] 测试带有固定标题栏的滚动功能