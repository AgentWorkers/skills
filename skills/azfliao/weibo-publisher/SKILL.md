---
name: weibo-publisher
description: 使用浏览器自动化技术将帖子发布到微博（Sina Weibo）。适用于用户需要向微博发布内容、分享更新或自动化微博发布操作的场景。支持包含表情符号（emoji）、话题标签（hashtags）和提及（mentions）的文本帖子。无需API密钥，仅依赖浏览器自动化功能及用户管理的浏览器配置文件即可完成操作。
---
# 微博发布工具

使用 OpenClaw 的管理浏览器功能，通过浏览器自动化实现向微博（Sina Weibo）的自动发布。

## 前提条件

- 必须通过管理浏览器登录微博账号（profile="openclaw"）
- 浏览器必须具有有效的会话和 cookies

## 快速入门

### 基本发布

```python
# 1. Prepare content with Unicode escape (for Chinese text)
content = "刚刚解决了一个技术难题！💪"
escaped_content = content.encode('unicode_escape').decode('ascii')

# 2. Navigate to Weibo homepage
browser(action="navigate", targetUrl="https://weibo.com/", targetId=<tab_id>)

# 3. Get page snapshot to find elements
browser(action="snapshot", targetId=<tab_id>)

# 4. Click the post textbox (ref from snapshot, usually e31 or e136)
browser(action="act", request={"kind": "click", "ref": "e31"}, targetId=<tab_id>)

# 5. Type content with Unicode escape
browser(action="act", request={"kind": "type", "ref": "e31", "text": escaped_content}, targetId=<tab_id>)

# 6. Get fresh snapshot to find send button
browser(action="snapshot", targetId=<tab_id>)

# 7. Click send button (ref from snapshot, usually e32 or e194)
browser(action="act", request={"kind": "click", "ref": "e32"}, targetId=<tab_id>)

# 8. Wait and verify by navigating to profile
sleep(3)
browser(action="navigate", targetUrl="https://weibo.com/u/<your_uid>", targetId=<tab_id>)
browser(action="snapshot", targetId=<tab_id>)
```

## 元素引用

截至 2026-03-02，微博首页的常见元素引用如下：

- **主发布文本框**：`e31`（占位符：“有什么新鲜事想分享给大家？”）
- **发送按钮**：`e32`（文本：“发送”，输入内容后启用）
- **快速发布按钮**（顶部导航栏）：`e10`（文本：“发微博”）
- **快速发布文本框**（弹出窗口）：`e746`（使用快速发布功能时）
- **快速发布发送按钮**：`e804`

**重要提示**：
- 元素引用在不同会话间可能会发生变化
- 每次操作前请务必获取最新的元素引用快照
- 首页（`/`）和个人主页（`/u/<uid>`）的元素引用可能不同
- 在输入内容之前，发送按钮是禁用的

## 内容格式

### 支持的内容类型

1. **纯文本**：直接输入文本
2. **表情符号**：在文本中直接使用表情符号（例如：“😊🎉”）
3. **话题标签**：使用 `#topic#` 格式（例如：“#微博话题#”）
4. **@提及**：使用 `@username` 格式
5. **换行**：在文本中使用 `\n` 符号

### 内容限制

- 最大长度：约 2000 个字符（微博的限制）
- 建议长度：140-280 个字符，以获得更好的互动效果

## 工作流程

### 工作流程 1：简单发布

使用首页的主文本框进行快速发布：

1. 打开 `https://weibo.com/`
2. 获取元素引用快照
3. 点击文本框（e136）
4. 输入内容
5. 点击发送（e194）
6. 验证发布是否成功

### 工作流程 2：快速发布（弹出窗口）

使用“发微博”按钮进行弹出式发布：

1. 打开 `https://weibo.com/`
2. 点击“发微博”按钮（通常为 e75）
3. 获取弹出窗口的元素引用快照
4. 在弹出窗口的文本框中输入内容（e1028）
5. 点击弹出窗口的发送按钮（e1086）
6. 验证发布是否成功

### 工作流程 3：定时发布

对于需要稍后发布的帖子：

1. 按照工作流程 1 或 2 输入内容
2. 点击“定时微博”图标（时钟图标，具体位置可能不同）
3. 选择发布日期和时间
4. 点击发送

