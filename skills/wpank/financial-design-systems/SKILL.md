---
name: financial-data-visualization
model: standard
description: 用于构建深色主题财务图表和数据可视化的模式。涵盖了图表样式设计、盈亏颜色刻度的设置以及实时数据展示的功能。适用于构建交易仪表板或进行财务分析时使用。相关关键词包括：图表主题（chart theme）、数据可视化（data visualization）、财务图表（financial chart）、深色主题（dark theme）、盈亏情况（gains/losses）、交易用户界面（trading UI）。
---

# 金融数据可视化

构建深色主题的金融图表和可视化效果，使其既易于阅读，美观大方，又与现代交易用户界面保持一致。

---

## 使用场景

- 构建包含图表的交易仪表板
- 显示投资组合表现
- 展示价格历史和趋势
- 任何金融数据的可视化展示

---

## 模式 1：图表颜色调色板

```typescript
// lib/chart-theme.ts
export const chartColors = {
  // Gains/Losses
  positive: 'hsl(154 80% 60%)',    // Green
  negative: 'hsl(346 80% 62%)',    // Red
  neutral: 'hsl(216 90% 68%)',     // Blue
  
  // Backgrounds
  background: 'hsl(222 47% 11%)',
  surface: 'hsl(222 47% 15%)',
  grid: 'hsl(222 47% 20%)',
  
  // Text
  textPrimary: 'hsl(210 40% 98%)',
  textSecondary: 'hsl(215 20% 65%)',
  textMuted: 'hsl(215 20% 45%)',
  
  // Data series
  series: [
    'hsl(200 90% 65%)',  // Cyan
    'hsl(280 90% 65%)',  // Purple
    'hsl(45 90% 65%)',   // Gold
    'hsl(160 90% 65%)',  // Teal
    'hsl(320 90% 65%)',  // Pink
  ],
};
```

---

## 模式 2：Recharts 主题配置

```tsx
// components/charts/chart-config.ts
import { chartColors } from '@/lib/chart-theme';

export const chartConfig = {
  // Axis styling
  axisStyle: {
    stroke: chartColors.textMuted,
    fontSize: 11,
    fontFamily: 'var(--font-mono)',
  },
  
  // Grid styling
  gridStyle: {
    stroke: chartColors.grid,
    strokeDasharray: '3 3',
  },
  
  // Tooltip styling
  tooltipStyle: {
    backgroundColor: chartColors.surface,
    border: `1px solid ${chartColors.grid}`,
    borderRadius: '8px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
  },
};

// Custom tooltip component
export function ChartTooltip({ active, payload, label }: any) {
  if (!active || !payload) return null;

  return (
    <div
      className="rounded-lg border bg-popover px-3 py-2 shadow-lg"
      style={chartConfig.tooltipStyle}
    >
      <p className="text-xs text-muted-foreground mb-1">{label}</p>
      {payload.map((entry: any, index: number) => (
        <p
          key={index}
          className="text-sm font-mono tabular-nums"
          style={{ color: entry.color }}
        >
          {entry.name}: {formatCurrency(entry.value)}
        </p>
      ))}
    </div>
  );
}
```

---

## 模式 3：价格图表组件

```tsx
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface PriceChartProps {
  data: { time: string; price: number }[];
  isPositive?: boolean;
}

export function PriceChart({ data, isPositive = true }: PriceChartProps) {
  const color = isPositive ? chartColors.positive : chartColors.negative;
  
  return (
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity={0.3} />
            <stop offset="100%" stopColor={color} stopOpacity={0} />
          </linearGradient>
        </defs>
        
        <XAxis
          dataKey="time"
          axisLine={false}
          tickLine={false}
          tick={{ ...chartConfig.axisStyle }}
        />
        
        <YAxis
          domain={['auto', 'auto']}
          axisLine={false}
          tickLine={false}
          tick={{ ...chartConfig.axisStyle }}
          tickFormatter={(value) => formatCompact(value)}
        />
        
        <Tooltip content={<ChartTooltip />} />
        
        <Area
          type="monotone"
          dataKey="price"
          stroke={color}
          strokeWidth={2}
          fill="url(#priceGradient)"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
```

---

## 模式 4：蜡烛图颜色设置

