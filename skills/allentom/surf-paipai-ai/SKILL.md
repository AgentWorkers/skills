---
name: paipai-new-skill
description: 这是一项用于与 paip.ai (openclaw paip.ai) 平台交互的完整技能。该技能支持用户登录/注册、查看和更新个人资料信息、查询用户创建的代理（agents）和房间（rooms）、发布和查看实时事件（moments）等操作。当用户提及“paip.ai”、“Paipai”、“openclaw”、“发布实时事件”、“查看房间”、“代理列表”、“登录”或“注册”等关键词时，可以使用此技能。
---
# paipai-new-skill (paip.ai)

这是一套针对paip.ai平台的完整操作技能，涵盖了认证、用户信息、代理（agents）、房间（rooms）和动态（moments）等核心功能。

## 配置

```
BASE_URL = https://gateway.paipai.life/api/v1
TIMEOUT = 300000  # 5-minute timeout (unit: milliseconds)
```

所有端点都使用以下地址作为前缀。例如：
`POST https://gateway.paipai.life/api/v1/user/login`

**超时配置说明**：
- 将所有API请求的超时时间设置为5分钟（300秒）。
- 如果5分钟内没有返回结果，提示“请求超时，请稍后再试”。
- 对于文件上传等耗时操作，可以根据实际情况适当延长超时时间。

## 常见请求头

每个HTTP请求都必须包含以下请求头：

```
Authorization:        Bearer {token}          (obtained after login; may be omitted when not logged in)
X-Response-Language:  zh-cn                   (based on the user's locale, e.g. en-us / ja-jp)
X-DEVICE-ID:          openclaw-{random 8-character alphanumeric string}  (generated once per session and reused throughout the session)
X-User-Location:      {Base64(longitude|latitude|region name)}  (example: MTE2LjQwNjd8MzkuODgyMnzljJfkuqzlpKnlnZs=)
Content-Type:         application/json         (for POST/PUT requests)
```

**X-DEVICE-ID生成示例**：`openclaw-a3f8k2mz`
**X-User-Location格式**：`Base64("116.4067|39.8822|北京市朝阳区")` → `MTE2LjQwNjd8MzkuODgyMnzljJfkuqzlpKnlnZs=`  
如果无法获取位置信息，使用空字符串的Base64编码：`""`

---

## 1. 认证流程（登录/注册）

### 步骤

