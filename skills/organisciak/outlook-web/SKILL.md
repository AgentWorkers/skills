---
name: outlook-web
description: **访问 Outlook Web 以进行电子邮件和日历操作**  
- 可以阅读、撰写（默认为草稿状态）电子邮件，  
- 进行搜索，  
- 以及管理电子邮件和日历事件。  
**适用场景**：  
当用户需要查看电子邮件、起草消息、搜索收件箱、查看日历或管理 Outlook 邮箱时，可以使用此功能。
allowed-tools: Bash(playwright-cli:*)
---

# Outlook Web Access 技能

该技能允许通过 `playwright-cli` 访问 Outlook Web（outlook.office.com），并支持会话的持久化管理。

## 会话配置

**所有命令必须使用**：`--session=outlook-web`

这确保了 cookie 和认证信息在命令执行之间保持一致。

## 首次认证

Microsoft 的登录过程需要用户手动操作。请按照以下步骤进行首次设置：

### 第一步：以全屏模式打开 Outlook 以触发登录
```bash
playwright-cli open "https://outlook.office.com/mail/inbox" --session=outlook-web --headed
```

浏览器将自动打开并跳转到 Microsoft 的登录页面。**请用户在该浏览器窗口中手动完成登录**。

### 第二步：验证认证

用户确认登录完成后：
```bash
playwright-cli snapshot --session=outlook-web
```

如果登录成功，快照将显示收件箱内容（邮件主题和文件夹）。如果显示登录表单，则表示认证未完成。

**注意**：初次认证后，后续命令可以以无界面的方式（默认模式）运行，因为会话 cookie 会一直保留。

## 检测会话过期

Microsoft 会话通常在 7-14 天后过期。过期的迹象包括：
- 快照显示登录表单而非收件箱内容
- 导航会重定向到登录页面

**重新认证的方法**：再次以全屏模式打开 Outlook：
```bash
playwright-cli open "https://outlook.office.com/mail/inbox" --session=outlook-web --headed
```
然后在浏览器窗口中手动完成登录。

## 关键 URL

```
Base: https://outlook.office.com

Email:
- /mail/inbox           - Inbox
- /mail/drafts          - Drafts folder
- /mail/sentitems       - Sent folder
- /mail/deleteditems    - Deleted/Trash
- /mail/archive         - Archive
- /mail/junkemail       - Junk/Spam
- /mail/search?q=TERM   - Search results
- /mail/deeplink/compose - New email composer

Calendar:
- /calendar             - Calendar view
- /calendar/view/day    - Day view
- /calendar/view/week   - Week view
- /calendar/view/month  - Month view
```

## 邮件操作

### 查看收件箱
```bash
playwright-cli open "https://outlook.office.com/mail/inbox" --session=outlook-web
playwright-cli snapshot --session=outlook-web
```

### 阅读邮件
导航到收件箱，然后点击邮件行进行选择：
```bash
playwright-cli click "EMAIL_SUBJECT_OR_SELECTOR" --session=outlook-web
playwright-cli snapshot --session=outlook-web
```

阅读窗格将显示邮件内容。

### 撰写新邮件（默认为草稿）
```bash
playwright-cli open "https://outlook.office.com/mail/deeplink/compose" --session=outlook-web
playwright-cli snapshot --session=outlook-web
```

填写相关信息：
```bash
# Add recipient
playwright-cli fill "[aria-label='To']" "recipient@example.com" --session=outlook-web

# Add subject
playwright-cli fill "[aria-label='Add a subject']" "Subject line" --session=outlook-web

# Add body (the editor area)
playwright-cli fill "[aria-label='Message body']" "Email content here" --session=outlook-web
```

**重要提示**：默认情况下，邮件会被保存为草稿，而不会立即发送：
```bash
# Save as draft (Ctrl+S or close the compose window)
playwright-cli keyboard "Control+s" --session=outlook-web
```

只有当用户明确要求时，才会发送邮件：
```bash
# Send email (only when explicitly requested by user)
playwright-cli click "[aria-label='Send']" --session=outlook-web
```

### 回复邮件

**方法 1：通过阅读窗格（简单方式）**

