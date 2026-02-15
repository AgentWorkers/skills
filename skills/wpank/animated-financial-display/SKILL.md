---
name: animated-financial-display
model: standard
description: **使用弹簧物理效果、格式化以及视觉反馈来动画化财务数字的技巧**  
涵盖了动画化计数器、价格行情显示、百分比变化以及数值闪烁效果等内容。适用于构建财务仪表板或交易用户界面时使用。这些技巧可用于实现数字的动画效果、价格动态显示、数值格式化以及视觉上的反馈效果。  

**适用场景**：  
- 动画化财务数据（如计数器、价格行情）  
- 百分比变化展示  
- 数值闪烁效果  

**技术要点**：  
- **弹簧物理效果**：利用物理模拟原理实现数字的平滑动画效果  
- **格式化**：自定义数字的显示格式（如货币单位、小数位数等）  
- **视觉反馈**：通过颜色变化、动画效果等增强用户交互体验  

**应用场景示例**：  
- 在金融仪表板中，数字会随着数据的更新而平滑地移动或闪烁，以吸引用户的注意力  
- 价格行情界面中，价格数字会随着市场波动而实时更新并伴有动画效果  
- 百分比变化时，数字会以动画方式显示变化幅度  

**推荐使用场景**：  
- 财务数据分析工具  
- 交易软件界面  
- 投资决策支持系统  

**注意事项**：  
- 确保动画效果与整体设计风格保持一致  
- 根据实际需求调整动画的节奏和细节  
- 测试不同设备上的显示效果，确保兼容性
---

# 动态财务数据显示

通过流畅的动画、正确的格式以及数值变化的视觉反馈，打造引人入胜的财务数字展示效果。

---

## 使用场景

- 构建显示实时价格的交易仪表板
- 实时更新投资组合价值
- 显示需要关注的指标变化
- 任何可以从动态效果中受益的财务用户界面

---

## 模式 1：弹簧动画数字（Spring-Animated Number）

使用 framer-motion 的弹簧物理效果实现动画：

```tsx
import { useSpring, animated } from '@react-spring/web';
import { useEffect, useRef } from 'react';

interface AnimatedNumberProps {
  value: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  duration?: number;
}

export function AnimatedNumber({
  value,
  prefix = '',
  suffix = '',
  decimals = 2,
  duration = 500,
}: AnimatedNumberProps) {
  const prevValue = useRef(value);

  const { number } = useSpring({
    from: { number: prevValue.current },
    to: { number: value },
    config: { duration },
  });

  useEffect(() => {
    prevValue.current = value;
  }, [value]);

  return (
    <animated.span className="tabular-nums">
      {number.to((n) => `${prefix}${n.toFixed(decimals)}${suffix}`)}
    </animated.span>
  );
}
```

### 使用方法

```tsx
<AnimatedNumber value={price} prefix="$" decimals={2} />
<AnimatedNumber value={percentage} suffix="%" decimals={1} />
```

---

## 模式 2：数值变化时的闪光效果（Value with Flash Effect）

数值发生变化时，数字会闪烁：

```tsx
import { useEffect, useState, useRef } from 'react';
import { cn } from '@/lib/utils';

interface FlashingValueProps {
  value: number;
  formatter: (value: number) => string;
}

export function FlashingValue({ value, formatter }: FlashingValueProps) {
  const [flash, setFlash] = useState<'up' | 'down' | null>(null);
  const prevValue = useRef(value);

  useEffect(() => {
    if (value !== prevValue.current) {
      setFlash(value > prevValue.current ? 'up' : 'down');
      prevValue.current = value;
      
      const timer = setTimeout(() => setFlash(null), 600);
      return () => clearTimeout(timer);
    }
  }, [value]);

  return (
    <span
      className={cn(
        'transition-colors duration-600',
        flash === 'up' && 'text-success',
        flash === 'down' && 'text-destructive'
      )}
    >
      {formatter(value)}
    </span>
  );
}
```

---

## 模式 3：财务数字格式化（Financial Number Formatting）

对财务数字进行专业的格式化处理：

