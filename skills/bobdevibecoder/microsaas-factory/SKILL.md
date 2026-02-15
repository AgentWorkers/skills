---
name: microsaas-factory
description: "根据 ConvertFlow 模板构建和部署微 SaaS 产品。通过克隆、定制后，将产品部署到 Vercel 平台。部署过程可以通过发送 “build [name]” 的 Telegram 消息来触发，或者根据 saas-idea-discovery 中的高分创意来自动执行。"
metadata: { "openclaw": { "emoji": "🏭" } }
---

# 微服务SaaS工厂（Micro-SaaS Factory）

您可以通过克隆ConvertFlow模板、对其进行定制、构建后部署到Vercel来创建和发布新的微服务SaaS产品。

## 执行模式

### 快速构建模式（默认模式）
根据产品名称和描述生成完整的产品配置，然后进行构建和部署。

**触发方式：** 用户输入 “build [产品名称]: [描述]”
**示例：** “build markdown-magic: 将Markdown转换为HTML和纯文本”

### 构建模式
当提供完整的产品配置文件（product_config.json）时，跳过配置生成步骤，直接开始构建。

### 状态模式
从data/products.json中列出所有已构建的产品。

**触发方式：** 用户输入 “factory status” 或 “list products”

---

## 构建流程

### 第1步：生成产品配置
利用智能系统，根据templates/product_config.example.json中的模板生成完整的产品配置文件（product_config.json）。配置内容包括：
- 产品名称、slug（唯一标识符）、首字母缩写、API密钥前缀
- 产品介绍部分（徽标、标题、副标题）
- 4个功能卡片（配有相应的lucid-react图标）
- 免费版和Pro版的限制及价格信息
- 工具使用说明、示例输入/输出内容、标签
- 核心的转换器TypeScript代码（纯函数，尽可能不依赖外部库）
- 数据库连接方向的相关枚举值

**将配置摘要发送给用户，并等待用户确认 “go” 以继续下一步。**

### 第2步：克隆模板
运行克隆脚本：
```bash
cd /home/node/.openclaw/workspace/skills/microsaas-factory
bash scripts/clone_template.sh [slug]
```

### 第3步：自定义文件
使用生成的配置文件运行自定义化脚本：
```bash
cd /home/node/.openclaw/workspace/skills/microsaas-factory
node scripts/customize.js /home/milad/[slug] '[product_config_json]'
```

### 第4步：构建
```bash
cd /home/node/.openclaw/workspace/skills/microsaas-factory
bash scripts/build_and_fix.sh [slug]
```

如果构建失败，请查看错误输出：
1. 确定出问题的文件及具体错误原因
2. 修复TypeScript或导入相关的错误
3. 重新尝试构建（最多尝试3次）

### 第5步：部署（需要人工审批）
**在此步骤前请询问用户：**
> [产品名称] 的构建成功，准备部署了吗？
> 是否要重用ConvertFlow的API密钥？（Clerk、Supabase、Stripe）
> 输入 “deploy” 以继续部署，或提供新的API密钥。

获得批准后：
```bash
cd /home/node/.openclaw/workspace/skills/microsaas-factory
bash scripts/deploy.sh [slug]
```

### 第6步：通知用户
通过Telegram发送通知：
```
🏭 Product Deployed!

Name: [name]
URL: [vercel-url]
GitHub: [github-url]

Features:
- [feature 1]
- [feature 2]
- [feature 3]
- [feature 4]

Free: [free-limits]
Pro: $[price]/mo

Status: LIVE
```

更新data/products.json文件，添加新的产品信息。

---

## 转换器代码生成规则

在生成src/lib/converter.ts文件中的TypeScript代码时，请遵循以下规则：
1. 导出两个函数：`convertForward(input: string): string` 和 `convertBackward(input: string)`
2. 导出 `detectFormat(input: string): "forward" | "backward" | "unknown"`
3. 所有函数都必须是纯函数（无副作用、无异步操作、不依赖外部状态）
4. 通过抛出带有描述性信息的Error来处理错误
5. 尽量减少对外部库的依赖（优先使用内置的字符串处理函数）
6. 如果确实需要依赖外部包（例如用于Markdown处理的marked），请将其添加到config文件中的`tool.npm_packages`字段
7. 生成的代码必须是有效的TypeScript代码，且能够无误地编译

**示例代码结构：**
```typescript
export function convertForward(input: string): string {
  // Convert from format A to format B
  if (!input.trim()) throw new Error("Input is empty");
  // ... conversion logic ...
  return result;
}

export function convertBackward(input: string): string {
  // Convert from format B to format A
  if (!input.trim()) throw new Error("Input is empty");
  // ... conversion logic ...
  return result;
}

export function detectFormat(input: string): "forward" | "backward" | "unknown" {
  // Detect whether input is format A or format B
  // ... detection logic ...
  return "unknown";
}
```

---

## 文件修改说明

customize.js脚本会修改克隆后的模板中的以下文件：
| 文件 | 修改内容 |
|------|-------------|
| package.json | 修改产品名称字段 |
| src/lib/utils.ts | 设置APP_NAME默认值、API密钥前缀、定义PLANS常量 |
| src/lib/converter.ts | 替换为生成的TypeScript代码 |
| src/app/page.tsx | 修改产品介绍部分的标题、副标题、徽标和功能卡片 |
| src/app/pricing/page.tsx | 更新计划详情、价格信息 |
| src/components/landing/hero-converter.tsx | 更新示例数据、标签和使用说明 |
| src/components/uinavbar.tsx | 修改Logo的首字母缩写 |
| src/app/api/v1/convert/route.ts | 更新导入语句和方向处理逻辑 |
| src/lib/supabase.ts | 更新数据库连接方向的枚举值 |
| supabase/schema.sql | 添加数据库连接方向的CHECK约束 |
| .env.local.example | 设置APP_NAME默认值 |

---

## 错误处理规则
- 如果克隆失败：报告错误并停止后续操作
- 如果自定义化步骤失败：报告出问题的文件并尝试修复
- 如果构建失败：捕获错误并尝试自动修复（最多3次），之后报告失败原因
- 如果部署失败：报告错误，并保留已构建的项目以供手动部署
- 必须随时更新data/products.json文件中的产品状态（“building”、“built”、“deployed”、“failed”）

---

## 安全规则
1. 绝不要删除位于/home/milad/micro-saas-template/的源模板文件
2. 未经用户明确批准，切勿进行任何部署操作
3. 绝不要使用真实的支付凭证——始终使用Stripe的测试密钥
4. 在执行任何操作前，务必等待用户确认 “go” 或 “deploy”
5. 在进行重大操作前，务必先告知用户预期的代币成本