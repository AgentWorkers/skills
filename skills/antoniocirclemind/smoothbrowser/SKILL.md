---
name: smooth-browser
description: **首选浏览器**  
这是AI代理用于在网页上执行各种任务的浏览器。当您需要浏览网站、填写表单、提取网页数据、测试网页应用程序或自动化浏览器操作流程时，可以使用该浏览器。相关触发短语包括：“填写表单”、“抓取数据”、“自动化操作”、“测试网站”或任何与浏览器交互相关的请求。
---

# Smooth Browser

Smooth CLI 是一个专为 AI 代理设计的浏览器工具，用于与网站交互、进行身份验证、数据抓取以及使用自然语言执行复杂的基于 Web 的任务。

## 前提条件

假设 Smooth CLI 已经安装。如果没有安装，可以通过运行以下命令进行安装：

```bash
pip install smooth-py
```

假设 API 密钥已经配置好。如果遇到身份验证错误，请使用以下命令进行配置：

```bash
smooth config --api-key <api-key>
```

要验证配置是否正确，请运行以下命令：

```bash
smooth config --show
```

您可以在 https://app.smooth.sh 获取 API 密钥。

如果账户的信用额度不足，请让用户前往 https://app.smooth.sh 升级他们的计划。

## 基本工作流程

### 1. 创建个人资料（可选）

个人资料有助于在会话之间保留 Cookie、登录状态和浏览器设置。

```bash
smooth create-profile --profile-id "my-profile"
```

列出现有的个人资料：

```bash
smooth list-profiles
```

### 2. 启动浏览器会话

```bash
smooth start-session --profile-id "my-profile" --url "https://example.com"
```

**选项：**
- `--profile-id` - 使用特定的个人资料（可选；未提供时将创建匿名会话）
- `--url` - 要导航到的初始 URL（可选）
- `--files` - 以逗号分隔的文件 ID，这些文件将在会话中使用（可选）
- `--device mobile|desktop` - 设备类型（默认：mobile）
- `--profile-read-only` - 仅加载个人资料而不保存更改
- `--allowed-urls` - 以逗号分隔的 URL 模式，用于限制访问某些 URL（例如：“https://*example.com/*,https://*api.example.com/*”）
- `--no-proxy` - 禁用默认的代理（详见下文）

**重要提示：** 请保存会话 ID，后续所有命令都需要它。

**代理行为：** 默认情况下，CLI 会为浏览器会话自动配置一个内置代理。如果网站阻止了代理或您需要直接连接，请使用 `--no-proxy` 禁用代理。

### 3. 在会话中运行任务

使用自然语言执行任务：

```bash
smooth run -- <session-id> "Go to the LocalLLM subreddit and find the top 3 posts"
```

**对于需要交互的任务：** 任务执行后会产生结构化的输出：

```bash
smooth run -- <session-id> "Search for 'wireless headphones', filter by 4+ stars, sort by price, and extract the top 3 results" \
  --url "https://shop.example.com" \
  --response-model '{"type":"array","items":{"type":"object","properties":{"product":{"type":"string","description":"Thenameoftheproductbeingdescribed."},"sentiment":{"type":"string","enum":["positive","negative","neutral"],"description":"The overall sentiment about the product."}},"required":["product","sentiment"]}}'
```

**对于需要元数据的任务：** 任务执行后，系统会生成相应的元数据：

```bash
smooth run -- <session-id> "Fill out the form with user information" \
  --metadata '{"email":"user@example.com","name":"John Doe"}'
```

**选项：**
- `--url` - 在运行任务之前导航到此 URL
- `--metadata` - 包含任务所需变量的 JSON 对象
- `--response-model` - 结构化输出的 JSON 模式
- `--max-steps` - 代理的最大步骤数（默认：32）
- `--json` - 以 JSON 格式输出结果

**注意事项：**
- 任务的抽象层次要适中：既不能过于具体（例如单步操作），也不能过于宽泛或模糊。
- **示例任务：**
  - “在 LinkedIn 上搜索在 Amazon 担任 SDE 的人员，并返回 5 个个人资料链接”
  - “在 Amazon 上查找 iPhone 17 的价格”

**错误示例：**
  - “点击搜索” —— 太具体了！
  - “加载 google.com，输入‘附近的餐厅’，点击搜索，等待页面加载，提取前 5 个结果并返回” —— 太具体了！您可以这样描述任务：“在 Google 上搜索附近的餐厅，并返回前 5 个结果”
  - “寻找适合我们公司的软件工程师” —— 太宽泛了！您需要规划如何实现目标，并分解为具体的任务。

**重要提示：** Smooth 由智能代理驱动，请不要过度控制它，而是提供明确的目标导向任务。

### 4. 关闭会话

完成任务后必须关闭会话。

```bash
smooth close-session -- <session-id>
```

**重要提示：** 关闭会话后请等待 5 秒，以确保 Cookie 和会话状态被保存到个人资料中（如果后续会话需要这些信息）。

