---
name: distinctive-design-systems
model: reasoning
description: 用于创建具有独特个性和美学风格的设计系统的模式。涵盖了美学文档、颜色令牌架构、排版系统、分层界面以及动态效果（如动画）。适用于构建超越通用模板的设计系统。相关内容与设计系统、设计令牌、美学原则、颜色调色板、排版样式、CSS变量以及Tailwind CSS配置相关。
---

# 独特的设计系统

创建具有鲜明个性的设计系统，让用户留下深刻印象。超越通用模板，构建统一且富有情感共鸣的视觉语言。

---

## 适用场景

- 需要独特视觉标识的新产品开发
- 为 Tailwind 和 CSS 变量创建设计元素
- 记录美学决策，以确保设计的一致性
- 希望突破 Bootstrap/Tailwind 的默认美学风格

---

## 核心理念

一个独特的设计系统应从**美学文档**开始，而非颜色选择工具。

```
1. Define the vibe      → What does this look and feel like?
2. Gather references    → Mood boards, inspiration, examples
3. Document emotions    → What should users feel?
4. Extract tokens       → Colors, typography, spacing, motion
5. Build components     → Implement the documented vision
```

---

## 模式 1：美学基础

在编写 CSS 之前，先记录整体的设计氛围：

### 示例：复古未来风格

**设计氛围**：晶莹剔透、充满光泽，略带忧郁感——色彩以柔和的渐变、清晰的字体和 CRT 风格的纹理为基调，营造出一种充满希望的氛围。所有元素都以“水晶蓝”作为主要色调。

**灵感来源**：
- 复古游戏机启动界面  
- 未来风格的有序菜单  
- 日本角色扮演游戏（JRPG）的用户界面  
- 科幻终端界面  

| 情感 | 实现方式 |  
|---------|-------------------|
| 精确性 | 清晰的字体、表格化的数字、网格布局 |  
| 怀旧感 | CRT 显示器的扫描线效果、像素颗粒感、复古色彩搭配 |  
| 希望感 | 浮动的蓝色圆球、柔和的动画、发光的点缀元素 |  
| 忧郁感 | 深色渐变、柔和的背景、模糊的视觉效果 |

### 示例：温暖中性的赛博朋克风格

**设计氛围**：温暖中性的赛博朋克风格，带有终端设备的质感。与冷色调的黑色和绿色搭配不同，这种风格以温暖的棕褐色为基础，营造出既亲和又科技感十足的氛围。

**关键区别**：大多数黑暗风格的 UI 采用冷色调和霓虹灯效果，而这种风格则利用温暖色调作为视觉亮点——中性的棕褐色基调带来舒适感，同时绿色点缀元素保留了未来感。

| 情感 | 实现方式 |  
|---------|-------------------|
| 技术可信度 | 类似终端设备的字体、单色字体、发光效果 |  
| 亲和力 | 温暖的中性色调而非冷黑色 |  
| 高品质感 | 玻璃材质的面板、模糊的背景效果、多层次的阴影效果 |  
| 未来感 | 电路图案、六边形网格、扫描线效果 |

---

## 模式 2：颜色元素架构

### 三层颜色管理系统

```
CSS Variables (source of truth)
    ↓
Tailwind Config (utility classes)
    ↓
TypeScript Tokens (runtime access)
```

### CSS 变量

```css
:root {
  /* Base tones (use in rgba()) */
  --tone-void: 2, 7, 18;
  --tone-midnight: 6, 12, 32;
  --tone-cyan: 76, 204, 255;
  
  /* Semantic colors (HSL) */
  --primary: 216 90% 68%;
  --success: 154 80% 60%;
  --destructive: 346 80% 62%;
  
  /* Effect variables */
  --glow-primary: 216 90% 68%;
  --glass-bg: 33 18% 71% / 0.8;
}
```

