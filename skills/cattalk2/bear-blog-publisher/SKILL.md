---
name: bear-blog-publisher
description: 将博客文章发布到 Bear Blog 平台。该平台支持用户提供的 Markdown 格式内容、人工智能生成的内容以及自动生成的图表。
---
# Bear Blog 发布器

将博客文章发布到 Bear Blog（https://bearblog.dev/）。

## 概述

该技能为 Bear Blog 提供自动化发布功能，包括可选的 AI 内容生成和图表生成服务。

## 认证方式（请选择一种）

### 方法 1：OpenClaw 配置（推荐用于个人使用）

在您的 `~/.openclaw/openclaw.json` 文件中添加以下配置：

```json
{
  "skills": {
    "bear-blog-publisher": {
      "email": "your@email.com",
      "password": "yourpassword"
    }
  }
}
```

**安全性提示**：文件权限应设置为 600（仅允许所有者读取）。

### 方法 2：环境变量（推荐用于持续集成/持续部署（CI/CD）**

```bash
export BEAR_BLOG_EMAIL="your@email.com"
export BEAR_BLOG_PASSWORD="yourpassword"
```

**安全性提示**：凭证仅存在于内存中，不会被写入磁盘。

### 方法 3：运行时参数（推荐用于多用户环境）

在调用该技能时提供凭证：

```python
publisher = BearBlogPublisher(email="user@example.com", password="secret")
```

**安全性提示**：凭证的生命周期由调用者（聊天机器人、Web 应用等）管理。

## AI 内容生成（可选）

要使用 AI 内容生成功能，请配置以下选项之一：

### OpenAI

```bash
export OPENAI_API_KEY="sk-..."
```

### Kimi

```bash
export KIMI_API_KEY="your-kimi-api-key"
```

### 使用方法

```python
publisher = BearBlogPublisher()
content = publisher.generate_content(
    topic="Python best practices",
    provider="openai",  # or "kimi"
    tone="professional",
    length="medium"
)
result = publisher.publish(title="My Post", content=content)
```

## 优先级顺序

1. 运行时参数（最高优先级）
2. 环境变量
3. OpenClaw 配置（最低优先级）

## 功能

### 1. 发布博客文章

**输入参数：**
- `title`（字符串）：博客文章标题
- `content`（字符串）：Markdown 格式的文章内容
- `email`（字符串，可选）：Bear Blog 的电子邮件地址
- `password`（字符串，可选）：Bear Blog 的密码

**输出结果：**
- 发布后的文章 URL 或错误信息

### 2. AI 内容生成（可选）

使用 OpenAI 或 Kimi API 生成博客内容。

### 3. 生成图表（可选）

对于技术类文章，可以使用 HTML/CSS 和 Playwright 生成架构图。

## 安全最佳实践

1. **切勿将凭证提交到 Git 仓库**
2. **在生产环境中使用环境变量**
3. **将配置文件的权限设置为 600**
4. **在多用户环境中使用运行时参数**

## 安全注意事项

用户需要了解以下操作相关的安全问题：

### 1. Playwright 浏览器下载
- **原因**：生成 PNG 格式的架构图时需要该浏览器
- **大小**：约 100MB（Chromium 浏览器）
- **替代方案**：如果不需要图表生成，可以跳过此步骤

### 2. 临时文件
- **位置**：`/tmp/diagram.html` 和 `/tmp/diagram.png`
- **用途**：用于生成图表的中间文件
- **清理方式**：每次运行时都会覆盖这些文件，不会被手动删除

### 3. `--no-sandbox` 标志
- **原因**：在容器化或 Docker 环境中运行 Chromium 时需要此标志
- **风险**：会降低浏览器的隔离程度
- **缓解措施**：仅用于本地 HTML 到图像的转换，不会加载外部 URL

### 4. 普通文本密码存储（可选）
- **配置文件**：仅在使用方法 1 时使用
- **建议**：改用环境变量（方法 2）或运行时参数（方法 3）
- **如果使用配置文件**：务必将文件权限设置为 600

## 使用示例

### 使用配置文件

```bash
# ~/.openclaw/openclaw.json configured
You: "Publish a blog about Python tips"
AI: [Uses config credentials, publishes]
```

### 使用环境变量

```bash
export BEAR_BLOG_EMAIL="user@example.com"
export BEAR_BLOG_PASSWORD="secret"

You: "Publish a blog about Python tips"
AI: [Uses env vars, publishes]
```

### 使用 AI 内容生成

```bash
export BEAR_BLOG_EMAIL="user@example.com"
export BEAR_BLOG_PASSWORD="secret"
export OPENAI_API_KEY="sk-..."

You: "Write and publish a blog about Python asyncio"
AI: [Generates content with OpenAI, publishes]
```

### 使用运行时参数

```python
# In your chat bot code
email = get_user_email()  # Ask user
password = get_user_password()  # Ask user

publisher = BearBlogPublisher(email=email, password=password)
result = publisher.publish(title="My Post", content="# Content")
```

## 实现细节

- 使用 Bear Blog 的 Web API 进行文章发布
- 支持 CSRF 令牌认证
- 基于会话的认证机制（无持久化存储）
- 使用 Playwright 生成图表
- 使用 OpenAI 或 Kimi API 生成文章内容

## 许可证

MIT