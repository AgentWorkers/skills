---
name: shopify-theme-pro
description: >
  **Shopify Theme Development Pro**  
  专为 OpenClaw 代理提供全面的主题开发、部署及设计系统管理功能。适用于构建 Shopify 主题、编写 Liquid 模板、推送主题变更、将主题部署到商店以及管理设计系统等场景。该工具与以下功能相关：Shopify 主题、Liquid 模板编写、主题开发、主题部署、主题推送、Shopify 设计系统以及 Online Store 2.0。
---
# Shopify主题开发专业版

提供端到端的Shopify主题开发、部署以及设计系统管理服务。涵盖Liquid模板语言、Online Store 2.0架构、性能优化、部署流程以及CSS设计系统等内容。

## 使用场景

以下情况适合使用本技能：
- 创建新的Shopify主题或主题模块
- 编写或重构Liquid模板
- 实现主题定制功能
- 将主题更改部署到开发环境或实际店铺
- 优化主题性能（速度、可访问性、SEO）
- 为Shopify创建或维护CSS设计系统
- 审查主题代码的质量和标准
- 将主题迁移到Online Store 2.0
- 使用Shopify CLI进行开发操作（如推送、拉取等）

## 快速入门

### 本地开发

使用以下命令启动本地开发服务器，并实现热重载功能：
```bash
shopify theme dev --store=your-store.myshopify.com
```

访问`http://localhost:9292`即可实时预览代码更改。

### 部署到店铺

将本地更改推送到店铺：
```bash
shopify theme push --theme <THEME_ID>
```

详细部署流程请参考`references/deployment.md`。

### 创建新模块

生成模块的模板框架：
```bash
mkdir -p sections
touch sections/my-section.liquid
```

常见模块模板和结构请参考`references/liquid-patterns.md`。

## 核心概念

### 主题架构

**目录结构：**
```
theme/
├── assets/          # CSS, JavaScript, images
├── config/          # Theme settings (settings_schema.json, settings_data.json)
├── layout/          # Template wrappers (theme.liquid required)
├── sections/        # Reusable, customizable content modules
├── snippets/        # Reusable code fragments
├── templates/       # Page-type templates (JSON or Liquid)
└── locales/         # Translation files (en.default.json, etc.)
```

**关键原则：**
- **模块（Sections）**是商家可自定义的组件（可包含多个子模块）
- **代码片段（Snippets）**是可复用的代码片段（不可直接修改）
- **模板（Templates）**用于包裹模块并定义页面布局
- **布局（Layouts）**包含重复使用的元素（如页头、页脚、脚本）
- **Online Store 2.0**推荐使用JSON模板来包裹模块

### Online Store 2.0架构

**推荐做法：**
- 使用JSON模板（支持在任意页面中使用模块）
- 设计时考虑与应用程序插件的集成
- 通过设置文件允许商家进行自定义
- 允许重新排序或切换模块的显示状态

**不建议的做法：**
- 将模块绑定到特定模板
- 硬编码应该可编辑的内容
- 对新主题继续使用仅支持Liquid语言的旧模板

**JSON模板示例：**
```json
{
  "sections": {
    "header": {
      "type": "header"
    },
    "main": {
      "type": "main-product"
    }
  },
  "order": ["header", "main"]
}
```

### Liquid模板基础

**基本语法：**
```liquid
{%- # Output variables -%}
{{ product.title }}
{{ product.price | money }}

{%- # Control flow -%}
{% if product.available %}
  <button type="submit">Add to Cart</button>
{% else %}
  <span class="sold-out">Sold Out</span>
{% endif %}

{%- # Loops -%}
{% for variant in product.variants limit: 10 %}
  {{ variant.title }}: {{ variant.price | money }}
{% endfor %}

{%- # Filter chaining (processes left to right) -%}
{{ product.description | strip_html | truncate: 150 | upcase }}
```

**性能优化技巧：**
- 使用`{%- -%}`去除空白字符以减少HTML文件大小
- 高效地链接多个过滤器
- 尽量限制循环的使用（例如：`{% for item in array limit: 10 % }`）
- 使用`liquid`标签实现嵌套逻辑

更多高级模板用法请参考`references/liquid-patterns.md`。

