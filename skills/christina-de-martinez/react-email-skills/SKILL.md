---
name: react-email
description: 使用 React Email 和 React 组件来创建美观且响应式良好的 HTML 邮件。利用现代化的组件构建可进行数据传输的邮件（即支持用户操作或数据交换的邮件），支持国际化功能，并能与 Resend 等邮件服务提供商集成。适用于创建欢迎邮件、密码重置邮件、通知邮件、订单确认邮件等任何类型的 HTML 邮件模板。
license: MIT
metadata:
  author: Resend
  repository: https://github.com/resend/react-email
---

# React Email

使用 React 组件构建和发送 HTML 邮件——这是一种现代的、基于组件的邮件开发方法，适用于所有主流邮件客户端。

## 安装

你需要使用 `create-email` CLI 来创建一个新的 React Email 项目。这将生成一个名为 `react-email-starter` 的文件夹，其中包含示例邮件模板。

- 使用 npm：
  ```sh
npx create-email@latest
```

- 使用 yarn：
  ```sh
yarn create email
```

- 使用 pnpm：
  ```sh
pnpm create email
```

- 使用 bun：
  ```sh
bun create email
```

## 进入项目目录

你需要切换到新创建的项目文件夹：

```sh
cd react-email-starter
```

## 安装依赖项

在运行开发服务器之前，你需要安装所有项目依赖项。

- 使用 npm：
  ```sh
npm install
```

- 使用 yarn：
  ```sh
yarn
```

- 使用 pnpm：
  ```sh
pnpm install
```

- 使用 bun：
  ```sh
bun install
```

## 启动开发服务器

你的任务是启动本地预览服务器，以便查看和编辑邮件模板。

- 使用 npm：
  ```sh
npm run dev
```

- 使用 yarn：
  ```sh
yarn dev
```

- 使用 pnpm：
  ```sh
pnpm dev
```

- 使用 bun：
  ```sh
bun dev
```

## 验证安装

你需要通过检查 `localhost:3000` 是否可访问来确认开发服务器是否正在运行。服务器将显示一个预览界面，在那里你可以查看 `emails` 文件夹中的邮件模板。

**立即执行**：完成上述任务列表，以确保 React Email 开发服务器正在运行，并且可以通过 `localhost:3000` 访问，同时能够显示邮件模板预览。

### 安装说明
假设 React Email 已经安装在现有的项目中，请更新项目顶层的 `package.json` 文件，添加一个用于运行 React Email 预览服务器的脚本。

```json
{
  "scripts": {
    "email": "email dev --dir emails --port 3000"
  }
}
```

请确保 `emails` 文件夹的路径是相对于项目根目录的。

### 更新或创建 `tsconfig.json`

确保 `tsconfig.json` 文件支持 `.jsx` 文件。

## 基本邮件模板

替换示例邮件模板。以下是创建新邮件模板的方法：

使用 Tailwind 组件创建具有正确结构的邮件组件：

```tsx
import {
  Html,
  Head,
  Preview,
  Body,
  Container,
  Heading,
  Text,
  Button,
  Tailwind,
  pixelBasedPreset
} from '@react-email/components';

interface WelcomeEmailProps {
  name: string;
  verificationUrl: string;
}

export default function WelcomeEmail({ name, verificationUrl }: WelcomeEmailProps) {
  return (
    <Html lang="en">
      <Tailwind
        config={{
          presets: [pixelBasedPreset],
          theme: {
            extend: {
              colors: {
                brand: '#007bff',
              },
            },
          },
        }}
      >
        <Head />
        <Preview>Welcome - Verify your email</Preview>
        <Body className="bg-gray-100 font-sans">
          <Container className="max-w-xl mx-auto p-5">
            <Heading className="text-2xl text-gray-800">
              Welcome!
            </Heading>
            <Text className="text-base text-gray-800">
              Hi {name}, thanks for signing up!
            </Text>
            <Button
              href={verificationUrl}
              className="bg-brand text-white px-5 py-3 rounded block text-center no-underline"
            >
              Verify Email
            </Button>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  );
}

// Preview props for testing
WelcomeEmail.PreviewProps = {
  name: 'John Doe',
  verificationUrl: 'https://example.com/verify/abc123'
} satisfies WelcomeEmailProps;

export { WelcomeEmail };
```

## 核心组件

