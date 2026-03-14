---
name: clawdbot-superskill
description: >
  ClawdBot 的完整生产技能集包含以下三项合并的功能：  
  (1) **FurrBudd WordPress 文章构建工具**：提供完整的 CSS 主题、HTML 组件模板、SVG 图标库，以及 7 条与 WordPress 兼容性的规则；同时包含用于在 furrbudd.com 上生成联盟产品评论文章的预交付检查清单。  
  (2) **编辑型联盟营销用户体验策略**：借鉴 The Spruce Pets、NYT Wirecutter 和 Dog Food Advisor 的竞争情报，为内容架构和编辑决策提供支持。  
  (3) **AI Money Mastery 网站构建工具**：提供完整的 React/Vite/Tailwind 源代码框架，以及用于 AI 营收 landing 页面的豪华级 UI 组件。  
  当用户提及 FurrBudd、产品评论、WordPress 文章、联盟营销内容、编辑策略、AI Money Mastery 或 React 网站构建时，ClawdBot 会自动激活相应的功能。
  ClawdBot's complete production skill set. Contains three merged capabilities:
  (1) The FurrBudd WordPress article builder — full CSS theme, HTML component
  templates, SVG icon library, 7 WordPress compatibility rules, and pre-delivery
  checklist for generating affiliate product review articles on furrbudd.com.
  (2) Editorial affiliate UX strategy — competitive intelligence from The Spruce
  Pets, NYT Wirecutter, and Dog Food Advisor for content architecture and
  editorial decision-making. (3) AI Money Mastery website builder — complete
  React/Vite/Tailwind source code scaffold with luxury UI components for
  AI-monetization landing pages. ClawdBot should activate this skill when the
  user mentions FurrBudd, product reviews, WordPress articles, affiliate
  content, editorial strategy, AI Money Mastery, or React website builds.
---
# ClawdBot超级技能

> ClawdBot的统一知识库。一个文件中包含了三个生产系统——从WordPress联盟文章到编辑策略，再到React网站框架。

---

# 技能1：FURRBUDD文章构建器

## 概述

ClawdBot生成自包含的HTML块（CSS + HTML，不使用JS框架），这些块可以直接粘贴到[furrbudd.com](https://furrbudd.com)的WordPress **代码编辑器**中。每篇文章都是一个单独的文件：一个`<link>`标签、一个`<style>`块，以及一个`<div class="fb-article">`包装器。

furrbudd.com的WordPress主题会强制覆盖SVG的大小、背景、字体和颜色。以下所有的兼容性规则都是因为实际网站渲染失败而制定的。ClawdBot必须严格遵循这些规则。

---

### 第1部分：WordPress兼容性规则

这些规则是不可商量的。违反任何一条规则都会导致网站渲染失败。

#### 规则1：字体加载 —— 使用`<link>`，严禁使用`@import`

WordPress会删除`<style>`标签内的`@import`。文章必须以以下方式开头：

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Oswald:wght@400;600;700&display=swap">
<style>
/* all CSS here */
</style>
<div class="fb-article">
  <!-- all HTML here -->
</div>
```

#### 规则2：SVG图标 —— 需要三层保护

WordPress主题会应用`svg { width: 100% }`，这会导致图标占据整个容器的宽度。每个`<svg>`都需要以下三层样式：

**第1层 —— 使用`!important`和WordPress包装器选择器进行CSS重置**（包含在下面的样式表中）。

**第2层 —— HTML的`width`/`height`属性：**
```html
<svg class="ico" width="18" height="18" viewBox="0 0 24 24" ...>
```

**第3层 —— 使用`!important`的内联`style`：**
```html
<svg class="ico" width="18" height="18"
  style="width:1.1em!important;height:1.1em!important;max-width:1.1em!important;max-height:1.1em!important;display:inline-block!important;vertical-align:-0.15em!important;overflow:visible!important"
  viewBox="0 0 24 24" ...>
```

每个SVG都必须包含这三层样式。任何一层都不可省略。

#### 规则3：深色背景部分 —— 使用带有硬编码颜色的内联样式

WordPress主题会覆盖`<div>`的CSS `background`属性。任何深色背景的部分（如`.callout`、`.final-verdict`）都必须具有：
- 使用内联`style`属性设置`background-color`和`background`
- 使用硬编码的十六进制颜色值（而不是CSS变量）
- 在`background`属性上使用`!important`
- 在每个子文本元素上使用带有硬编码颜色的内联`style`

#### 规则4：文本属性 —— 必须使用`!important`

WordPress主题会覆盖`font-size`、`line-height`、`color`和`font-family`属性。每个与文本相关的CSS规则都需要在这些属性上使用`!important`。

#### 规则5：CSS变量与硬编码值

- 在样式表中使用CSS变量来设置通用属性
- 对于深色部分，使用硬编码的十六进制值来设置`background`
- 对于深色部分中的文本，使用硬编码的十六进制值来设置`color`
- 始终在`.fb-article`根选择器中定义变量

#### 规则6：超链接 —— 需要三层保护（与SVG相同）

WordPress主题会删除链接的`text-decoration: underline`属性。每个`<a>`标签（`.btn-primary`按钮除外）都需要以下三层样式：

**第1层 —— 使用`!important`和WordPress包装器选择器进行CSS重置**（包含在下面的样式表中）：
```css
.fb-article a,
.entry-content .fb-article a,
body .entry-content .fb-article a {
  color: #0f2b4a !important;
  text-decoration: underline !important;
  text-decoration-color: #d4a843 !important;
  text-underline-offset: 3px !important;
  text-decoration-thickness: 2px !important;
  text-decoration-style: solid !important;
}
```

**第2层 —— 在每个`<a>`标签上使用内联`style`：**
```html
<a href="AFFILIATE_LINK" target="_blank" rel="noopener nofollow sponsored"
  style="color:#0f2b4a!important;text-decoration:underline!important;text-decoration-color:#d4a843!important;text-underline-offset:3px!important;text-decoration-thickness:2px!important">
  link text
</a>
```

**第3层 —— 深色部分中的链接**使用金色浅色调：
```html
<a href="AFFILIATE_LINK" target="_blank" rel="noopener nofollow sponsored"
  style="color:#e8c46a!important;text-decoration:underline!important;text-decoration-color:#d4a843!important;text-underline-offset:3px!important;text-decoration-thickness:2px!important">
  link text
</a>
```

**例外：`.btn-primary`按钮**的`text-decoration`设置为`none !important` —— CTA按钮不允许下划线。

#### 规则7：文章宽度 —— 居中于1100px

WordPress主题的单篇文章容器宽度设置为1100px。每个文章的`.fb-article`根选择器都必须包含以下代码：

```css
.fb-article {
  max-width: 1100px;
  margin: 0 auto;
  /* ...rest of variables and properties... */
}
```

---

### 第2部分：完整的CSS样式表

ClawdBot必须将整个`<style>`块复制到每篇文章中。只有特定产品的内容会在不同文章之间变化，CSS保持不变。

```css
.fb-article {
  max-width: 1100px;
  margin: 0 auto;
  --fb-navy: #0f2b4a;
  --fb-navy-dark: #0a1e33;
  --fb-teal: #0d7377;
  --fb-gold: #d4a843;
  --fb-gold-light: #e8c46a;
  --fb-white: #ffffff;
  --fb-off-white: #f5f5f5;
  --fb-light-gray: #e8e8e8;
  --fb-mid-gray: #888888;
  --fb-dark-gray: #333333;
  --fb-text: #333333;
  --fb-text-light: #666666;
  --fb-shadow: 0 4px 15px rgba(0,0,0,0.1);
  --fb-shadow-lg: 0 8px 30px rgba(0,0,0,0.15);
  --fb-transition: all 0.3s ease;
  font-family: 'Open Sans', sans-serif;
  color: var(--fb-text);
  line-height: 1.6;
}

/* GLOBAL SVG RESET */
.fb-article svg,
.fb-article svg[viewBox],
.fb-article svg.ico,
.entry-content .fb-article svg,
.entry-content .fb-article svg.ico,
.entry-content .fb-article svg[viewBox],
.post-content .fb-article svg,
.wp-block-group .fb-article svg,
body .entry-content svg.ico,
body .entry-content svg[viewBox] {
  width: 1.1em !important;
  height: 1.1em !important;
  max-width: 1.1em !important;
  max-height: 1.1em !important;
  min-width: 0 !important;
  min-height: 0 !important;
  display: inline-block !important;
  vertical-align: -0.15em !important;
  overflow: visible !important;
  flex-shrink: 0 !important;
}
.fb-article .ico-check { color: var(--fb-teal) !important; }
.fb-article .ico-warn { color: #b07a2a !important; }
.fb-article .art-tag svg,
.fb-article .verdict-title svg { width: 1em !important; height: 1em !important; max-width: 1em !important; max-height: 1em !important; }
.fb-article .pc-item svg,
.fb-article .who-item svg { width: 1em !important; height: 1em !important; max-width: 1em !important; max-height: 1em !important; margin-top: 2px; }
.fb-article .faq-q svg { width: 1.2em !important; height: 1.2em !important; max-width: 1.2em !important; max-height: 1.2em !important; }

/* ROPE BORDER */
.fb-article .rope-border {
  width: 100%;
  height: 10px;
  background: linear-gradient(to right, #8B6914, #C4982B, #D4A843, #C4982B, #8B6914, #C4982B, #D4A843, #C4982B, #8B6914, #C4982B, #D4A843);
  background-size: 60px 10px;
  margin-bottom: 40px;
}

/* EYEBROW TAGS */
.fb-article .eyebrow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 32px;
}
.fb-article .art-tag {
  font-family: 'Oswald', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  padding: 5px 14px;
  border-radius: 4px;
}
.fb-article .tag-cat { background: var(--fb-teal); color: #fff; }
.fb-article .tag-pick { background: var(--fb-gold); color: var(--fb-navy); }
.fb-article .art-meta {
  color: var(--fb-mid-gray);
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 36px;
}

/* VERDICT BOX */
.fb-article .verdict-box {
  background: var(--fb-off-white);
  border: 2px solid var(--fb-light-gray);
  border-radius: 12px;
  padding: 30px;
  margin: 0 0 32px;
  box-shadow: var(--fb-shadow);
}
.fb-article .verdict-title {
  font-family: 'Oswald', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--fb-navy);
  letter-spacing: 0.5px;
  margin: 0 0 20px;
  padding-bottom: 12px;
  border-bottom: 3px solid var(--fb-gold);
}
.fb-article .verdict-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 24px;
  margin-bottom: 20px;
}
.fb-article .verdict-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 0.9rem !important;
  line-height: 1.5 !important;
  color: var(--fb-text) !important;
  font-family: 'Open Sans', sans-serif !important;
  margin: 0;
}
.fb-article .verdict-rating {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 18px;
  border-top: 1px solid var(--fb-light-gray);
  flex-wrap: wrap;
}
.fb-article .stars { color: var(--fb-gold); font-size: 22px; letter-spacing: 2px; }
.fb-article .rating-num {
  font-family: 'Oswald', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--fb-navy);
}
.fb-article .rating-meta { font-size: 0.85rem !important; color: var(--fb-mid-gray) !important; font-family: 'Open Sans', sans-serif !important; }