### Tailwind 配置

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        // Tone palette for rgba usage
        tone: {
          void: 'rgb(var(--tone-void))',
          cyan: 'rgb(var(--tone-cyan))',
        },
      },
    },
  },
};
```

### TypeScript 颜色定义

```typescript
// styles/design-tokens.ts
export const colors = {
  primary: 'hsl(var(--primary))',
  success: 'hsl(var(--success))',
  // For rgba usage
  toneCyan: 'rgb(var(--tone-cyan))',
};

export const withOpacity = (token: string, opacity: number) =>
  token.replace('rgb(', 'rgba(').replace(')', `, ${opacity})`);
```

---

## 模式 3：字体系统

### 字体组合

```typescript
fonts: {
  display: ['Orbitron', 'system-ui'],     // Headings, labels
  mono: ['Share Tech Mono', 'monospace'], // Metrics, code
  sans: ['Inter', 'system-ui'],           // Body fallback
}
```

### 基于倍数的字体大小调整

```css
:root {
  --typo-scale: 0.88;  /* Responsive multiplier */
  
  --typo-page-title: calc(1.75rem * var(--typo-scale));
  --typo-section-title: calc(1rem * var(--typo-scale));
  --typo-metric-lg: calc(1.75rem * var(--typo-scale));
  --typo-metric-md: calc(0.96rem * var(--typo-scale));
  --typo-body: calc(0.9rem * var(--typo-scale));
}

@media (min-width: 640px) {
  :root { --typo-scale: 1; }
}
```

### 字体样式

**杂志风格的数字显示**：
```css
.metric {
  font-weight: 800;
  letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums;
}
```

**标签元素**：
```css
.label {
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 700;
  font-size: 0.72rem;
}
```

---

## 模式 4：分层视觉效果

### 层次结构

| 层次 | 名称 | 作用 |  
|-------|------|---------|
| 0 | 环境层 | 全屏渐变效果、慢动作效果 |  
| 1 | 光晕层 | 浮动的圆球、氛围光效 |  
| 2 | 纹理层 | CRT 显示器的扫描线效果、像素颗粒感、滤镜效果 |  
| 3 | 面板层 | 升高的卡片元素、章节标题 |  
| 4 | 内容层 | 数据指标、图表、表格 |  
| 5 | 详细信息层 | 嵌套的子面板、文本行 |

### 组件示例

```tsx
interface SurfaceProps {
  layer?: 'panel' | 'tile' | 'chip' | 'deep' | 'metric';
  children: React.ReactNode;
}

export function Surface({ layer = 'tile', children }: SurfaceProps) {
  return (
    <div className={cn(
      'rounded-lg backdrop-blur-sm',
      layerStyles[layer]
    )}>
      {children}
    </div>
  );
}

