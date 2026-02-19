---
name: twitter-post
description: 通过官方的 API v2（OAuth 1.0a）将推文发布到 Twitter/X。适用于用户需要发布推文、创建推文串、回复推文或引用推文的情况。该接口支持单条推文、推文串、回复以及引用推文的发送，并具备自动字符长度验证功能。
---
# 发布推文

通过官方的 Twitter/X API v2 使用 OAuth 1.0a 认证来发布推文。

## 先决条件

必须设置四个环境变量。请从 [developer.x.com](https://developer.x.com) 获取这些变量：

```
TWITTER_CONSUMER_KEY=<API Key>
TWITTER_CONSUMER_SECRET=<API Key Secret>
TWITTER_ACCESS_TOKEN=<Access Token>
TWITTER_ACCESS_TOKEN_SECRET=<Access Token Secret>
```

可选参数：
- `HTTPS_PROXY` — HTTP 代理 URL（例如 `http://127.0.0.1:7897`），适用于需要代理的地区
- `TWITTER_DRY_RUN=1` — 仅进行验证和打印，不实际发布推文

## 设置

将凭据存储为环境变量。建议将其添加到 OpenClaw 实例配置中或导出到 shell 配置文件中。**切勿在 SKILL.md 或脚本中硬编码密钥。**

如果用户尚未设置 OAuth，请指导他们按照以下步骤操作：
1. 访问 [developer.x.com](https://developer.x.com) → 仪表板 → 创建应用
2. 将应用权限设置为 **读取和写入**
3. 转到 **密钥和令牌** 选项卡
4. 复制 API 密钥和 API 密钥密钥
5. 生成访问令牌（Access Token）和访问令牌密钥密钥（确保权限为读取+写入）
6. 如果门户仅显示“读取”权限，请使用基于 PIN 的 OAuth 流程：
   - 发送 `POST /oauth/request_token` 请求，其中 `oauth_callback=oob`
   - 用户会打开 `https://api.twitter.com/oauth/authorize?oauth_token=<token>`
   - 用户输入 PIN 码
   - 发送 `POST /oauth/access_token` 请求，将 PIN 作为 `oauth_verifier` 参数

## 使用方法

所有命令均通过 `exec` 执行。脚本路径：`scripts/tweet.js`（相对于当前技能目录）。

### 发布单条推文

```bash
node scripts/tweet.js "Your tweet content here"
```

### 回复推文

```bash
node scripts/tweet.js --reply-to 1234567890 "Reply text"
```

### 引用推文

```bash
node scripts/tweet.js --quote 1234567890 "Your commentary"
```

### 发布多条推文（形成话题）

```bash
node scripts/tweet.js --thread "First tweet" "Second tweet" "Third tweet"
```

### 输出结果

输出结果以 JSON 格式显示到标准输出（stdout）：

```json
{"ok":true,"id":"123456789","url":"https://x.com/i/status/123456789","remaining":"99","limit":"100"}
```

发生错误时，输出如下内容：`{"ok":false,"error":"..."}`

## 字符限制

- 每条推文的最大字符数为 280 个
- 中文（CJK 字符，包括汉字、日文和韩文）每个字符计为 **2** 个字符
- URL 无论长度如何，每个计为 **23** 个字符
- 脚本在发布前会自动验证内容；超过字符限制时将拒绝发布

## 速率限制

- 每用户每 15 分钟最多可发布 100 条推文（使用 OAuth 1.0a 认证）
- 基础计划（每月 200 美元）下每月最多可发布 3,000 条推文
- 通过输出中的 `remaining` 字段查看剩余的发布次数

## 提示

- 如果推文内容来自 Notion 或数据库，请先获取文本，再将其传递给 `tweet.js` 脚本
- 对于基于 cron 的自动发布任务，请使用 `exec` 命令，并设置相应的环境变量；解析 JSON 输出以确认操作是否成功
- 多条推文会按顺序发布；每条推文会自动回复前一条推文
- 可同时使用 `--thread` 和 `--reply-to` 参数，在现有推文下创建新的话题