---
name: ai-labs-builder
description: **AI Labs Builder** – 用于创建现代网站、AI应用程序、仪表板以及自动化工作流程的工具。该平台提供了一个统一的系统，支持使用 Next.js、TypeScript、Tailwind CSS、shadcn/ui 以及 MCP（Machine Learning Platform）等技术来构建可投入生产的项目。适用于新项目的创建、AI功能的开发、仪表板的设计以及工作流程的自动化。支持的触发命令包括：“create website”（创建网站）、“build ai app”（构建 AI 应用程序）、“make dashboard”（制作仪表板）以及任何与项目创建相关的操作。
version: "1.0.0"
user-invocable: true
triggers:
  - ai labs
  - create website
  - build ai app
  - make dashboard
  - setup workflow
  - create project
  - build application
  - ai agent
  - chat interface
  - dashboard
  - automation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Node
metadata:
  clawdbot:
    emoji: "🚀"
    config:
      stateDirs: [".ailabs"]
---
# AI Labs Builder

这是一个用于创建现代网站、AI应用程序、仪表盘和工作流的统一系统。

## 快速入门

```bash
# Create a website
ailabs create website my-portfolio --type portfolio

# Create an AI app
ailabs create ai-app my-chatbot --type chat

# Create a dashboard
ailabs create dashboard my-analytics --type analytics

# Create a workflow
ailabs create workflow my-automation --template automation

# Deploy
ailabs deploy my-project --platform vercel
```

## 命令

### 网站创建

```bash
ailabs create website <name> [options]

Options:
  --type <type>      portfolio | saas | blog | ecommerce
  --style <style>    modern | glassmorphism | brutalism | minimal
  --components       Include shadcn/ui components
  --animations       Include Framer Motion animations
  --seo              Include SEO optimization
```

### AI 应用程序

```bash
ailabs create ai-app <name> [options]

Options:
  --type <type>      chat | agent | rag | multimodal
  --provider         openai | claude | gemini | local
  --streaming        Enable streaming responses
  --memory           Enable conversation memory
  --tools            Enable tool calling
```

### 仪表盘

```bash
ailabs create dashboard <name> [options]

Options:
  --type <type>      analytics | admin | personal | monitoring
  --widgets          Include widget system
  --realtime         Enable real-time updates
  --charts           Include chart components
```

### 工作流

```bash
ailabs create workflow <name> [options]

Options:
  --template         automation | integration | pipeline
  --mcp              Include MCP server setup
  --schedule         Add cron scheduling
  --webhook          Add webhook triggers
```

## 项目类型

### 1. 网站

**作品集**
- 带有动画的首页
- 项目展示区
- 技能/经验时间线
- 联系表单
- 博客集成

**SaaS 登录页**
- 功能亮点
- 价格表
- 客户评价
- 行动号召（CTA）区域
- 常见问题（FAQ）折叠面板

**博客**
- 支持 MDX 格式
- 标签/分类
- 搜索功能
- RSS 订阅
- 新闻通讯订阅

### 2. AI 应用程序

**聊天界面**
- 消息历史记录
- 实时响应
- 代码语法高亮显示
- 文件附件
- 语音输入/输出

**AI 代理**
- 自主任务执行
- 工具调用
- 内存管理
- 多步骤推理
- 人工干预机制

**RAG 系统**
- 文档导入
- 向量数据库
- 语义搜索
- 引用来源
- 上下文管理

### 3. 仪表盘

**分析功能**
- 关键绩效指标（KPI）卡片
- 图表（折线图、条形图、饼图）
- 日期范围选择器
- 数据导出功能
- 实时更新

**管理员面板**
- 用户管理
- 基于角色的访问控制
- 创建/读取/更新/删除（CRUD）操作
- 审计日志
- 设置面板

**个人仪表盘**
- 天气小部件
- 日历集成
- 任务管理
- 笔记/快速记录
- 收藏夹

### 4. 工作流

**自动化**
- 定时任务
- 电子邮件通知
- 数据处理
- 报告生成

**集成**
- API 连接
- Webhook 处理
- 数据同步
- 事件触发