/* CTA */
.fb-article .cta-wrap { text-align: center; margin: 32px 0; }
.fb-article .btn-primary {
  display: inline-block;
  background-color: var(--fb-gold);
  color: var(--fb-navy) !important;
  font-family: 'Oswald', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 14px 40px;
  border-radius: 30px;
  letter-spacing: 1px;
  transition: var(--fb-transition);
  box-shadow: 0 4px 15px rgba(212,168,67,0.4);
  text-decoration: none !important;
}
.fb-article .btn-primary:hover {
  background-color: var(--fb-gold-light);
  transform: translateY(-2px);
}
.fb-article .cta-note { font-size: 0.8rem !important; color: var(--fb-mid-gray) !important; margin: 8px 0 0; font-family: 'Open Sans', sans-serif !important; }

/* HEADINGS */
.fb-article h2 {
  font-family: 'Oswald', sans-serif !important;
  font-size: 1.7rem !important;
  font-weight: 700 !important;
  text-transform: uppercase;
  color: var(--fb-navy) !important;
  letter-spacing: 0.5px;
  margin: 44px 0 16px !important;
  padding-bottom: 10px !important;
  border-bottom: 3px solid var(--fb-teal) !important;
  display: flex;
  align-items: center;
  gap: 10px;
}
.fb-article h2::before {
  content: '';
  display: inline-block;
  width: 6px;
  height: 26px;
  background: var(--fb-gold);
  border-radius: 3px;
  flex-shrink: 0;
}
.fb-article h3 {
  font-family: 'Oswald', sans-serif !important;
  font-size: 1.15rem !important;
  font-weight: 600 !important;
  color: var(--fb-navy) !important;
  margin: 28px 0 10px !important;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}
.fb-article p {
  font-size: 1rem !important;
  line-height: 1.8 !important;
  color: var(--fb-text) !important;
  margin-bottom: 18px !important;
  font-family: 'Open Sans', sans-serif !important;
}
.fb-article strong { font-weight: 600; color: var(--fb-navy); }

/* HYPERLINK STYLE — hardened for WP (Rule 6) */
.fb-article a,
.entry-content .fb-article a,
.post-content .fb-article a,
.wp-block-group .fb-article a,
body .entry-content .fb-article a {
  color: #0f2b4a !important;
  text-decoration: underline !important;
  text-decoration-color: #d4a843 !important;
  text-underline-offset: 3px !important;
  text-decoration-thickness: 2px !important;
  text-decoration-style: solid !important;
  transition: var(--fb-transition);
}
.fb-article a:hover,
.entry-content .fb-article a:hover,
body .entry-content .fb-article a:hover {
  color: #0d7377 !important;
  text-decoration-color: #e8c46a !important;
}
.fb-article .btn-primary,
.entry-content .fb-article .btn-primary,
body .entry-content .fb-article .btn-primary {
  text-decoration: none !important;
}

