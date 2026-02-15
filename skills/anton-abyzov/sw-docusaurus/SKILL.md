---
name: docusaurus
description: Docusaurus 3.x 文档框架：支持 MDX 格式的编写、主题定制、版本管理以及国际化（i18n）功能。适用于构建文档网站或类似 spec-weave.com 的平台。
---

# Docusaurus 专家技能

我是 Docusaurus 3.x 文档框架的专家——这是一个用于技术文档、博客和登录页的现代静态站点生成器。

## 核心能力

### 1. 站点设置与配置
- **安装**：使用模板快速入门
- **配置**：`docusaurus.config.ts` 的最佳实践
- **插件**：内容管理、搜索功能、分析工具、站点地图
- **主题**：经典主题、Material 主题以及自定义主题
- **部署**：GitHub Pages、Netlify、Vercel、AWS

### 2. 内容创作
- **Markdown**：支持 Docusaurus 扩展的标准 Markdown
- **MDX**：在 Markdown 中使用 React 组件
- **代码块**：语法高亮显示、实时代码编辑器
- **警告提示**：用于显示注意事项、提示、警告和危险提示
- **标签页**：支持多语言示例及平台特定内容

### 3. 高级功能
- **版本管理**：多版本文档管理
- **国际化（i18n）**：支持多语言本地化
- **搜索**：使用 Algolia DocSearch 或本地搜索插件
- **Mermaid 图表**：通过 `@docusaurus/theme-mermaid` 支持 Mermaid 图表
- **OpenAPI**：使用 `docusaurus-plugin-openapi-docs` 生成 API 文档

### 4. 自定义
- **自定义组件**：为文档创建 React 组件
- **样式设置**：使用 CSS 模块和 Tailwind CSS
- **主题定制**：自定义主题组件
- **插件开发**：开发自定义插件

## 快速入门

### 安装

```bash
npx create-docusaurus@latest my-website classic --typescript
cd my-website
npm start
```

### 项目结构

```
my-website/
├── docs/                  # Documentation pages
│   ├── intro.md
│   └── tutorial/
├── blog/                  # Blog posts (optional)
│   └── 2024-01-01-post.md
├── src/
│   ├── components/       # Custom React components
│   ├── css/             # Custom styles
│   └── pages/           # Standalone pages
├── static/              # Static assets
│   └── img/
├── docusaurus.config.ts # Main configuration
├── sidebars.ts          # Sidebar configuration
└── package.json
```

## 配置

### 基本配置

```typescript
// docusaurus.config.ts
import {Config} from '@docusaurus/types';

const config: Config = {
  title: 'My Project',
  tagline: 'Documentation made easy',
  url: 'https://myproject.com',
  baseUrl: '/',

  // GitHub Pages deployment config
  organizationName: 'facebook',
  projectName: 'docusaurus',

  // Theme config
  themeConfig: {
    navbar: {
      title: 'My Project',
      logo: {
        alt: 'My Project Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Docs',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/facebook/docusaurus',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Tutorial',
              to: '/docs/intro',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} My Project`,
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/facebook/docusaurus/tree/main/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/facebook/docusaurus/tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],
};

export default config;
```

## MDX 内容特性

### 警告提示

```markdown
:::note
This is a note
:::

:::tip
This is a tip
:::

:::warning
This is a warning
:::

:::danger
This is a danger alert
:::

:::info Custom Title
This is an info box with a custom title
:::
```

### 带有功能的代码块

```markdown
\```typescript
title="src/components/HelloWorld.tsx"
showLineNumbers {1, 3-5}
import React from 'react';

export function HelloWorld() {
  return <h1>Hello World!</h1>;
}
\```
```

### 标签页

```markdown
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="js" label="JavaScript">
    \```js
    const greeting = 'Hello';
    \```
  </TabItem>
  <TabItem value="ts" label="TypeScript">
    \```ts
    const greeting: string = 'Hello';
    \```
  </TabItem>
</Tabs>
```

### 实时代码编辑器

```markdown
\```jsx
live
function Clock() {
  const [date, setDate] = useState(new Date());
  useEffect(() => {
    const timerID = setInterval(() => setDate(new Date()), 1000);
    return () => clearInterval(timerID);
  }, []);
  return <div>{date.toLocaleTimeString()}</div>;
}
\```
```

## 插件

### 必备插件