const layerStyles = {
  panel: 'bg-tone-cadet/40 border border-tone-jordy/10',
  tile: 'bg-tone-midnight/60 border border-tone-jordy/5',
  chip: 'bg-tone-cyan/10 border border-tone-cyan/20',
  deep: 'bg-tone-void/80',
  metric: 'bg-tone-cadet/20',
};
```

---

## 模式 5：动态效果

### 动画节奏控制

```css
:root {
  --transition-fast: 0.15s;
  --transition-default: 0.2s;
  --transition-medium: 0.25s;
  --transition-slow: 0.3s;
}
```

### 动画样式

```javascript
// tailwind.config.ts
keyframes: {
  'shimmer': {
    '0%': { backgroundPosition: '200% 0' },
    '100%': { backgroundPosition: '-200% 0' },
  },
  'pulse-glow': {
    '0%, 100%': { opacity: '1', transform: 'scale(1)' },
    '50%': { opacity: '0.5', transform: 'scale(1.05)' },
  },
  'slide-in': {
    '0%': { opacity: '0', transform: 'translateY(10px)' },
    '100%': { opacity: '1', transform: 'translateY(0)' },
  },
  'value-flash': {
    '0%': { textShadow: '0 0 8px currentColor' },
    '100%': { textShadow: 'none' },
  },
},
animation: {
  'shimmer': 'shimmer 1.5s ease-in-out infinite',
  'pulse-glow': 'pulse-glow 1.8s ease-in-out infinite',
  'slide-in': 'slide-in 0.2s ease-out',
  'value-flash': 'value-flash 0.6s ease-out',
}
```

---

## 模式 6：玻璃与发光效果

### 玻璃材质的面板

```css
.glass-panel {
  background: linear-gradient(180deg, 
    hsl(var(--glass-bg) / 0.95) 0%, 
    hsl(var(--glass-bg) / 0.85) 100%
  );
  backdrop-filter: blur(16px);
  border: 1px solid hsl(var(--glass-border));
  box-shadow: 
    0 4px 16px hsl(var(--glass-shadow)),
    0 0 0 1px hsl(var(--glass-border) / 0.6) inset,
    0 0 20px hsl(var(--glow-primary) / 0.1);
}
```

### 霓虹灯边框效果

```css
.neon-border {
  border: 1px solid hsl(var(--brand-600) / 0.4);
  box-shadow: 
    0 0 10px hsl(var(--glow-primary) / 0.3),
    0 0 20px hsl(var(--glow-primary) / 0.2),
    inset 0 0 10px hsl(var(--glow-primary) / 0.1);
}
```

---

## 经验证的美学方向

| 美学风格 | 灵感来源 | 情感表达 |  
|-----------|--------------|----------|
| 复古未来风格的玻璃质感 | 复古游戏机 UI、JRPG 用户界面、科幻终端 | 精确性、怀旧感、希望感 |  
| 温暖中性的赛博朋克风格 | 未来风格的终端界面、科幻电影中的界面 | 专业感、亲和力 |  
| 杂志风格的金融界面 | 交易平台、数据仪表盘 | 信任感、清晰度、精致感 |

---

## 相关技能

- **元技能**：[ai/skills/meta/design-system-creation/](../../meta/design-system-creation/) — 完整的设计系统开发流程  
- [design-system-components](../design-system-components/) — CVA 组件模式和基础视觉元素  
- [loading-state-patterns](../loading-state-patterns/) — 与设计风格相匹配的加载效果  

---

## 绝对不要这样做

- **不要使用纯黑色 (#000) 作为背景色** — 应始终使用带有色调的黑色  
- **不要使用纯白色 (#fff) 作为文本颜色** — 应使用带有色调的白色  
- **不要使用 Inter/Roboto 作为标题字体** — 应使用具有辨识度的字体  
- **不要使用 Tailwind 的默认颜色** — 应自定义颜色调色板  
- **不要省略背景的模糊效果** — 玻璃材质的面板需要模糊效果  
- **不要在可读内容上使用装饰性图案** — 模糊效果仅应用于背景  
- **不要使用高饱和度的颜色且不设置透明度** — 应使用 rgba() 进行颜色调整  
- **不要硬编码字体大小** — 应使用可调整的字体大小设置  
- **不要忽略美学文档** — 在编写代码之前，先确定整体设计氛围  

---

## 文件结构

```
styles/
├── globals.css          # CSS variables, base styles
├── design-tokens.ts     # TypeScript token exports
├── theme.css            # Component patterns
└── patterns/
    ├── glass.css
    ├── neon.css
    └── backgrounds.css

tailwind.config.ts       # Token integration
```

---

## 快速参考

```css
/* 1. Define CSS variables */
:root {
  --tone-primary: 76, 204, 255;
  --primary: 200 90% 65%;
}

/* 2. Configure Tailwind */
colors: {
  primary: 'hsl(var(--primary))',
  tone: { primary: 'rgb(var(--tone-primary))' },
}

/* 3. Use in components */
<div className="bg-primary text-tone-primary/80">
```