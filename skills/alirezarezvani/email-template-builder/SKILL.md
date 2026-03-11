---
name: "email-template-builder"
description: "电子邮件模板构建器"
---
# 电子邮件模板构建器

**等级：** 高级  
**类别：** 工程团队  
**领域：** 交易型电子邮件 / 通信基础设施  

---

## 概述  

该工具可帮助您构建完整的交易型电子邮件系统，支持以下功能：React Email模板、提供商集成、预览服务器、国际化（i18n）支持、暗黑模式、垃圾邮件优化以及分析跟踪。生成的代码可直接用于 Resend、Postmark、SendGrid 或 AWS SES 等邮件服务。  

---

## 核心功能  

- React Email 模板（欢迎邮件、验证邮件、密码重置邮件、发票邮件、通知邮件、摘要邮件）  
- MJML 模板，以确保与大多数电子邮件客户端兼容  
- 支持多种邮件服务提供商，并提供统一的发送接口  
- 内置本地预览服务器，支持热重载  
- 支持通过键入翻译内容进行国际化（i18n）  
- 通过媒体查询（media queries）实现暗黑模式  
- 提供垃圾邮件评分优化检查清单  

---

## 适用场景  

- 为新产品设置交易型电子邮件系统  
- 从旧电子邮件系统迁移  
- 添加新的电子邮件类型（如发票邮件、摘要邮件、通知邮件）  
- 调试电子邮件发送问题  
- 为电子邮件模板实现国际化（i18n）  

---

## 项目结构  

```
emails/
├── components/
│   ├── layout/
│   │   ├── email-layout.tsx       # Base layout with brand header/footer
│   │   └── email-button.tsx       # CTA button component
│   ├── partials/
│   │   ├── header.tsx
│   │   └── footer.tsx
├── templates/
│   ├── welcome.tsx
│   ├── verify-email.tsx
│   ├── password-reset.tsx
│   ├── invoice.tsx
│   ├── notification.tsx
│   └── weekly-digest.tsx
├── lib/
│   ├── send.ts                    # Unified send function
│   ├── providers/
│   │   ├── resend.ts
│   │   ├── postmark.ts
│   │   └── ses.ts
│   └── tracking.ts                # UTM + analytics
├── i18n/
│   ├── en.ts
│   └── de.ts
└── preview/                       # Dev preview server
    └── server.ts
```  

---

## 基础电子邮件布局  