在阅读窗格中打开邮件后：
```bash
# Click Reply button
playwright-cli click "[aria-label='Reply']" --session=outlook-web

# Fill reply message
playwright-cli fill "[aria-label='Message body']" "Your reply text here" --session=outlook-web

# Save as draft (auto-saves, or use Ctrl+S)
playwright-cli press "Control+s" --session=outlook-web
```

**方法 2：完成回复流程**
从收件箱导航到草稿界面进行回复：
```bash
# 1. Navigate to inbox
playwright-cli open "https://outlook.office.com/mail/inbox" --session=outlook-web

# 2. Click the email (get ref from snapshot)
playwright-cli snapshot --session=outlook-web
playwright-cli click <email-ref> --session=outlook-web

# 3. Click Reply button
playwright-cli snapshot --session=outlook-web
playwright-cli click <reply-button-ref> --session=outlook-web

# 4. Fill reply
playwright-cli fill <message-body-ref> "Your reply message" --session=outlook-web

# 5. Save draft (Ctrl+S or Escape)
playwright-cli press "Control+s" --session=outlook-web
```

**方法 3：快速批量回复**
使用 `run-code` 来提高效率：
```bash
playwright-cli run-code "
  await page.goto('https://outlook.office.com/mail/inbox');
  await page.getByRole('option').first().click();
  await page.getByRole('button', { name: 'Reply', exact: true }).click();
  await page.getByRole('textbox', { name: 'Message body' }).fill('Your reply');
  await page.keyboard.press('Control+s');
" --session=outlook-web
```

**注意**：回复内容会自动保存为草稿，并带有 “Re: [原始主题]” 的格式。

### 转发邮件
```bash
playwright-cli click "[aria-label='Forward']" --session=outlook-web
playwright-cli snapshot --session=outlook-web
# Add recipient and content
```

### 删除邮件
选中邮件后：
```bash
playwright-cli click "[aria-label='Delete']" --session=outlook-web
```

### 搜索邮件
```bash
playwright-cli open "https://outlook.office.com/mail/search?q=YOUR_SEARCH_TERM" --session=outlook-web
playwright-cli snapshot --session=outlook-web
```

或者使用搜索框：
```bash
playwright-cli click "[aria-label='Search']" --session=outlook-web
playwright-cli fill "[aria-label='Search']" "search query" --session=outlook-web
playwright-cli keyboard "Enter" --session=outlook-web
playwright-cli snapshot --session=outlook-web
```

### 导航文件夹
```bash
# Drafts
playwright-cli open "https://outlook.office.com/mail/drafts" --session=outlook-web

# Sent
playwright-cli open "https://outlook.office.com/mail/sentitems" --session=outlook-web

# Deleted
playwright-cli open "https://outlook.office.com/mail/deleteditems" --session=outlook-web
```

## 日历操作

### 查看日历
```bash
playwright-cli open "https://outlook.office.com/calendar" --session=outlook-web
playwright-cli snapshot --session=outlook-web
```

### 查看特定时间范围的事件
```bash
# Day view
playwright-cli open "https://outlook.office.com/calendar/view/day" --session=outlook-web

# Week view
playwright-cli open "https://outlook.office.com/calendar/view/week" --session=outlook-web

# Month view
playwright-cli open "https://outlook.office.com/calendar/view/month" --session=outlook-web
```

### 查看事件详情
在日历视图中点击事件：
```bash
playwright-cli click "EVENT_TITLE_OR_SELECTOR" --session=outlook-web
playwright-cli snapshot --session=outlook-web
```

## 最佳实践

1. **每次导航后都生成快照** - Outlook 的加载是异步的；快照可以确认内容已准备好。
2. **必要时等待** - 如果快照显示加载中，请等待后再生成快照：
   ```bash
   playwright-cli wait 2000 --session=outlook-web
   playwright-cli snapshot --session=outlook-web
   ```
3. **使用 ARIA 标签** - Outlook 具有良好的 ARIA 标签；建议使用 `[aria-label='...']` 选择器。
4. **检查错误** - 如果操作失败，生成快照以查看当前状态。
5. **默认保存为草稿** - 未经用户确认切勿发送邮件。

## 高级用法与优化

### 使用 `run-code` 进行批量操作

