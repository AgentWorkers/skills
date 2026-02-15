---
name: tailwind-v4-+-shadcn/ui-stack
model: fast
---

# Tailwind v4 + shadcn/ui 组合方案

这是一个经过生产环境测试的 Tailwind v4 与 shadcn/ui 配置方案，通过强制性的四步流程有效避免了 8 种常见错误。

## 什么是 Tailwind v4 + shadcn/ui？

- 完整的 Tailwind v4 + shadcn/ui 配置：
  - 强制性的四步主题设置流程
  - 基于 CSS 变量的颜色系统
  - 自动切换暗模式功能
  - 预防 8 种常见配置错误
  - 从 Tailwind v3 迁移的指南
  - 适用于生产环境的模板

## 适用场景

- 新建使用 Tailwind v4 的 React/Vite 项目
- 从 Tailwind v3 迁移到 v4
- 配置 shadcn/ui 与 Tailwind v4
- 解决颜色显示异常、暗模式失效或构建失败等问题
- 修复与 `@theme inline`、`@apply` 或 `@layer base` 相关的问题

## 关键词

- Tailwind v4
- TailwindCSS 4
- shadcn
- shadcn/ui
- @theme inline
- 暗模式
- CSS 变量
- vite
- tw-animate-css
- Tailwind 配置
- 迁移