## 开发流程

### 1. 设置

从模板开始创建新主题：
```bash
shopify theme init
```

或克隆现有主题：
```bash
shopify theme pull --theme <THEME_ID>
```

### 2. 本地开发

运行开发服务器：
```bash
shopify theme dev --store=your-store.myshopify.com
```

代码更改会自动同步到开发主题中，浏览器会自动刷新。

### 3. 代码质量检查

运行主题检查工具（Theme Check）：
```bash
shopify theme check
```

在部署前修复所有错误或警告。

### 4. 部署

完整部署流程请参考`references/deployment.md`：
- 部署前检查（目标主题、认证信息、Git状态）
- 扫描代码中的问题（如未完成的代码、待办事项、本地URL等）
- 将更改推送到店铺
- 部署后的验证

**重要提示：** 未经`--allow-live`标志和明确确认，切勿将更改推送到实际店铺。

### 5. 发布

将主题发布到实际店铺：
```bash
shopify theme publish --theme <THEME_ID>
```

## 性能优化

详细优化策略请参考`references/performance.md`：
- 减少JavaScript的使用（优先使用浏览器的原生功能）
- 拖动加载图片（`loading="lazy"`）
- 延迟加载非关键CSS
- 使用响应式图片（`srcset`）
- 压缩资源（优化CSS/JS、压缩图片）
- 实现资源预加载（`preload`、`dns-prefetch`）
- 在真实移动设备和慢速网络环境下进行测试

**避免的做法：**
- 在`<head>`标签中放置同步执行的脚本
- 对简单交互使用复杂的JavaScript库
- 使用未压缩的图片
- 使用会阻塞页面渲染的CSS

## 可访问性标准

从设计初期就考虑可访问性：
- 使用语义化的HTML元素
- 在需要的地方添加ARIA标签和角色
- 确保键盘导航功能正常工作
- 保持足够的颜色对比度（符合WCAG AA标准）
- 使用屏幕阅读器（如VoiceOver、NVDA）进行测试
- 支持降低动画效果的设置

**示例：**
```liquid
<button
  type="button"
  aria-label="{{ 'cart.add_to_cart' | t }}"
  aria-describedby="variant-{{ variant.id }}"
>
  {{ 'cart.add' | t }}
</button>
```

## 设计系统管理

有关构建和维护CSS设计系统的详细信息，请参考`references/design-system.md`：
- **品牌颜色**（主色、辅助色、强调色、中性色）
- **字体样式**（标题、正文、标签的字体大小）
- **间距规范**（以4px或8px为基本单位）
- **组件库**（按钮、卡片、网格、表单）
- **响应式布局**（不同屏幕尺寸下的布局调整）
- **CSS自定义属性**（变量）

**实现方法：**
- 在`assets/variables.css`或`config/settings_schema.json`中定义设计相关变量
- 创建可复用的组件类
- 在`references/design-system.md`中记录组件的使用方法
- 通过主题设置允许商家自定义组件

## 商家自定义功能

允许商家无需编写代码即可自定义主题：
- **主题设置**（`config/settings_schema.json`）：
```json
{
  "name": "Colors",
  "settings": [
    {
      "type": "color",
      "id": "color_primary",
      "label": "Primary Color",
      "default": "#000000"
    },
    {
      "type": "font_picker",
      "id": "font_heading",
      "label": "Heading Font",
      "default": "helvetica_n4"
    }
  ]
}
```

- **模块设置**：
```liquid
{% schema %}
{
  "name": "Featured Collection",
  "settings": [
    {
      "type": "collection",
      "id": "collection",
      "label": "Collection"
    },
    {
      "type": "range",
      "id": "products_to_show",
      "min": 2,
      "max": 12,
      "step": 1,
      "default": 4,
      "label": "Products to show"
    }
  ],
  "blocks": [
    {
      "type": "heading",
      "name": "Heading",
      "settings": [
        {
          "type": "text",
          "id": "heading",
          "label": "Heading"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Featured Collection"
    }
  ]
}
{% endschema %}
```

## Shopify CLI参考