## 状态管理

在 `memory/weibo-state.json` 文件中记录发布历史：

```json
{
  "lastPublishTime": 1740880260,
  "lastPublishDate": "2026-03-02T12:38:00+08:00",
  "lastContent": "Your last post content..."
}
```

每次成功发布后，请更新此文件。

## 错误处理

### 常见问题

1. **“request: must be object” 验证错误**
   - 症状：工具 “browser” 的验证失败：`request: must be object`
   - 原因：文本中的中文引号导致 JSON 解析失败
   - 解决方案：对所有中文字符使用 Unicode 转义（详见技术细节）

2. **登录过期**
   - 症状：被重定向到登录页面
   - 解决方案：通过浏览器手动登录，然后重试

3. **发送按钮被禁用**
   - 症状：按钮带有 `disabled` 属性
   - 解决方案：检查文本框是否为空或内容是否符合规则

4. **元素引用发生变化**
   - 症状：使用旧引用时找不到元素
   - 解决方案：获取新的元素引用快照并使用更新后的引用

5. **内容被拒绝**
   - 症状：点击发送后出现错误信息
   - 解决方案：检查是否存在敏感词汇，并调整内容

6. **帖子未显示**
   - 症状：没有错误提示，但帖子未显示在时间线上
   - 解决方案：等待 5-10 秒，刷新页面，检查内容是否触发审核

## 最佳实践

1. **对中文内容始终使用 Unicode 转义**：防止因中文引号导致的 JSON 解析错误
2. **始终先获取快照**：元素引用在不同会话间可能会发生变化
3. **分步操作**：点击文本框 → 输入内容 → 获取快照 → 点击发送（不要连续操作）
4. **发布后验证**：导航到个人主页并获取快照，确认帖子已显示
5. **限制发送频率**：至少等待 60 秒后再发布，以避免被限制
6. **内容质量**：保持帖子的吸引力，使用话题标签提高可见性
7. **状态跟踪**：每次成功发布后更新 weibo-state.json 文件
8. **正确处理表情符号**：表情符号需要使用 Unicode 转义格式（例如：`\ud83d\udcaa` 表示 💪）

## 技术细节

### 浏览器自动化

- **管理浏览器**：`openclaw`
- **方法**：Chrome DevTools 协议（CDP）
- **会话**：基于 cookies，重启后仍保持
- **无需 API**：纯浏览器自动化

### 请求格式

**重要提示**：`request` 参数必须是一个 JSON 对象，而不是字符串：

```javascript
// ✅ Correct
request={"kind": "type", "ref": "e136", "text": "content"}

// ❌ Wrong
request="{\"kind\": \"type\", \"ref\": \"e136\", \"text\": \"content\"}"
```

### 中文内容的 Unicode 转义（非常重要！）

**问题**：JSON 文本中的中文引号（""、''）可能导致解析错误。

**解决方案**：对所有中文字符使用 Unicode 转义（`\uXXXX`）：

```python
# Convert Chinese text to Unicode escape
text = "刚刚解决了一个技术难题，感觉特别有成就感！"
escaped = text.encode('unicode_escape').decode('ascii')
# Result: \u521a\u521a\u89e3\u51b3\u4e86...
```

**示例**：

```javascript
// ✅ Correct - Unicode escaped
request={"kind": "type", "ref": "e31", "text": "\u521a\u521a\u89e3\u51b3\u4e86\u4e00\u4e2a\u6280\u672f\u96be\u9898"}

// ❌ Wrong - Direct Chinese with quotes
request={"kind": "type", "ref": "e31", "text": "刚刚解决了一个"技术难题""}
```

**原因**：中文引号与 JSON 字符串的分隔符冲突，导致 `request` 参数被序列化为字符串而非对象。

## 参考文件

- **[EXAMPLES.md](references/EXAMPLES.md)**：实际发布示例（包括 Unicode 转义的用法）
- **[TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)**：详细的错误解决方法（包括问题 11 和 12）
- **[UNICODE_ESCAPE.md](references/UNICODE_ESCAPE.md)**：中文内容 Unicode 转义的完整指南

## 脚本

- **[post_weibo.py](scripts/post_weibo.py)**：用于发布的独立 Python 脚本（可选）