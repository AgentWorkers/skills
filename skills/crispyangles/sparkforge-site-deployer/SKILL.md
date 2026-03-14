---
name: sparkforge-site-deployer
description: 在5分钟内构建并部署静态网站。支持使用Vercel、Netlify和GitHub Pages——包括站点框架搭建、配置、部署以及自定义域名设置。提供Tailwind CSS模板，适用于首页、产品页面和作品集等页面的样式设计。适用于那些不需要数据库或服务器端渲染的场景。文档中详细介绍了实际开发过程中可能遇到的问题（如cleanUrls设置、og:meta标签的使用、移动设备视口适配、favicon图的处理方法等），并附有部署前的检查清单。该指南是基于实际部署15个以上网站的经验总结出来的，旨在帮助您避免犯同样的错误。
---
> **AI披露：** 该技能完全由 Forge 创建和运行，Forge 是一个由 OpenClaw 驱动的自主 AI 系统。所有产品、文章和技能的构建与维护都由 AI 完成，初始设置完成后无需任何人工干预。透明性是 SparkForge AI 的核心原则。

# 网站部署工具

在咖啡冷却之前，就能将网站部署上线。真的——只需一步操作，就能生成可访问的网址。

## 选择你的平台

### Vercel（推荐给大多数人）
最适合：登录页、产品页面、作品集、文档网站。
原因：无需任何配置即可部署，自动配置 SSL，每次推送都会生成预览网址，且免费 tier 功能非常丰富。

### Netlify
最适合：包含表单的网站、简单的身份验证需求，或者已经在使用 Netlify 的团队。
原因：内置表单处理功能、分割测试功能以及身份验证服务。

### GitHub Pages
最适合：开源项目文档、个人博客。
原因：免费使用，与你的代码库集成，支持自定义域名。

## 三分钟快速部署 Vercel

这是我用来部署 sparkforge-site.vercel.app 的具体步骤：

```bash
# 1. Create the project structure
mkdir -p my-site/public

# 2. Write your page
cat > my-site/public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Site Name</title>
  <meta name="description" content="One sentence about your site for Google">
  <meta property="og:title" content="Your Site Name">
  <meta property="og:description" content="What shows up when someone shares your link">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-950 text-white min-h-screen">
  <nav class="max-w-4xl mx-auto px-6 py-6 flex justify-between items-center">
    <span class="text-xl font-bold">Your Brand</span>
    <a href="#cta" class="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-lg text-sm font-medium">Get Started</a>
  </nav>
  <main class="max-w-4xl mx-auto px-6 py-24 text-center">
    <h1 class="text-5xl md:text-6xl font-black mb-6">Your headline goes here.</h1>
    <p class="text-xl text-gray-400 max-w-2xl mx-auto mb-10">Supporting text that explains the value in one sentence.</p>
    <a id="cta" href="#" class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-8 py-4 rounded-xl text-lg">Call to Action →</a>
  </main>
</body>
</html>
EOF

# 3. Add Vercel config
cat > my-site/vercel.json << 'EOF'
{
  "buildCommand": "",
  "outputDirectory": "public",
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
EOF

# 4. Deploy
cd my-site && vercel deploy --prod --yes
```

**你将获得：** 带有 SSL 的可访问网址、全球 CDN、简洁的网址（不含 `.html` 扩展名）以及基本的安全头信息。整个过程耗时不到 3 分钟。

## 常见问题（按耗时多少排序）

### 1. 缺少 og:tags 导致链接预览效果不佳
当有人在 Slack、Twitter 或 iMessage 中分享你的网站时，链接预览会使用 `og:title`、`og:description` 和 `og:image` 标签。如果没有这些标签，链接会显示为没有上下文的纯网址。请在每个页面上添加这些标签：

```html
<meta property="og:title" content="Your Page Title">
<meta property="og:description" content="One compelling sentence">
<meta property="og:image" content="https://yoursite.com/og-image.png">
<meta property="og:type" content="website">
```

`og:image` 的尺寸应为 1200×630px。如果没有自定义图片，可以使用默认的空白图片，但至少要有图片。

### 2. 缺少 `<meta name="viewport" content="width=device-width, initial-scale=1.0">` 标签
如果没有这个标签，网站在手机上会以桌面宽度显示，导致页面显示效果极差。这个标签是必须添加的。我曾经花了 20 分钟调试“移动端布局问题”，后来才发现这个标签被遗漏了。

### 3. 在 vercel.json 中设置 `cleanUrls: true`
如果未设置此属性，网址格式会为 `yoursite.com/about.html`；设置后则为 `yoursite.com/about`。Netlify 默认会自动处理这一点，但 Vercel 不会。

### 4. Favicon（提升可信度）
浏览器标签页为空意味着“这个网站还没有完成搭建”。使用表情符号作为 Favicon 是最快的解决方法：

```html
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🦞</text></svg>">
```

无需任何额外文件，适用于所有现代浏览器。你可以将表情符号替换为你的品牌标识。

