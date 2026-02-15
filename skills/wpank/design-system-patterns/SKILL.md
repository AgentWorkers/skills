---
name: design-system-patterns
model: standard
description: 基础设计系统架构包括：令牌层次结构（token hierarchies）、主题管理基础设施（theming infrastructure）、令牌处理流程（token pipelines）以及系统治理机制（governance）。该架构适用于创建设计相关令牌（design tokens）、实现主题切换（theme switching）、配置样式字典（Style Dictionary），以及建立多品牌主题管理系统（multi-brand theming）。相关功能会触发设计令牌（design tokens）、主题提供者（theme provider）、样式字典（Style Dictionary）、令牌处理流程（token pipelines）以及多品牌主题管理机制（multi-brand theming）的运行。此外，该架构还涉及CSS自定义属性（CSS custom properties）的相关设计。
---

# 设计系统模式

可扩展设计系统的基础架构：令牌层次结构、主题基础设施、令牌管道以及治理模式。

---

## 适用场景

- 定义令牌架构（从基本类型到语义类型再到组件类型）
- 使用 React 实现浅色/深色/系统主题切换
- 设置样式字典或 Figma 到代码的令牌管道
- 构建多品牌主题系统
- 建立令牌命名规范和治理机制
- 防止服务器端渲染（SSR）时出现无样式内容（FOUC，Flash of Unstyled Content）

---

## 模式 1：令牌层次结构

三层令牌架构将原始值、语义信息和使用方式分开。

```css
/* Layer 1: Primitive tokens — raw values, never used directly in components */
:root {
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-gray-50: #fafafa;
  --color-gray-900: #171717;

  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;

  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
}

/* Layer 2: Semantic tokens — contextual meaning, theme-aware */
:root {
  --text-primary: var(--color-gray-900);
  --text-secondary: var(--color-gray-600);
  --surface-default: white;
  --surface-elevated: var(--color-gray-50);
  --border-default: var(--color-gray-200);
  --interactive-primary: var(--color-blue-500);
  --interactive-primary-hover: var(--color-blue-600);
}

/* Layer 3: Component tokens — specific usage, optional */
:root {
  --button-bg: var(--interactive-primary);
  --button-bg-hover: var(--interactive-primary-hover);
  --button-text: white;
  --button-radius: var(--radius-md);
  --button-padding-x: var(--space-4);
  --button-padding-y: var(--space-2);
}
```

> 语义令牌是最重要的层次——它们决定了主题样式。组件令牌是可选的，对于复杂的组件库非常有用。

---

## 模式 2：使用 React 进行主题切换

关键功能：`theme`（用户选择）、`resolvedTheme`（实际应用的浅色/深色主题）、`setTheme`、系统偏好检测、使用 `localStorage` 保存设置、以及应用 DOM 属性。

```tsx
type Theme = "light" | "dark" | "system";

export function ThemeProvider({ children, defaultTheme = "system", storageKey = "theme",
  attribute = "data-theme" }: { children: React.ReactNode; defaultTheme?: Theme;
  storageKey?: string; attribute?: "class" | "data-theme" }) {
  const [theme, setThemeState] = useState<Theme>(() =>
    typeof window === "undefined" ? defaultTheme
      : (localStorage.getItem(storageKey) as Theme) || defaultTheme);
  const [resolvedTheme, setResolvedTheme] = useState<"light" | "dark">("light");

  const getSystem = useCallback(() =>
    matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light" as const, []);

  const apply = useCallback((r: "light" | "dark") => {
    const root = document.documentElement;
    attribute === "class"
      ? (root.classList.remove("light", "dark"), root.classList.add(r))
      : root.setAttribute(attribute, r);
    root.style.colorScheme = r;
    setResolvedTheme(r);
  }, [attribute]);

  useEffect(() => { apply(theme === "system" ? getSystem() : theme); }, [theme, apply, getSystem]);

  useEffect(() => {  // Listen for system preference changes
    if (theme !== "system") return;
    const mq = matchMedia("(prefers-color-scheme: dark)");
    const handler = () => apply(getSystem());
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, [theme, apply, getSystem]);

  const setTheme = useCallback((t: Theme) => {
    localStorage.setItem(storageKey, t); setThemeState(t);
  }, [storageKey]);

  return <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme }}>
    {children}
  </ThemeContext.Provider>;
}
```

完整的实现方式包括 `toggleTheme`、`disableTransitionOnChange`，以及相关测试，请参阅 [references/theming-architecture.md](references/theming-architecture.md)。

### 在 SSR 中防止 FOUC（Next.js）

`<head>` 标签中的内联脚本会在页面绘制之前执行：

```tsx
const themeScript = `(function(){
  var t=localStorage.getItem('theme')||'system';
  var d=t==='dark'||(t==='system'&&matchMedia('(prefers-color-scheme:dark)').matches);
  document.documentElement.setAttribute('data-theme',d?'dark':'light');
  document.documentElement.style.colorScheme=d?'dark':'light';
})()`;

// In layout.tsx
<html lang="en" suppressHydrationWarning>
  <head>
    <script dangerouslySetInnerHTML={{ __html: themeScript }} />
  </head>
  <body><ThemeProvider>{children}</ThemeProvider></body>
</html>
```

