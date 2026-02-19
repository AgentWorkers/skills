---
name: line-oa
description: 通过浏览器自动化工具来操作 LINE 官方账户管理器（chat.line.biz）。当需要检查 LINE 消息、回复 LINE 客户或管理 LINE OA 聊天界面时，请使用该工具。
---
# LINE官方账户管理器

### 重要提示：
- 在执行所有浏览器操作时，务必使用`profile:"openclaw"`（独立浏览器环境），切勿使用Chrome中继。请确保所有操作使用相同的`targetId`，以避免丢失当前标签页。

## 配置
首次使用前，请检查`config.json`文件是否存在：
```
read file_path:"<skill_dir>/config.json"
```

如果文件缺失，请提示用户运行设置向导：
```bash
cd <skill_dir>
node scripts/setup.js
```

设置脚本将引导用户完成配置过程。

## 快速启动流程
当用户请求查看LINE消息时：
1. **检查配置** → 如果配置文件缺失，提示用户运行设置向导。
2. **打开浏览器** → 使用`browser action:"open"`并传入`chatUrl`。
3. **等待2秒** → 等待页面加载完成。
4. **生成快照** → 检查是否已进入聊天列表页面。
5. **如果已进入聊天列表页面**（看到聊天列表项及“点击聊天开始对话！”的提示）：
   - ✅ **继续执行“未读消息列表”步骤。
6. **如果仍在登录页面**（看到“LINE账户”或“企业账户”按钮）：
   - 完成登录流程。
   - 重新生成快照并再次检查。
   - 确认已进入聊天列表页面后，再继续执行后续操作。
7. **运行list-unread.js** → 提取并显示未读聊天记录。

**关键规则**：在执行未读消息列表功能之前，必须确认已进入聊天列表页面（步骤5）。

## 登录
**重要提示**：请按顺序执行以下步骤。每完成一个操作后，务必检查是否已进入聊天列表页面。

### 第1步：加载配置并打开浏览器
1. 从`config.json`中读取聊天URL：
   ```
   read file_path:"<skill_dir>/config.json"
   ```
   解析JSON文件并提取`chatUrl`。如果文件缺失，请提示用户先运行设置向导。
2. 打开聊天界面：
   ```
   browser action:"open" profile:"openclaw" targetUrl:"<chatUrl_from_config>"
   ```
   此操作会返回一个`targetId`——请将其保存以供后续操作使用。

### 第2步：检查是否已登录
3. 等待2秒，让页面加载完成：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"wait","timeMs":2000}
   ```

4. 生成快照以确认当前页面内容：
   ```
   browser action:"snapshot" profile:"openclaw" targetId:"<your_targetId>" refs:"aria"
   ```

5. **检查快照内容**：
   - 如果看到以下元素，则表示已登录：
     - 多个聊天项（如“John Smith”、“Alice Chen”、“Sarah Johnson”等）。
     - 文本“点击聊天开始对话！”
     - 带有“LINE官方账户管理器”标题的横幅。
     - 带有“搜索”输入框的文本框。

   **如果看到这些元素，则直接跳转到“未读消息列表”步骤。登录完成。**

### 第3步：处理登录页面（仅适用于未登录状态）
6. 如果快照显示包含“LINE账户”或“企业账户”按钮的登录页面：
   - 点击绿色的“LINE账户”按钮（请确保按钮文本为“LINE账户”或类似内容）：
     ```
     browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"<button_ref>"}
     ```

7. 等待2秒后，再次生成快照：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"wait","timeMs":2000}
   ```
   ```
   browser action:"snapshot" profile:"openclaw" targetId:"<your_targetId>" refs:"aria"
   ```

8. 如果看到“登录”或“登录”按钮，请点击它：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"<login_button_ref>"}
   ```

9. 等待3秒，直到页面重新加载：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"wait","timeMs":3000}
   ```

10. 重新生成快照，并根据步骤5中的条件再次确认是否已进入聊天列表页面。如果已进入聊天列表页面，则继续执行后续操作。

### 故障排除
- **URL检查**：如果快照中的URL包含`https://chat.line.biz/xxx`，且快照中有多个聊天链接元素，则表示已登录。
- **如果登录失败**：请提示用户在OpenClaw浏览器中手动完成身份验证后再尝试。
- **会话过期**：如果打开`chatUrl`后看到“LINE企业ID”标题或登录表单，说明会话已过期，请重新执行步骤6-10。

## 显示未读消息
该功能会从左侧聊天列表中提取未读聊天记录。无需点击每个聊天记录。

**前提条件**：用户必须已登录并进入聊天列表页面（请参考登录步骤5进行验证）。

### 操作步骤
1. 读取脚本内容：
   ```
   read file_path:"<skill_dir>/scripts/list-unread.js"
   ```
   脚本内容会被包裹在`(() => { ... })()`格式中。