/* STAR RATING (CSS mask, not SVG) */
.fb-article .star-bar {
  display: inline-flex;
  gap: 2px;
}
.fb-article .star-icon {
  width: 22px;
  height: 22px;
  background: var(--fb-gold);
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z'/%3E%3C/svg%3E") center/contain no-repeat;
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z'/%3E%3C/svg%3E") center/contain no-repeat;
}
.fb-article .star-icon.empty { background: var(--fb-light-gray); }
.fb-article .star-icon.partial { background: linear-gradient(to right, var(--fb-gold) 60%, var(--fb-light-gray) 60%); }

/* ACCORDION FAQ */
.fb-article .faq-item { cursor: pointer; }
.fb-article .faq-q { display: flex; justify-content: space-between; align-items: center; }
.fb-article .faq-chevron {
  font-style: normal;
  font-size: 1.2rem;
  transition: transform 0.3s ease;
  color: var(--fb-teal);
  flex-shrink: 0;
  margin-left: 12px;
}
.fb-article .faq-item.open .faq-chevron { transform: rotate(180deg); }
.fb-article .faq-a {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.35s ease, margin 0.35s ease;
  margin: 0;
}
.fb-article .faq-item.open .faq-a {
  max-height: 300px;
  margin-top: 10px;
}

/* STAT PILLS */
.fb-article .stat-row { display: flex; flex-wrap: wrap; gap: 12px; margin: 24px 0; }
.fb-article .stat-pill {
  background: var(--fb-white);
  border: 2px solid var(--fb-light-gray);
  border-radius: 12px;
  padding: 14px 20px;
  text-align: center;
  min-width: 100px;
  transition: var(--fb-transition);
}
.fb-article .stat-pill:hover { border-color: var(--fb-teal); box-shadow: var(--fb-shadow); }
.fb-article .stat-num {
  font-family: 'Oswald', sans-serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--fb-teal);
  display: block;
  line-height: 1;
  margin-bottom: 4px;
}
.fb-article .stat-lbl {
  font-family: 'Oswald', sans-serif;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--fb-mid-gray);
}

/* INGREDIENT BOX */
.fb-article .ingredient-box {
  background: #f0f9f9;
  border: 2px solid rgba(13,115,119,0.2);
  border-left: 5px solid var(--fb-teal);
  border-radius: 8px;
  padding: 20px 24px;
  margin: 20px 0;
  font-size: 0.95rem;
  line-height: 2;
  color: var(--fb-dark-gray);
}
.fb-article .ingredient-box strong { color: var(--fb-teal); font-weight: 700; }