```typescript
// lib/formatters.ts
export function formatCurrency(
  value: number,
  options: {
    currency?: string;
    compact?: boolean;
    decimals?: number;
  } = {}
): string {
  const { currency = 'USD', compact = false, decimals = 2 } = options;

  if (compact && Math.abs(value) >= 1_000_000_000) {
    return `$${(value / 1_000_000_000).toFixed(1)}B`;
  }
  if (compact && Math.abs(value) >= 1_000_000) {
    return `$${(value / 1_000_000).toFixed(1)}M`;
  }
  if (compact && Math.abs(value) >= 1_000) {
    return `$${(value / 1_000).toFixed(1)}K`;
  }

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

export function formatPercentage(
  value: number,
  options: { showSign?: boolean; decimals?: number } = {}
): string {
  const { showSign = true, decimals = 2 } = options;
  const sign = showSign && value > 0 ? '+' : '';
  return `${sign}${value.toFixed(decimals)}%`;
}

export function formatNumber(
  value: number,
  options: { compact?: boolean; decimals?: number } = {}
): string {
  const { compact = false, decimals = 0 } = options;

  if (compact) {
    return Intl.NumberFormat('en-US', {
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(value);
  }

  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}
```

---

## 模式 4：价格行情组件（Price Ticker Component）

用于显示实时价格变化的组件：

```tsx
interface PriceTickerProps {
  symbol: string;
  price: number;
  change24h: number;
  changePercent24h: number;
}

export function PriceTicker({
  symbol,
  price,
  change24h,
  changePercent24h,
}: PriceTickerProps) {
  const isPositive = changePercent24h >= 0;

  return (
    <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
      <div className="flex items-center gap-2">
        <span className="font-display font-medium">{symbol}</span>
      </div>
      
      <div className="flex items-center gap-3">
        <AnimatedNumber value={price} prefix="$" decimals={2} />
        
        <span
          className={cn(
            'text-sm font-mono tabular-nums',
            isPositive ? 'text-success' : 'text-destructive'
          )}
        >
          {formatPercentage(changePercent24h)}
        </span>
      </div>
    </div>
  );
}
```

---

## 模式 5：带动画的指标卡片（Metric Card with Animation）

为关键指标添加动画效果：

```tsx
interface MetricCardProps {
  label: string;
  value: number;
  previousValue?: number;
  format: 'currency' | 'percent' | 'number';
}

export function MetricCard({
  label,
  value,
  previousValue,
  format,
}: MetricCardProps) {
  const formatValue = (v: number) => {
    switch (format) {
      case 'currency': return formatCurrency(v, { compact: true });
      case 'percent': return formatPercentage(v);
      case 'number': return formatNumber(v, { compact: true });
    }
  };

  const change = previousValue ? ((value - previousValue) / previousValue) * 100 : null;

  return (
    <Surface layer="metric" className="p-4">
      <div className="text-xs uppercase tracking-wider text-muted-foreground mb-1">
        {label}
      </div>
      
      <div className="text-2xl font-bold font-mono tabular-nums">
        <FlashingValue value={value} formatter={formatValue} />
      </div>
      
      {change !== null && (
        <div className={cn(
          'text-xs font-mono mt-1',
          change >= 0 ? 'text-success' : 'text-destructive'
        )}>
          {formatPercentage(change)} from previous
        </div>
      )}
    </Surface>
  );
}
```

---

## 模式 6：CSS 数值闪烁动画（CSS Value Flash Animation）

利用 CSS 实现数值变化的动画效果：

```css
@keyframes value-flash-up {
  0% { 
    color: hsl(var(--success));
    text-shadow: 0 0 8px hsl(var(--success) / 0.5);
  }
  100% { 
    color: inherit;
    text-shadow: none;
  }
}

@keyframes value-flash-down {
  0% { 
    color: hsl(var(--destructive));
    text-shadow: 0 0 8px hsl(var(--destructive) / 0.5);
  }
  100% { 
    color: inherit;
    text-shadow: none;
  }
}

.animate-flash-up {
  animation: value-flash-up 0.6s ease-out;
}

.animate-flash-down {
  animation: value-flash-down 0.6s ease-out;
}
```

---

## 相关技能

- **元技能：** [ai/skills/meta/design-system-creation/](../../meta/design-system-creation/) — 完整的设计系统工作流程
- [financial-data-visualization](../financial-data-visualization/) — 数据图表化和可视化技术
- [realtime-react-hooks](../../realtime/realtime-react-hooks/) — 实时数据更新钩子

---

## 绝对不要这样做

- **省略表格格式** — 数字在变化时可能会突然跳动
- **使用线性动画** — 弹簧/缓动效果更自然
- **快速动画化小数部分** — 过度的动画效果会分散注意力
- **忽略简洁的格式** — 大数字需要使用缩写
- **直接显示原始浮点数** — 必须使用适当的精度进行格式化
- **每次渲染都闪烁** — 仅在数值实际变化时才显示动画效果

---

## 数字的排版规范（Typography for Numbers）

```css
.metric {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.price-large {
  font-size: 2rem;
  font-weight: 800;
}

.percentage {
  font-size: 0.875rem;
  font-weight: 500;
}
```