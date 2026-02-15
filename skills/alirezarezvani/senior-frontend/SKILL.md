---
name: senior-frontend
description: 前端开发技能，涵盖 React、Next.js、TypeScript 和 Tailwind CSS 应用程序。这些技能可用于构建 React 组件、优化 Next.js 的性能、分析代码包的大小、搭建前端项目框架、实现可访问性功能，以及审查前端代码的质量。
---

# 高级前端开发

针对 React/Next.js 应用程序的前端开发模式、性能优化以及自动化工具。

## 目录

- [项目搭建](#project-scaffolding)
- [组件生成](#component-generation)
- [打包分析](#bundle-analysis)
- [React 开发模式](#react-patterns)
- [Next.js 优化](#nextjs-optimization)
- [可访问性与测试](#accessibility-and-testing)

---

## 项目搭建

使用 TypeScript、Tailwind CSS 以及最佳实践配置来创建一个新的 Next.js 或 React 项目。

### 工作流程：创建新的前端项目

1. 使用项目名称和模板运行项目搭建工具：
   ```bash
   python scripts/frontend_scaffolder.py my-app --template nextjs
   ```

2. 添加可选功能（身份验证、API、表单、测试、Storybook）：
   ```bash
   python scripts/frontend_scaffolder.py dashboard --template nextjs --features auth,api
   ```

3. 进入项目并安装依赖项：
   ```bash
   cd my-app && npm install
   ```

4. 启动开发服务器：
   ```bash
   npm run dev
   ```

### 项目搭建选项

| 选项 | 描述 |
|--------|-------------|
| `--template nextjs` | 使用 Next.js 14+ 版本，包含 App Router 和服务器组件 |
| `--template react` | 使用 React 和 Vite，配合 TypeScript |
| `--features auth` | 添加 NextAuth.js 身份验证功能 |
| `--features api` | 添加 React Query 和 API 客户端 |
| `--features forms` | 添加 React Hook Form 和 Zod 验证功能 |
| `--features testing` | 添加 Vitest 和测试库 |
| `--dry-run` | 预览文件，不实际创建文件 |

### 生成的项目结构（Next.js）

```
my-app/
├── app/
│   ├── layout.tsx        # Root layout with fonts
│   ├── page.tsx          # Home page
│   ├── globals.css       # Tailwind + CSS variables
│   └── api/health/route.ts
├── components/
│   ├── ui/               # Button, Input, Card
│   └── layout/           # Header, Footer, Sidebar
├── hooks/                # useDebounce, useLocalStorage
├── lib/                  # utils (cn), constants
├── types/                # TypeScript interfaces
├── tailwind.config.ts
├── next.config.js
└── package.json
```

---

## 组件生成

使用 TypeScript 生成 React 组件，并自动生成测试用例和 Storybook 文档。

### 工作流程：创建新组件

1. 生成客户端组件：
   ```bash
   python scripts/component_generator.py Button --dir src/components/ui
   ```

2. 生成服务器端组件：
   ```bash
   python scripts/component_generator.py ProductCard --type server
   ```

3. 生成包含测试用例和 Storybook 文档的组件：
   ```bash
   python scripts/component_generator.py UserProfile --with-test --with-story
   ```

4. 生成自定义 React 钩子：
   ```bash
   python scripts/component_generator.py FormValidation --type hook
   ```

### 组件生成选项

| 选项 | 描述 |
|--------|-------------|
| `--type client` | 客户端组件（默认选项） |
| `--type server` | 异步服务器端组件 |
| `--type hook` | 自定义 React 钩子 |
| `--with-test` | 包含测试文件 |
| `--with-story` | 包含 Storybook 文档 |
| `--flat` | 将组件直接生成在输出目录中，不创建子目录 |
| `--dry-run` | 预览组件，不实际创建文件 |

### 生成的组件示例

```tsx
'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps {
  className?: string;
  children?: React.ReactNode;
}

export function Button({ className, children }: ButtonProps) {
  return (
    <div className={cn('', className)}>
      {children}
    </div>
  );
}
```

---

## 打包分析

分析 `package.json` 和项目结构，寻找打包优化的机会。

### 工作流程：优化打包大小

1. 在项目中运行打包分析工具：
   ```bash
   python scripts/bundle_analyzer.py /path/to/project
   ```

2. 查看分析结果和存在的问题：
   ```
   Bundle Health Score: 75/100 (C)

   HEAVY DEPENDENCIES:
     moment (290KB)
       Alternative: date-fns (12KB) or dayjs (2KB)

     lodash (71KB)
       Alternative: lodash-es with tree-shaking
   ```

3. 根据分析结果替换占用大量空间的依赖项。

4. 以详细模式重新运行工具，检查导入模式：
   ```bash
   python scripts/bundle_analyzer.py . --verbose
   ```

### 打包评分解读

| 评分 | 等级 | 处理建议 |
|-------|-------|--------|
| 90-100 | A | 打包效果非常好 |
| 80-89 | B | 需要一些小优化 |
| 70-79 | C | 需要替换占用大量空间的依赖项 |
| 60-69 | D | 存在多个问题需要解决 |
| 0-59 | F | 打包大小存在严重问题 |

### 常见的高占用空间依赖项

分析工具会识别以下常见的占用大量空间的依赖项：

| 依赖项 | 大小 | 替代方案 |
|---------|------|-------------|
| moment | 290KB | 可以使用 date-fns（12KB）或 dayjs（2KB） |
| lodash | 71KB | 可以使用 lodash-es 并结合 tree-shaking 技术进行优化 |
| axios | 14KB | 可以使用原生的 fetch 或 ky（3KB） |
| jquery | 87KB | 可以使用原生的 DOM API |
| @mui/material | 体积较大 | 可以使用 shadcn/ui 或 Radix UI 替代 |

---

## React 开发模式

参考文档：`references/react_patterns.md`

### 复合组件

在相关组件之间共享状态：

```tsx
const Tabs = ({ children }) => {
  const [active, setActive] = useState(0);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      {children}
    </TabsContext.Provider>
  );
};

Tabs.List = TabList;
Tabs.Panel = TabPanel;

// Usage
<Tabs>
  <Tabs.List>
    <Tabs.Tab>One</Tabs.Tab>
    <Tabs.Tab>Two</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel>Content 1</Tabs.Panel>
  <Tabs.Panel>Content 2</Tabs.Panel>
</Tabs>
```

### 自定义钩子

提取可重用的逻辑：

```tsx
function useDebounce<T>(value: T, delay = 500): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
const debouncedSearch = useDebounce(searchTerm, 300);
```

### 渲染属性

共享渲染逻辑：

```tsx
function DataFetcher({ url, render }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(url).then(r => r.json()).then(setData).finally(() => setLoading(false));
  }, [url]);

  return render({ data, loading });
}

// Usage
<DataFetcher
  url="/api/users"
  render={({ data, loading }) =>
    loading ? <Spinner /> : <UserList users={data} />
  }
/>
```

---

## Next.js 优化

参考文档：`references/nextjs_optimization_guide.md`

### 服务器组件与客户端组件的使用

默认情况下使用服务器组件。仅在以下情况下使用客户端组件：
- 事件处理（onClick、onChange）
- 状态管理（useState、useReducer）
- 效果（useEffect）
- 浏览器 API

```tsx
// Server Component (default) - no 'use client'
async function ProductPage({ params }) {
  const product = await getProduct(params.id);  // Server-side fetch

  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton productId={product.id} />  {/* Client component */}
    </div>
  );
}

// Client Component
'use client';
function AddToCartButton({ productId }) {
  const [adding, setAdding] = useState(false);
  return <button onClick={() => addToCart(productId)}>Add</button>;
}
```

### 图像优化

```tsx
import Image from 'next/image';

// Above the fold - load immediately
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
/>

// Responsive image with fill
<div className="relative aspect-video">
  <Image
    src="/product.jpg"
    alt="Product"
    fill
    sizes="(max-width: 768px) 100vw, 50vw"
    className="object-cover"
  />
</div>
```

### 数据获取策略

```tsx
// Parallel fetching
async function Dashboard() {
  const [user, stats] = await Promise.all([
    getUser(),
    getStats()
  ]);
  return <div>...</div>;
}

// Streaming with Suspense
async function ProductPage({ params }) {
  return (
    <div>
      <ProductDetails id={params.id} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />
      </Suspense>
    </div>
  );
}
```

---

## 可访问性与测试

参考文档：`references/frontend_best_practices.md`

### 可访问性检查清单

1. **语义化 HTML**：使用正确的元素（如 `<button>`、`<nav>`、`<main>`）
2. **键盘导航**：所有交互式元素都应可聚焦
3. **ARIA 标签**：为图标和复杂控件提供标签
4. **颜色对比度**：正常文本的对比度至少为 4.5:1
5. **焦点指示器**：确保焦点状态可见

```tsx
// Accessible button
<button
  type="button"
  aria-label="Close dialog"
  onClick={onClose}
  className="focus-visible:ring-2 focus-visible:ring-blue-500"
>
  <XIcon aria-hidden="true" />
</button>

// Skip link for keyboard users
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

### 测试策略

```tsx
// Component test with React Testing Library
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('button triggers action on click', async () => {
  const onClick = vi.fn();
  render(<Button onClick={onClick}>Click me</Button>);

  await userEvent.click(screen.getByRole('button'));
  expect(onClick).toHaveBeenCalledTimes(1);
});

// Test accessibility
test('dialog is accessible', async () => {
  render(<Dialog open={true} title="Confirm" />);

  expect(screen.getByRole('dialog')).toBeInTheDocument();
  expect(screen.getByRole('dialog')).toHaveAttribute('aria-labelledby');
});
```

---

## 快速参考

### 常见的 Next.js 配置选项

```js
// next.config.js
const nextConfig = {
  images: {
    remotePatterns: [{ hostname: 'cdn.example.com' }],
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    optimizePackageImports: ['lucide-react', '@heroicons/react'],
  },
};
```

### Tailwind CSS 实用工具

```tsx
// Conditional classes with cn()
import { cn } from '@/lib/utils';

<button className={cn(
  'px-4 py-2 rounded',
  variant === 'primary' && 'bg-blue-500 text-white',
  disabled && 'opacity-50 cursor-not-allowed'
)} />
```

### TypeScript 开发模式

```tsx
// Props with children
interface CardProps {
  className?: string;
  children: React.ReactNode;
}

// Generic component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}
```

---

## 资源

- React 开发模式参考：`references/react_patterns.md`
- Next.js 优化参考：`references/nextjs_optimization_guide.md`
- 最佳实践参考：`references/frontend_best_practices.md`