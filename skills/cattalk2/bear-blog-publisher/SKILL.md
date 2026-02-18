---
name: bear-blog-publisher
description: 将博客文章发布到 Bear Blog 平台。该平台支持 AI 生成的内容、用户提供的 Markdown 格式的内容以及自动生成的图表。
---
# Bear Blog 发布器

将博客文章发布到 Bear Blog（https://bearblog.dev/）。

## 概述

该技能提供了自动发布博客文章到 Bear Blog 的功能。

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

**安全提示**：文件权限应设置为 600（仅允许所有者读取）。

### 方法 2：环境变量（推荐用于持续集成/持续部署（CI/CD）**

```bash
export BEAR_BLOG_EMAIL="your@email.com"
export BEAR_BLOG_PASSWORD="yourpassword"
```

**安全提示**：认证信息仅存储在内存中，不会写入磁盘。

### 方法 3：运行时参数（推荐用于多用户环境）

在调用该技能时提供认证信息：

```python
publisher = BearBlogPublisher(email="user@example.com", password="secret")
```

**安全提示**：调用者（聊天机器人、Web 应用等）负责管理认证信息的生命周期。

## 优先级顺序

1. 运行时参数（最高优先级）
2. 环境变量
3. OpenClaw 配置（最低优先级）

## 功能

### 1. 发布博客文章

**输入参数：**
- `title`（字符串）：博客文章标题
- `content`（字符串）：Markdown 格式的文章内容
- `email`（字符串，可选）：Bear Blog 的邮箱地址
- `password`（字符串，可选）：Bear Blog 的密码

**输出结果：**
- 发布后的文章链接或错误信息

### 2. 生成内容（可选）

如果未提供 `content`，则会根据 `topic` 生成内容。

### 3. 生成图表（可选）

对于技术类主题，可以生成相应的架构图。

## 安全最佳实践

1. **切勿将认证信息提交到 Git**  
2. **在生产环境中使用环境变量**  
3. **将配置文件的权限设置为 600**  
4. **在多用户环境中使用运行时参数**  

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

### 使用运行时参数

```python
# In your chat bot code
email = get_user_email()  # Ask user
password = get_user_password()  # Ask user

publisher = BearBlogPublisher(email=email, password=password)
result = publisher.publish(title="My Post", content="# Content")
```

## 实现细节

- 使用 Bear Blog 的 Web API 进行发布  
- 支持 CSRF 令牌认证  
- 基于会话的认证机制（无持久化存储）  
- 使用 Playwright 工具生成图表  

## 许可证

MIT