---
name: astro
description: Deploy multilingual static websites for free on Cloudflare using Astro framework with markdown source files. Use when: (1) Creating new static sites or blogs, (2) Setting up multilingual (i18n) content, (3) Deploying to Cloudflare Pages, (4) Converting markdown to static websites, (5) Setting up free hosting infrastructure.
---

# Astro 静态网站生成器

使用 Astro 框架，您可以免费在 Cloudflare 上部署多语言静态网站。

## 先决条件

- 已安装 Node.js 20 及更高版本
- 拥有 Cloudflare 账户（免费）
- 拥有 Git 仓库（GitHub、GitLab 或 Bitbucket）

## 快速入门

### 1. 创建项目

```bash
npm create astro@latest my-site -- --template minimal
cd my-site
npm install
```

### 2. 配置 Cloudflare

**静态网站（推荐用于大多数场景）**

无需使用适配器。使用默认的静态输出格式：

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://your-site.pages.dev',
});
```

**SSR/Edge 函数（可选）**

如果您需要服务器端渲染或 Edge 函数，请按照以下步骤配置：

```bash
npm install @astrojs/cloudflare
```

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'server',
  adapter: cloudflare(),
  site: 'https://your-site.pages.dev',
});
```

### 3. 部署到 Cloudflare

**推荐使用 Git 集成**

1. 将代码推送到 GitHub/GitLab
2. 登录 Cloudflare 控制台 → 进入 “Pages” → 创建项目 → 连接 Git 仓库
3. 配置以下参数：
   - 构建命令：`npm run build`
   - 构建输出目录：`dist`

**直接上传文件**

```bash
# Deploy (authenticate via Cloudflare dashboard or wrangler)
npx wrangler pages deploy dist
```

## 多语言配置

### Astro 配置

```javascript
// astro.config.mjs
export default defineConfig({
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'fr', 'de'],
    routing: {
      prefixDefaultLocale: false,  // /about instead of /en/about
    },
  },
});
```

**路由模式：**

| 设置 | URL 结构 | 适用场景 |
|---------|--------------|----------|
| `prefixDefaultLocale: false` | `/about`, `/es/about` | 根目录显示默认语言的内容 |
| `prefixDefaultLocale: true` | `/en/about`, `/es/about` | 所有语言的内容都加上语言前缀 |

### 内容结构

```
src/content/
├── config.ts          # Content collection schema
└── docs/
    ├── en/
    │   ├── index.md
    │   └── guide.md
    ├── es/
    │   ├── index.md
    │   └── guide.md
    └── fr/
        ├── index.md
        └── guide.md
```

### 内容集合架构

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const docs = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    lang: z.enum(['en', 'es', 'fr', 'de']),
  }),
});

export const collections = { docs };
```

**注意：** 在添加内容集合后，请运行 `npx astro sync` 以生成相应的类型文件。

### 语言切换组件

```astro
---
// src/components/LanguageSwitcher.astro
const languages = {
  en: 'English',
  es: 'Español',
  fr: 'Français',
  de: 'Deutsch',
};

const currentPath = Astro.url.pathname;
const currentLang = Astro.currentLocale || 'en';
---

<select onchange="window.location = this.value">
  {Object.entries(languages).map(([code, name]) => (
    <option 
      value={`/${code}${currentPath}`} 
      selected={code === currentLang}
    >
      {name}
    </option>
  ))}
</select>
```

## 文件结构

```
my-site/
├── astro.config.mjs      # Astro configuration
├── package.json
├── public/
│   ├── favicon.svg
│   └── _redirects        # Cloudflare redirects (optional)
├── src/
│   ├── components/
│   │   └── LanguageSwitcher.astro
│   ├── content/
│   │   ├── config.ts
│   │   └── blog/
│   │       ├── en/
│   │       └── es/
│   ├── layouts/
│   │   └── BaseLayout.astro
│   └── pages/
│       ├── index.astro
│       ├── en/
│       │   └── index.astro
│       └── es/
│           └── index.astro
```

## Cloudflare Pages 配置

| 设置 | 值 |
|---------|-------|
| 构建命令 | `npm run build` |
| 构建输出目录 | `dist` |
| Node.js 版本 | `20` |
| 环境变量 | `NODE_VERSION=20` |

### 自定义域名

登录 Cloudflare 控制台 → 进入 “Pages” → 选择您的网站 → 添加自定义域名

### 重定向规则

在 `public/_redirects` 文件中配置重定向规则：

```
/  /en/  302
/old-page  /new-page  301
```

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `npm run dev` | 启动开发服务器 |
| `npm run build` | 生成生产环境的代码 |
| `npm run preview` | 预览生产环境的代码 |
| `npx astro sync` | 生成内容集合的类型文件 |
| `npx wrangler login` | 用 Cloudflare 身份认证 |
| `npx wrangler pages deploy dist` | 将代码部署到 Cloudflare |

## 带有内容集合的博客

```astro
---
// src/pages/blog/[...slug].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<article>
  <h1>{post.data.title}</h1>
  <Content />
</article>
```

## 故障排除

### 在 Cloudflare 上构建失败

请在 Cloudflare Pages 的环境变量中设置 `NODE_VERSION=20`。

### 嵌套路由出现 404 错误

```javascript
// astro.config.mjs
export default defineConfig({
  trailingSlash: 'always',
});
```

### i18n 功能无法使用

请确保：
1. 语言文件名与文件夹名完全匹配
2. 内容文件包含正确的 `lang` 前缀
3. 在创建内容集合后运行 `npx astro sync` 以生成类型文件

### 内容集合类型错误

运行 `npx astro sync` 以生成 TypeScript 类型文件。

## 资源

- [Astro 文档](https://docs.astro.build)
- [Cloudflare Pages 文档](https://developers.cloudflare.com/pages)
- [Astro i18n 使用指南](https://docs.astro.build/en/guides/i18n/)
- [Cloudflare 适配器文档](https://docs.astro.build/en/guides/deploy/cloudflare/)

## 脚本

| 脚本 | 描述 |
|--------|-------------|
| `astro-new-post.py` | 创建多语言博客文章 |
| `astro-i18n-check.py` | 验证翻译覆盖率 |

### 脚本使用方法

```bash
# Create a new post in multiple languages
python scripts/astro-new-post.py --title "My Post" --langs en,es,fr

# Create with author and tags
python scripts/astro-new-post.py --title "Tutorial" --langs en,es --author "John" --tags tutorial,astro

# Check translation coverage
python scripts/astro-i18n-check.py --langs en,es,fr

# Check specific content directory
python scripts/astro-i18n-check.py --content-dir src/content/blog --langs en,es

# Output as JSON
python scripts/astro-i18n-check.py --langs en,es,fr --json
```

所有脚本仅使用 Python 标准库（无额外依赖）。