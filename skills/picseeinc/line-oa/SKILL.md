---
name: line-oa
description: 通过浏览器自动化工具来操作 LINE 官方账户管理器（chat.line.biz）。当需要检查 LINE 消息、回复 LINE 客户或管理 LINE OA 聊天界面时，请使用该工具。
---
# LINE官方账户管理器

### 重要提示：
- **务必使用`profile:"openclaw"`（隔离浏览器环境）进行所有浏览器操作，切勿使用Chrome中继。**请确保所有操作使用相同的`targetId`，以避免丢失标签页。
- **上下文管理**：
  - 快照文件体积较大，切勿重复使用相同的数据。只需提取所需信息并立即处理，无需重新描述整个快照内容。
  - **推荐方法**：使用`snapshot refs:"aria" compact:true`来获取元素引用，然后通过`act` + `click`/`type`操作来执行具体操作。
- **避免使用`textContent.includes()`进行硬编码的判断**——由于DOM渲染时机和结构变化，这种方法不可靠。

### 自动登录脚本：
- `auto-login.mjs`是一个**参考实现**（代理程序无法直接执行）。
- `login-flow.md`是**可供代理程序执行的版本**（用于自动化操作）。
- **为何分开？**因为代理程序使用的是浏览器内置工具，而非Node模块。

#### 配置
首次使用前，请检查`config.json`文件是否存在：
```
read file_path:"skills/line-oa/config.json"
```

### 路径规则：
- 请始终使用以`skills/line-oa/`为基准的相对路径，切勿使用`../`或以`/`开头的绝对路径。

如果`config.json`文件缺失，请帮助用户运行以下命令以启动设置向导：
```bash
cd skills/line-oa
node scripts/setup.js
```

### 登录LINE官方账户管理器
这是执行后续所有操作的第一步：
1. **检查并启动浏览器服务**：
   ```
   browser action:"status"
   ```
   如果服务状态为`"running": false`，请启动浏览器服务：
   ```
   browser action:"start" profile:"openclaw"
   ```
   等待2-3秒，直到服务初始化完成。
2. **读取配置文件以获取`chatUrl`**：
   ```
   read file_path:"skills/line-oa/config.json"
   ```
   从JSON配置文件中提取`chatUrl`（例如：`https://chat.line.biz/U1234567890abcdef1234567890abcdef/`）。
3. **打开浏览器**：
   ```
   browser action:"open" profile:"openclaw" targetUrl:"<chatUrl>"
   ```
   从响应中获取`targetId`和`url`。
4. **等待页面加载完成**：
   ```
   browser action:"act" profile:"openclaw" targetId:"<targetId>" request:{"kind":"wait","timeMs":2000}
   ```
5. **检查当前URL**：
   ```
   browser action:"act" profile:"openclaw" targetId:"<targetId>" request:{"kind":"evaluate","fn":"function(){return window.location.href;}"}
   ```
   如果当前URL与`chatUrl`匹配，表示登录成功！请进入第5步；否则请进行故障排查。

#### 故障排查
如果看到登录页面（URL重定向至`account.line.biz`），请尝试以下自动化脚本：
- **点击“LINE账户”按钮**：
  ```
      read file_path:"skills/line-oa/scripts/click-line-account.js"
      ```
  直接执行相应脚本：
  ```
      browser action:"act" profile:"openclaw" targetId:"<targetId>" request:{"kind":"evaluate","fn":"<script_content>"}
      ```
  等待2秒。
- **点击“登录”按钮**：
  ```
      read file_path:"skills/line-oa/scripts/click-login.js"
      ```
  直接执行相应脚本：
  ```
      browser action:"act" profile:"openclaw" targetId:"<targetId>" request:{"kind":"evaluate","fn":"<script_content>"}
      ```
  等待3秒。
- **重新加载`chatUrl`页面**：
  ```
      browser action:"navigate" profile:"openclaw" targetId:"<targetId>" targetUrl:"<chatUrl>"
      ```
  等待2秒后，再次截图以确认左侧聊天列表是否可见。