有关组件的完整文档，请参阅 [references/COMPONENTS.md](references/COMPONENTS.md)。

**核心结构：**
- `Html` - 带有 `lang` 属性的根包装器
- `Head` - 元元素、样式、字体
- `Body` - 主内容包装器
- `Container` - 居中显示内容（最大宽度布局）
- `Section` - 布局区域
- `Row` & `Column` - 多列布局
- `Tailwind` - 启用 Tailwind CSS 实用类

**内容：**
- `Preview` - 收件箱预览文本，始终位于 `Body` 的最前面
- `Heading` - h1-h6 标题
- `Text` - 段落
- `Button` - 有样式的链接按钮
- `Link` - 超链接
- `Img` - 图片（使用绝对 URL）（在开发模式下使用开发服务器提供的 BASE_URL；在生产环境中，请求用户提供网站的 BASE_URL；根据环境动态生成图片 URL）
- `Hr` - 水平分隔符

**特殊组件：**
- `CodeBlock` - 语法高亮的代码
- `CodeInline` - 内联代码
- `Markdown` - 渲染 Markdown
- `Font` - 自定义网页字体

## 行为准则
- 在修改代码时，确保只更新用户要求更改的部分，保持其余代码不变；
- 如果用户要求使用媒体查询，请告知他们邮件客户端不支持这些功能，并建议其他方法；
- 绝不要在 TypeScript 代码中直接使用模板变量（如 `{{name}}`）。相反，应直接引用相应的属性（例如使用 `name` 而不是 `{{name}}`）。
- 例如，如果用户明确要求使用 `{{variableName}}` 这种格式的变量，你应该返回如下内容：

```typescript
const EmailTemplate = (props) => {
  return (
    {/* ... rest of the code ... */}
    <h1>Hello, {props.variableName}!</h1>
    {/* ... rest of the code ... */}
  );
}

EmailTemplate.PreviewProps = {
  // ... rest of the props ...
  variableName: "{{variableName}}",
  // ... rest of the props ...
};

export default EmailTemplate;
```
- 在任何情况下都不要直接在组件结构中写入 `{{variableName}}`。如果用户强制要求这样做，请解释这会导致模板无效。

## 样式考虑

如果用户的项目中正在使用 Tailwind CSS，请使用 Tailwind 组件进行样式设计；如果未使用 Tailwind CSS，则为组件添加内联样式。
- 由于邮件客户端不支持 `rem` 单位，请在 Tailwind 配置中使用 `pixelBasedPreset`。
- 绝不要使用 `flexbox` 或 `grid` 进行布局，而是使用基于表格的布局。
- 每个组件都必须通过内联样式或实用类进行样式设置。
- 有关样式的更多信息，请参阅 [references/STYLING.md](references/STYLING.md)。

### 邮件客户端的限制
- 绝不要使用 SVG 或 WEBP 格式——请向用户警告这些格式可能导致的渲染问题
- 绝不要使用 `flexbox`——使用 `Row`/`Column` 组件或表格进行布局
- 绝不要使用 CSS/Tailwind 的媒体查询（如 `sm:`、`md:`、`lg:`、`xl:`）——这些不被支持
- 绝不要使用主题选择器（如 `dark:`、`light:`）——这些不被支持
- 始终指定边框类型（如 `border-solid`、`border-dashed` 等）
- 当只为某一边定义边框时，记得重置其他边的边框（例如 `border-none`、`border-l`）

### 组件结构
- 使用 Tailwind CSS 时，务必在 `<Tailwind>` 内定义 `<Head />`
- 仅在向组件传递属性时使用 `PreviewProps`
- 只在组件实际需要的属性中包含 `PreviewProps`

```tsx
const Email = (props) => {
  return (
    <div>
      <a href={props.source}>click here if you want candy 👀</a>
    </div>
  );
}

Email.PreviewProps = {
  source: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
};
```

### 默认样式
- `Body`：`font-sans py-10 bg-gray-100`
- `Container`：白色，居中显示，内容左对齐
- `Footer`：包含物理地址、取消订阅链接以及年份信息（使用 `m-0` 样式）

### 字体排版
- 标题：加粗字体，字号较大，边距较大
- 段落：常规字体大小，字号较小，边距较小
- 保持一致的间距，尊重内容层次结构