**生产环境验证：** WordPress Auditor (https://wordpress-auditor.webfonts.workers.dev)
**版本：** tailwindcss@4.1.18, @tailwindcss/vite@4.1.18

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install tailwind-v4-shadcn
```


---

## 快速入门

```bash
# 1. Install dependencies
pnpm add tailwindcss @tailwindcss/vite
pnpm add -D @types/node tw-animate-css
pnpm dlx shadcn@latest init

# 2. Delete v3 config (v4 doesn't use it)
rm tailwind.config.ts
```

**vite.config.ts：**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': path.resolve(__dirname, './src') } }
})
```

**components.json（关键文件）：**
```json
{
  "tailwind": {
    "config": "",
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true
  }
}
```

---

## 强制性的四步流程

跳过任意一步都会导致主题设置失败，请严格遵循以下步骤：

### 第一步：在根目录定义 CSS 变量

```css
/* src/index.css */
@import "tailwindcss";
@import "tw-animate-css";

:root {
  --background: hsl(0 0% 100%);
  --foreground: hsl(222.2 84% 4.9%);
  --primary: hsl(221.2 83.2% 53.3%);
  --primary-foreground: hsl(210 40% 98%);
  /* ... all light mode colors with hsl() wrapper */
}

.dark {
  --background: hsl(222.2 84% 4.9%);
  --foreground: hsl(210 40% 98%);
  --primary: hsl(217.2 91.2% 59.8%);
  --primary-foreground: hsl(222.2 47.4% 11.2%);
  /* ... all dark mode colors */
}
```

**注意：** 变量必须定义在根目录（而非 `@layer base` 内部），并使用 `hsl()` 包装器。

### 第二步：将变量映射到 Tailwind CSS

```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  /* ... map ALL CSS variables */
}
```

**原因：** 这一步会生成辅助类（如 `bg-background`、`text-primary`）。如果没有这一步，辅助类将无法使用。

### 第三步：应用基础样式

```css
@layer base {
  body {
    background-color: var(--background);
    color: var(--foreground);
  }
}
```

**注意：** 直接引用变量，切勿重复包装：例如 `hsl(var(--background))`。

### 第四步：自动切换暗模式

```tsx
<div className="bg-background text-foreground">
  {/* Theme switches automatically via .dark class */}
</div>
```

对于具有语义意义的颜色，无需使用 `dark:` 变体。

---

## 重要规则

### 必须遵守的规则：
1. 在 `:root` 或 `.dark` 中使用 `hsl()` 包装颜色：`--bg: hsl(0 0% 100%)`
2. 使用 `@theme inline` 来映射所有 CSS 变量
3. 在 `components.json` 中设置 `"config": ""`
4. 如果存在 `tailwind.config.ts`，请删除它
5. 使用 `@tailwindcss/vite` 插件（而非 PostCSS）

### 绝对不能做的：
1. 将 `:root` 或 `.dark` 放在 `@layer base` 内部
2. 使用 `.dark { @theme { } }`（v4 不支持嵌套的 `@theme`）
3. 重复包装颜色：例如 `hsl(var(--background))`
4. 使用 `tailwind.config.ts` 来管理主题设置
5. 在 `@layer base/components` 类上使用 `@apply`
6. 对于具有语义意义的颜色使用 `dark:` 变体

---

## 常见错误及解决方法

### 错误 1：`tw-animate-css` 无法导入

**错误：** “无法找到模块 ‘tailwindcss-animate’”

```bash
# Wrong (v3 package)
npm install tailwindcss-animate

# Correct (v4 package)
pnpm add -D tw-animate-css
```

```css
@import "tailwindcss";
@import "tw-animate-css";
```

### 错误 2：颜色显示异常

**原因：** 缺少 `@theme inline` 的映射

```css
@theme inline {
  --color-primary: var(--primary);
  /* Map ALL variables */
}
```

### 错误 3：暗模式无法切换

**原因：** 缺少 ThemeProvider

请参考 `templates/theme-provider.tsx` 并正确配置应用程序。

### 错误 4：构建失败

**原因：** 配置文件格式不正确

```bash
rm tailwind.config.ts  # v4 doesn't use this
```

### 错误 5：`@theme inline` 导致多主题系统出现问题

**原因：** `@theme inline` 会在构建时固定颜色值

对于多主题系统，请使用 `@theme`（而非 `@theme inline`）：

```css
/* For multi-theme (not just light/dark) */
@theme {
  --color-text-primary: var(--color-slate-900);
}

@layer theme {
  [data-theme="dark"] {
    --color-text-primary: var(--color-white);
  }
}
```

### 错误 6：`@apply` 使用错误

**原因：** 无法应用某些辅助类

v4 中的 `@apply` 行为发生了变化：

```css
/* Wrong (v3 pattern) */
@layer components {
  .custom-button { @apply px-4 py-2; }
}

/* Correct (v4 pattern) */
@utility custom-button {
  @apply px-4 py-2;
}
```

### 错误 7：`@layer base` 的样式被忽略

**原因：** CSS 层级覆盖问题

```css
/* Better: Don't use @layer base for critical styles */
body {
  background-color: var(--background);
}
```

---

## 快速参考

| 症状 | 原因 | 解决方法 |
|---------|-------|-----|
| `bg-primary` 无法显示颜色 | 缺少 `@theme inline` 的映射 | 添加相应的映射 |
| 颜色显示为黑色或白色 | 变量包装错误（使用了 `hsl(var(--color))` 而不是 `hsl(var(--color))`） | 使用 `var(--color)` |
| 暗模式无法切换 | 缺少 ThemeProvider | 正确配置 ThemeProvider |
| 构建失败 | 存在 `tailwind.config.ts` 文件 | 删除该文件 |
| 动画效果异常 | 依赖的库版本不正确 | 使用 `tw-animate-css` |

---

## Tailwind v4 的新特性

- **OKLCH 颜色空间**：v4 使用 OKLCH 颜色空间，确保颜色显示更加均匀。
- **内置的容器查询** 和 **行限制功能**。

---


## 从 Tailwind v3 迁移

- 删除 `tailwind.config.ts`
- 将主题设置移到 CSS 中，并使用 `@theme inline`
- 将 `tailwindcssanimate` 替换为 `tw-animate-css`
- 将 `require()` 替换为 `@plugin`
- 将 `@apply` 从 `@layer components` 中移除，改为使用 `@utility`

### 颜色迁移

---


## 视觉上的变化

- 环形图元素的默认宽度从 3px 更改为 1px（使用 `ring-3` 以保持与 v3 兼容）
- 标题样式已从 Preflight 移除（需通过 `@tailwindcss/typography` 或自定义样式添加）

---

## 相关文件

- `templates/index.css`：包含所有 CSS 变量的完整样式文件
- `templates/theme-provider.tsx`：暗模式提供者
- `templates/vite.config.ts`：Vite 配置文件
- `templates/components.json`：shadcn/ui v4 的配置文件
- `templates/utils.ts`：辅助函数库
- `references/architecture.md`：四步配置流程的详细说明
- `references/migration-guide.md`：颜色迁移指南
- `references/dark-mode.md`：完整的暗模式配置指南

---

## 配置检查清单

- 确保已安装 `@tailwindcss/vite`
- `vite.config.ts` 中使用了 `tailwindcss()` 插件
- `components.json` 中设置了 `"config": ""`
- 不存在 `tailwind.config.ts`
- `src/index.css` 遵循四步配置流程
- 应用程序正确使用了 ThemeProvider
- 暗模式切换功能正常工作

---

## 绝对不能做的事情：

- 不要在 `@layer base` 内部使用 `:root` 或 `.dark`
- 在 v4 中使用 `tailwind.config.ts`（它会被忽略）
- 重复包装颜色（例如 `hsl(var(--background))`
- 在 v4 中使用 `tailwindcssanimate`（应使用 `tw-animate-css`）
- 在 `@layer base/components` 类上使用 `@apply`
- 跳过 `@theme inline` 的步骤