```typescript
// docusaurus.config.ts
plugins: [
  // Multiple docs instances
  [
    '@docusaurus/plugin-content-docs',
    {
      id: 'api',
      path: 'api',
      routeBasePath: 'api',
      sidebarPath: './sidebarsApi.ts',
    },
  ],

  // Sitemap
  [
    '@docusaurus/plugin-sitemap',
    {
      changefreq: 'weekly',
      priority: 0.5,
    },
  ],

  // Google Analytics
  [
    '@docusaurus/plugin-google-gtag',
    {
      trackingID: 'G-XXXXXXXXXX',
      anonymizeIP: true,
    },
  ],
],
```

### Mermaid 图表

```bash
npm install @docusaurus/theme-mermaid
```

### 其他插件

```typescript
// docusaurus.config.ts
themes: ['@docusaurus/theme-mermaid'],
markdown: {
  mermaid: true,
},
```

### 使用 Mermaid 图表

```markdown
\```mermaid
graph TD
  A[开始] -->|处理| B[结束]
\```
```

### 搜索

#### Algolia DocSearch

```typescript
themeConfig: {
  algolia: {
    appId: 'YOUR_APP_ID',
    apiKey: 'YOUR_SEARCH_API_KEY',
    indexName: 'YOUR_INDEX_NAME',
  },
},
```

#### 本地搜索

```bash
npm install @easyops-cn/docusaurus-search-local
```

#### 自定义搜索

```typescript
themes: [
  [
    require.resolve('@easyops-cn/docusaurus-search-local'),
    {
      hashed: true,
      language: ['en', 'zh'],
    },
  ],
],
```

## 版本管理

### 启用版本管理

```bash
npm run docusaurus docs:version 1.0.0
```

### 版本结构

```
website/
├── docs/               # Current version (Next)
├── versioned_docs/
│   ├── version-1.0.0/  # Version 1.0.0
│   └── version-2.0.0/  # Version 2.0.0
├── versioned_sidebars/
│   ├── version-1.0.0-sidebars.json
│   └── version-2.0.0-sidebars.json
└── versions.json       # List of versions
```

### 版本配置

```typescript
themeConfig: {
  navbar: {
    items: [
      {
        type: 'docsVersionDropdown',
        position: 'right',
      },
    ],
  },
},
```

## 国际化（i18n）

### 配置

```typescript
// docusaurus.config.ts
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'fr', 'es'],
  localeConfigs: {
    en: {
      label: 'English',
    },
    fr: {
      label: 'Français',
    },
    es: {
      label: 'Español',
    },
  },
},
```

### 目录结构

```
website/
├── i18n/
│   ├── en/
│   │   ├── docusaurus-plugin-content-docs/
│   │   └── docusaurus-theme-classic/
│   ├── fr/
│   └── es/
└── docs/              # Default locale content
```

### 为特定语言生成文档

```bash
npm run build -- --locale fr
```

## 自定义组件

### 创建自定义组件

```tsx
// src/components/FeatureCard.tsx
import React from 'react';
import styles from './styles.module.css';

export function FeatureCard({title, description, icon}) {
  return (
    <div className={styles.featureCard}>
      <div className={styles.icon}>{icon}</div>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}
```

### 在 MDX 中使用自定义组件

```markdown
---
title: Features
---

import {FeatureCard} from '@site/src/components/FeatureCard';

# Our Features

<FeatureCard
  title="Fast"
  description="Lightning-fast performance"
  icon="⚡"
/>
```

## 部署

### 使用 GitHub Pages

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Install dependencies
        run: npm ci
      - name: Build website
        run: npm run build
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

### 使用 Netlify

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 使用 Vercel

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build"
}
```

## 最佳实践

- **逻辑清晰地组织内容**
- **使用 Frontmatter（文档头部信息）**
- **充分利用 MDX 的功能**
- **优化图片质量**
- **添加编辑链接**

## 故障排除

- **构建错误处理**
- **修复失效的链接**
- **检查端口是否已被占用**

## 资源

- [官方文档](https://docusaurus.io/)
- [案例展示](https://docusaurus.io/showcase)
- [Discord 社区](https://discord.gg/docusaurus)
- [GitHub 仓库](https://github.com/facebook/docusaurus)

## 常见问题解答

- **如何设置 Docusaurus？**
- **Docusaurus 的配置最佳实践**
- **如何为 Docusaurus 添加搜索功能？**
- **如何对 Docusaurus 进行版本管理？**
- **如何在 Docusaurus 中使用 MDX 组件？**
- **如何将 Docusaurus 部署到 GitHub Pages？**
- **如何实现 Docusaurus 的国际化？**
- **如何自定义 Docusaurus 主题？**