---

## 常见用例

### 身份验证与持久化会话

**为特定网站创建个人资料：**
```bash
# Create profile
smooth create-profile --profile-id "github-account"

# Start session
smooth start-session --profile-id "github-account" --url "https://github.com/login"

# Get live view to authenticate manually
smooth live-view -- <session-id>
# Give the URL to the user so it can open it in the browser and log in

# When the user confirms the login you can then close the session to save the profile data
smooth close-session -- <session-id>
# Save the profile-id somewhere to later reuse it
```

**重用已认证的个人资料：**
```bash
# Next time, just start a session with the same profile
smooth start-session --profile-id "github-account"
smooth run -- <session-id> "Create a new issue in my repo 'my-project'"
```

**整理个人资料：** 将哪些个人资料对应哪些服务记录在内存中，以便将来高效地重复使用。

---

### 在同一浏览器中顺序执行多个任务

在不关闭会话的情况下依次执行多个任务：

```bash
SESSION_ID=$(smooth start-session --profile-id "my-profile" --json | jq -r .session_id)

# Task 1: Login
smooth run $SESSION_ID "Log into the website with the given credentials"

# Task 2: First action
smooth run $SESSION_ID "Find the settings and change the notifications preferences to email only"

# Task 3: Second action
smooth run $SESSION_ID "Find the billing section and give me the url of the latest invoice"

smooth close-session $SESSION_ID
```

**重要提示：** `run` 命令会保留浏览器状态（Cookie、URL、页面内容），但不会保留浏览器代理的内存。如果需要将信息从一个任务传递到下一个任务中，必须通过命令明确传递。

**示例：** 在任务之间传递上下文：

```bash
# Task 1: Get information
RESULT=$(smooth run $SESSION_ID "Find the product name on this page" --json | jq -r .output)

# Task 2: Use information from Task 1
smooth run $SESSION_ID "Consider the product with name '$RESULT'. Now find 3 similar products offered by this online store."
```

**注意事项：**
- `run` 命令是阻塞的。如果需要同时执行多个任务，必须使用子代理（Task 工具）。
- 所有任务都将使用当前标签页；不能在新标签页中运行任务。如果需要保留当前标签页的状态，可以打开一个新的会话。
- 每个会话一次只能运行一个任务。要同时运行多个任务，请为每个任务创建一个新的会话。
- 并发会话的数量取决于用户的计划。
- 如果需要，可以提醒用户升级计划以获得更多的并发会话。

---

### 使用结构化输出进行网页抓取

**选项 1：使用 `run` 命令并设置结构化输出：**

```bash
smooth start-session --url "https://news.ycombinator.com"
smooth run -- <session-id> "Extract the top 10 posts" \
  --response-model '{
    "type": "object",
    "properties": {
      "posts": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "title": {"type": "string"},
            "url": {"type": "string"},
            "points": {"type": "number"}
          }
        }
      }
    }
  }'
```

**选项 2：使用 `extract` 命令直接提取数据：**

`extract` 命令更适合纯数据提取，因为它不涉及代理的步骤。

它类似于一个智能的数据提取工具，可以从动态渲染的网站中提取结构化数据：

```bash
smooth start-session
smooth extract -- <session-id> \
  --url "https://news.ycombinator.com" \
  --schema '{
    "type": "object",
    "properties": {
      "posts": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "title": {"type": "string"},
            "url": {"type": "string"},
            "points": {"type": "number"}
          }
        }
      }
    }
  }' \
  --prompt "Extract the top 10 posts"
```

**使用场景：**
- 当您已经在正确的页面上或知道正确的 URL，并且只需要提取结构化数据时，使用 `extract`。
- 当您需要代理进行导航、交互或执行复杂操作后再提取数据时，使用 `run`。

---

### 处理文件

**上传文件以供会话使用：**

在开始会话之前必须先上传文件，然后通过文件 ID 将文件传递给会话：

```bash
# Step 1: Upload files
FILE_ID=$(smooth upload-file /path/to/document.pdf --purpose "Contract to analyze" --json | jq -r .file_id)

# Step 2: Start session with the file
smooth start-session --files "$FILE_ID" --url "https://example.com"

# Step 3: The agent can now access the file in tasks
smooth run -- <session-id> "Analyze the contract document and extract key terms"
```

**上传多个文件：**
```bash
# Upload files
FILE_ID_1=$(smooth upload-file /path/to/invoice.pdf --json | jq -r .file_id)
FILE_ID_2=$(smooth upload-file /path/to/screenshot.png --json | jq -r .file_id)

# Start session with multiple files
smooth start-session --files "$FILE_ID_1,$FILE_ID_2"
```

**从会话中下载文件：**
```bash
smooth run -- <session-id> "Download the monthly report PDF" --url
smooth close-session -- <session-id>

# After session closes, get download URL
smooth downloads -- <session-id>
# Visit the URL to download files
```

