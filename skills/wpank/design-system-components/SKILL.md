---
name: design-system-components
model: standard
description: 使用 Surface 原语、CVA 变体以及一致的样式来构建设计系统组件的模式。适用于构建遵循设计令牌架构的可重用 UI 组件。这些模式会在 Surface 组件、CVA（Class-Variable-Authority）、组件变体以及设计令牌发生变化时被触发。
---

# 设计系统组件

构建可重用的组件，这些组件利用设计令牌（design tokens）结合 Surface 原语（Surface primitives）和 CVA（class-variance-authority）来实现功能。

---

## 使用场景

- 使用设计令牌构建组件库
- 需要根据变体（如大小、颜色、状态）进行样式调整
- 创建具有统一外观的分层用户界面（layered UI）
- 希望组件 API 具有类型安全性（type-safe）

---

## 模式 1：Surface 原语

使用单个组件来处理所有分层界面：

```tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const surfaceVariants = cva(
  'rounded-lg backdrop-blur-sm transition-colors',
  {
    variants: {
      layer: {
        panel: 'bg-tone-cadet/40 border border-tone-jordy/10 shadow-card',
        tile: 'bg-tone-midnight/60 border border-tone-jordy/5',
        chip: 'bg-tone-cyan/10 border border-tone-cyan/20 rounded-full',
        deep: 'bg-tone-void/80',
        metric: 'bg-tone-cadet/20 border border-tone-jordy/8',
        glass: 'bg-glass-bg backdrop-blur-lg border border-glass-border',
      },
      interactive: {
        true: 'cursor-pointer hover:bg-tone-cadet/50 active:scale-[0.98]',
        false: '',
      },
      glow: {
        true: 'shadow-glow',
        false: '',
      },
    },
    defaultVariants: {
      layer: 'tile',
      interactive: false,
      glow: false,
    },
  }
);

interface SurfaceProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof surfaceVariants> {}

export function Surface({
  layer,
  interactive,
  glow,
  className,
  ...props
}: SurfaceProps) {
  return (
    <div
      className={cn(surfaceVariants({ layer, interactive, glow }), className)}
      {...props}
    />
  );
}
```

### 使用方法

```tsx
<Surface layer="panel" className="p-4">
  <h2>Dashboard</h2>
</Surface>

<Surface layer="chip" interactive>
  <span>Active</span>
</Surface>

<Surface layer="metric" glow>
  <span className="text-2xl">$1,234.56</span>
</Surface>
```

---

## 模式 2：CVA 按钮变体

```tsx
const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-all focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
        cyber: 'bg-gradient-to-r from-tone-cadet to-tone-azure text-white border border-tone-cyan/30 shadow-glow hover:shadow-glow-lg',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);
```

---

## 模式 3：度量显示组件

```tsx
const metricVariants = cva(
  'font-mono tabular-nums',
  {
    variants: {
      size: {
        lg: 'text-3xl font-bold tracking-tight',
        md: 'text-xl font-semibold',
        sm: 'text-base font-medium',
      },
      trend: {
        positive: 'text-success',
        negative: 'text-destructive',
        neutral: 'text-foreground',
      },
    },
    defaultVariants: {
      size: 'md',
      trend: 'neutral',
    },
  }
);

interface MetricProps extends VariantProps<typeof metricVariants> {
  value: string | number;
  label?: string;
  prefix?: string;
  suffix?: string;
}

export function Metric({
  value,
  label,
  prefix = '',
  suffix = '',
  size,
  trend,
}: MetricProps) {
  return (
    <div className="flex flex-col">
      {label && (
        <span className="text-xs uppercase tracking-wider text-muted-foreground mb-1">
          {label}
        </span>
      )}
      <span className={cn(metricVariants({ size, trend }))}>
        {prefix}{value}{suffix}
      </span>
    </div>
  );
}
```

---

## 模式 4：带标题的卡片

```tsx
interface CardProps {
  title?: string;
  description?: string;
  action?: React.ReactNode;
  children: React.ReactNode;
}

export function Card({ title, description, action, children }: CardProps) {
  return (
    <Surface layer="panel" className="flex flex-col">
      {(title || action) && (
        <div className="flex items-center justify-between px-4 py-3 border-b border-tone-jordy/10">
          <div>
            {title && (
              <h3 className="font-display text-sm font-medium">{title}</h3>
            )}
            {description && (
              <p className="text-xs text-muted-foreground">{description}</p>
            )}
          </div>
          {action}
        </div>
      )}
      <div className="p-4">{children}</div>
    </Surface>
  );
}
```

---

## 模式 5：徽章/芯片变体

```tsx
const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary/10 text-primary border border-primary/20',
        success: 'bg-success/10 text-success border border-success/20',
        warning: 'bg-warning/10 text-warning border border-warning/20',
        destructive: 'bg-destructive/10 text-destructive border border-destructive/20',
        outline: 'border border-input text-foreground',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);
```

---

## 模式 6：组合变体

将 CVA 与条件类（conditional classes）结合使用：

```tsx
function StatusIndicator({ 
  status, 
  size = 'md' 
}: { 
  status: 'online' | 'offline' | 'away';
  size?: 'sm' | 'md' | 'lg';
}) {
  const sizeClasses = {
    sm: 'size-2',
    md: 'size-3',
    lg: 'size-4',
  };

  const statusClasses = {
    online: 'bg-success animate-pulse',
    offline: 'bg-muted-foreground',
    away: 'bg-warning',
  };

  return (
    <span
      className={cn(
        'rounded-full',
        sizeClasses[size],
        statusClasses[status]
      )}
    />
  );
}
```

---

## 相关技能

- **元技能：** [ai/skills/meta/design-system-creation/](../../meta/design-system-creation/) — 完整的设计系统工作流程
- [distinctive-design-systems](../distinctive-design-systems/) — 令牌架构与美学基础
- [loading-state-patterns](../loading-state-patterns/) — 用于显示加载状态的骨架组件

---

## 绝对不要做的事情

- **自定义卡片容器** — 应使用 Surface 原语
- **在组件中硬编码颜色** — 应使用设计令牌
- **忽略变体类型** — CVA 提供了类型安全性
- **混合使用不同的样式方法** — 选择 CVA 或 cn()，而不是随意使用内联样式
- **忽略默认变体** — 组件应能够在没有属性的情况下正常工作

---

## 快速参考

```tsx
// 1. Define variants with CVA
const variants = cva('base-classes', {
  variants: {
    size: { sm: '...', md: '...', lg: '...' },
    color: { primary: '...', secondary: '...' },
  },
  defaultVariants: { size: 'md', color: 'primary' },
});

// 2. Type props from variants
interface Props extends VariantProps<typeof variants> {}

// 3. Apply in component
<div className={cn(variants({ size, color }), className)} />
```