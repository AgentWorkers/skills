---
name: portal
description: "**使用说明：**  
当需要创建门户网站、演示网站功能、进行产品体验、搭建交互式沙箱环境，或将任意 URL 转换为可共享的实时浏览器会话时，请使用该工具。Portal（makeportals.com）会在云虚拟机中启动一个真实的浏览器窗口——既不是截图，也不是视频。该工具提供两种模式：  
1. **观看模式（Watch）**：由人工智能引导的演示过程，并配有旁白说明。  
2. **播放模式（Play）**：用户可以在有安全限制的环境中自由探索网站功能。  
**不适用场景：**  
- 用于构建 HTML 页面  
- 用于生成网站原型  
- 用于创建静态网站"
---
# 门户（Portal）

可以将任何 URL 转换为可共享的实时浏览器会话。观众将在云虚拟机中看到一个真实的浏览器界面——每个会话持续 10 分钟。

## 安装（Install）

```
openclaw plugins install openclaw-portal
openclaw gateway restart
```

**观看模式（Watch Mode）**：人工智能会点击、滚动页面并进行讲解。
**播放模式（Play Mode）**：观众可以自由探索，但人工智能会限制访问某些区域。

## 快速参考（Quick Reference）

| 情况 | 操作 |
|---|---|
| 用户请求创建门户或演示网站 | 从步骤 1 开始 |
| 公共网站（登录页、文档、营销内容） | 跳过登录步骤，直接进入步骤 3 |
| 需要登录的网站（仪表板、SaaS 服务、管理员页面） | 先执行 `save_login` 操作（步骤 2） |
| 本地文件或本地主机 | 将文件压缩为 ZIP 格式，并使用 `base64` 编码，然后作为 `ptl.entry.source` 传递 |
| Chrome 扩展程序 | 将扩展程序压缩为 ZIP 格式，并设置 `entry.url` 以用于测试 |
| 用户希望观看演示 | 选择“观看模式”（Watch Mode）→ 执行 `create_script` |
| 用户希望自由探索 | 选择“播放模式”（Play Mode）→ 执行 `create_script` |
| 用户希望录制自己操作的过程 | 选择 `record_demo` → 用户将在托管的浏览器中录制 |
| 用户希望选择被屏蔽的元素 | 选择 `pick_selectors` → 用户将在托管的浏览器中点击相应元素 |
| 门户正在创建中 | 执行 `make_portal` → 等待创建结果 |
| 会话尚未完成 | 调用 `get_session` → 该操作会在服务器端阻塞 30 秒，请持续调用 |
| 需要查看会话回放 | 调用 `get_portal_sessions` → 会返回对话记录和录制 URL |
| 用户需要更多信用点数 | 选择 `buy_credits` → 系统会跳转到 Stripe 结账页面 |

## 向用户发送 URL

当任何工具返回需要用户访问的 URL（如 `verification_url`、`hosted_url` 或其他链接）时，必须将其通过聊天窗口发送给用户。  
**禁止** 使用 `open` 或 `xdg-open` 等 shell 命令来打开 URL——用户当前使用的是消息通道（如 WhatsApp、Telegram 等），而不是本地桌面环境。  
只需在回复中包含 URL，用户会在自己的设备上点击该链接即可。

## 工作流程（Workflow）

请按以下步骤操作，切勿跳过步骤 4（用户审核步骤）。

### 步骤 1：身份验证（Step 1 – Authentication）

调用 `portal_status`。如果用户尚未登录，调用 `portal_login`。  
该操作会返回 `verification_url` 和 `device_code`。**将 `verification_url` 发送给用户**，以便他们可以登录。  
每隔 5 秒使用 `device_code` 调用 `portal_login_check`，直到用户完成登录。  
新用户会获得 3 个创建信用点和 10 个观看信用点。

### 步骤 2：判断网站类型（Step 2 – Classify the Site）

**询问用户** 是否需要登录才能访问该网站：  
- **如果是公共网站**，直接进入步骤 3。  
- **如果需要登录**，请执行以下操作：  

**代码示例（Code Example）**：  
```python
save_login()
```
该操作会返回 `hosted_url`。**将 `hosted_url` 发送给用户**，以便他们可以打开托管的浏览器并登录。  
持续调用 `get_session`，直到状态变为 “ready”。**无需询问用户是否完成登录**——工具会自动通知你。登录完成后，获取 `saved_state_id`。

