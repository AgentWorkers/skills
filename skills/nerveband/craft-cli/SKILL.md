# Craft CLI 技能

通过 `craft` CLI 工具与 Craft 文档进行交互。该工具响应迅速、高效且支持大语言模型（LLM）的使用。

## 安装

`craft` CLI 可执行文件应安装在 `/usr/local/bin/craft` 目录下。

如果尚未安装：
```bash
curl -L https://github.com/nerveband/craft-cli/releases/download/v1.0.0/craft-darwin-arm64 -o craft
chmod +x craft
sudo mv craft /usr/local/bin/
```

## 配置

目前有两个 Craft 空间可供使用：

### wavedepth 空间（商业用途）
```bash
~/clawd/skills/craft-cli/craft config set-api https://connect.craft.do/links/5VruASgpXo0/api/v1
```

### 个人空间
```bash
~/clawd/skills/craft-cli/craft config set-api https://connect.craft.do/links/HHRuPxZZTJ6/api/v1
```

### 快速切换（辅助脚本）
```bash
# Switch to wavedepth space
~/clawd/skills/craft-cli/craft-helper.sh wavedepth

# Switch to personal space
~/clawd/skills/craft-cli/craft-helper.sh personal

# Check current space
~/clawd/skills/craft-cli/craft-helper.sh current
```

**检查当前配置：**
```bash
~/clawd/skills/craft-cli/craft config get-api
```

## 命令

### 列出文档
```bash
# JSON format (default - LLM-friendly)
~/clawd/skills/craft-cli/craft list

# Human-readable table
~/clawd/skills/craft-cli/craft list --format table

# Markdown format
~/clawd/skills/craft-cli/craft list --format markdown
```

### 搜索文档
```bash
# Search for documents
~/clawd/skills/craft-cli/craft search "query terms"

# With table output
~/clawd/skills/craft-cli/craft search "query" --format table
```

### 获取文档
```bash
# Get document by ID (JSON)
~/clawd/skills/craft-cli/craft get <document-id>

# Save to file
~/clawd/skills/craft-cli/craft get <document-id> --output document.md

# Different format
~/clawd/skills/craft-cli/craft get <document-id> --format markdown
```

### 创建文档
```bash
# Create with title only
~/clawd/skills/craft-cli/craft create --title "My New Document"

# Create from file
~/clawd/skills/craft-cli/craft create --title "My Document" --file content.md

# Create with inline markdown
~/clawd/skills/craft-cli/craft create --title "Quick Note" --markdown "# Hello\nThis is content"

# Create as child of another document
~/clawd/skills/craft-cli/craft create --title "Child Doc" --parent <parent-id>
```

### 更新文档
```bash
# Update title
~/clawd/skills/craft-cli/craft update <document-id> --title "New Title"

# Update from file
~/clawd/skills/craft-cli/craft update <document-id> --file updated-content.md

# Update with inline markdown
~/clawd/skills/craft-cli/craft update <document-id> --markdown "# Updated\nNew content"

# Update both title and content
~/clawd/skills/craft-cli/craft update <document-id> --title "New Title" --file content.md
```

### 删除文档
```bash
~/clawd/skills/craft-cli/craft delete <document-id>
```

### 信息查询命令
```bash
# Show API info and recent documents
~/clawd/skills/craft-cli/craft info

# List all available documents
~/clawd/skills/craft-cli/craft docs
```

### 查看版本信息
```bash
~/clawd/skills/craft-cli/craft version
```

## 输出格式

- **json**（默认）：机器可读的 JSON 格式，适合大语言模型和脚本使用
- **table**：人类可读的表格格式
- **markdown**：Markdown 格式的输出

您可以在配置文件中设置默认输出格式，或通过 `--format` 标志在每次命令执行时指定输出格式。

## API URL 覆盖

您可以覆盖已配置的 API URL，适用于任何命令：
```bash
~/clawd/skills/craft-cli/craft list --api-url https://connect.craft.do/links/ANOTHER_LINK/api/v1
```

## 错误处理

CLI 会提供清晰的错误信息以及相应的退出代码：

- **退出代码 0**：操作成功
- **退出代码 1**：用户错误（输入无效、参数缺失）
- **退出代码 2**：API 错误（服务器端问题）
- **退出代码 3**：配置错误

常见错误：
- `authentication failed. Check API URL`：API URL 无效或未授权
- `resource not found`：文档 ID 不存在
- `rate limit exceeded. Retry later`：请求次数过多
- `no API URL configured. Run 'craft config set-api <url>' first`：配置文件中未设置 API URL

## 使用示例

### 工作流程：列出和搜索文档
```bash
# List all documents in wavedepth space
~/clawd/skills/craft-cli/craft config set-api https://connect.craft.do/links/5VruASgpXo0/api/v1
~/clawd/skills/craft-cli/craft list --format table

# Search for specific documents
~/clawd/skills/craft-cli/craft search "proposal" --format table
```

### 工作流程：创建和更新文档
```bash
# Create a new document
~/clawd/skills/craft-cli/craft create --title "Project Notes" --markdown "# Initial notes\n\nStart here."

# Get the document ID from output, then update
~/clawd/skills/craft-cli/craft update <doc-id> --title "Updated Project Notes"

# Verify the update
~/clawd/skills/craft-cli/craft get <doc-id> --format markdown
```

### 工作流程：导出文档
```bash
# Get a specific document and save to file
~/clawd/skills/craft-cli/craft get <doc-id> --output exported-notes.md
```

### 与大语言模型的集成
```bash
# Get all documents as JSON (pipe to processing)
~/clawd/skills/craft-cli/craft list | jq '.[] | {id, title}'

# Search and extract specific fields
~/clawd/skills/craft-cli/craft search "meeting" | jq '.[].title'
```

## 提示

1. **默认使用 JSON 格式**，以便大语言模型读取
2. **向用户展示结果时使用表格格式**
3. **执行操作前请检查配置**：`craft config get-api`
4. **使用 `craft config set-api <url>` 轻松切换空间**
5. **使用 `--api-url` 标志临时覆盖 API URL，无需修改配置文件**

## GitHub 仓库

源代码和文档：https://github.com/nerveband/craft-cli

## 版本

当前版本：1.6.0