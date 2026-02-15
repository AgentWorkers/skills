---
name: design-system-creation
model: reasoning
description: 从零开始创建独特设计系统的完整工作流程。该流程协调了美学文档、代币架构、组件以及动画效果等方面的工作。适用于新设计系统的开发或现有设计系统的重构。相关操作包括：创建设计系统、设计代币、设置设计系统参数、定义视觉识别元素以及构建主题系统。
---

# 设计系统创建（元技能）

这是一个用于创建具有独特个性的设计系统的完整工作流程。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install design-system-creation
```


---

## 使用场景

- 需要视觉标识的新产品开发
- 重构风格分散的现有设计
- 构建包含设计元素的组件库
- 希望超越通用的 Tailwind/Bootstrap 美学风格

---

## 工作流程概述

```
1. Aesthetic Foundation   → Document the vibe before code
2. Color Token System     → CSS variables + Tailwind + TypeScript
3. Typography System      → Font stack + scale + patterns
4. Surface Components     → Layered primitives with CVA
5. Motion Tokens          → Consistent animation timing
6. Loading States         → Skeleton + shimmer patterns
```

---

## 第一步：美学基础

**阅读材料：`ai/skills/design-systems/distinctive-design-systems`**

在编写 CSS 之前，先记录下你的设计美学理念：

```markdown
## The Vibe
[1-2 sentences describing the visual feel]

## Inspirations
- [Reference 1 - what to take from it]
- [Reference 2 - what to take from it]

## Emotions to Evoke
| Emotion | How It's Achieved |
|---------|-------------------|
| [X] | [specific technique] |
| [Y] | [specific technique] |
```

### 建议考虑的美学方向

| 美学风格 | 特征                |
|-----------|-------------------|
| 复古未来风   | CRT 纹理、发光效果、等宽字体       |
| 温暖赛博朋克风 | 棕褐色/米色基调、翡翠色点缀、玻璃材质   |
| 杂志风格（金融类）| 粗体字体、深色主题、渐变文字     |

---

## 第二步：颜色体系构建

**阅读材料：`ai/skills/design-systems/distinctive-design-systems`**

创建一个三层颜色体系：

```css
/* 1. CSS Variables (source of truth) */
:root {
  --tone-primary: 76, 204, 255;
  --primary: 200 90% 65%;
  --success: 154 80% 60%;
  --destructive: 346 80% 62%;
}
```

```typescript
// 2. Tailwind Config
colors: {
  primary: 'hsl(var(--primary))',
  tone: { primary: 'rgb(var(--tone-primary))' },
}
```

```typescript
// 3. TypeScript Tokens (optional)
export const colors = {
  primary: 'hsl(var(--primary))',
};
```

---

## 第三步：字体系统设计

**阅读材料：`ai/skills/design-systems/distinctive-design-systems`**

定义字体及其使用规范：

```css
:root {
  --font-display: 'Orbitron', system-ui;
  --font-mono: 'Share Tech Mono', monospace;
  --font-sans: 'Inter', system-ui;
  
  --typo-scale: 0.88;  /* Mobile */
}

@media (min-width: 640px) {
  :root { --typo-scale: 1; }
}
```

### 字体样式示例

```css
/* Magazine-style numbers */
.metric { font-weight: 800; letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }

/* Labels */
.label { text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; }
```

---

## 第四步：界面组件设计

**阅读材料：`ai/skills/design-systems/design-system-components`**

使用 CVA（Component Visualization Architecture）构建分层界面组件：

```tsx
const surfaceVariants = cva(
  'rounded-lg backdrop-blur-sm transition-colors',
  {
    variants: {
      layer: {
        panel: 'bg-tone-cadet/40 border border-tone-jordy/10',
        tile: 'bg-tone-midnight/60 border border-tone-jordy/5',
        chip: 'bg-tone-cyan/10 border border-tone-cyan/20 rounded-full',
      },
    },
  }
);

export function Surface({ layer, children }: SurfaceProps) {
  return <div className={surfaceVariants({ layer })}>{children}</div>;
}
```

---

## 第五步：动态效果设计

**阅读材料：`ai/skills/design-systems/distinctive-design-systems`**

定义统一的动画效果：

```javascript
// tailwind.config.ts
keyframes: {
  'shimmer': { '0%': { backgroundPosition: '200% 0' }, '100%': { backgroundPosition: '-200% 0' } },
  'pulse-glow': { '0%, 100%': { opacity: '1' }, '50%': { opacity: '0.5' } },
  'slide-in': { '0%': { opacity: '0', transform: 'translateY(10px)' }, '100%': { opacity: '1', transform: 'translateY(0)' } },
},
animation: {
  'shimmer': 'shimmer 1.5s ease-in-out infinite',
  'pulse-glow': 'pulse-glow 1.8s ease-in-out infinite',
  'slide-in': 'slide-in 0.2s ease-out',
}
```

---

## 第六步：加载状态处理

**阅读材料：`ai/skills/design-systems/load-state-patterns`**

创建符合你设计风格的加载状态组件：

```tsx
export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        'rounded-md bg-muted animate-shimmer',
        'bg-gradient-to-r from-muted via-muted-foreground/10 to-muted bg-[length:200%_100%]',
        className
      )}
    />
  );
}
```

---

## 组件技能参考

| 技能            | 用途                        |
|-----------------|---------------------------|
| `distinctive-design-systems` | 设计美学基础、颜色体系构建    |
| `design-system-components` | 界面组件设计、CVA 应用           |
| `animated-financial-display` | 数字动画效果实现           |
| `loading-state-patterns` | 加载状态组件的实现             |
| `financial-data-visualization` | 数据可视化功能的实现           |

---

## 文件结构

```
styles/
├── globals.css          # CSS variables, base styles
├── design-tokens.ts     # TypeScript exports
└── theme.css            # Component patterns

tailwind.config.ts       # Token integration

components/
├── ui/
│   ├── surface.tsx      # Surface primitive
│   ├── skeleton.tsx     # Loading states
│   └── button.tsx       # Variant components
```

---

## 避免的做法

- **切勿在记录美学理念之前就开始编写代码** — 先确定设计风格再编写代码
- **切勿使用纯黑色（#000）作为背景色** — 应使用带有色调的黑色来增加层次感
- **切勿使用纯白色（#fff）作为文字颜色** — 应使用与整体配色方案相匹配的白色
- **切勿为了简化代码而省略颜色设置** — 颜色设置有助于保持设计的一致性
- **切勿在没有变体设计的情况下创建组件** — 应使用 CVA 等工具来确保一致性
- **切勿使用 Inter/Roboto 作为标题字体** — 应使用具有辨识度的自定义字体
- **切勿使用 Tailwind 的默认颜色** — 应自定义颜色方案
- **切勿省略玻璃材质的背景模糊效果** — 玻璃材质需要模糊效果才能体现质感
- **切勿在可阅读的内容上使用装饰性图案** — 装饰性图案仅应用于背景
- **切勿使用高饱和度的颜色而不添加透明度** — 应使用 rgba() 来调节颜色饱和度

---

## 检查清单

- [ ] 记录设计美学基础（风格、灵感来源、情感表达）
- [ ] 创建颜色体系（CSS + Tailwind + TypeScript）
- [ ] 定义字体样式及使用规范
- [ ] 构建界面基础组件
- [ ] 添加动态效果和动画
- [ ] 创建加载状态组件
- [ ] 记录设计中的禁忌做法（避免犯的错误）