**开发相关命令：**
- `shopify theme init` — 从模板创建新主题
- `shopify theme dev` — 启动本地开发服务器并实现热重载
- `shopify theme list` — 列出店铺中的所有主题
- `shopify theme open` — 在Shopify管理后台打开主题

**部署相关命令：**
- `shopify theme push` — 将本地更改推送到店铺
- `shopify theme pull` — 从远程仓库拉取更改到本地
- `shopify theme publish` — 将主题设置为在线状态
- `shopify theme share` — 生成可分享的预览链接
- `shopify theme package` — 创建可发布的ZIP文件包

**质量检查：**
- `shopify theme check` — 运行代码检查工具
- `shopify theme check --auto-correct` — 自动修复问题

**常用参数：**
- `--store <store.myshopify.com>` — 指定目标店铺
- `--theme <THEME_ID>` — 指定目标主题
- `--allow-live` — 允许将更改推送到实际店铺（需要确认）
- `--only <glob>` — 仅推送指定文件
- `--ignore <glob>` — 跳过指定文件
- `--nodelete` — 不删除本地不存在的远程文件

## Ajax API（用于实现交互功能）

常见用途：
- 不需要重新加载页面即可添加商品到购物车
- 动态更新购物车数量
- 快速查看产品信息
- 提供搜索建议

**示例（添加商品到购物车）：**
```javascript
fetch(`${window.Shopify.routes.root}cart/add.js`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    id: variantId,
    quantity: 1
  })
})
.then(response => response.json())
.then(item => {
  console.log('Added to cart:', item);
  // Update cart UI
})
.catch(error => console.error('Error:', error));
```

**获取购物车内容：**
```javascript
fetch(`${window.Shopify.routes.root}cart.js`)
  .then(response => response.json())
  .then(cart => console.log('Cart:', cart));
```

有关Shopify Ajax API的详细信息，请参考官方文档。

## 代码质量标准

**推荐做法：**
- 使用版本控制工具（Git）
- 编写清晰、易于维护的代码
- 用注释解释复杂逻辑
- 遵循Liquid语言的编码规范
- 在持续集成/持续部署（CI/CD）流程中使用代码检查工具
- 在多种设备和浏览器上进行测试

**不建议的做法：**
- 对代码进行混淆处理
- 欺骗搜索引擎
- 硬编码商家特定的数据
- 忽略代码检查工具的警告
- 跳过可访问性测试

## 测试 checklist

在部署到生产环境之前，请确保：
- [ ] 运行`shopify theme check`，确保没有严重错误
- [ ] 在移动设备（iOS和Android）上进行测试
- [ ] 使用屏幕阅读器验证可访问性
- [ ] 检查页面性能（Lighthouse评分建议达到90分以上）
- [ ] 在主题编辑器中测试所有自定义选项
- [ ] 在所有支持的本地化语言中验证翻译内容
- [ ] 测试完整的购物车和结账流程
- [ ] 在3G网络环境下进行测试
- [ ] 检查浏览器兼容性（至少支持最近两个主要版本的浏览器）
- [ ] 遵循安全最佳实践（如使用HTTPS、设置CSP头部）

## 常见开发模式

详细示例请参考`references/liquid-patterns.md`：
- 模块化模块开发
- 可复用的代码片段
- 产品卡片组件
- 动态模块渲染
- 元字段访问方式
- 自定义表单处理

## 资源链接

- **官方文档：** https://shopify.dev/docs/themes
- **Liquid语言参考：** https://shopify.dev/docs/api/liquid
- **主题检查工具：** https://shopify.dev/docs/storefronts/themes/tools/theme-check
- **CLI参考：** https://shopify.dev/docs/themes/tools/cli
- **Ajax API参考：** https://shopify.dev/docs/api/ajax
- **最佳实践：** https://shopify.dev/docs/themes/best-practices

## 相关资源

- **参考文档：**
  - `references/liquid-patterns.md` — 常见的Liquid模板模式和模块结构
  - `references/design-system.md` — CSS设计系统指南
  - `references/deployment.md` — 完整的部署流程和检查清单
  - `references/performance.md` — 性能优化策略

---

**版本：** 1.0（由`shopify-theme-dev`和`shopify-theme-push`合并而成）
**最后更新时间：** 2026-03-13