为了提高编程操作的效率，可以使用 `run-code` 批量执行多个命令：
```bash
playwright-cli run-code "
  // Open inbox and reply to first email
  await page.goto('https://outlook.office.com/mail/inbox');
  await page.getByRole('option').first().click();
  await page.getByRole('button', { name: 'Reply', exact: true }).click();
  await page.getByRole('textbox', { name: 'Message body' }).fill('Your reply text');
  await page.keyboard.press('Control+s');
" --session=outlook-web
```

**优势**：比单独执行命令快 60-70%，且只占用一个进程。

### 直接导航到邮件

如果你有邮件 ID（来自 URL 或之前的快照），可以直接导航到该邮件：
```bash
# Instead of: inbox → find → click
playwright-cli open "https://outlook.office.com/mail/inbox/id/AAQkAGMxODI1MWVlLTgy..." --session=outlook-web
```

邮件 ID 通常位于 URL 中，例如：`/mail/inbox/id/<EMAIL_ID>`

### 避免不必要的快照生成

在编程使用时，仅在需要提取数据时才生成快照：
```bash
# Fast: No intermediate snapshots
playwright-cli open "https://outlook.office.com/mail/inbox" --session=outlook-web
playwright-cli click e600 --session=outlook-web
playwright-cli click "Reply" --session=outlook-web
playwright-cli fill "Message body" "Text" --session=outlook-web
# Only snapshot if you need to verify or extract data
```

### 优化资源加载速度（高级技巧）

通过屏蔽图片、字体和分析数据，可以加快页面加载速度 30-50%：
```bash
playwright-cli run-code "
  // Block non-essential resources
  await page.route('**/*', (route) => {
    const url = route.request().url();
    if (url.includes('browser.events.data.microsoft.com') ||
        url.includes('csp.microsoft.com') ||
        url.match(/\\.(png|jpg|jpeg|gif|svg|woff|woff2|ttf)$/)) {
      route.abort();
    } else {
      route.continue();
    }
  });

  // Then navigate
  await page.goto('https://outlook.office.com/mail/inbox');
" --session=outlook-web
```

**注意**：请彻底测试，因为屏蔽某些资源可能会影响功能。

### 信任自动保存功能

Outlook Web 会每隔几秒自动保存草稿。对于编程流程：
- 可以跳过前往草稿文件夹的步骤。
- 如果没有错误发生，就信任系统自动保存的草稿。
- 仅在需要时才进行验证。

### 为大型语言模型（LLM）高效提取内容

**问题**：完整的页面快照包含 60-95% 的用户界面元素（工具栏、导航栏等），而只有 5-40% 是实际内容。

**解决方案**：使用 `run-code` 仅提取所需的文本：
```bash
# Extract email list as text (no YAML overhead)
playwright-cli run-code "
  const listbox = await page.locator('[role=\"listbox\"]');
  return await listbox.innerText();
" --session=outlook-web
```

```bash
# Extract just message body text
playwright-cli run-code "
  const body = await page.locator('[role=\"document\"]').first();
  return await body.innerText();
" --session=outlook-web
```

```bash
# Extract structured data as JSON
playwright-cli run-code "
  const emails = await page.locator('[role=\"option\"]')
    .evaluateAll(opts => opts.slice(0, 10).map(o => ({
      text: o.textContent.trim(),
      unread: o.textContent.includes('Unread')
    })));
  return JSON.stringify(emails, null, 2);
" --session=outlook-web
```

**优势**：
- 减少数据量 70-90%
- 提高大型语言模型的处理速度
- 输出更简洁（文本或 JSON 格式）

**使用场景**：
- 完整快照：用于交互式探索或获取元素引用
- 文本提取：用于阅读邮件内容或处理邮件
- JSON 提取：用于批量操作或数据分析

## 故障排除

### “浏览器已在使用中” 错误
关闭现有的 `playwright` 会话：
```bash
playwright-cli close --session=outlook-web
```
然后重新尝试命令。

### 登录页面意外出现
可能是会话已过期，请重新认证：
```bash
playwright-cli open "https://outlook.office.com/mail/inbox" --session=outlook-web --headed
# User completes login in the opened browser window
```

### 内容无法加载
等待片刻后再尝试：
```bash
playwright-cli wait 3000 --session=outlook-web
playwright-cli snapshot --session=outlook-web
```

## 用户界面模式参考

请参阅 `references/ui-patterns.md`，以获取 Outlook Web 特有的元素选择器和模式。