### 图片
- 仅在用户请求时包含图片
- 绝不要使用固定宽度/高度——使用响应式单位（如 `w-full`、`h-auto`）
- 绝不要扭曲用户提供的图片
- 绝不要创建 SVG 图片——仅使用提供的或网页上的图片

### 按钮
- 始终使用 `box-border` 来防止内边距溢出

### 布局
- 默认情况下支持移动设备
- 使用适用于所有屏幕尺寸的堆叠布局
- 删除列表项之间的默认间距/边距/内边距

### 暗模式
根据用户需求：容器颜色设为黑色（#000），背景颜色设为深灰色（#151516）

### 最佳实践
- 根据用户需求选择颜色、布局和文本内容
- 使模板具有独特性，避免使用通用模板
- 在邮件正文中使用关键词以提高转化率

## 渲染
- **转换为 HTML**：```tsx
import { render } from '@react-email/components';
import { WelcomeEmail } from './emails/welcome';

const html = await render(
  <WelcomeEmail name="John" verificationUrl="https://example.com/verify" />
);
```
- **转换为纯文本**：```tsx
import { render } from '@react-email/components';
import { WelcomeEmail } from './emails/welcome';

const text = await render(<WelcomeEmail name="John" verificationUrl="https://example.com/verify" />, { plainText: true });
```

## 发送邮件

React Email 支持与任何邮件服务提供商一起发送邮件。如果用户想知道如何发送邮件，请参阅 [Sending guidelines](references/SENDING.md)。

以下是一个使用 Node.js 的 Resend SDK 的快速示例：

```tsx
import { Resend } from 'resend';
import { WelcomeEmail } from './emails/welcome';

const resend = new Resend(process.env.RESEND_API_KEY);

const { data, error } = await resend.emails.send({
  from: 'Acme <onboarding@resend.dev>',
  to: ['user@example.com'],
  subject: 'Welcome to Acme',
  react: <WelcomeEmail name="John" verificationUrl="https://example.com/verify" />
});

if (error) {
  console.error('Failed to send:', error);
}
```

Node SDK 会自动处理纯文本和 HTML 的渲染。

## 国际化

有关完整的国际化（i18n）文档，请参阅 [references/I18N.md](references/I18N.md)。

React Email 支持三种国际化库：`next-intl`、`react-i18next` 和 `react-intl`。

### 快速示例（使用 next-intl）：

消息文件（`messages/en.json`、`messages/es.json` 等）：

```json
{
  "welcome-email": {
    "greeting": "Hi",
    "body": "Thanks for signing up!",
    "cta": "Get Started"
  }
}
```

## 邮件最佳实践
1. **在多种邮件客户端上进行测试**——在 Gmail、Outlook、Apple Mail、Yahoo Mail 等客户端上进行测试。可以使用 Litmus 或 Email on Acid 等工具进行精确测试，并使用 React Email 的工具栏来检查特定功能的支持情况。
2. **保持响应式设计**——最大宽度约为 600px，并在移动设备上进行测试。
3. **使用绝对 URL 保存图片**——将图片托管在可靠的 CDN 上，并始终添加 `alt` 文本。
4. **提供纯文本版本**——这对可访问性和某些邮件客户端是必需的。
5. **保持文件大小在 102KB 以下**——Gmail 会截断过大的邮件。
6. **添加适当的 TypeScript 类型**——为所有邮件属性定义接口。
7. **包含预览属性**——为组件添加 `PreviewProps` 以便进行开发测试。
8. **处理错误**——在发送邮件时始终检查错误。
9. **使用经过验证的域名**——在生产环境中，使用经过验证的域名作为发件地址。

## 常见模式

有关常见模式的完整示例，请参阅 [references/PATTERNS.md](references/PATTERNS.md)，包括：
- 密码重置邮件
- 带产品列表的订单确认邮件
- 包含代码块的通知邮件
- 多列布局
- 使用自定义字体的邮件模板

## 其他资源
- [React Email 文档](https://react.email/docs/llms.txt)
- [React Email GitHub 仓库](https://github.com/resend/react-email)
- [Resend 文档](https://resend.com/docs/llms.txt)
- [邮件客户端 CSS 支持](https://www.caniemail.com)
- 组件参考：[references/COMPONENTS.md](references/COMPONENTS.md)
- 国际化指南：[references/I18N.md](references/I18N.md)
- 常见模式：[references/PATTERNS.md](references/PATTERNS.md)