```tsx
// emails/components/layout/email-layout.tsx
import {
  Body, Container, Head, Html, Img, Preview, Section, Text, Hr, Font
} from "@react-email/components"

interface EmailLayoutProps {
  preview: string
  children: React.ReactNode
}

export function EmailLayout({ preview, children }: EmailLayoutProps) {
  return (
    <Html lang="en">
      <Head>
        <Font
          fontFamily="Inter"
          fallbackFontFamily="Arial"
          webFont={{ url: "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfAZ9hiJ-Ek-_EeA.woff2", format: "woff2" }}
          fontWeight={400}
          fontStyle="normal"
        />
        {/* Dark mode styles */}
        <style>{`
          @media (prefers-color-scheme: dark) {
            .email-body { background-color: #0f0f0f !important; }
            .email-container { background-color: #1a1a1a !important; }
            .email-text { color: #e5e5e5 !important; }
            .email-heading { color: #ffffff !important; }
            .email-divider { border-color: #333333 !important; }
          }
        `}</style>
      </Head>
      <Preview>{preview}</Preview>
      <Body className="email-body" style={styles.body}>
        <Container className="email-container" style={styles.container}>
          {/* Header */}
          <Section style={styles.header}>
            <Img src="https://yourapp.com/logo.png" width={120} height={40} alt="MyApp" />
          </Section>
          
          {/* Content */}
          <Section style={styles.content}>
            {children}
          </Section>
          
          {/* Footer */}
          <Hr style={styles.divider} />
          <Section style={styles.footer}>
            <Text style={styles.footerText}>
              MyApp Inc. · 123 Main St · San Francisco, CA 94105
            </Text>
            <Text style={styles.footerText}>
              <a href="{{unsubscribe_url}}" style={styles.link}>Unsubscribe</a>
              {" · "}
              <a href="https://yourapp.com/privacy" style={styles.link}>Privacy Policy</a>
            </Text>
          </Section>
        </Container>
      </Body>
    </Html>
  )
}

const styles = {
  body: { backgroundColor: "#f5f5f5", fontFamily: "Inter, Arial, sans-serif" },
  container: { maxWidth: "600px", margin: "0 auto", backgroundColor: "#ffffff", borderRadius: "8px", overflow: "hidden" },
  header: { padding: "24px 32px", borderBottom: "1px solid #e5e5e5" },
  content: { padding: "32px" },
  divider: { borderColor: "#e5e5e5", margin: "0 32px" },
  footer: { padding: "24px 32px" },
  footerText: { fontSize: "12px", color: "#6b7280", textAlign: "center" as const, margin: "4px 0" },
  link: { color: "#6b7280", textDecoration: "underline" },
}
```  

---

## 欢迎邮件模板  

```tsx
// emails/templates/welcome.tsx
import { Button, Heading, Text } from "@react-email/components"
import { EmailLayout } from "../components/layout/email-layout"

interface WelcomeEmailProps {
  name: "string"
  confirmUrl: string
  trialDays?: number
}

export function WelcomeEmail({ name, confirmUrl, trialDays = 14 }: WelcomeEmailProps) {
  return (
    <EmailLayout preview={`Welcome to MyApp, ${name}! Confirm your email to get started.`}>
      <Heading style={styles.h1}>Welcome to MyApp, {name}!</Heading>
      <Text style={styles.text}>
        We're excited to have you on board. You've got {trialDays} days to explore everything MyApp has to offer — no credit card required.
      </Text>
      <Text style={styles.text}>
        First, confirm your email address to activate your account:
      </Text>
      <Button href={confirmUrl} style={styles.button}>
        Confirm Email Address
      </Button>
      <Text style={styles.hint}>
        Button not working? Copy and paste this link into your browser:
        <br />
        <a href={confirmUrl} style={styles.link}>{confirmUrl}</a>
      </Text>
      <Text style={styles.text}>
        Once confirmed, you can:
      </Text>
      <ul style={styles.list}>
        <li>Connect your first project in 2 minutes</li>
        <li>Invite your team (free for up to 3 members)</li>
        <li>Set up Slack notifications</li>
      </ul>
    </EmailLayout>
  )
}

export default WelcomeEmail

const styles = {
  h1: { fontSize: "28px", fontWeight: "700", color: "#111827", margin: "0 0 16px" },
  text: { fontSize: "16px", lineHeight: "1.6", color: "#374151", margin: "0 0 16px" },
  button: { backgroundColor: "#4f46e5", color: "#ffffff", borderRadius: "6px", fontSize: "16px", fontWeight: "600", padding: "12px 24px", textDecoration: "none", display: "inline-block", margin: "8px 0 24px" },
  hint: { fontSize: "13px", color: "#6b7280" },
  link: { color: "#4f46e5" },
  list: { fontSize: "16px", lineHeight: "1.8", color: "#374151", paddingLeft: "20px" },
}
```  

---

## 发票邮件模板  

```tsx
// emails/templates/invoice.tsx
import { Row, Column, Section, Heading, Text, Hr, Button } from "@react-email/components"
import { EmailLayout } from "../components/layout/email-layout"

interface InvoiceItem { description: string; amount: number }

interface InvoiceEmailProps {
  name: "string"
  invoiceNumber: string
  invoiceDate: string
  dueDate: string
  items: InvoiceItem[]
  total: number
  currency: string
  downloadUrl: string
}

export function InvoiceEmail({ name, invoiceNumber, invoiceDate, dueDate, items, total, currency = "USD", downloadUrl }: InvoiceEmailProps) {
  const formatter = new Intl.NumberFormat("en-US", { style: "currency", currency })

  return (
    <EmailLayout preview={`Invoice ${invoiceNumber} - ${formatter.format(total / 100)}`}>
      <Heading style={styles.h1}>Invoice #{invoiceNumber}</Heading>
      <Text style={styles.text}>Hi {name},</Text>
      <Text style={styles.text}>Here's your invoice from MyApp. Thank you for your continued support.</Text>

      {/* Invoice Meta */}
      <Section style={styles.metaBox}>
        <Row>
          <Column><Text style={styles.metaLabel}>Invoice Date</Text><Text style={styles.metaValue}>{invoiceDate}</Text></Column>
          <Column><Text style={styles.metaLabel}>Due Date</Text><Text style={styles.metaValue}>{dueDate}</Text></Column>
          <Column><Text style={styles.metaLabel}>Amount Due</Text><Text style={styles.metaValueLarge}>{formatter.format(total / 100)}</Text></Column>
        </Row>
      </Section>

      {/* Line Items */}
      <Section style={styles.table}>
        <Row style={styles.tableHeader}>
          <Column><Text style={styles.tableHeaderText}>Description</Text></Column>
          <Column><Text style={{ ...styles.tableHeaderText, textAlign: "right" }}>Amount</Text></Column>
        </Row>
        {items.map((item, i) => (
          <Row key={i} style={i % 2 === 0 ? styles.tableRowEven : styles.tableRowOdd}>
            <Column><Text style={styles.tableCell}>{item.description}</Text></Column>
            <Column><Text style={{ ...styles.tableCell, textAlign: "right" }}>{formatter.format(item.amount / 100)}</Text></Column>
          </Row>
        ))}
        <Hr style={styles.divider} />
        <Row>
          <Column><Text style={styles.totalLabel}>Total</Text></Column>
          <Column><Text style={styles.totalValue}>{formatter.format(total / 100)}</Text></Column>
        </Row>
      </Section>

      <Button href={downloadUrl} style={styles.button}>Download PDF Invoice</Button>
    </EmailLayout>
  )
}

export default InvoiceEmail

const styles = {
  h1: { fontSize: "24px", fontWeight: "700", color: "#111827", margin: "0 0 16px" },
  text: { fontSize: "15px", lineHeight: "1.6", color: "#374151", margin: "0 0 12px" },
  metaBox: { backgroundColor: "#f9fafb", borderRadius: "8px", padding: "16px", margin: "16px 0" },
  metaLabel: { fontSize: "12px", color: "#6b7280", fontWeight: "600", textTransform: "uppercase" as const, margin: "0 0 4px" },
  metaValue: { fontSize: "14px", color: "#111827", margin: 0 },
  metaValueLarge: { fontSize: "20px", fontWeight: "700", color: "#4f46e5", margin: 0 },
  table: { width: "100%", margin: "16px 0" },
  tableHeader: { backgroundColor: "#f3f4f6", borderRadius: "4px" },
  tableHeaderText: { fontSize: "12px", fontWeight: "600", color: "#374151", padding: "8px 12px", textTransform: "uppercase" as const },
  tableRowEven: { backgroundColor: "#ffffff" },
  tableRowOdd: { backgroundColor: "#f9fafb" },
  tableCell: { fontSize: "14px", color: "#374151", padding: "10px 12px" },
  divider: { borderColor: "#e5e5e5", margin: "8px 0" },
  totalLabel: { fontSize: "16px", fontWeight: "700", color: "#111827", padding: "8px 12px" },
  totalValue: { fontSize: "16px", fontWeight: "700", color: "#111827", textAlign: "right" as const, padding: "8px 12px" },
  button: { backgroundColor: "#4f46e5", color: "#fff", borderRadius: "6px", padding: "12px 24px", fontSize: "15px", fontWeight: "600", textDecoration: "none" },
}
```  

---

## 统一发送功能  

```typescript
// emails/lib/send.ts
import { Resend } from "resend"
import { render } from "@react-email/render"
import { WelcomeEmail } from "../templates/welcome"
import { InvoiceEmail } from "../templates/invoice"
import { addTrackingParams } from "./tracking"

const resend = new Resend(process.env.RESEND_API_KEY)

type EmailPayload =
  | { type: "welcome"; props: Parameters<typeof WelcomeEmail>[0] }
  | { type: "invoice"; props: Parameters<typeof InvoiceEmail>[0] }

export async function sendEmail(to: string, payload: EmailPayload) {
  const templates = {
    welcome: { component: WelcomeEmail, subject: "Welcome to MyApp — confirm your email" },
    invoice: { component: InvoiceEmail, subject: `Invoice from MyApp` },
  }

  const template = templates[payload.type]
  const html = render(template.component(payload.props as any))
  const trackedHtml = addTrackingParams(html, { campaign: payload.type })

  const result = await resend.emails.send({
    from: "MyApp <hello@yourapp.com>",
    to,
    subject: template.subject,
    html: trackedHtml,
    tags: [{ name: "email-type", value: payload.type }],
  })

  return result
}
```  

---

## 预览服务器配置  

```typescript
// package.json scripts
{
  "scripts": {
    "email:dev": "email dev --dir emails/templates --port 3001",
    "email:build": "email export --dir emails/templates --outDir emails/out"
  }
}

// Run: npm run email:dev
// Opens: http://localhost:3001
// Shows all templates with live preview and hot reload
```  

---

## 国际化（i18n）支持  

```typescript
// emails/i18n/en.ts
export const en = {
  welcome: {
    preview: (name: "string-welcome-to-myapp-name"
    heading: (name: "string-welcome-to-myapp-name"
    body: (days: number) => `You've got ${days} days to explore everything.`,
    cta: "Confirm Email Address",
  },
}

// emails/i18n/de.ts
export const de = {
  welcome: {
    preview: (name: "string-willkommen-bei-myapp-name"
    heading: (name: "string-willkommen-bei-myapp-name"
    body: (days: number) => `Du hast ${days} Tage Zeit, alles zu erkunden.`,
    cta: "E-Mail-Adresse bestätigen",
  },
}

// Usage in template
import { en, de } from "../i18n"
const t = locale === "de" ? de : en
```  

---

## 垃圾邮件评分优化检查清单  

- [ ] 发件人域名已配置 SPF、DKIM 和 DMARC 记录  
- [ ] 发件地址使用您的自定义域名（而非 gmail.com 或 hotmail.com）  
- [ ] 主题行长度不超过 50 个字符，避免全部使用大写字母，且不包含 “FREE!!!” 等字样  
- [ ] 文本与图片的比例至少为 60%  
- 提供 HTML 和纯文本两种版本  
- 每封营销邮件中都包含退订链接（符合 CAN-SPAM 和 GDPR 规范）  
- 不使用网址缩短服务，使用完整的品牌链接  
- 主题行中避免使用 “guarantee”（保证）、”no risk”（无风险）、“limited time offer”（限时优惠）等可能引发争议的词汇  
- 每封邮件中仅包含一个明确的呼叫行动（CTA）按钮  
- 每张图片都配有替代文本（alt text）  
- HTML 代码格式正确，无标签错误  
- 在首次发送前使用 Mail-Tester.com 进行测试（评分目标：9 分以上）  

---

## 分析跟踪  

```typescript
// emails/lib/tracking.ts
interface TrackingParams {
  campaign: string
  medium?: string
  source?: string
}

export function addTrackingParams(html: string, params: TrackingParams): string {
  const utmString = new URLSearchParams({
    utm_source: params.source ?? "email",
    utm_medium: params.medium ?? "transactional",
    utm_campaign: params.campaign,
  }).toString()

  // Add UTM params to all links in the email
  return html.replace(/href="(https?:\/\/[^"]+)"/g, (match, url) => {
    const separator = url.includes("?") ? "&" : "?"
    return `href="${url}${separator}${utmString}"`
  })
}
```  

---

## 常见问题  

- **需要内联样式**：大多数电子邮件客户端会删除 `<head>` 标签中的样式，React Email 可自动处理这一问题  
- **最大宽度限制为 600px**：超过此宽度会导致 Gmail 移动版显示异常  
- **禁止使用 flexbox 或 grid**：请使用 react-email 提供的 `<Row>` 和 `<Column>` 组件，而非 CSS 的 grid 结构  
- **暗黑模式下的样式覆盖**：必须使用 `!important` 语句来覆盖内联样式  
- **缺少纯文本版本**：所有主流邮件服务都支持纯文本版本，请务必添加  
- **区分交易型邮件和营销邮件**：使用不同的发送域名或 IP 地址，以确保邮件正常送达