---

## 模式 3：多品牌主题

在语义令牌的基础上添加品牌特定的令牌，以实现白标签产品的定制化主题效果：

```css
[data-brand="corporate"] {
  --brand-primary: #0066cc;
  --brand-primary-hover: #0052a3;
  --brand-font-heading: "Helvetica Neue", sans-serif;
  --brand-radius: 0.25rem;
}

[data-brand="startup"] {
  --brand-primary: #7c3aed;
  --brand-primary-hover: #6d28d9;
  --brand-font-heading: "Poppins", sans-serif;
  --brand-radius: 1rem;
}

/* Map brand tokens into semantic tokens */
:root {
  --interactive-primary: var(--brand-primary);
  --interactive-primary-hover: var(--brand-primary-hover);
}
```

---

## 模式 4：样式字典管道

从单一 JSON 源文件生成适用于多个平台的令牌：

```javascript
// style-dictionary.config.js — generates CSS, iOS Swift, and Android XML
module.exports = {
  source: ["tokens/**/*.json"],
  platforms: {
    css: {
      transformGroup: "css", buildPath: "dist/css/",
      files: [{ destination: "variables.css", format: "css/variables",
        options: { outputReferences: true } }],
    },
    ios: {
      transformGroup: "ios-swift", buildPath: "dist/ios/",
      files: [{ destination: "DesignTokens.swift", format: "ios-swift/class.swift",
        className: "DesignTokens" }],
    },
    android: {
      transformGroup: "android", buildPath: "dist/android/",
      files: [{ destination: "colors.xml", format: "android/colors",
        filter: { attributes: { category: "color" } } }],
    },
  },
};
```

有关令牌类别定义、自定义转换规则以及平台特定输出示例，请参阅 [references/design-tokens.md](references/design-tokens.md)。

---

## 模式 5：可访问性令牌

```css
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0ms;
    --duration-normal: 0ms;
    --duration-slow: 0ms;
  }
}

@media (prefers-contrast: high) {
  :root {
    --text-primary: #000000;
    --surface-default: #ffffff;
    --border-default: #000000;
    --interactive-primary: #0000ee;
  }
}

@media (forced-colors: active) {
  .button { border: 2px solid currentColor; }
  .card { border: 1px solid CanvasText; }
}
```

---

## 令牌命名规范

命名格式：`[类别]-[属性]-[变体]-[状态]`（例如 `color-border-input-focus`）

1. **使用驼峰式命名法**（如 `text-primary` 而非 `textPrimary`）
2. **使用语义化的名称**（如 `danger` 而非 `red`）
3. **使用状态后缀**（如 `-hover`、`-focus`、`-active`、`-disabled`）
4. **用于表示尺寸变化的后缀**（如 `spacing-4`、`font-size-lg`）

---

## 令牌治理流程

变更管理流程：**提案** → **审查**（设计团队和开发团队共同参与）→ **测试**（所有平台和主题）→ **逐步淘汰**（并提供迁移路径）→ **最终移除**（在淘汰期限结束后）。

```json
{
  "color.primary": {
    "value": "{color.primitive.blue.500}",
    "deprecated": true,
    "deprecatedMessage": "Use semantic.accent.default instead",
    "replacedBy": "semantic.accent.default"
  }
}
```

---

## 最佳实践

1. **根据功能来命名令牌**——使用语义化的名称，而非视觉描述
2. **保持层次结构**——从基本类型到语义类型再到组件类型
3. **为令牌版本进行版本控制**——将令牌的变更视为 API 变更，并使用 semver 版本号进行管理
4. **测试所有主题组合**——确保每个主题都能与所有组件正常配合使用
5. **自动化流程**——利用 CI/CD 工具实现 Figma 到代码的同步
6. **提供迁移路径**——逐步淘汰旧令牌，并提供明确的替代方案
7. **验证对比度**——自动检查令牌对是否符合 WCAG AA/AAA 标准

---

## 常见问题

- **令牌过多且缺乏层次结构**——令牌数量过多且没有清晰的分类
- **命名不一致**——混合使用驼峰式和蛇形命名法
- **使用硬编码值**——直接使用十六进制或 REM 单位而非令牌引用
- **循环引用**——令牌之间相互引用
- **平台差异**——某些令牌仅适用于 Web 平台，而移动平台缺少相应的令牌
- **缺少深色模式**——某些语义令牌无法根据主题进行切换

---

## 相关技能

- [design-system-components](../design-system-components/)——CVA 变体模式和基础组件
- [distinctive-design-systems](../distinctive-design-systems/)——美学设计和视觉识别系统
- [theme-factory](../theme-factory/)——预构建的主题调色板

---

## 参考资料

- [references/design-tokens.md](references/design-tokens.md)——完整的令牌类别定义
- [references/theming-architecture.md](references/theming-architecture.md)——详细的主题实现方式
- [references/component-architecture.md](references/component-architecture.md)——复合组件、多态组件和无头组件相关的设计模式