2. 通过浏览器执行该脚本：
   ⚠️ **重要提示**：浏览器执行脚本时必须使用`function(){...}`格式，而非`(() => {...})()`格式。
   ❌ **错误格式**：使用`(() => {...})()`会导致脚本执行失败。
   ✅ **正确格式**：
   ```json
   {"kind":"evaluate","fn":"function(){const items=document.querySelectorAll('.list-group-item-chat');return Array.from(items).map(el=>{const h6=el.querySelector('h6');const preview=el.querySelector('.text-muted.small');const prevText=preview?.textContent?.trim()||'';const allMuted=el.querySelectorAll('.text-muted');let time='';for(const m of allMuted){const t=m.textContent.trim();if(t&&t.length<20&&t!==prevText)time=t;}const dot=el.querySelector('span.badge.badge-pin');const unread=!!dot&&getComputedStyle(dot).display!=='none';return{name:h6?.textContent?.trim()||'',time,lastMsg:prevText.substring(0,100),unread};}).filter(i=>i.name);}"}
   ```
   完整的浏览器调用方式：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"evaluate","fn":"function(){const items=document.querySelectorAll('.list-group-item-chat');return Array.from(items).map(el=>{const h6=el.querySelector('h6');const preview=el.querySelector('.text-muted.small');const prevText=preview?.textContent?.trim()||'';const allMuted=el.querySelectorAll('.text-muted');let time='';for(const m of allMuted){const t=m.textContent.trim();if(t&&t.length<20&&t!==prevText)time=t;}const dot=el.querySelector('span.badge.badge-pin');const unread=!!dot&&getComputedStyle(dot).display!=='none';return{name:h6?.textContent?.trim()||'',time,lastMsg:prevText.substring(0,100),unread};}).filter(i=>i.name);}"}
   ```

3. 脚本会返回一个包含所有聊天记录的JSON数组：`[{ name, time, lastMsg, unread }]`
   - `name`：消息发送者的显示名称。
   - `time`：聊天列表中显示的时间戳（例如“21:32”、“昨天”、“周五”）。
   - `lastMsg`：最后一条消息的预览文本（截取约100个字符）。
   - `unread`：布尔值——如果消息标记有绿色圆点，则表示未读；否则表示已读。

### 示例输出
```json
[
  {
    "name": "John Smith",
    "time": "21:32",
    "lastMsg": "Good evening! Thank you for your message. We will respond within 12 hours as this is outside our support hours.",
    "unread": false
  },
  {
    "name": "Alice Chen",
    "time": "Yesterday",
    "lastMsg": "Hello! Thank you for reaching out. Happy New Year! 🎊 I've confirmed your payment was successful ✅",
    "unread": true
  }
]
```

### 结果展示方式
- **如果有未读消息**（`unread: true`）：
  - 列出每条未读消息的发送者名称、时间和预览内容。
  - 例如：“有1条未读消息：Alice Chen（昨天）：你好！感谢你的联系！新年快乐！...”
- **如果没有未读消息**：
  - 显示：“当前没有未读消息”。

### 注意事项
- **未读提示**：每个聊天列表项中都有一个`span.badge.badge-pin`元素（绿色圆点），表示消息未读。
- **限制**：`lastMsg`显示的是聊天记录中的最后一条消息，可能是自动回复而非客户发送的原始消息。
- **查看完整聊天记录**：点击聊天项链接，聊天记录将在右侧面板中打开，并将消息标记为已读。

## 回复消息
1. 生成快照以定位目标聊天记录：
   ```
   browser action:"snapshot" profile:"openclaw" targetId:"<your_targetId>" refs:"aria"
   ```
2. 点击左侧面板中的聊天链接（例如`ref:"e68"`）：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"e68"}
   ```
3. 如果输入框被锁定（处于自动回复模式），请点击顶部横幅中的手动切换按钮解锁输入框。
4. 生成新的快照以定位输入框和发送按钮。
5. 点击文本输入框（例如`ref:"e509"`）：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"e509"}
   ```
6. 输入回复内容：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"type","ref":"e509","text":"Hello! I'm Emma, happy to help you!"}
   ```
7. 点击绿色的“发送”按钮（例如`ref:"e522"`）或按Enter键：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"e522"}
   ```

## 管理备注
每个聊天记录的右侧都有一个备注面板。备注内容仅对内部人员可见，最多可输入300个字符。

### 添加备注
1. 打开聊天记录。
2. 点击右侧面板中“备注”标题旁边的“+”按钮。
3. 在文本框中输入内容。
4. 点击“保存”。

### 修改备注
1. 在右侧面板中找到所需备注。
2. 点击备注右下角的铅笔图标。
3. 修改文本框内容。
4. 点击“保存”。

### 删除备注
1. 点击备注右下角的垃圾桶图标。
2. 出现确认对话框后，点击“删除”确认删除。

## 管理标签
标签会显示在用户名称下方的右侧面板中。标签用于对聊天记录进行分类。

### 添加标签
1. 打开聊天记录。
2. 点击右侧面板中的“添加标签”链接（或现有标签旁边的铅笔图标）。
3. 打开标签编辑框，选择所需的标签。
4. 点击“保存”。

### 删除标签
1. 打开标签编辑框。
2. 点击输入框中的“×”图标取消选中标签。
3. 点击“保存”。

## 切换账户
LINE官方账户管理器支持管理多个官方账户。可以通过左上角的账户下拉菜单在账户之间切换。
1. 生成快照以定位账户选择器：
   ```
   browser action:"snapshot" profile:"openclaw" targetId:"<your_targetId>" refs:"aria"
   ```
2. 点击账户下拉菜单（显示当前账户名称）：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"e11"}
   ```
3. 等待下拉菜单出现：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"wait","timeMs":1000}
   ```
4. 生成新的快照以查看可用账户列表：
   ```
   browser action:"snapshot" profile:"openclaw" targetId:"<your_targetId>" refs:"aria"
   ```
   列表中会显示你可访问的所有账户。请注意，每个账户都会显示名称和“管理员”或角色标签。
5. 点击所需账户（例如`ref:"e589"`）：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"click","ref":"e589"}
   ```
6. 等待页面加载新账户的聊天列表：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"wait","timeMs":2000}
   ```

### 注意事项
- LINE会定期更新会话状态；此时需要重新登录。
- 如果浏览器保持打开状态，会话通常可以持续数小时。