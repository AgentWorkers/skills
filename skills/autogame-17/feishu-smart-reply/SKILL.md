# Feishu 智能回复

根据内容分析和用户角色（persona）的上下文，智能地将消息路由到最适合的格式（卡片、帖子或文本）。

专为“Catgirl”（带有表情符号的帖子）和“Mad Dog”（带有样式化标题的卡片）模式进行了优化。

## 特点
- **自动格式选择**：
  - 包含代码块？ -> 选择 **卡片**（渲染效果更好）
  - 包含原生表情符号 `[微笑]`？ -> 选择 **帖子**（支持动画贴纸）
  - 文本过长（>500个字符）？ -> 选择 **帖子**（阅读体验更佳）
  - 默认格式？ -> 选择 **帖子**（更符合对话风格）
- **用户角色支持**：如果指定了用户角色（如 `green-tea`、`mad-dog` 等），系统会自动使用 `feishu-card/send_persona.js` 脚本。
- **安全执行**：系统会自动处理临时文件的创建，以防止shell逃逸问题。

## 使用方法

```bash
node skills/feishu-smart-reply/send.js --target "ou_..." --text "Hello world"
```

### 参数选项
- `-t, --target <id>`：目标用户/聊天ID（必需参数）。
- `-x, --text <text>`：文本内容。
- `-f, --text-file <path>`：文本文件的路径。
- `-p, --persona <type>`：用户角色模式（`default`、`green-tea`、`mad-dog`、`d-guide`、`little-fairy`）。
- `--title <text>`：可选的标题。

## 示例

**1. 包含代码块的文本（自动转换为卡片）：**
```bash
node skills/feishu-smart-reply/send.js --target "ou_..." --text "Here is code:\n\`\`\`js\nconsole.log('hi');\n\`\`\`"
```

**2. 包含表情符号的文本（自动转换为帖子）：**
```bash
node skills/feishu-smart-reply/send.js --target "ou_..." --text "好耶！[欢呼] 任务完成啦~ [撒花]"
```

**3. 使用“Mad Dog”用户角色的文本（自动转换为带有样式化标题的卡片）：**
```bash
node skills/feishu-smart-reply/send.js --target "ou_..." --text "SYSTEM CRITICAL. FIX IT NOW." --persona "mad-dog"
```