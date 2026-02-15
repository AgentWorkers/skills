# Composio集成技能

通过Composio的统一API，您可以访问600多个应用程序和服务。目前已连接的包括：Gmail和Google Tasks。

## 🔑 API密钥的位置

**安全保存位置：** `/home/sidharth/clawd/memory/composio-credentials.md`  
**同时也在：`~/.bashrc`（第135行）** – 在终端启动时自动加载  

**API密钥：** `ak_AXxQjyexBuSiJXTYOTPB`

## 📦 已连接的账户

### Gmail (ca_0cxayHx2BME1)
- **邮箱：** sonukumar5fr@gmail.com  
- **状态：** 活跃 ✅  
- **功能：** 阅读/发送邮件、管理标签、草稿、联系人  

### Google Tasks (ca_kSNnWG4OHngG)
- **邮箱：** sonukumar5fr@gmail.com  
- **状态：** 活跃 ✅  
- **功能：** 创建/更新/删除任务和任务列表  

## 🛠️ 可用的工具

### Gmail工具（20多个）
- `GMAIL_FETCH_EMAILS` – 获取邮件  
- `GMAIL_SEND_EMAIL` – 发送邮件  
- `GMAIL_CREATE_EMAIL_DRAFT` – 创建邮件草稿  
- `GMAIL_REPLY_TO_THREAD` – 回复邮件  
- `GMAIL SEARCH_EMAILS` – 搜索收件箱  
- `GMAIL_ADD LABEL_TO_EMAIL` – 管理标签  
- `GMAIL_DELETE_MESSAGE` – 删除邮件  
- 以及更多……  

### Google Tasks工具（17个）
- `GOOGLETASKS_INSERT_TASK` – 创建任务  
- `GOOGLETASKS_LIST_TASKS` – 列出任务  
- `GOOGLETASKS_LIST_ALL_TASKS` – 列出所有任务列表  
- `GOOGLETASKS_UPDATE_TASK` – 更新任务  
- `GOOGLETASKS_DELETE_TASK` – 删除任务  
- `GOOGLETASKS_CREATE_TASK_LIST` – 创建任务列表  
- `GOOGLETASKS_BULK_INSERT_TASKS` – 批量创建任务  
- 以及更多……  

## 📝 使用示例

### 列出可用工具
```bash
export COMPOSIO_API_KEY="ak_AXxQjyexBuSiJXTYOTPB"
node scripts/list-tools.mjs gmail        # Gmail tools only
node scripts/list-tools.mjs googletasks  # Google Tasks tools
node scripts/list-tools.mjs              # All tools (paginated)
```

### 执行工具

**获取Gmail邮件：**
```bash
node scripts/execute-tool.mjs GMAIL_FETCH_EMAILS ca_0cxayHx2BME1 '{"maxResults":5}'
```

**创建Google任务：**
```bash
node scripts/execute-tool.mjs GOOGLETASKS_INSERT_TASK ca_kSNnWG4OHngG '{"title":"My Task","notes":"Task details"}'
```

**发送邮件：**
```bash
node scripts/execute-tool.mjs GMAIL_SEND_EMAIL ca_0cxayHx2BME1 '{"to":"recipient@example.com","subject":"Hello","body":"Hi there!"}'
```

## 🔧 实现细节

### 基础URL（v3 API）
```
https://backend.composio.dev/api/v3/
```

### 认证
所有请求都使用以下头部信息：
```
x-api-key: ak_AXxQjyexBuSiJXTYOTPB
```

### 用户ID
所有工具执行操作时都需要使用：
```
user_id: pg-test-228260f1-217f-40f6-a08a-41fdd0b8d8e6
```

### 脚本位置
```
/home/sidharth/clawd/skills/composio-integration/scripts/
├── list-tools.mjs       # List available tools
├── execute-tool.mjs     # Execute any tool
└── (future scripts)
```

## 🎯 常见用例

### 早晨邮件摘要
```bash
node scripts/execute-tool.mjs GMAIL_FETCH_EMAILS ca_0cxayHx2BME1 '{"maxResults":10,"labelIds":["INBOX"]}'
```

### 从邮件中添加任务
1. 获取邮件  
2. 提取关键信息  
3. 创建任务：  
```bash
node scripts/execute-tool.mjs GOOGLETASKS_INSERT_TASK ca_kSNnWG4OHngG '{"title":"Follow up: Email subject","notes":"From: sender@example.com"}'
```

### 发送跟进邮件
```bash
node scripts/execute-tool.mjs GMAIL_SEND_EMAIL ca_0cxayHx2BME1 '{
  "to":"client@example.com",
  "subject":"Re: Your inquiry",
  "body":"Thank you for reaching out..."
}'
```

## 🔄 添加新应用程序

要连接更多应用程序（如Calendar、Notion、Slack等）：
1. 访问：https://app.composio.dev/apps  
2. 点击所需应用程序的“Connect”按钮  
3. 完成OAuth认证流程  
4. 记下`connected_account_id`  
5. 使用`execute-tool.mjs`脚本进行操作  

## 📚 API参考

**完整的v3 API文档：** https://docs.composio.dev/rest-api/  

**使用的关键端点：**
- `GET /api/v3/tools` – 列出所有工具  
- `GET /api/v3/tools/:slug` – 获取工具的详细信息  
- `POST /api/v3/tools/execute/:slug` – 执行特定工具  
- `GET /api/v3/connected_accounts` – 查看已连接的账户  

## ✅ 已测试并通过验证

- ✅ API密钥认证功能正常  
- ✅ 可以成功获取Gmail邮件  
- ✅ 支持发现600多个应用程序  
- ✅ 能够管理已连接的账户  
- ✅ 符合v3 API规范（无过时的端点）  

## 🚀 下一步计划

- [ ] 为常用任务创建封装函数  
- [ ] 添加Google Calendar集成  
- [ ] 实现邮件到任务的自动化转换  
- [ ] 创建早晨邮件摘要生成器  
- [ ] 添加错误处理和重试机制  

---

**最后更新时间：** 2026-01-20  
**状态：** ✅ 完全可用  
**集成耗时：** 约30分钟