**如果是本地文件**，请将项目文件（排除 `node_modules`、`.git` 和 `dist` 目录）压缩为 ZIP 格式，并使用 `base64` 编码。**将压缩后的文件作为 `ptl.entry.source` 传递**，并设置 `entry.type` 为 “local_file”。

### 步骤 3：生成内容（Step 3 – Generate Content）

如果用户没有指定具体需求，提供以下 4 个选项：  
1. **观看模式（Watch Mode）**：使用人工智能脚本（适用于登录页）  
2. **观看模式（Watch Mode）**：用户自行录制操作过程  
3. **播放模式（Play Mode）**：使用人工智能选择的元素  
4. **播放模式（Play Mode）**：用户自行选择要操作的元素  

**观看模式（Watch Mode）**：  
**代码示例（Code Example）**：  
```python
create_script()
```
该操作会自动执行相关操作并返回完整的演示内容，无需再次调用 `get_script`。

**观看模式（Watch Mode）：用户录制自己操作**：  
调用 `record_demo`，并将生成的 `hosted_url` 发送给用户，以便他们在托管的浏览器中录制自己的操作。

**播放模式（Play Mode）：使用人工智能选择的元素**：  
调用 `create_script`，并设置 `mode` 为 “play”。  
**播放模式（Play Mode）：用户自行选择元素**：  
调用 `pick_selectors`，并将生成的 `hosted_url` 发送给用户，以便他们在托管的浏览器中点击相应元素。

### 步骤 4：与用户一起审核内容（Step 4 – Review with User，必选）

**切勿跳过此步骤**。**向用户展示演示内容的全部细节：**  
- **观看模式**：每个场景都会附带讲解文字和操作说明；  
- 提供示例问答对，确认用户的回答是否正确；  
- 显示人工智能生成的问候语和知识总结。  
- **播放模式**：显示被屏蔽的元素和允许访问的 URL；  
- 显示人工智能生成的问候语和知识总结。  
**询问用户**：“您希望给这个内容起什么名字？看起来可以了吗？”  
**注意**：为 URL 生成一个简洁的名称（使用小写字母、连字符，不要使用空格）。

### 步骤 5：部署门户（Step 5 – Deploy the Portal）

使用完整的 PTL 规范（PTL Specification）调用 `make_portal`。该操作需要 1 个创建信用点。  
系统会自动进行内部处理，直到门户准备就绪，然后生成最终的门户 URL 并发送给用户。

### 步骤 6：部署后的操作（Post-Deployment Operations）  

- **添加点击按钮（Add CTA Button）**：调用 `configure_portal`，并提供 `cta_text` 和 `cta_url`。  
- **获取嵌入代码片段（Get Embed Code）**：调用 `configure_embed`，并设置 `allowed_origin`。  
- **查看会话回放（View Session Replays）**：调用 `get_portal_sessions`。  
- **调试问题（Debug Issues）**：调用 `get_creation_logs`。

## PTL 规范（PTL Specification，最低要求）  

传递给 `make_portal` 的 `ptl` 参数必须是一个 JSON 对象（而非字符串）。**切勿使用 `JSON.stringify` 方法对其进行转换**。

**播放模式（Play Mode）**：  
**代码示例（Code Example）**：  
```python
# 代码示例（Play Mode）
```

**观看模式（Watch Mode）**：  
**代码示例（Code Example）**：  
```python
# 代码示例（Watch Mode）
```
服务器会自动填充 `version`、`region` 和 `entry.type` 参数。在调用 `make_portal` 之前，无需执行 `normalize_ptl` 或 `validate_ptl`——这些验证功能已内置在系统中。

## 规则（Rules）：  
- **禁止** 使用内置的画布工具来创建门户——请使用本插件提供的 `portal_*` 系列工具。  
- **切勿自行猜测 CSS 选择器**——仅使用 `create_script` 或 `pick_selectors` 返回的選擇器。  
- **切勿自动访问需要登录的网站**——对于需要登录的网站，仅获取单页内容。  
- **在创建门户之前，务必向用户展示演示内容并获取他们的确认**。  
- **持续调用 `get_session`——该操作会在服务器端阻塞 30 秒，请勿询问用户是否完成操作。**  
- **在所有点击操作中传递 `inner_text` 参数**——这是在动态页面上选择器失效时的备用方案。  
- **在当前门户创建过程中，禁止创建第二个门户**——请调用 `get_portal` 来获取最新状态。  
- **通过聊天窗口向用户发送 URL**——禁止使用 shell 命令来打开 URL。用户当前使用的是消息通道，他们会自行点击链接。