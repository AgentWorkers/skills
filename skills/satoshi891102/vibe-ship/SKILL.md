---
name: vibe-ship
description: 将一个完整的Web应用程序从构思阶段快速开发并部署到线上。适用于用户提出“为我开发一个应用程序”、“实现这个想法”、“快速开发”、“部署这个应用程序”等需求时，适用于任何需要构建和部署的消费类应用程序、工具或网站。该流程包括需求验证、技术栈选择、代码开发、测试，以及将应用程序部署到Vercel或GitHub Pages平台。
---

# Vibe Ship

在一个工作日内，将一个从简单想法出发的、可运行的Web应用从开发阶段部署到生产环境。无需繁琐的规划过程，也无需使用本地服务器（localhost）。必须提供一个公共URL，否则就算没有完成。

## 工作流程

### 第1步：验证（最多2分钟）

在编写任何代码之前，回答以下四个问题：

1. **你能用一句话解释这个应用的价值吗？** 如果不能，说明这个想法还不够清晰——请用户进一步说明。
2. **核心功能是否可行？** 使用现有的工具（除非用户拥有付费API的密钥，否则不使用这些API），这个功能在技术上是否可以实现？
3. **谁会使用这个应用？** 需要具体说明。不能笼统地说“所有人”。
4. **这个应用存在什么致命的缺陷吗？** 要主动尝试找出这些问题；如果找不到问题，再继续开发。

如果任何问题的答案都不明确，就告诉用户并建议调整方向。不要在存在缺陷的概念上继续开发。

### 第2步：选择技术栈

**推荐的技术栈（90%的应用）：**
- Next.js 14及以上版本（用于应用路由管理）
- Tailwind CSS
- TypeScript
- 通过Vercel进行部署

**在以下情况下可以选择其他技术栈：**
- 如果是静态网站且不需要后端服务 → 使用纯HTML/CSS/JS → 通过GitHub Pages部署
- 需要数据库 → 使用Supabase（免费版本）
- 需要身份验证功能 → 使用NextAuth或Clerk
- 需要AI功能 → 使用本地推理技术或用户提供的API密钥（切勿硬编码密钥）

**绝对不要使用：**
- Create React App（已经过时）
- 从头开始配置Webpack
- 对于简单的应用使用复杂的-state管理库（例如Redux）

### 第3步：逐步开发

**第1轮迭代：实现核心功能：**
```
1. Initialize project: npx create-next-app@latest [name] --typescript --tailwind --app --src-dir
2. Build the ONE core feature that makes this app valuable
3. Test it locally: npm run dev
4. Verify it actually works in the browser
```

**第2轮迭代：优化界面美观：**
```
1. Dark mode by default (users expect it)
2. Mobile responsive (test at 375px width)
3. Loading states, empty states, error states
4. Micro-interactions (hover effects, transitions)
5. No default Tailwind look — intentional design choices
```

**第3轮迭代：增强应用稳定性：**
```
1. Error handling on all external calls
2. Input validation
3. Environment variables for any secrets (never hardcode)
4. Meta tags: title, description, og:image
5. Favicon
```

### 第4步：部署

**推荐使用Vercel：**
```bash
# If Vercel CLI available:
cd [project-dir]
vercel --yes --prod

# If not, push to GitHub and connect:
git init && git add . && git commit -m "Ship it"
gh repo create [name] --public --push
# Then deploy via Vercel dashboard or CLI
```

**仅适用于静态网站的情况：使用GitHub Pages：**
```bash
git init && git add . && git commit -m "Ship it"
gh repo create [name] --public --push
# Enable Pages in repo settings → deploy from main branch
```

**部署完成后：**
1. 确认公共URL能够正确加载。
2. 在移动设备上测试应用的响应性。
3. 对核心功能进行端到端的测试。
4. 将URL分享给用户。

### 第5步：项目交付后的工作

1. 为所有代码提交代码，并附上清晰的提交信息。
2. 创建README.md文件，内容包括：应用的功能、技术栈、以及公共URL。
3. 向用户报告应用的详细信息，包括公共URL、已实现的功能以及任何已知的局限性。

## 质量检查清单

在宣布项目“完成并部署”之前，必须验证以下所有内容：
- [ ] 公共URL可以访问（不能使用localhost）
- [ ] 核心功能能够正常运行。
- [ ] 应用在桌面和移动设备上的显示效果符合设计意图。
- [ ] 没有控制台错误。
- [ ] 没有硬编码的敏感信息（如API密钥）。
- [ ] 页面有合适的标题和描述。
- [ ] 错误情况得到了妥善处理（当应用出问题时，用户能够得到相应的提示）。
- [ ] 在加载过程中有适当的加载提示（避免出现空白屏幕）。

## 避免的错误做法：
- **过度设计**：对于MVP（最小可行产品）来说，不要添加不必要的身份验证、数据库或分析功能。只需实现核心价值即可。
- **使用默认的Tailwind样式**：如果应用看起来和其他使用Tailwind的网站一样，就需要重新设计，以体现独特的风格。
- **使用本地服务器进行部署**：仅仅因为在自己的机器上可以运行，并不意味着应用已经准备好部署到生产环境。
- **功能蔓延**：用户只提出了一个需求，就立即实现它；可以在应用上线后再根据用户反馈决定是否添加额外功能。
- **每一步都征求用户许可**：要果断做出决策，然后立即部署应用，并在应用上线后收集用户的反馈。

## 开发速度目标

| 应用复杂度 | 预计开发时间 | 示例 |
|----------------|-------------|---------|
| 简单的登录页面 | 30分钟 | 产品等待列表页面 |
| 单功能工具 | 1-2小时 | 颜色调色板生成器、计算器 |
| 多页面应用 | 2-4小时 | 仪表盘、内容管理工具 |
| 完整的产品 | 4-8小时 | 带有身份验证和数据库功能的SaaS MVP |

## 常用开发模式

**Next.js中的API路由配置：**
```typescript
// src/app/api/[endpoint]/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    // ... logic
    return NextResponse.json({ success: true, data: result });
  } catch (error) {
    return NextResponse.json({ error: 'Something went wrong' }, { status: 500 });
  }
}
```

**全局样式设置（globals.css）：**
```css
:root {
  --background: #0a0a0a;
  --foreground: #ededed;
}
body {
  background: var(--background);
  color: var(--foreground);
}
```

**响应式布局设计：**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```