**管道**
- 持续集成/持续部署（CI/CD）自动化
- 测试工作流
- 部署管道
- 质量检查

## 设计系统

### 颜色方案

```css
/* Modern */
--primary: #6366f1;
--secondary: #8b5cf6;
--accent: #ec4899;

/* Glassmorphism */
--glass-bg: rgba(255, 255, 255, 0.05);
--glass-border: rgba(255, 255, 255, 0.1);
--glass-blur: blur(20px);

/* Brutalism */
--brutal-black: #000;
--brutal-white: #fff;
--brutal-accent: #ff00ff;
```

### 字体样式

- **标题**: Inter, Geist 或 JetBrains Mono
- **正文**: Inter 或 system-ui
- **代码**: JetBrains Mono 或 Fira Code

### 组件

所有项目均包含以下组件：
- 按钮类型（主要按钮、次要按钮、透明按钮、轮廓按钮）
- 卡片（默认样式、悬停效果、玻璃材质样式）
- 表单（输入框、文本区域、下拉菜单、复选框、单选框）
- 导航元素（页头、侧边栏、面包屑导航）
- 反馈提示（弹出通知、警告信息、模态窗口、工具提示）
- 数据展示元素（表格、分页功能、标签页）

## AI 集成

### OpenAI

```typescript
import { OpenAI } from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Streaming chat
const stream = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: prompt }],
  stream: true,
});
```

### Claude

```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const message = await anthropic.messages.create({
  model: 'claude-3-opus-20240229',
  max_tokens: 1024,
  messages: [{ role: 'user', content: prompt }],
});
```

### 向量数据库（Pinecone/Memory）

```typescript
import { Pinecone } from '@pinecone-database/pinecone';

const pc = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY,
});

// Store embeddings
await index.upsert([{
  id: '1',
  values: embedding,
  metadata: { text: content }
}]);
```

## 部署方案

### Vercel（推荐）

```bash
ailabs deploy my-project --platform vercel
```

**特点**：
- 自动 Git 集成
- 部署预览功能
- 边缘计算（Edge Computing）支持
- 分析数据功能

### Netlify

```bash
ailabs deploy my-project --platform netlify
```

**特点**：
- 基于 Git 的部署方式
- 分支预览功能
- 表单处理功能
- 边缘计算支持

### GitHub Pages

```bash
ailabs deploy my-project --platform github
```

**特点**：
- 免费托管服务
- 支持自定义域名
- Jekyll 框架支持
- 可集成第三方插件（Actions）

## 最佳实践

### 性能优化
- 使用 Next.js 的 Image 组件
- 实现懒加载技术
- 通过 next/font 优化字体显示
- 使用 React Server Components 提升性能

### SEO 最佳实践
- 在 `next/head` 文件中添加元标签
- 生成站点地图（Sitemap）
- 配置 robots.txt 文件
- 提供结构化数据

### 安全性
- 使用环境变量进行配置
- 对用户输入进行验证
- 实施 CSRF 防护机制
- 遵循内容安全策略（Content Security Policy）

### 可访问性优化
- 添加 ARIA 标签以提高可访问性
- 支持键盘导航
- 保持适当的颜色对比度
- 支持屏幕阅读器

## 示例

### 创建作品集

```bash
ailabs create website portfolio \
  --type portfolio \
  --style glassmorphism \
  --components \
  --animations \
  --seo
```

### 创建 AI 聊天机器人

```bash
ailabs create ai-app chatbot \
  --type chat \
  --provider openai \
  --streaming \
  --memory
```

### 创建分析仪表盘

```bash
ailabs create dashboard analytics \
  --type analytics \
  --widgets \
  --realtime \
  --charts
```

### 创建自动化工作流

```bash
ailabs create workflow daily-report \
  --template automation \
  --mcp \
  --schedule "0 9 * * *"
```

## 与其他工具的集成

- **mcp-workflow**: 用于高级工作流自动化
- **gcc-context**: 用于项目版本的版本控制
- **agent-reflect**: 用于持续改进流程

## 资源链接

- [Next.js 文档](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com)
- [OpenAI API](https://platform.openai.com/docs)
- [MCP 规范](https://modelcontextprotocol.io/)