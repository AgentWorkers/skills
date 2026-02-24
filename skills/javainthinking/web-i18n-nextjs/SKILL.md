---
name: i18n-nextjs
description: Next.js / Node.js Web应用程序的国际化（i18n）指南，使用App Router实现。涵盖了翻译文件的结构、根据地区设置路由、针对不同地区的SEO元数据、`hreflang`属性、结构化的JSON-LD数据、用户界面组件的翻译以及多语言站点地图的生成。适用于以下场景：需要为项目添加国际化支持、新增语言、翻译页面或组件、为多个地区生成SEO元数据、实现`hreflang`功能、更新新地区的站点地图，或遵循Next.js项目中的国际化最佳实践。
---
# Next.js 的国际化（i18n）实现指南

## 核心原则

- 所有面向用户的功能 **必须** 支持国际化（i18n）—— 组件中不得使用硬编码的字符串。
- 翻译内容必须 **自然且符合语言习惯**—— 绝不要使用脚本或机器翻译；将翻译质量视为与英文文案写作同等重要。
- SEO 元数据、JSON-LD 结构化数据以及站点地图（sitemap）都必须支持多语言。
- 默认语言（英语）使用 **无前缀的 URL**（例如 `/products`）；其他语言则使用带有前缀的 URL（例如 `/es/products`）。

## 支持的语言

语言列表存储在 `src/lib/i18n/locales.ts` 文件中。请确保站点地图脚本中的 `locales` 数组与该文件保持同步。

```typescript
export const locales = ['en', 'es', 'fr', 'de', 'ja', 'zh-CN', /* ... add as needed */]
export const defaultLocale = 'en'
export type Locale = typeof locales[number]
```

## 目录结构

```
src/app/[lang]/
├── dictionaries/       ← One JSON file per locale
│   ├── en.json
│   ├── es.json
│   └── ...
├── dictionaries.ts     ← getDictionary(locale) server helper
├── layout.tsx          ← Root layout: generateMetadata + hreflang + JSON-LD
└── <page>/
    └── page.tsx        ← generateMetadata + page content
```

## 翻译文件

请参阅 **[references/translation-files.md](references/translation-files.md)**，了解以下内容：
- JSON 键的命名规则（`page.section.key`）
- 服务器端 `getDictionary()` 的使用方法
- 客户端 `useDictionary()` 钩子的使用方法
- 模板变量替换模式（例如 `{count}`）
- 键缺失时的回退处理方式

## 路由与中间件

请参阅 **[references/routing.md](references/routing.md)**，了解以下内容：
- `src/middleware.ts`：用于检测用户语言，并将 `/en/*` 路由重定向到 `//*`；为默认语言重写路由规则。
- `LocalizedLink` 组件：为非默认语言自动添加路径前缀。
- `useLocale()` 钩子：从 URL 参数、路径名或本地存储（localStorage）中读取当前语言设置。
- `getLocalizedPath()` 和 `removeLocalePrefix()` 工具方法。

## SEO 元数据

请参阅 **[references/seo-metadata.md](references/seo-metadata.md)**，了解以下内容：
- 在布局/页面文件中使用的 `generateMetadata()` 方法。
- 从 `src/lib/i18n/seo.ts` 中生成的 `generateAlternatesMetadata()` 方法。
- 全部语言的 `hreflang` 属性（包括默认语言 `x-default`）。
- OpenGraph 标签中的 `locale` 和 `alternateLocale` 字段。
- `html lang` 属性以及 `LangSetter` 客户端组件。

## 结构化 JSON-LD 数据

请参阅 **[references/structured-data.md](references/structured-data.md)**，了解以下内容：
- 包含翻译后的 `featureList` 和 `description` 的 WebApplication 数据结构。
- 包含 `inLanguage` 字段的 BlogPosting 数据结构。
- 包含翻译后的 `acceptedAnswer` 的 FAQ 数据结构。
- 包含本地化 URL 的 BreadcrumbList 数据结构。
- 通过 `<Script>` 或 `<script>` 标签渲染数据。

## 多语言站点地图

请参阅 **[references/sitemap.md](references/sitemap.md)**，了解以下内容：
- 站点地图的结构：每个页面对应一个 `<url>` 条目，并为每种语言提供 `<xhtml:link>` 替代链接。
- `<loc>` 标签使用默认语言的 URL；`x-default` 也指向该 URL。
- 包含静态和动态页面的完整 XML 示例。
- Next.js 应用程序的 `sitemap.ts` 实现方式。
- 需要包含或排除的页面内容（例如排除管理后台/API 路由）。
- Hreflang 语言代码的格式规则。

## 快速检查清单 —— 为新功能添加国际化支持

1. **为所有语言的 JSON 文件**（位于 `src/app/[lang]/dictionaries/`）添加翻译键：
   - 先添加英语翻译，然后依次为其他语言添加翻译。
2. **服务器端组件**：使用 `const dict = await getDictionary(locale)`，并在找不到翻译时返回 `dict?.page?.section?.key || 'fallback'`。
3. **客户端组件**：使用 `const dict = useDictionary()`，并采用相同的回退处理方式。
4. 在页面文件中添加 `generateMetadata()` 方法，并调用 `generateAlternatesMetadata()`。
5. 添加包含翻译字段和 `inLanguage` 属性的 JSON-LD 结构化数据标签。
6. 如果页面是新添加的，请更新站点地图：将其添加到站点地图源文件中（参见 [references/sitemap.md]）。
7. 对于内部链接使用 `<LocalizedLink>` 组件，对程序化导航使用 `getLocalizedPath()` 方法。

## 快速检查清单 —— 添加新语言支持

1. 在 `src/lib/i18n/locales.ts` 的 `locales` 数组中添加新的语言代码。
2. 以 `<code>.json` 格式将新语言的翻译内容添加到 `dictionaries/` 文件中（例如 `en.json`）。
3. 在 `src/app/[lang]/dictionaries.ts` 的导入映射中添加新语言的条目。
4. 在 `LanguageSwitcher` 组件的 `languageNames` 映射中添加新语言的显示名称。
5. 确保站点地图中的语言列表与应用程序的 `locales` 数组保持同步。
6. 重新生成并部署站点地图。