/* PROS / CONS */
.fb-article .pc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 28px 0; }
.fb-article .pc-box { border-radius: 12px; padding: 22px 24px; box-shadow: var(--fb-shadow); }
.fb-article .pc-box.pros { background: #f0f9f4; border: 2px solid #a8d5b5; }
.fb-article .pc-box.cons { background: #fff8f0; border: 2px solid #f0d5a8; }
.fb-article .pc-label {
  font-family: 'Oswald', sans-serif;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0 0 14px;
  padding-bottom: 10px;
  border-bottom: 2px solid currentColor;
}
.fb-article .pc-box.pros .pc-label { color: var(--fb-teal); }
.fb-article .pc-box.cons .pc-label { color: #b07a2a; }
.fb-article .pc-item { font-size: 0.88rem !important; line-height: 1.5 !important; margin-bottom: 9px; display: flex; gap: 8px; align-items: flex-start; color: var(--fb-text) !important; font-family: 'Open Sans', sans-serif !important; }

/* CALLOUT (dark background — needs inline style too) */
.fb-article .callout {
  background-color: #0f2b4a !important;
  background: linear-gradient(135deg, #0a1e33 0%, #0f2b4a 100%) !important;
  border-radius: 12px !important;
  padding: 28px 32px !important;
  margin: 32px 0;
  position: relative;
  overflow: hidden;
}
.fb-article .callout::before {
  content: '\201C';
  position: absolute;
  top: -10px; left: 16px;
  font-family: 'Oswald', sans-serif;
  font-size: 8rem;
  color: rgba(212,168,67,0.15);
  line-height: 1;
}
.fb-article .callout p {
  color: rgba(255,255,255,0.9) !important;
  font-size: 1.05rem;
  font-style: italic;
  line-height: 1.7;
  margin-bottom: 0 !important;
  position: relative;
  z-index: 1;
}
.fb-article .callout cite {
  display: block;
  margin-top: 10px;
  color: #d4a843 !important;
  font-family: 'Oswald', sans-serif;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-style: normal;
  position: relative;
  z-index: 1;
}

/* WHO BOXES */
.fb-article .who-box { border-radius: 12px; padding: 24px 26px; margin: 16px 0; box-shadow: var(--fb-shadow); }
.fb-article .who-box.good { background: #f0f9f4; border: 2px solid #a8d5b5; }
.fb-article .who-box.skip { background: #fff8f0; border: 2px solid #f0d5a8; }
.fb-article .who-box h3 { margin: 0 0 14px !important; font-size: 1rem !important; text-transform: uppercase; }
.fb-article .who-box.good h3 { color: var(--fb-teal) !important; }
.fb-article .who-box.skip h3 { color: #b07a2a !important; }
.fb-article .who-item { font-size: 0.9rem !important; margin-bottom: 9px; display: flex; gap: 10px; align-items: flex-start; line-height: 1.5 !important; color: var(--fb-text) !important; font-family: 'Open Sans', sans-serif !important; }

/* PRICE TABLE */
.fb-article .price-table { width: 100%; border-collapse: collapse; margin: 20px 0; border-radius: 12px; overflow: hidden; box-shadow: var(--fb-shadow); font-size: 0.95rem; }
.fb-article .price-table th { background: var(--fb-navy); color: var(--fb-white); text-align: left; padding: 12px 16px; font-family: 'Oswald', sans-serif; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; }
.fb-article .price-table td { padding: 12px 16px; border-bottom: 1px solid var(--fb-light-gray); font-family: 'Open Sans', sans-serif !important; color: var(--fb-text) !important; font-size: 0.95rem !important; }
.fb-article .price-table tr:nth-child(even) td { background: var(--fb-off-white); }
.fb-article .price-table .best-row td { font-weight: 700; color: var(--fb-teal); background: #e8f5f5; }

/* FAQ */
.fb-article .faq-item { border: 2px solid var(--fb-light-gray); border-radius: 8px; padding: 20px 24px; margin-bottom: 12px; transition: var(--fb-transition); }
.fb-article .faq-item:hover { border-color: var(--fb-teal); box-shadow: var(--fb-shadow); }
.fb-article .faq-q { font-family: 'Oswald', sans-serif; font-size: 1rem; font-weight: 700; color: var(--fb-navy); text-transform: uppercase; letter-spacing: 0.3px; margin: 0 0 10px; }
.fb-article .faq-a { font-size: 0.92rem !important; color: var(--fb-text-light) !important; line-height: 1.75 !important; margin: 0; font-family: 'Open Sans', sans-serif !important; }

/* FINAL VERDICT (dark background — needs inline style too) */
.fb-article .final-verdict {
  background-color: #0f2b4a !important;
  background: linear-gradient(135deg, #0a1e33 0%, #0f2b4a 50%, #1a3d5c 100%) !important;
  border-radius: 12px !important;
  padding: 36px 38px !important;
  margin-top: 48px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.15) !important;
}
.fb-article .fv-header { display: flex; align-items: center; gap: 24px; margin-bottom: 20px; flex-wrap: wrap; }
.fb-article .fv-score { font-family: 'Oswald', sans-serif; font-size: 4rem; font-weight: 700; color: #d4a843 !important; line-height: 1; }
.fb-article .fv-score-max { font-size: 1.5rem !important; color: rgba(255,255,255,0.35) !important; }
.fb-article .fv-label { font-family: 'Oswald', sans-serif; font-size: 0.72rem !important; color: rgba(255,255,255,0.45) !important; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; }
.fb-article .fv-title h2 {
  color: #fff !important;
  font-size: 1.6rem !important;
  margin: 0 0 4px !important;
  padding: 0 !important;
  border: none !important;
}
.fb-article .fv-title h2::before { display: none !important; }
.fb-article .fv-title p { color: #e8c46a !important; font-size: 0.85rem !important; font-family: 'Oswald', sans-serif !important; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 !important; }
.fb-article .fv-divider { border: none; border-top: 1px solid rgba(255,255,255,0.15); margin: 20px 0; }
.fb-article .body-text { color: rgba(255,255,255,0.8) !important; font-size: 0.95rem !important; line-height: 1.8 !important; margin-bottom: 14px !important; font-family: 'Open Sans', sans-serif !important; }

/* DIVIDER */
.fb-article .divider { border: none; border-top: 1px solid var(--fb-light-gray); margin: 40px 0; }

/* AFFILIATE NOTE */
.fb-article .affiliate-note {
  background: var(--fb-off-white);
  border: 1px solid var(--fb-light-gray);
  border-radius: 8px;
  padding: 16px 20px;
  font-size: 0.82rem;
  color: var(--fb-mid-gray);
  line-height: 1.6;
  margin-top: 48px;
  font-style: italic;
}

/* RESPONSIVE */
@media (max-width: 640px) {
  .fb-article .verdict-grid { grid-template-columns: 1fr; }
  .fb-article .pc-grid { grid-template-columns: 1fr; }
  .fb-article h2 { font-size: 1.3rem !important; }
}
```

---

### 第3部分：SVG图标库

每个SVG都必须包含`class="ico" width="18" height="18"`以及完整的内联`style`字符串。内联样式被缩写为`ICO_STYLE` —— ClawdBot必须始终将其展开为完整的样式：

```
style="width:1.1em!important;height:1.1em!important;max-width:1.1em!important;max-height:1.1em!important;display:inline-block!important;vertical-align:-0.15em!important;overflow:visible!important"
```

#### 对勾（青色，表示优点/正面信息）
```html
<svg class="ico ico-check" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="#0d7377" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
```

#### 警告三角形（琥珀色，表示缺点/注意事项）
```html
<svg class="ico ico-warn" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="#b07a2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
```

#### 猫爪图案（实心，用于“适合谁”信息框）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="currentColor"><ellipse cx="8" cy="7" rx="2.5" ry="3"/><ellipse cx="16" cy="7" rx="2.5" ry="3"/><ellipse cx="4.5" cy="13" rx="2" ry="2.5"/><ellipse cx="19.5" cy="13" rx="2" ry="2.5"/><path d="M12 20c-3 0-5-2-6-4s0-4 2-4.5c1.5-.4 2.5.5 4 .5s2.5-.9 4-.5c2 .5 3 2.5 2 4.5s-3 4-6 4z"/></svg>
```

#### 猫爪轮廓（用于类别标签、小狗常见问题解答）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 5.172C10 3.782 8.423 2.679 6.5 3c-2.823.47-4.113 6.006-4 7 .137 1.217 1.5 2 2.5 2s2-.5 3-1.5c.5-.5 1-1 1.5-1s1 .5 1.5 1c1 1 2 1.5 3 1.5s2.363-.783 2.5-2c.113-.994-1.177-6.53-4-7C10.577 2.679 10 3.782 10 5.172z"/><path d="M12 17c-2 0-4-1-4-3s2-4 4-4 4 2 4 4-2 3-4 3z"/><circle cx="8.5" cy="12.5" r=".5" fill="currentColor"/><circle cx="15.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 17v4"/></svg>
```

#### 星形（实心，用于徽章标签）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
```

#### 闪电符号（用于快速总结标题）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="currentColor"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
```

#### 日历（用于元数据中的日期）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
```

#### 笔（用于元数据中的作者信息）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
```

#### 时钟（用于元数据中的阅读时间）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l2 2"/><path d="M10 2h4"/></svg>
```

#### 树叶（用于表示天然/有机产品的优点）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="#0d7377" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 21c3-6 10-9 16-10C20 5 14 3 8 5c-4 1.33-5 5-4 8l-1 8"/><path d="M8 13c3-2 7-3 11-3"/></svg>
```

#### 瞄准镜/目标（用于表示益生菌/科学产品的优点）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="#0d7377" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1" fill="currentColor"/><line x1="12" y1="2" x2="12" y2="7"/><line x1="12" y1="17" x2="12" y2="22"/><line x1="2" y1="12" x2="7" y2="12"/><line x1="17" y1="12" x2="22" y2="12"/></svg>
```

#### 下降趋势（用于表示重量/血糖产品的缺点）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/></svg>
```

#### 旗帜（用于表示来源信息的优点）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>
```

#### 烧瓶/量筒（用于表示无召回风险的产品的优点）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 100-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 01-2-2V6h6v4a2 2 0 01-2 2z"/><path d="M12 6V3a1 1 0 00-1-1H9a1 1 0 00-1 1v3"/></svg>
```

#### 闪光符号（用于表示涂层/结果产品的优点）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l1.5 5.5L19 9l-5.5 1.5L12 16l-1.5-5.5L5 9l5.5-1.5L12 2z"/><path d="M19 14l1 3 3 1-3 1-1 3-1-3-3-1 3-1 1-3z" opacity=".6"/></svg>
```

#### 美元符号（用于表示价格的缺点）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="#b07a2a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
```

#### 植物/小麦图案（用于表示谷物产品的缺点）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 22l10-10"/><path d="M16 8l-4 4"/><path d="M12 12c1-2 3-4 6-4 0 3-2 5-4 6"/><path d="M8 16c1-2 3-4 6-4 0 3-2 5-4 6"/><path d="M16 4c1-2 3-2 5 0 0 3-2 4-4 4"/><path d="M12 8c1-2 3-2 5 0 0 3-2 4-4 4"/></svg>
```

#### 条形图（用于表示碳水化合物含量的缺点）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
```

#### 刷新/循环符号（用于表示过渡期的缺点）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/></svg>
```

#### 购物车（用于表示产品可用性的缺点）
```html
<svg class="ico" width="18" height="18" ICO_STYLE viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6"/></svg>
```

#### 向下箭头（用于表示常见问题解答的折叠功能）
---  
在`<i class="faq-chevron">▼</i>`中使用文本字符`▼`（不是SVG图标）。

---

### 第4部分：HTML组件模板

ClawdBot使用以下HTML模板来构建每个组件部分。将括号中的`[PLACEHOLDER]`替换为特定产品的内容。`AFFILIATE_URL`是用户为每篇文章提供的唯一联盟链接。

#### 4.1 绳索边框
```html
<div class="rope-border"></div>
```

#### 4.2 眉毛标签
```html
<div class="eyebrow">
  <span class="art-tag tag-cat">[PAWN_OUTLINE_SVG] [Category Name] Reviews</span>
  <span class="art-tag tag-pick">[STAR_SVG] [Badge Text, e.g. "Amazon Overall Pick"]</span>
</div>
```

#### 4.3 文章元数据
```html
<div class="art-meta">
  <span>[CALENDAR_SVG] [Month Year]</span>
  <span>·</span>
  <span>[PEN_SVG] FurrBudd Editorial Team</span>
  <span>·</span>
  <span>[CLOCK_SVG] [X] min read</span>
</div>
```

#### 4.4 快速总结框
```html
<div class="verdict-box">
  <div class="verdict-title">[LIGHTNING_SVG] Quick Verdict</div>
  <div class="verdict-grid">
    <div class="verdict-item"><span>[CHECKMARK_SVG]</span><span>[Pro point]</span></div>
    <div class="verdict-item"><span>[CHECKMARK_SVG]</span><span>[Pro point]</span></div>
    <div class="verdict-item"><span>[WARNING_SVG]</span><span>[Con point]</span></div>
    <div class="verdict-item"><span>[WARNING_SVG]</span><span>[Con point]</span></div>
  </div>
  <div class="verdict-rating">
    <span class="star-bar" role="img" aria-label="[X] out of 5 stars">
      <span class="star-icon"></span>
      <span class="star-icon"></span>
      <span class="star-icon"></span>
      <span class="star-icon"></span>
      <span class="star-icon partial"></span>
    </span>
    <span class="rating-num">[X.X]</span>
    <span class="rating-meta">out of 5 &nbsp;·&nbsp; [N] Amazon reviews &nbsp;·&nbsp; [N]+ sold last month</span>
  </div>
</div>
```

#### 4.5 主要呼叫行动（CTA）
```html
<div class="cta-wrap">
  <a class="btn-primary" href="AFFILIATE_URL" target="_blank" rel="noopener nofollow sponsored">Check Price on Amazon →</a>
  <p class="cta-note">[Available sizes / shipping info]</p>
</div>
```

#### 4.6 分隔符
```html
<hr class="divider" />
```

#### 4.7 正文部分
```html
<h2>[Section Title]</h2>
<p>[Body paragraph with <a href="AFFILIATE_URL" target="_blank" rel="noopener nofollow sponsored"><strong>anchor text</strong></a> links woven in naturally.]</p>
<h3>[Subheading]</h3>
<p>[Sub-section paragraph.]</p>
```

#### 4.8 成分框（可选，用于食品产品）
```html
<div class="ingredient-box">
  <strong>[Key Ingredient 1]</strong> · <strong>[Key Ingredient 2]</strong> · Regular Ingredient · <strong>[Key Ingredient 3]</strong> · Regular Ingredient
</div>
```

#### 4.9 强调引用（深色背景 —— 必须使用内联样式）
```html
<div class="callout" style="background-color:#0f2b4a!important;background:linear-gradient(135deg,#0a1e33 0%,#0f2b4a 100%)!important;border-radius:12px!important;padding:28px 32px!important;position:relative;overflow:hidden">
  <p style="color:rgba(255,255,255,0.9)!important;font-style:italic!important;line-height:1.7!important;position:relative;z-index:1">[Quote text]</p>
  <cite style="color:#d4a843!important;display:block!important;position:relative;z-index:1">— [Attribution]</cite>
</div>
```

#### 4.10 统计数据块
```html
<div class="stat-row">
  <div class="stat-pill"><span class="stat-num">[Value]</span><span class="stat-lbl">[Label]</span></div>
  <div class="stat-pill"><span class="stat-num">[Value]</span><span class="stat-lbl">[Label]</span></div>
</div>
```

#### 4.11 优点与缺点表格
```html
<div class="pc-grid">
  <div class="pc-box pros">
    <div class="pc-label">[CHECKMARK_SVG] What We Love</div>
    <div class="pc-item"><span>[THEMED_ICON_SVG]</span><span>[Pro point]</span></div>
  </div>
  <div class="pc-box cons">
    <div class="pc-label">[WARNING_SVG] Worth Knowing</div>
    <div class="pc-item"><span>[THEMED_ICON_SVG]</span><span>[Con point]</span></div>
  </div>
</div>
```

#### 4.12 适用人群框
```html
<div class="who-box good">
  <h3>[CHECKMARK_SVG] Great Fit If Your Dog…</h3>
  <div class="who-item"><span>[PAWN_FILLED_SVG]</span><span>[Good-fit scenario]</span></div>
</div>
<div class="who-box skip">
  <h3>[WARNING_SVG] Less Ideal If Your Dog…</h3>
  <div class="who-item"><span>[WARNING_SVG]</span><span>[Less-ideal scenario]</span></div>
</div>
```

#### 4.14 常见问题解答折叠框
```html
<div class="faq-item" onclick="this.classList.toggle('open')">
  <div class="faq-q"><span>[THEMED_ICON_SVG] [Question text]</span><i class="faq-chevron">▼</i></div>
  <p class="faq-a">[Answer text]</p>
</div>
```

#### 4.15 最终总结（深色背景 —— 必须使用内联样式）
```html
<div class="final-verdict" style="background-color:#0f2b4a!important;background:linear-gradient(135deg,#0a1e33 0%,#0f2b4a 50%,#1a3d5c 100%)!important;border-radius:12px!important;padding:36px 38px!important">
  <div class="fv-header">
    <div>
      <div class="fv-score" style="color:#d4a843!important;font-family:'Oswald',sans-serif!important;font-size:4rem!important;font-weight:700!important">[X.X]<span class="fv-score-max" style="color:rgba(255,255,255,0.35)!important;font-size:1.5rem!important">/10</span></div>
      <div class="fv-label" style="color:rgba(255,255,255,0.45)!important;font-family:'Oswald',sans-serif!important;font-size:0.72rem!important">FurrBudd Rating</div>
    </div>
    <div class="fv-title">
      <h2 style="color:#ffffff!important;font-size:1.6rem!important;margin:0 0 4px!important;padding:0!important;border:none!important">Final Verdict</h2>
      <p style="color:#e8c46a!important;font-size:0.85rem!important;font-family:'Oswald',sans-serif!important;text-transform:uppercase!important;margin:0!important">Editor's Choice — [Product Category]</p>
    </div>
  </div>
  <hr class="fv-divider" style="border:none!important;border-top:1px solid rgba(255,255,255,0.15)!important;margin:20px 0!important" />
  <p class="body-text" style="color:rgba(255,255,255,0.8)!important;font-size:0.95rem!important;line-height:1.8!important;font-family:'Open Sans',sans-serif!important">[Verdict paragraph with <a href="AFFILIATE_URL" target="_blank" rel="noopener nofollow sponsored" style="color: var(--fb-gold-light);">affiliate link</a>.]</p>
  <div class="cta-wrap" style="text-align:left; margin-bottom:0;">
    <a class="btn-primary" href="AFFILIATE_URL" target="_blank" rel="noopener nofollow sponsored">Shop [Product] on Amazon →</a>
  </div>
</div>
```

#### 4.16 联盟披露
```html
<div class="affiliate-note">
  <strong>Disclosure:</strong> FurrBudd participates in the Amazon Services LLC Associates Program. If you purchase through our links, we may earn a small commission at no extra cost to you. This does not influence our editorial opinions or recommendations. Thank you for supporting FurrBudd!
</div>
```

---

### 第5部分：联盟链接

用户为每篇文章提供一个联盟链接。ClawdBot必须将其放置在：
- 每个呼叫行动（CTA）按钮上（`<a class="btn-primary" href="AFFILIATE_URL" ...>`）
- 正文段落中的上下文文本链接（在产品名称、关键短语上）
- 价格表中的“最佳价值”行
- 最终总结中的呼叫行动链接和正文链接

每个联盟链接都必须包含以下样式：
```html
<a href="AFFILIATE_URL" target="_blank" rel="noopener nofollow sponsored">
```

`.final-verdict`深色部分中的链接也需要`style="color: var(--fb-gold-light);`。

---

### 第6部分：文章部分顺序

ClawdBot必须严格按照以下顺序在`<div class="fb-article">`内部组织内容：

| # | 部分 | 类别 | 是否需要深色背景？ |
|---|---------|-------|----------|
| 1 | 绳索边框 | `.rope-border` | 否 |
| 2 | 眉毛标签 | `.eyebrow` > `.art-tag` | 否 |
| 3 | 文章元数据 | `.art-meta` | 否 |
| 4 | 快速总结 | `.verdict-box` | 否 |
| 5 | 主要呼叫行动 | `.cta-wrap` > `.btn-primary` | 否 |
| 6 | 分隔符 | `.divider` | 否 |
| 7 | 正文部分 | `h2` + `p` + `h3` | 否 |
| 8 | 强调引用 | `.callout` | **是 —— 需要使用内联样式** |
| 9 | 更多正文 | `h2` + `p` | 否 |
| 10 | 统计数据块 | `.stat-row` > `.stat-pill` | 否 |
| 11 | 优点与缺点 | `.pc-grid` | 否 |
| 12 | 价格表 | `.price-table` | 否 |
| 13 | 适用人群 | `.who-box` | 否 |
| 14 | 常见问题解答折叠框 | `.faq-item` | 否 |
| 15 | 最终总结 | `.final-verdict` | **是 —— 需要使用内联样式** |
| 16 | 联盟披露 | `.affiliate-note` | 否 |

---

### 第7部分：颜色调色板与字体样式

#### 颜色

| 变量 | 十六进制代码 | 用途 |
|----------|-----|-------|
| `--fb-navy` | `#0f2b4a` | 标题、强调文本、深色背景 |
| `--fb-navy-dark` | `#0a1e33` | 深色部分的渐变起始色 |
| `--fb-teal` | `#0d7377` | 对勾图标、h2边框、强调色 |
| `--fb-gold` | `#d4a843` | CTA按钮、星星、装饰性边框、引用文本 |
| `--fb-gold-light` | `#e8c46a` | 鼠标悬停状态、深色部分中的子标题文本 |
| `--fb-text` | `#333333` | 正文文本 |
| `--fb-text-light` | `#666666` | 常见问题解答中的文本 |
| `--fb-mid-gray` | `#888888` | 元数据文本、标题栏 |
| `--fb-off-white` | `#f5f5f5` | 浅色框背景 |
| `--fb-light-gray` | `#e8e8e8` | 边框、分隔符 |

#### 字体样式

| 元素 | 字体 | 字体重量 | 字体大小 | 大写/小写 |
|---------|------|--------|------|------|
| h2标题 | Oswald | 700 | 1.7rem | 大写 |
| h3副标题 | Oswald | 600 | 1.15rem | 大写 |
| 正文段落 | Open Sans | 400 | 1rem | 普通 |
| 眉毛标签 | Oswald | 700 | 0.72rem | 大写 |
| CTA按钮 | Oswald | 700 | 1rem | 大写 |
| 统计数字 | Oswald | 700 | 1.6rem | 普通 |
| 统计标签 | Oswald | — | 0.68rem | 大写 |

---

### 第8部分：FurrBudd发布前检查清单

在ClawdBot发布任何新文章之前，需要验证以下内容：
- 文件以`<link rel="stylesheet">`开头，用于加载Google Fonts（禁止使用`@import`）
- 所有的CSS都放在`<link>`和`<div class="fb-article">`之间的单个`<style>`块中
- CSS与第2部分中的样式表完全相同
- 每个`<svg>`都具备三层保护：CSS重置、`width="18" height="18"`属性、带有`!important`的内联样式
- 所有的文本CSS规则都使用`!important`来设置`font-size`、`line-height`、`color`、`font-family`
- 两个`.callout``div`都使用带有硬编码十六进制颜色的内联样式
- `.final-verdict``div`使用带有硬编码十六进制颜色的内联样式
- 深色部分中的每个文本元素都使用带有硬编码颜色的内联样式
- 所有的联盟链接都使用`target="_blank" rel="noopener nofollow sponsored"`
- 页底有联盟披露信息
- 常见问题解答项使用`onclick="this.classList.toggle('open')`事件
- 星形评分使用`<span class="star-icon">`上的CSS `mask`效果（不是SVG）
- 在`@media (max-width: 640px)`条件下，将总结表格和优点与缺点表格折叠为单列显示
- 文章部分的顺序与第6部分完全一致
- 用户提供的联盟链接被放置在所有的CTA按钮、文本链接、价格表和最终总结中

---

# 技能2：编辑联盟用户体验策略

ClawdBot利用这些策略来规划网站架构、撰写文章内容，并为FurrBudd做出编辑决策。

---

### 第9部分：竞争格局分析

#### 分析的网站

1. **The Spruce Pets** (thesprucepets.com) —— 杂志风格的编辑内容
2. **NYT Wirecutter — Pets** (nytimes.com/wirecutter/pets/) —— 新闻风格的测试权威
3. **Dog Food Advisor** (dogfoodadvisor.com) —— 专家博客/资源中心

#### 核心模式

这三个网站都遵循相同的转化漏斗模型：

```
Trust → Education → Recommendation → Affiliate Click
```

**注意：**  
产品永远不会成为焦点 —— **专家意见**才是重点。产品仅会在编辑判断、测试方法和专家验证的背景下出现。ClawdBot在制作FurrBudd的内容时必须始终遵循这一模式。

---

### 第10部分：首页与导航原则

#### 首页必备元素

1. **以编辑内容为主，而不是产品列表** —— 展示区上方不得有任何商品信息
2. **量化可信度的横幅** —— “X款产品已评测”这样的信息可以立即建立信任
3. **首页上的专家团队介绍** —— 显示专家的资质信息
4. **方法论预览** —— 在深入介绍页面之前，先简要说明“我们的评估方式”
5. **关于产品召回/安全性的实用信息** —— 召回警告可以促进电子邮件注册，并提升品牌保护形象

#### 导航结构

- **首先按宠物类型分类**（狗、猫等），而不是按产品类别分类
- 深度分类：按品种、健康状况、生命阶段、成分分类
- “最佳[产品]”列表作为主要导航选项
- 召回/安全性信息作为一级导航项

---

### 第11部分：评论文章内容策略

#### 文章标题格式（经过验证的格式）

- “[N]款最佳[产品]，经过测试和评测”
- “[年份]年[产品名称]评测：值得购买吗？”
- “针对[特定需求]的最佳[产品] —— 专家推荐”

#### 文章结构（编辑最佳实践）

ClawdBot生成的每篇文章都应该包括：
1. **顶部的“最佳推荐”摘要** —— 便于用户快速浏览
2. **类别标签** —— 如“最佳整体”、“最佳预算”、“最适合[特定需求]”
3. **优点与缺点结构** —— 每个产品都必须有详细的缺点说明
4. **测试方法论部分** —— 说明我们的评估方式
5. **作者与专家署名** —— 显示作者的资质信息
6. **规格表格** —— 用于产品对比的详细数据
7. **“为什么信任我们”部分** —— 说明我们的评估依据
8. **“适合谁”框架** —— 在销售之前明确读者的需求

#### 建立信任的内容元素

| 元素 | ClawdBot的实现方式 |
|---------|------------------------|
| 如实的缺点说明 | 每个产品都必须包含3条以上的真实缺点，并使用“值得了解”的表述 |
| 测试来源的说明 | 明确说明产品的评估方式。如果基于标签进行评估，也要如实说明 |
| 专家署名 | 使用“FurrBudd编辑团队”的署名；如有兽医评价，也要一并展示 |
| 独立性声明 | 每篇文章都应披露联盟关系，并声明“我们不接受品牌方的资助” |
| 时效性提示 | 包括文章的发布/更新日期。在“最佳推荐”列表中添加每月的日期戳 |

---

### 第12部分：呼叫行动（CTA）语言规则

#### ClawdBot绝对不能使用的词语
- “立即购买”
- “加入购物车”
- “购物”（除非在最终总结中的CTA中，例如“在Amazon上购买[产品]”）
- “购买”

#### 批准的CTA短语

| 语句 | 使用场景 |
|--------|---------|
| “在Amazon上查看价格” | 主要的CTA按钮 |
| “在Amazon上查看” | 辅助/内联链接 |
| “[价格]在Amazon上” | 价格相关的链接 |
| “[尺寸] —— 最佳价值” | 价格表中的高亮行 |
| “在Amazon上购买[产品]” | 仅用于最终总结中的CTA |

---

### 第13部分：联盟链接的处理方式

#### ClawdBot必须遵循的链接放置规则

1. 主要的呼叫行动按钮（位于总结框之后）
2. 正文段落中的2-3个上下文文本链接（在产品名称、关键优势描述中）
3. 价格表中的“最佳价值”行
4. 最终总结中的呼叫行动链接和正文链接
5. 任何时候，如果没有足够的文本内容，显示的CTA按钮不得超过一个

---

### 第14部分：信任信号的优先级

根据影响程度排序，ClawdBot应优先维护以下信任信号，并计划在未来的版本中逐步实现：

| 优先级 | 信号 | 状态 |
|----------|--------|--------|
| 1 | 每篇文章中的联盟披露信息 | **当前已启用** |
| 2 | 每个产品的诚实缺点说明（优点与缺点） | **当前已启用** |
| 3 | 带有“FurrBudd编辑团队”署名的作者信息 | **当前已启用** |
| 4 | 每篇文章的发布/更新日期 | **当前已启用** |
| 5 | 透明的评分方法论页面 | 计划在未来实现 |
| 6 | 有资质的专家评审委员会 | 计划在未来实现 |
| 7 | 每篇评论中的“我们的评估方式”部分 | 计划在未来实现 |
| 8 | “最佳推荐”列表中的每月日期戳 | 计划在未来实现 |
| 9 | 用户评论/社区功能 | 计划在未来实现 |
| 10 | 学术/科学来源的引用 | 计划在未来实现 |

---

### 第15部分：品牌语言指南

ClawdBot在编写FurrBudd的内容时必须遵循以下规则：

- 使用第三人称编辑语气（例如“FurrBudd推荐...”）或包容性的第一人称复数形式（例如“我们发现...”）
- 绝不使用过于推销的语言
- 如实承认产品的局限性和缺点
- 从狗的需求出发来推荐产品，而不是仅仅强调产品的特点
- 使用数据点和具体事实，而不是笼统的赞美
- 使网站看起来像一本杂志，而不是一个购物网站

---

### 第16部分：SEO内容指南

#### 目标字数

- 单个产品评论：1,500字以上
- “最佳推荐”列表：2,500字以上
- 信息性/教育性文章：1,000字以上

#### 关键词布局

- H1标题中包含主要关键词
- 前100个单词中包含主要关键词
- H2和H3标题中包含次要关键词
- 正文中自然分布关键词
- 元描述和URL路径中包含主要关键词

#### 内部链接策略

- 每篇文章都链接到2-3篇相关的FurrBudd文章
- “最佳推荐”列表链接到相应的产品评论
- 单个评论链接回相关的“最佳推荐”列表

---

### 第17部分：编辑内容发布前的检查清单

ClawdBot在完成技术检查（第8部分）的同时，还需要验证以下内容：
- 文章长度达到1,500字以上（针对单个产品评论）
- 标题遵循经过验证的格式（第11部分）
- 至少列出3条真实的缺点；避免编写夸大的评论
- CTA语言使用官方批准的短语（第12部分）
- 联盟链接放置在所有规定的位置（第13部分）
- 包含作者署名和发布日期
- 内容应体现编辑推荐的风格，而不是销售文案
- 不使用“立即购买”、“加入购物车”或“购物”等语言（除了最终总结中的CTA）
- 从狗的角度来评估产品，而不仅仅是产品特点
- 标题、前100个单词以及至少2个H2标题中都包含主要关键词
- 常见问题解答部分包含5个以上问题，并自然地使用关键词

---

# 技能3：AI货币化网站构建器

该技能最初由Manus AI开发。当用户请求创建AI货币化 landing 页面或React网站时，ClawdBot会使用这个框架。

**实时参考链接：** https://bcdluqyt.manussite.space

---

### 第18部分：项目设置

```bash
npx create-react-app ai-money-website
cd ai-money-website

npm install @radix-ui/react-slot @radix-ui/react-separator lucide-react class-variance-authority clsx tailwind-merge framer-motion
npm install -D tailwindcss @tailwindcss/vite tw-animate-css
```

---

### 第19部分：文件结构

```
ai-money-website/
├── public/
├── src/
│   ├── assets/          # Images
│   ├── components/
│   │   └── ui/         # UI components
│   ├── App.jsx         # Main application
│   ├── App.css         # Luxury styling
│   ├── index.css       # Global styles
│   └── main.jsx        # Entry point
├── index.html          # SEO-optimized HTML
├── package.json        # Dependencies
└── vite.config.js      # Vite configuration
```

---

### 第20部分：index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Money Mastery - 25+ Proven Ways to Make Money Online with Artificial Intelligence</title>
    <meta name="description" content="Discover 25+ proven strategies to make money online with AI. From AI content creation to automated businesses, learn how to generate income using artificial intelligence tools and technologies." />
    <meta name="keywords" content="make money with AI, artificial intelligence business, AI monetization, online income AI, AI side hustle, generative AI profit, AI automation business, machine learning income" />
    <meta name="author" content="AI Money Mastery" />
    <meta name="robots" content="index, follow" />
    <meta property="og:title" content="AI Money Mastery - 25+ Proven Ways to Make Money Online with AI" />
    <meta property="og:description" content="Discover proven strategies to generate income using artificial intelligence. Learn from industry experts and start your AI-powered business today." />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://ai-money-mastery.com" />
    <meta property="og:image" content="/src/assets/ai_business_hero.webp" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="AI Money Mastery - Make Money Online with AI" />
    <meta name="twitter:description" content="25+ proven ways to generate income using artificial intelligence" />
    <meta name="twitter:image" content="/src/assets/ai_business_hero.webp" />
    <link rel="canonical" href="https://ai-money-mastery.com" />
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "AI Money Mastery",
      "description": "Learn proven strategies to make money online with artificial intelligence",
      "url": "https://ai-money-mastery.com",
      "author": { "@type": "Organization", "name": "AI Money Mastery" },
      "publisher": { "@type": "Organization", "name": "AI Money Mastery" }
    }
    </script>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

---

### 第21部分：核心配置文件

#### package.json

```json
{
  "name": "ai-money-website",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "@radix-ui/react-slot": "^1.2.2",
    "@radix-ui/react-separator": "^1.1.6",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "framer-motion": "^12.15.0",
    "lucide-react": "^0.510.0",
    "react": "^19.1.0",
    "react-dom": "^19.1.0",
    "tailwind-merge": "^3.3.0",
    "tailwindcss": "^4.1.7"
  },
  "devDependencies": {
    "@eslint/js": "^9.25.0",
    "@types/react": "^19.1.2",
    "@types/react-dom": "^19.1.2",
    "@vitejs/plugin-react": "^4.4.1",
    "@tailwindcss/vite": "^4.1.7",
    "eslint": "^9.25.0",
    "eslint-plugin-react-hooks": "^5.2.0",
    "eslint-plugin-react-refresh": "^0.4.19",
    "globals": "^16.0.0",
    "tw-animate-css": "^1.2.9",
    "vite": "^6.3.5"
  }
}
```

#### vite.config.js

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

#### src/main.jsx

```jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

---

### 第22部分：全局样式（src/index.css）

```css
@import "tailwindcss";
@import "tw-animate-css";

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 0 0% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    --secondary: 0 0% 96.1%;
    --secondary-foreground: 0 0% 9%;
    --muted: 0 0% 96.1%;
    --muted-foreground: 0 0% 45.1%;
    --accent: 0 0% 96.1%;
    --accent-foreground: 0 0% 9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 89.8%;
    --input: 0 0% 89.8%;
    --ring: 0 0% 3.9%;
    --chart-1: 12 76% 61%;
    --chart-2: 173 58% 39%;
    --chart-3: 197 37% 24%;
    --chart-4: 43 74% 66%;
    --chart-5: 27 87% 67%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    --card: 0 0% 3.9%;
    --card-foreground: 0 0% 98%;
    --popover: 0 0% 3.9%;
    --popover-foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 0 0% 9%;
    --secondary: 0 0% 14.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 0 0% 14.9%;
    --muted-foreground: 0 0% 63.9%;
    --accent: 0 0% 14.9%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 14.9%;
    --input: 0 0% 14.9%;
    --ring: 0 0% 83.1%;
    --chart-1: 220 70% 50%;
    --chart-2: 160 60% 45%;
    --chart-3: 30 80% 55%;
    --chart-4: 280 65% 60%;
    --chart-5: 340 75% 55%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

---

### 第23部分：用户界面组件

#### src/lib/utils.js

```javascript
import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}
```

#### src/components/ui/button.jsx

```jsx
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

const Button = React.forwardRef(({ className, variant, size, asChild = false, ...props }, ref) => {
  const Comp = asChild ? Slot : "button"
  return (
    <Comp
      className={cn(buttonVariants({ variant, size, className }))}
      ref={ref}
      {...props}
    />
  )
})
Button.displayName = "Button"

export { Button, buttonVariants }
```

#### src/components/ui/card.jsx

```jsx
import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("rounded-xl border bg-card text-card-foreground shadow", className)} {...props} />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("font-semibold leading-none tracking-tight", className)} {...props} />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("flex items-center p-6 pt-0", className)} {...props} />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
```

#### src/components/ui/badge.jsx

```jsx
import * as React from "react"
import { cva } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default: "border-transparent bg-primary text-primary-foreground shadow hover:bg-primary/80",
        secondary: "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive: "border-transparent bg-destructive text-destructive-foreground shadow hover:bg-destructive/80",
        outline: "text-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

function Badge({ className, variant, ...props }) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}

export { Badge, badgeVariants }
```

#### src/components/ui/separator.jsx

```jsx
import * as React from "react"
import * as SeparatorPrimitive from "@radix-ui/react-separator"
import { cn } from "@/lib/utils"

const Separator = React.forwardRef(
  ({ className, orientation = "horizontal", decorative = true, ...props }, ref) => (
    <SeparatorPrimitive.Root
      ref={ref}
      decorative={decorative}
      orientation={orientation}
      className={cn(
        "shrink-0 bg-border",
        orientation === "horizontal" ? "h-[1px] w-full" : "h-full w-[1px]",
        className
      )}
      {...props}
    />
  )
)
Separator.displayName = SeparatorPrimitive.Root.displayName

export { Separator }
```

---

### 第24部分：开发命令

```bash
npm install       # Install dependencies
npm run dev       # Start development server
npm run build     # Build for production
npm run preview   # Preview production build
```

---

### 第25部分：定制指南

当ClawdBot构建或修改AI货币化网站时，需要执行以下操作：
1. **内容**：编辑`App.jsx`中的`aiMethods`、`marketStats`和`successStories`数组
2. **样式**：修改`App.css`中的豪华风格设置
3. **SEO**：更新`index.html`中的元标签
4. **图片**：替换`src/assets/`文件夹中的图片
5. **颜色**：调整`index.css`和`App.css`中的CSS变量
6. **组件**：创建新组件并在`App.jsx`中导入它们
7. **动画**：使用Framer Motion来实现自定义动画

该网站具有完全的响应式设计：适用于桌面（1200px以上）、平板电脑（768-1199px）和手机（320-767px）。

---

*这些技能整合在一个文件中，专为ClawdBot设计。在furrbudd.com上经过实际测试，并参考了顶级宠物类网站的编辑内容策略进行了优化，同时基于Manus AI的React框架进行构建。*