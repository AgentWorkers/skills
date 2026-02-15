---
name: loading-state-patterns
model: fast
description: 这些模式涵盖了与设计系统美学相匹配的骨架加载器（skeleton loaders）、闪烁效果（shimmer effects）以及加载状态（loading states）的实现方式。包括骨架组件（skeleton components）、闪烁动画（shimmer animations）以及渐进式加载（progressive loading）的相关内容。适用于构建精致、用户体验良好的加载效果（loading experiences）。这些模式会在骨架组件加载完成时、加载状态发生变化时、出现闪烁效果时，或加载动画启动时被触发（triggered）。
---

# 加载状态设计

创建具有明确意图的加载状态，并使其与您的设计系统风格相匹配。

---

## 使用场景

- 为内容区域构建基础加载框架
- 需要为流式内容添加闪烁效果
- 希望实现渐进式加载体验
- 构建高级的加载用户体验

---

## 模式 1：基础骨架

```tsx
import { cn } from '@/lib/utils';

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  shimmer?: boolean;
}

export function Skeleton({ className, shimmer = true, ...props }: SkeletonProps) {
  return (
    <div
      className={cn(
        'rounded-md bg-muted',
        shimmer && 'animate-shimmer bg-gradient-to-r from-muted via-muted-foreground/10 to-muted bg-[length:200%_100%]',
        className
      )}
      {...props}
    />
  );
}
```

### CSS 动画

```css
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.animate-shimmer {
  animation: shimmer 1.5s ease-in-out infinite;
}
```

---

## 模式 2：内容骨架布局

### 卡片骨架

```tsx
export function CardSkeleton() {
  return (
    <div className="rounded-lg border bg-card p-4 space-y-3">
      <div className="flex items-center gap-3">
        <Skeleton className="size-10 rounded-full" />
        <div className="space-y-1.5 flex-1">
          <Skeleton className="h-4 w-1/3" />
          <Skeleton className="h-3 w-1/4" />
        </div>
      </div>
      <Skeleton className="h-20 w-full" />
      <div className="flex gap-2">
        <Skeleton className="h-8 w-20" />
        <Skeleton className="h-8 w-20" />
      </div>
    </div>
  );
}
```

### 表格行骨架

```tsx
export function TableRowSkeleton({ columns = 4 }: { columns?: number }) {
  return (
    <tr>
      {Array.from({ length: columns }).map((_, i) => (
        <td key={i} className="p-3">
          <Skeleton className="h-4 w-full" />
        </td>
      ))}
    </tr>
  );
}
```

### 指标骨架

```tsx
export function MetricSkeleton() {
  return (
    <div className="space-y-2">
      <Skeleton className="h-3 w-16" />
      <Skeleton className="h-8 w-24" />
    </div>
  );
}
```

---

## 模式 3：设计系统骨架

将骨架设计与您的整体风格相协调：

```tsx
// For retro-futuristic theme
export function CyberSkeleton({ className, ...props }: SkeletonProps) {
  return (
    <div
      className={cn(
        'rounded-md bg-tone-cadet/30',
        'animate-pulse-glow',
        'border border-tone-cyan/10',
        className
      )}
      {...props}
    />
  );
}

// CSS
@keyframes pulse-glow {
  0%, 100% { opacity: 0.4; box-shadow: 0 0 0 0 rgba(var(--tone-cyan), 0); }
  50% { opacity: 0.6; box-shadow: 0 0 8px 0 rgba(var(--tone-cyan), 0.1); }
}
```

---

## 模式 4：渐进式加载

在内容加载过程中逐步显示内容：

```tsx
interface ProgressiveLoadProps {
  isLoading: boolean;
  skeleton: React.ReactNode;
  children: React.ReactNode;
}

export function ProgressiveLoad({
  isLoading,
  skeleton,
  children,
}: ProgressiveLoadProps) {
  return (
    <div className="relative">
      {isLoading ? (
        skeleton
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2 }}
        >
          {children}
        </motion.div>
      )}
    </div>
  );
}
```

---

## 模式 5：流式内容指示器

适用于 AI/LLM 流式内容：

```tsx
export function StreamingIndicator() {
  return (
    <div className="flex items-center gap-1">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          className="size-1.5 rounded-full bg-primary"
          animate={{ scale: [1, 1.3, 1], opacity: [0.5, 1, 0.5] }}
          transition={{
            duration: 0.8,
            repeat: Infinity,
            delay: i * 0.15,
          }}
        />
      ))}
    </div>
  );
}
```

---

## 模式 6：加载进度条

显示加载进度：

```tsx
interface LoadingProgressProps {
  progress?: number; // 0-100, undefined = indeterminate
}

export function LoadingProgress({ progress }: LoadingProgressProps) {
  const isIndeterminate = progress === undefined;

  return (
    <div className="h-1 w-full bg-muted overflow-hidden rounded-full">
      <div
        className={cn(
          'h-full bg-primary transition-all duration-300',
          isIndeterminate && 'animate-indeterminate'
        )}
        style={!isIndeterminate ? { width: `${progress}%` } : undefined}
      />
    </div>
  );
}

// CSS
@keyframes indeterminate {
  0% { transform: translateX(-100%); width: 50%; }
  100% { transform: translateX(200%); width: 50%; }
}

.animate-indeterminate {
  animation: indeterminate 1.5s ease-in-out infinite;
}
```

---

## 模式 7：骨架网格

```tsx
export function GridSkeleton({ 
  count = 6, 
  columns = 3 
}: { 
  count?: number; 
  columns?: number;
}) {
  return (
    <div 
      className="grid gap-4" 
      style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}
    >
      {Array.from({ length: count }).map((_, i) => (
        <CardSkeleton key={i} />
      ))}
    </div>
  );
}
```

---

## 相关技能

- **元技能：** [ai/skills/meta/design-system-creation/](../../meta/design-system-creation/) — 完整的设计系统工作流程
- [distinctive-design-systems/(../distinctive-design-systems/) — 为不同主题的设计框架提供美学匹配方案

---

## 绝对不要做

- **在深色主题中使用灰色骨架** — 应与页面背景颜色保持一致
- **省略闪烁动画** — 静态的骨架会显得不协调
- **使骨架大小完全相同** — 适当的尺寸差异是自然的
- **忽略宽高比** — 图像需要遵循统一的骨架比例
- **永久显示骨架** — 为错误情况添加超时处理机制

---

## 快速参考

```tsx
// Basic skeleton
<Skeleton className="h-4 w-full" />

// Avatar skeleton
<Skeleton className="size-10 rounded-full" />

// Text lines
<div className="space-y-2">
  <Skeleton className="h-4 w-3/4" />
  <Skeleton className="h-4 w-1/2" />
</div>

// Card skeleton
<div className="p-4 space-y-3">
  <Skeleton className="h-6 w-1/3" />
  <Skeleton className="h-20 w-full" />
</div>
```