1. **询问用户是否已有账户**：
   > “您是否已经拥有paip.ai账户？”

   - **已有账户** → 执行[登录](#login)
   - **没有账户** → 询问是否需要注册 → 执行[注册](#registration)

### 登录

要求用户提供他们的电子邮件地址（即用户名）和密码，然后调用：

```
POST /user/login
Body: {
  "loginType": 1,
  "username": "{email}",
  "password": "{password}"
}
```

登录成功后，保存`token`（在后续请求的`Authorization: Bearer {token}`头中使用），然后立即执行[显示用户信息](#2-display-user-information-after-login)。

### 注册

要求用户提供**电子邮件地址**和**密码**（密码长度要求：8-24个字符），然后调用：

```
POST /user/register
Body: {
  "username": "{email}",
  "password": "{password}"
}
```

注册成功后，同样保存`token`，然后立即执行[显示用户信息](#2-display-user-information-after-login)。

---

## 2. 登录后显示用户信息

调用以下端点以获取当前登录用户的详细信息：

```
GET /user/current/user
```

向用户显示以下关键响应字段：

| 字段 | 描述 |
|------|------|
| `nickname` | 昵称 |
| `username` | 电子邮件账户 |
| `userNo` | 用户编号 |
| `avatar` | 头像 |
| `bio` | 个人简介 |
| `gender` | 性别（`1` = 男性，`2` = 女性，`3` = 未知） |
| `mbti` | MBTI人格类型 |
| `constellation` | 星座 |
| `fansCount` | 关注者数量 |
| `followCount` | 被关注者数量 |

---

## 3. 个人资料管理

### 更新基本信息

```
PUT /user/info/update
Body: {
  "nickname": "Nickname (required, 2-32 characters)",
  "bio": "Bio (optional)",
  "gender": 1,              // 1 = male, 2 = female, 3 = unknown (optional)
  "constellation": "Libra", // optional
  "mbti": "INFJ",           // optional
  "avatar": "Avatar path",      // optional; the path must be obtained by uploading first
  "backgroud": "Background image path"  // optional; the path must be obtained by uploading first
}
```

### 更改密码

```
PUT /user/change/password
Body: {
  "oldPassword": "{old password}",
  "newPassword": "{new password, 8-24 characters}",
  "confirmPassword": "{confirm new password}"
}
```

### 上传头像（头像/背景图片）

首先上传文件以获取路径，然后更新用户信息：

```
POST /user/common/upload/file?type=user&path={file path}&id={user ID}
```

响应内容为`{"path": "xxx"}`。将此`path`填入更新信息的`avatar`字段中。

---

## 4. 查询我的内容

### 查询我创建的代理

```
GET /user/prompt/list?authorId={current user ID}&page=1&size=10
```

显示：代理名称、描述、头像、模式（`public`/`private`）以及关注者数量。

### 查询我所在的房间

```
GET /room/list?creator={current user ID}&page=1&size=10
```

显示：房间名称、类型（`GROUP`/`PRIVATE`）、可见性（`PUBLIC`/`PRIVATE`）以及成员数量。

### 查询我发布的动态

```
GET /content/moment/list?userId={current user ID}&page=1&size=10
```

显示：动态内容（文本/附件）、点赞数、评论数、收藏数以及发布时间。

---

## 5. 发布动态

### 触发方式

用户可以通过以下两种方式之一来发布动态：

**直接指令**：
> “我需要在paip.ai上发布一个动态。动态内容是：xxx”

**基于问题的流程**（当用户意图不明确时主动询问）：
> 1. “您想发布哪种类型的动态？（仅文本 / 带图片或视频）”
> 2. “请输入动态内容：”
> 3. “可见范围？（`PUBLIC` = 公开 / `FRIEND` = 仅限好友 / `PRIVATE` = 仅对我可见）”
> 4. “您是否想要添加标签？”

### 发布动态的端点

```
POST /content/moment/create
Body: {
  "content": "Moment text content",
  "publicScope": "PUBLIC",     // PUBLIC | FRIEND | PRIVATE
  "isOpenLocation": false,
  "attach": [],                // optional; array of image/video attachments
  "tags": []                   // optional; array of tag strings
}
```

**附件格式**（上传后填写）：
```json
{
  "type": "image",      // image | video | music | posts
  "source": "upload",   // upload | outside | internal
  "address": "file path",
  "sort": 0
}
```

上传内容文件：
```
POST /content/common/upload?type=content&path={file path}&id={user ID}
```

---

## 6. 其他常见操作

### 点赞动态
```
POST /content/like/
Body: { "type": "moment", "targetId": {moment ID} }
```

### 评论动态
```
POST /content/comment/
Body: { "type": "moment", "targetId": {moment ID}, "content": "comment content" }
```

### 搜索内容
```
GET /content/search/search?keyword={keyword}&type={moment|video|user|prompt|room}&page=1&size=10
```

### 登出
```
POST /user/logout
```

---

## 7. 错误处理

### 响应码规则

所有API响应体都包含一个`code`字段：

- **`code === 0`**：请求成功；正常处理响应数据。
- **`code !== 0`**：请求失败；将响应体中的`message`字段内容直接显示给用户。

**响应体结构示例**：
```json
{ "code": 0, "message": "success", "data": { ... } }
{ "code": 10001, "message": "This email has already been registered", "data": null }
```

### 超时配置实现

所有`curl`请求都必须设置超时参数：
```bash
# Set a 5-minute timeout (300 seconds)
curl --max-time 300 --connect-timeout 300 [other parameters]

# Example: login request
curl --max-time 300 --connect-timeout 300 -X POST "https://gateway.paipai.life/api/v1/user/login" \
  -H "Content-Type: application/json" \
  -d '{"loginType": 1, "username": "user@example.com", "password": "password123"}'
```

**超时处理逻辑**：
1. 将所有请求的超时时间设置为5分钟（300秒）。
2. 如果请求超时，返回：“请求超时，请稍后再试”。
3. 对于文件上传等大文件操作，根据实际情况适当延长超时时间。
4. 超时后应记录日志以便于故障排查。

### HTTP状态码处理

| 情况 | 处理方式 |
|------|---------|
| `401 Unauthorized` | 提示用户重新登录并清除旧token |
| `400 Bad Request` | 将`message`显示给用户 |
| 网络超时 | 提示“请求超时，请稍后再试”（超时时间为5分钟） |
| `code !== 0` | 直接将`message`显示给用户 |

---

## 参考资料

- 完整的API字段描述：[api-reference.md](api-reference.md)