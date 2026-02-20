---
name: clawpost
description: 通过Claw Post API将推文发布到X（Twitter）上。适用于用户需要向X（Twitter）发布推文或分享内容的情况。
metadata: {"openclaw":{"primaryEnv":"CLAWPOST_API_KEY","homepage":"https://clawpost.net/api-docs"}}
---
# Claw Post

该功能使用 Claw Post API 将推文发布到 X（Twitter）平台。用户需要安装并配置相应的浏览器扩展程序来执行发布操作。

## 前提条件（用户需完成以下步骤）：

在开始发布推文之前，用户必须：

1. **在 clawpost.net 上注册**。
2. **安装 Claw Post Chrome 扩展程序**。
3. 在控制面板中完成扩展程序的配对操作（输入扩展程序弹窗中显示的 6 位代码）。
4. 将从控制面板获取的 API 密钥提供给代理程序（或下载包含 API 密钥的文件）。
5. 至少登录一次 X（Twitter）平台。

如果代理程序收到 `EXTENSION_NOT_PAIRED` 或 `not_logged_in` 的错误信息，需引导用户完成上述步骤。

## API 基本 URL

请使用以下 URL：**```
https://claw-post-api-ukpr57vsgq-uc.a.run.app
```**。请勿使用 `api.clawpost.net` 或其他类似的 URL。

## 所需输入参数：

- **API 密钥**：在请求头中设置 `clawpost-api-key`（详见下方说明；或通过 OpenClaw 配置文件设置 `CLAWPOST_API_KEY`）。
- **推文内容**：推文的文本内容（必填）。

## 工作流程：

1. 发送 POST 请求以创建一个新的推文任务。
2. 定期调用 `GET /v1/jobs/:id` 接口查询任务状态，直到状态变为 `succeeded` 或 `failed`。

### 创建推文

```
POST https://claw-post-api-ukpr57vsgq-uc.a.run.app/v1/jobs/tweet
Header: clawpost-api-key: claw_00befabe022666a86f18effea768fd40531b5c132ade52d3
Content-Type: application/json
Body: { "text": "<tweet content>" }
```

可选的推文正文字段：
- `mediaPaths`：URL 列表（需先通过 `POST https://claw-post-api-ukpr57vsgq-uc.a.run.app/v1/media/upload` 上传媒体文件）。
- `idempotencyKey`：用于防止推文重复发布的唯一字符串。

### 查询任务状态

```
GET https://claw-post-api-ukpr57vsgq-uc.a.run.app/v1/jobs/:id
```

任务状态：`queued` → `processing` → `succeeded` | `failed`

## 错误处理：

| 错误代码 | 原因 | 处理方式 |
|------|-------|--------|
| 401 | API 密钥无效或缺失 | 请检查请求头中的 `clawpost-api-key`。|
| 503 | 扩展程序未配对 | 用户需要安装 Claw Post 扩展程序并在 clawpost.net/dashboard 上完成配对操作。|
| `not_logged_in` | 用户未登录 X 平台 | 请用户登录 x.com。|
| `no_x_tab` | 扩展程序无法打开 X 页面 | 请用户刷新 x.com 页面。|
| `content_script_unavailable` | 扩展程序无法访问 X 页面的相关内容 | 请用户刷新 x.com 页面。|
| `selector_not_found` | X 平台的 UI 发生变化 | 请稍后重试。|

如果请求失败，请再次调用 `GET /v1/jobs/:id` 接口，查看详细的错误信息（`error` 和 `errorCode`）。

## 参考资料：

完整的 API 文档：https://clawpost.net/api-docs