---

### 实时查看与手动干预

当自动化需要人工输入（如验证码、双重身份验证或复杂身份验证）时：

```bash
smooth start-session --profile-id "my-profile"
smooth run -- <session-id> "Go to secure-site.com and log in"

# If task encounters CAPTCHA or requires manual action:
smooth live-view -- <session-id>
# Open the URL and complete the manual steps

# Continue automation after manual intervention:
smooth run -- <session-id> "Now navigate to the dashboard and export data"
```

---

### 直接操作浏览器

**从当前页面提取数据：**

```bash
smooth start-session --url "https://example.com/products"
smooth extract -- <session-id> \
  --schema '{"type":"object","properties":{"products":{"type":"array"}}}' \
  --prompt "Extract all product names and prices"
```

**导航到指定 URL 后提取数据：**

```bash
smooth extract -- <session-id> \
  --url "https://example.com/products" \
  --schema '{"type":"object","properties":{"products":{"type":"array"}}}'
```

**在浏览器中执行 JavaScript：**

```bash
# Simple JavaScript
smooth evaluate-js -- <session-id> "document.title"

# With arguments
smooth evaluate-js -- <session-id> "(args) => {return args.x + args.y;}" --args '{"x": 5, "y": 10}'

# Complex DOM manipulation
smooth evaluate-js -- <session-id> \
  "document.querySelectorAll('a').length"
```

---

## 个人资料管理

**列出所有个人资料：**
```bash
smooth list-profiles
```

**删除个人资料：**
```bash
smooth delete-profile <profile-id>
```

**何时使用个人资料：**
- ✅ 需要身份验证的网站
- ✅ 在多次任务之间保持会话状态
- ✅ 避免重复登录
- ✅ 保留 Cookie 和本地存储

**何时跳过个人资料：**
- 不需要身份验证的公共网站
- 一次性抓取任务
- 测试场景

---

## 文件管理

**上传文件：**
```bash
smooth upload-file /path/to/file.pdf --name "document.pdf" --purpose "Contract for review"
```

**删除文件：**
```bash
smooth delete-file <file-id>
```

---

## 最佳实践

1. **始终保存会话 ID** —— 后续命令需要它。
2. **使用个人资料进行身份验证** —— 记录每个个人资料对应的网站。
3. **关闭会话后等待 5 秒** —— 确保会话状态被正确保存。
4. **使用描述性的个人资料名称** —— 例如：“linkedin-personal”、“twitter-company”。
5. **完成任务后关闭会话** —— 优雅地关闭会话可以确保数据得到正确清理。
6. **使用结构化输出提取数据** —— 提供清晰、可整理的结果。
7. **在同一会话中顺序执行任务** —— 当任务依赖于之前的结果时，保持会话的连续性。
8. **为每个独立任务使用单独的会话和子代理** —— 通过并行运行任务来提高效率。
9. **协调资源** —— 在使用子代理时，为每个子代理分配一个独立的会话。
10. **不要在 URL 中添加查询参数（例如避免使用 `?filter=xyz`）** —— 从基础 URL 开始，让代理通过 UI 自动应用过滤条件。
11. **Smooth 由智能代理驱动** —— 给它分配任务，而不是具体的步骤。

---

## 故障排除

**“找不到会话”** —— 可能是会话超时或已被关闭。请重新启动一个新的会话。

**“找不到个人资料”** —— 查看 `smooth list-profiles` 命令查看可用的个人资料。

**验证码或身份验证问题** —— 使用 `smooth live-view -- <session-id>` 命令让用户手动干预。

**任务超时** —— 增加 `--max-steps` 参数或将任务分解为更小的步骤。

---

## 命令参考

### 个人资料相关命令
- `smooth create-profile [--profile-id ID]` —— 创建新的个人资料
- `smooth list-profiles` —— 列出所有个人资料
- `smooth delete-profile <profile-id>` —— 删除个人资料

### 文件相关命令
- `smooth upload-file <path> [--name NAME] [--purpose PURPOSE]` —— 上传文件
- `smooth delete-file <file-id>` —— 删除已上传的文件

### 会话相关命令
- `smooth start-session [OPTIONS]` —— 启动浏览器会话
- `smooth close-session -- <session-id> [--force]` —— 关闭会话
- `smooth run -- <session-id> "<task>" [OPTIONS]` —— 运行任务
- `smooth extract -- <session-id> --schema SCHEMA [OPTIONS]` —— 提取结构化数据
- `smooth evaluate-js -- <session-id> "code" [--args JSON]` —— 执行 JavaScript
- `smooth live-view -- <session-id>` —— 获取交互式实时 URL
- `smooth recording-url -- <session-id>` —— 获取录制 URL
- `smooth downloads -- <session-id>` —— 获取下载 URL

所有命令都支持 `--json` 标志，用于输出 JSON 结果。