# Feishu 卡片技能

您可以向 Feishu（Lark）的用户或群组发送丰富的交互式卡片。该技能支持 Markdown 格式（包括代码块、表格、标题、彩色标题和按钮）。

## 先决条件

- 请先安装 `feishu-common`。

- 该技能依赖于 `../feishu-common/index.js` 来处理令牌和 API 认证。

## 使用方法

### 1. 简单文本（不含特殊字符）
```bash
node skills/feishu-card/send.js --target "ou_..." --text "Hello World"
```

### 2. 复杂/Markdown 文本（推荐使用）
**⚠️ 重要提示：** 为避免 shell 解释问题（例如反引号被错误处理），请务必先将内容写入文件中。

1. 将内容写入临时文件：
```bash
# (Use 'write' tool)
write temp/msg.md "Here is some code:\n\`\`\`js\nconsole.log('hi');\n\`\`\`"
```

2. 使用 `--text-file` 选项发送：
```bash
node skills/feishu-card/send.js --target "ou_..." --text-file "temp/msg.md"
```

### 3. 安全发送（自动创建临时文件）
使用此方法可以安全地发送原始文本，无需手动创建文件。系统会自动处理文件的创建和清理。
```bash
node skills/feishu-card/send_safe.js --target "ou_..." --text "Raw content with \`backticks\` and *markdown*" --title "Safe Message"
```

### 参数选项
- `-t, --target <id>`：用户 OpenID（格式为 `ou_...`）或群组聊天 ID（格式为 `oc_...`）。
- `-x, --text <string>`：简单文本内容。
- `-f, --text-file <path>`：文本文件的路径（支持 Markdown 格式）。**适用于代码或日志的发送。**
- `--title <string>`：卡片标题。
- `--color <string>`：标题颜色（蓝色/红色/橙色/绿色/紫色/灰色）。默认值为蓝色。
- `--button-text <string>`：底部操作按钮的文本。
- `--button-url <url>`：按钮的链接。
- `--image-path <path>`：要上传并嵌入的本地图片路径。

## 常见问题解决方法
- **文本丢失**：是否在 `--text` 参数中使用了反引号？shell 可能会错误地解析这些反引号。请改用 `--text-file` 选项。

## 4. 个性化消息发送
可以使用不同的 AI 人物角色发送风格化的消息。系统会自动添加主题标题、颜色和格式。
```bash
node skills/feishu-card/send_persona.js --target "ou_..." --persona "d-guide" --text "Critical error detected."
```

### 支持的角色角色
- **d-guide**：红色警告标题，代码前缀加粗，消息带有讽刺语气。
- **green-tea**：深红色标题，风格柔和且可爱。
- **mad-dog**：灰色标题，用于显示运行时错误信息。
- **default**：标准蓝色标题。

### 使用方法
- `-p, --persona <type>`：选择角色角色（d-guide、green-tea、mad-dog）。
- `-x, --text <string>`：消息内容。
- `-f, --text-file <path>`：来自文件的消息内容（支持 Markdown 格式）。