```typescript
export const candlestickColors = {
  up: {
    fill: 'hsl(154 80% 60%)',
    stroke: 'hsl(154 80% 50%)',
  },
  down: {
    fill: 'hsl(346 80% 62%)',
    stroke: 'hsl(346 80% 52%)',
  },
  wick: 'hsl(215 20% 45%)',
};

// Usage with lightweight-charts or similar
const candlestickSeries = chart.addCandlestickSeries({
  upColor: candlestickColors.up.fill,
  downColor: candlestickColors.down.fill,
  borderUpColor: candlestickColors.up.stroke,
  borderDownColor: candlestickColors.down.stroke,
  wickUpColor: candlestickColors.wick,
  wickDownColor: candlestickColors.wick,
});
```

---

## 模式 5：百分比条形图

```tsx
interface PercentageBarProps {
  value: number;  // -100 to 100
  showLabel?: boolean;
}

export function PercentageBar({ value, showLabel = true }: PercentageBarProps) {
  const isPositive = value >= 0;
  const absValue = Math.min(Math.abs(value), 100);

  return (
    <div className="flex items-center gap-2">
      {/* Negative side */}
      <div className="flex-1 flex justify-end">
        {!isPositive && (
          <div
            className="h-2 rounded-l bg-destructive"
            style={{ width: `${absValue}%` }}
          />
        )}
      </div>
      
      {/* Center divider */}
      <div className="w-px h-4 bg-border" />
      
      {/* Positive side */}
      <div className="flex-1">
        {isPositive && (
          <div
            className="h-2 rounded-r bg-success"
            style={{ width: `${absValue}%` }}
          />
        )}
      </div>
      
      {showLabel && (
        <span
          className={cn(
            'text-xs font-mono tabular-nums w-12 text-right',
            isPositive ? 'text-success' : 'text-destructive'
          )}
        >
          {formatPercentage(value)}
        </span>
      )}
    </div>
  );
}
```

---

## 模式 6：迷你折线图

```tsx
interface SparklineProps {
  data: number[];
  width?: number;
  height?: number;
}

export function Sparkline({ data, width = 80, height = 24 }: SparklineProps) {
  const first = data[0];
  const last = data[data.length - 1];
  const isPositive = last >= first;
  const color = isPositive ? chartColors.positive : chartColors.negative;

  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;

  const points = data
    .map((value, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - ((value - min) / range) * height;
      return `${x},${y}`;
    })
    .join(' ');

  return (
    <svg width={width} height={height} className="overflow-visible">
      <polyline
        points={points}
        fill="none"
        stroke={color}
        strokeWidth={1.5}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
```

---

## 模式 7：图表图例

```tsx
interface LegendItem {
  label: string;
  color: string;
  value?: string;
}

export function ChartLegend({ items }: { items: LegendItem[] }) {
  return (
    <div className="flex flex-wrap gap-4">
      {items.map((item) => (
        <div key={item.label} className="flex items-center gap-2">
          <div
            className="size-3 rounded-full"
            style={{ backgroundColor: item.color }}
          />
          <span className="text-xs text-muted-foreground">{item.label}</span>
          {item.value && (
            <span className="text-xs font-mono">{item.value}</span>
          )}
        </div>
      ))}
    </div>
  );
}
```

---

## 相关技能

- **元技能：** [ai/skills/meta/design-system-creation/](../../meta/design-system-creation/) — 完整的设计系统工作流程
- [animated-financial-display](../animated-financial-display/) — 数字动画和数值闪烁效果
- [dual-stream-architecture](../../realtime/dual-stream-architecture/) — 实时数据流处理技术

---

## 绝对不要做

- **使用浅色主题** — 确保在深色背景上具有足够的对比度
- **在未考虑色盲用户的情况下使用红色/绿色** — 应添加形状或图案来辅助识别
- **省略网格线** — 网格线有助于读取数据值
- **使用过粗的线条** — 数据线的最佳粗细为 1-2 像素
- **对每个数据点都进行动画处理** — 将动画效果保留到初次加载时使用

---

## 快速参考

```tsx
// Color assignment
const color = value >= 0 ? chartColors.positive : chartColors.negative;

// Gradient definition
<linearGradient id="gradient" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stopColor={color} stopOpacity={0.3} />
  <stop offset="100%" stopColor={color} stopOpacity={0} />
</linearGradient>

// Axis styling
<XAxis tick={{ fill: chartColors.textMuted, fontSize: 11 }} />

// Tooltip styling
<Tooltip contentStyle={{ background: chartColors.surface }} />
```