#### 操作完成后
6. **执行用户的其他请求**。
7. **清理浏览器标签页**：
  - 打开一个空白标签页：
  ```
   browser action:"open" profile:"openclaw" targetUrl:"about:blank"
   ```
  - 获取所有标签页的内容：
  ```
   browser action:"tabs" profile:"openclaw"
   ```
  - 关闭除空白标签页（`about:blank`）之外的所有标签页：
  ```
   browser action:"close" profile:"openclaw" targetId:"<your_targetId>"
   ```
  **注意**：操作完成后务必清理标签页，以防止资源占用。空白标签页有助于保持浏览器服务的持续运行，便于下次使用。

#### 快速检查（适用于定时任务/自动化脚本）
操作流程：登录 → 查看聊天记录 → 报告结果。请严格按照以下步骤执行：
1. 读取配置文件：`read file_path:"skills/line-oa/config.json"` → 获取`chatUrl`
2. 打开浏览器：`browser action:"open" profile:"openclaw" targetUrl:<chatUrl>` → 获取`targetId`
3. 等待：`browser action:"act" profile:"openclaw" targetId:<targetId> request:{"kind":"wait","timeMs":3000}``
4. 检查URL：`browser action:"act" profile:"openclaw" targetId:<targetId> request:{"kind":"evaluate","fn":"function(){return window.location.href;}"`
   - 如果URL包含`account.line.biz`，请进入故障排查部分重新登录；否则继续下一步。
5. **直接执行以下脚本，切勿修改**：
   ```
   browser action:"act" profile:"openclaw" targetId:<targetId> request:{"kind":"evaluate","fn":"(function(){var r=document.querySelectorAll('.list-group-item-chat');return Array.from(r).map(function(e){var h=e.querySelector('h6');var p=e.querySelector('.text-muted.small');var pt=p?p.textContent.trim():'';var ms=e.querySelectorAll('.text-muted');var t='';for(var i=0;i<ms.length;i++){var v=ms[i].textContent.trim();if(v&&v.length<20&&v!==pt)t=v;}var d=e.querySelector('span.badge.badge-pin');var u=!!d&&getComputedStyle(d).display!=='none';return{name:h?h.textContent.trim():'',time:t,lastMsg:pt.substring(0,100),unread:u};}).filter(function(i){return i.name;});})()"}
   ```
   **检查点**：你是否真正调用了浏览器相关功能？如果只是考虑了但没有实际执行，请立即执行。在继续之前，必须确保已获取到操作结果。
6. **报告结果**：提取前5条聊天记录，格式为：`<名称> (<时间>) <最后一条消息> [未读]`或`[已读]`（根据`unread`字段判断）。如果数组为空，显示“当前没有聊天记录”。
7. **清理浏览器**：打开空白标签页，列出所有标签页，然后关闭除空白标签页之外的所有标签页。

#### 查看LINE聊天记录
此功能可提取左侧聊天列表中所有未读状态的聊天记录，无需逐条点击聊天记录。

**前提条件**：用户必须已登录并处于聊天列表页面（详见登录步骤）。

### 步骤：
1. 读取脚本内容：
   ```
   read file_path:"skills/line-oa/scripts/list-chats.js"
   ```
2. 通过浏览器执行脚本：
   将脚本内容作为`fn`参数传递给浏览器：
   ```
   browser action:"act" profile:"openclaw" targetId:"<your_targetId>" request:{"kind":"evaluate","fn":"<script_content>"}
   ```
3. 脚本会返回一个包含所有聊天记录的JSON数组，结构如下：
   - `name`：客户显示名称
   - `time`：时间戳（例如：“21:32”、“昨天”、“周五”
   - `lastMsg`：最后一条消息的预览内容（约100个字符）
   - `unread`：如果存在绿色圆点，则表示消息未读；否则表示已读

**可选步骤（建议执行）**：
- 为未读聊天记录获取直接链接（可加快后续操作速度）：
  - 对于每个未读聊天记录，点击该记录以获取其URL，然后返回聊天列表。
  - 等待500毫秒后，获取该聊天的URL。
  - 返回聊天列表后，等待1秒再处理下一个未读聊天记录。

#### 报告结果
- 如果存在未读聊天记录，列出每条记录的名称、时间、预览内容及URL（如果已获取）。
- 如果没有未读聊天记录，显示“当前没有未读消息”。

### 注意事项：
- **未读状态指示**：每个聊天记录项中会有一个绿色圆点（`span.badge.badge-pin`）。
- **限制**：`lastMsg`显示的是聊天记录中的最后一条消息，可能是自动回复而非客户发送的消息。
- **获取聊天链接**：需要点击未读聊天记录才能获取其URL，以便后续快速回复。

#### 查看具体聊天记录
此功能可查看任何聊天记录（无论是否已读）：
- **前提条件**：用户必须已登录并处于聊天列表页面。您需要知道客户的名称（可从`list-chats.js`或用户请求中获取）。
- **步骤**：
  - 使用`evaluate`功能按名称查找对应的聊天记录。
  - 等待消息面板加载完成。
  - 截取屏幕截图以查看聊天记录内容：
    - 左侧面板显示最新消息
    - 右侧面板显示客户信息和标签
    - 如果有自动回复，会显示相应的提示信息

#### 程序化读取最新消息
如果您需要结构化的数据而非截图，可以执行以下脚本：
- 执行该脚本以获取最新消息的详细信息：
  - 时间戳
  - 消息内容
  - `isCustomer`：表示消息来自客户
  - `hasImage`：表示消息中包含图片

#### 导航提示：
- **滚动查看旧消息**：消息面板会自动滚动到底部。
- 如需查看更早的消息，请再次截图。

### 常见问题：
- 如果消息无法加载，请将等待时间延长至3000毫秒。
- 如果客户名称包含特殊字符，请使用部分匹配（例如：“John”代替“John ⭐️”）。
- 如果点击失败，可能是因为聊天记录在当前屏幕位置不可见。

#### 处理图片：
- 如果截图中显示图片或`hasImage`为`true`，请执行以下操作：
  - 获取图片的URL。
  - 将获取到的图片保存（文件名为`line_oa_chat_YYMMDD_HHMMSS.jpg`）。

#### 回复消息
- **快捷方式**：如果之前已经获取到聊天URL，可直接跳过步骤1-2，直接执行步骤3。
- **常规步骤**（未获取聊天URL时）：
  - 获取聊天记录的URL。
  - 点击左侧面板中的聊天记录链接。
  - 如果输入框被锁定（处于自动回复状态），请点击顶部栏中的切换按钮解锁输入框。
  - 获取输入框和发送按钮的URL，然后输入回复内容。
  - 点击发送按钮。

#### 管理备注
每个聊天记录的右侧都有一个备注面板，用于记录内部信息（客户不可见）。备注最多可包含300个字符。

### 添加备注
1. 打开聊天记录。
2. 点击右侧面板中“备注”旁边的“+”按钮。
3. 在文本框中输入备注内容。
4. 点击“保存”。

### 编辑备注
1. 在右侧面板中找到对应的备注记录。
2. 点击备注右下角的铅笔图标。
3. 修改备注内容。
4. 点击“保存”。

### 删除备注
1. 点击备注右下角的垃圾桶图标。
2. 出现确认对话框后，点击“删除”确认删除。

#### 管理标签
标签用于对聊天记录进行分类：
1. 打开聊天记录。
2. 点击右侧面板中的“添加标签”链接或标签旁边的铅笔图标。
3. 打开标签编辑窗口，选择所需的标签。
4. 点击“保存”。

### 切换账户
LINE官方账户管理器支持同时管理多个账户。请使用左上角的账户下拉菜单进行切换：
1. 获取账户选择器的截图。
2. 点击账户下拉菜单（显示当前账户名称）。
3. 等待下拉菜单出现。
4. 查看列表中的可用账户。
5. 点击目标账户项（例如：`ref:"e589"`）。
6. 等待页面加载新的聊天记录列表。

### 注意事项：
- LINE会定期失效；此时需要重新登录。
- 如果浏览器保持打开状态，会话通常会持续数小时。