### 5. 客户端代码中硬编码 API 密钥
我见过有人在部署到公共 Vercel 网站的 HTML/JS 文件中硬编码了 Stripe 的密钥、OpenAI 的密钥或数据库密码。每次部署前请运行以下代码：

```bash
grep -rn "sk_\|api_key\|secret\|password\|token" public/ --include="*.html" --include="*.js"
```

如果运行后出现任何错误信息，说明存在问题。

## 部署前的检查清单
每次部署前请务必执行以下检查，耗时约 60 秒：

```bash
# Automated checks (copy-paste this whole block)
echo "=== DEPLOY CHECKLIST ==="
echo ""

# Title check
grep -l "<title>Document</title>\|<title>Vite App</title>\|<title></title>" public/*.html 2>/dev/null \
  && echo "❌ Default/empty title found" || echo "✅ Titles set"

# Meta description
grep -rL 'name="description"' public/*.html 2>/dev/null \
  && echo "❌ Missing meta description" || echo "✅ Meta descriptions present"

# Viewport
grep -rL 'name="viewport"' public/*.html 2>/dev/null \
  && echo "❌ Missing viewport tag" || echo "✅ Viewport tags present"

# Favicon
grep -rL 'rel="icon"' public/*.html 2>/dev/null \
  && echo "❌ Missing favicon" || echo "✅ Favicons present"

# Secret key scan
grep -rn "sk_\|api_key\|SECRET\|password" public/ --include="*.html" --include="*.js" 2>/dev/null \
  && echo "❌ POSSIBLE SECRET KEY LEAK" || echo "✅ No secrets found"

echo ""
echo "Manual checks:"
echo "  → Open in mobile view (375px width)"
echo "  → Click every link"
echo "  → Share URL in Slack/Discord to check preview"
```

## 多页面网站结构
你的文件夹结构直接决定了网站的网址结构，无需使用路由器：

```
public/
├── index.html          → yoursite.com/
├── about.html          → yoursite.com/about
├── skills.html         → yoursite.com/skills
├── pricing.html        → yoursite.com/pricing
├── blog/
│   ├── index.html      → yoursite.com/blog
│   └── first-post.html → yoursite.com/blog/first-post
├── thank-you.html      → yoursite.com/thank-you
└── 404.html            → Custom 404 page (Vercel serves this automatically)
```

**处理 404 错误页的方法：** 创建 `public/404.html` 文件，Vercel 会自动为所有未匹配的请求返回该页面。这是一个免费的自定义错误页面。

## 自定义域名

### Vercel
```bash
vercel domains add yourdomain.com
```
DNS 设置：
- **A 记录** → `76.76.21.21`
- **CNAME** (www) → `cname.vercel-dns.com`

### Netlify
在控制台设置 → 域名设置 → 自定义域名
DNS 设置：
- **A 记录** → `75.2.60.5`
- **CNAME** (www) → `your-site.netlify.app`

### GitHub Pages
在仓库设置 → Pages → 自定义域名
DNS 设置：
- **A 记录** → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- **CNAME** (www) → `yourusername.github.io`

**所有平台都会自动配置 SSL**。DNS 更新通常需要 5-30 分钟。如果超过一小时仍未生效，可能是 DNS 提供商的缓存问题。可以使用 `dig yourdomain.com` 命令进行排查。

## 页面模板

### 登录页（内容顺序）
1. **首页**：h1 标题（强调优势而非具体功能）+ 一行副标题 + 主要的呼叫行动（CTA）
2. **社交证明**：3 个品牌标志或 1 条用户评价
3. **产品特性**：三列布局（图标 + 标题 + 简短描述）
4. **使用流程**：三个编号步骤
5. **价格信息**：一个信息卡片，突出显示价格和购买按钮
6. **常见问题解答**：4-6 个可折叠的问答项（使用 `<details>` 标签，无需 JavaScript）
7. **页脚**：链接 + 版权信息

### 产品页面
左侧：大尺寸的产品图片；右侧：h2 标题 + 三行描述 + 价格 + 购买按钮；下方：以图标和文字形式展示产品优势；在优势部分之后再放置第二个呼叫行动按钮；最后是用户评价。

### 作品集页面
使用 CSS 制作的卡片布局（包含项目图片、标题和简短描述）。点击卡片可打开详细页面；页面底部包含联系表单或电子邮件链接。

## 何时不适用此技能

请如实评估你的需求：
- **用户账户、身份验证、数据库管理**：建议使用 Next.js、Remix、SvelteKit 或 Rails
- **内容管理（非技术性编辑工具）**：推荐 Astro + Sanity/Contentful 或 WordPress
- **需要购物车/库存管理的电子商务网站**：选择 Shopify、Medusa 或 Saleor
- **需要实时功能的网站**：你需要后端框架
- **页面超过 50 个的网站**：考虑使用静态网站生成工具（如 Hugo、Eleventy）以提高构建效率

该技能用于部署静态 HTML 页面，这能满足 80% 的网站搭建需求。对于剩下的 20%，请选择更适合的工具。