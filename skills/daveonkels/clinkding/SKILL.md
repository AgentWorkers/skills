---
name: clinkding
description: 管理链接书签：保存网址、搜索书签、添加标签、整理和检索您的个人书签集合。适用于用户需要保存链接、搜索书签、管理标签或整理阅读列表的场景。
homepage: https://github.com/daveonkels/clinkding
metadata: {"clawdis":{"emoji":"🔖","requires":{"bins":["clinkding"]},"install":[{"id":"homebrew","kind":"brew","formula":"daveonkels/tap/clinkding","bins":["clinkding"],"label":"Install clinkding (Homebrew)"},{"id":"go","kind":"go","module":"github.com/daveonkels/clinkding@latest","bins":["clinkding"],"label":"Install clinkding (Go)"}]}}
---

# clinkding - Linkding 书签管理 CLI

这是一个基于 Go 的现代 CLI 工具，用于管理 [linkding](https://github.com/sissbruecker/linkding) 中的书签。Linkding 是一个自托管的书签管理工具（类似于 Pocket 或 Instapaper）。

## 功能概述

Linkding 是一个自托管的书签管理工具，允许用户通过终端或 AI 动态代理来管理书签。clinkding 提供了以下功能：
- **保存链接以备后续阅读**：捕获用户想要阅读的网址。
- **可搜索的库**：支持对书签的标题、描述和标签进行全文搜索。
- **组织化的收藏夹**：用户可以为书签添加标签并将相关书签分组。
- **个人档案**：用户可以保存重要链接，并附上笔记和元数据。

## 快速入门

### 初始设置

```bash
# Interactive configuration
clinkding config init

# Or manually configure
clinkding config set url https://your-linkding-instance.com
clinkding config set token YOUR_API_TOKEN

# Test connection
clinkding config test
```

### 配置文件

位置：`~/.config/clinkding/config.yaml`

```yaml
url: https://linkding.example.com
token: your-api-token-here

defaults:
  bookmark_limit: 100
  output_format: auto
```

### 环境变量

```bash
export LINKDING_URL="https://linkding.example.com"
export LINKDING_TOKEN="your-api-token-here"
```

## 核心命令

### 书签操作

#### 列出和搜索书签

```bash
# List recent bookmarks
clinkding bookmarks list

# Search by keyword
clinkding bookmarks list --query "golang tutorial"

# Filter by tag
clinkding bookmarks list --query "tag:programming"

# Recent bookmarks (last 7 days)
clinkding bookmarks list --added-since "7d"

# Unread bookmarks
clinkding bookmarks list --query "unread:yes"

# JSON output for scripting
clinkding bookmarks list --json

# Plain text (tab-separated)
clinkding bookmarks list --plain
```

#### 创建书签

```bash
# Simple bookmark
clinkding bookmarks create https://go.dev

# With metadata
clinkding bookmarks create https://go.dev \
  --title "Go Programming Language" \
  --tags "golang,programming,reference" \
  --description "Official Go website" \
  --unread

# Check if URL already exists before creating
clinkding bookmarks check https://go.dev
```

#### 更新书签

```bash
# Update title
clinkding bookmarks update 42 --title "New Title"

# Add tags
clinkding bookmarks update 42 --add-tags "important,work"

# Remove tags
clinkding bookmarks update 42 --remove-tags "old-tag"

# Mark as read
clinkding bookmarks update 42 --read

# Update description
clinkding bookmarks update 42 --description "Updated notes"
```

#### 查看书签详情

```bash
# Full details
clinkding bookmarks get 42

# JSON output
clinkding bookmarks get 42 --json
```

#### 归档和删除书签

```bash
# Archive (hide from main list)
clinkding bookmarks archive 42

# Unarchive
clinkding bookmarks unarchive 42

# Delete permanently
clinkding bookmarks delete 42
```

### 标签操作

```bash
# List all tags
clinkding tags list

# Create a tag
clinkding tags create "golang"

# Get tag details
clinkding tags get 1

# Plain text output
clinkding tags list --plain
```

### 书签分组

书签分组是相关书签的集合。

```bash
# List bundles
clinkding bundles list

# Create a bundle
clinkding bundles create "Go Resources" \
  --description "Everything related to Go programming"

# Update a bundle
clinkding bundles update 1 --name "Go Lang Resources"

# Get bundle details
clinkding bundles get 1

# Delete a bundle
clinkding bundles delete 1
```

### 附件管理

用户可以上传和管理书签的附件。

```bash
# List assets for a bookmark
clinkding assets list 42

# Upload a file
clinkding assets upload 42 ~/Documents/screenshot.png

# Download an asset
clinkding assets download 42 1 -o ./downloaded-file.png

# Delete an asset
clinkding assets delete 42 1
```

### 用户信息

```bash
# Get user profile info
clinkding user profile
```

## 动态代理使用示例

### 从对话中保存链接

```bash
# User: "Save this for later: https://example.com"
clinkding bookmarks create https://example.com \
  --title "Article Title" \
  --description "Context from conversation" \
  --tags "topic,context"
```

### 搜索书签

```bash
# User: "Find my golang bookmarks"
clinkding bookmarks list --query "golang"

# User: "Show me unread programming articles"
clinkding bookmarks list --query "tag:programming unread:yes"

# User: "What did I save last week?"
clinkding bookmarks list --added-since "7d"
```

### 组织和标记书签

```bash
# User: "Tag bookmark 42 as important"
clinkding bookmarks update 42 --add-tags "important"

# User: "Create a bundle for my AI research links"
clinkding bundles create "AI Research" \
  --description "Machine learning and AI papers"
```

### 取回书签以供阅读

```bash
# User: "Give me something to read"
clinkding bookmarks list --query "unread:yes" --limit 5

# User: "Show me my golang tutorials"
clinkding bookmarks list --query "tag:golang tag:tutorial"
```

## 输出格式

- **自动格式（默认）**：适合终端显示的友好界面和颜色。
- **JSON**：适合脚本编写和代理解析的机器可读格式。
- **纯文本**：适合管道传输的文本格式（以制表符分隔）。

## 相对日期过滤

支持以下时间范围（便于用户理解）：
- `h`（小时）
- `d`（天）
- `y`（年）

## 常见工作流程

- **晨间阅读计划**
- **从剪贴板保存链接**
- **批量操作**
- **备份书签**

## 全局参数

所有命令都支持以下参数：
| 参数 | 说明 |
|------|-------------|
| `-c, --config <文件路径>` | 配置文件路径 |
| `-u, --url <链接地址>` | Linkding 服务地址 |
| `-t, --token <API 令牌>` | API 令牌 |
| `--json` | 以 JSON 格式输出 |
| `--plain` | 以纯文本格式输出 |
| `--no-color` | 禁用颜色显示 |
| `-q, --quiet` | 降低输出量 |
| `-v, --verbose` | 显示详细信息 |

## 错误代码

- `0`：成功
- `1`：一般错误（API/网络问题）
- `2`：使用错误（参数错误）
- `3`：认证错误
- `4`：未找到资源
- `130`：操作被中断（例如按下 Ctrl-C）

## 故障排除

### 测试配置

```bash
# Verify settings
clinkding config show

# Test connection
clinkding config test
```

### 常见问题

- **认证错误**：请在 Linkding 的 Web 界面验证 API 令牌。
- 确保链接地址包含协议（例如 `https://`）。
- 删除链接地址末尾的斜杠。

### 命令帮助

```bash
clinkding bookmarks --help
clinkding bookmarks create --help
```

## 链接信息

- **GitHub**：https://github.com/daveonkels/clinkding
- **Linkding**：https://github.com/sissbruecker/linkding
- **通过 Homebrew 安装**：`brew install daveonkels/tap/clinkding`

## 安装方法

- **Homebrew（macOS/Linux）**：[安装命令](```bash
brew install daveonkels/tap/clinkding
```)
- **Go 语言安装**：[安装命令](```bash
go install github.com/daveonkels/clinkding@latest
```)
- **二进制文件下载**：从 [版本页面](https://github.com/daveonkels/clinkding/releases) 下载适合您操作系统的版本。

## Shell 完成提示

---  

**开发者**：[@daveonkels](https://github.com/daveonkels)  
**许可证**：MIT 许可证  

## 智能书签创建的代理工作流程

当用户请求“将此链接添加到 Linkding”或“保存此链接”时，系统会执行以下步骤：

1. **从链接中提取元数据**：
   使用 `summarize` 功能提取链接的标题和描述：
   这将返回包含标题、描述和主要内容的结构化数据。

2. **根据内容推断合适的标签**：
   仅使用现有的标准标签。**禁止**创建新的标签。
   可用的标准标签列表（共 263 个）包括：
   - **技术**：webdev、design、programming、ai、cloud、devops、docker、linux、networking、security、privacy
   - **内容**：content、media、video、audio、books、podcasting
   - **商业**：business、marketing、ecommerce、finance、career、productivity
   - **家居**：smart-home、home-assistant、esphome、iot
   - **工具**：tools、cli、git、github、editor、reference、documentation
   - **数据**：data、analytics、mysql、nosql
   - **通信**：communication、email、messaging、slack
   - **教育**：education、guide、howto、research、testing
   - **地点**：texas、seattle、dallas

3. **使用这些规则将内容映射到标准标签**：
   - 最多使用 2-5 个标签。
   - 选择最具体的标签。
   - 如果不确定，使用更通用的标签（例如选择 `tools` 而不是 `generator`）。
   - 先检查现有标签：`clinkding tags list --plain | grep -i <关键词>`。
   - **禁止**创建如 `awesome`、`cool`、`interesting`、`resources`、`tips` 这类通用标签。

4. **使用提取的元数据创建书签**。

### 示例工作流程

**用户**：“将这个链接保存到 Linkding：https://github.com/awesome/project”

**系统操作**：
- 提取链接的元数据。
- 根据内容选择合适的标签。
- 使用提取的元数据创建书签。

### 标签映射规则

根据内容类型映射到相应的标准标签：
- **Web 开发、HTML、CSS、JavaScript**：`webdev`、`css`、`javascript`
- **React、框架、前端**：`webdev`、`react`
- **设计、UI/UX**：`design`
- **Python、Go、Ruby**：`programming`、`python`/`ruby`
- **Docker、K8s、DevOps**：`docker`、`devops`、`cloud`
- **家居自动化、ESP32、传感器**：`smart-home`、`esphome`、`iot`
- **AI、机器学习、大型语言模型**：`ai`、`llm`
- **生产力工具**：`productivity`、`tools`
- **金融、投资、加密货币**：`finance`
- **营销、SEO、广告**：`marketing`
- **购物、优惠、商店**：`ecommerce`
- **教程、指南、文档**：`guide`、`howto`、`documentation`
- **安全、隐私、加密**：`security`、`privacy`
- **地点**：`texas`、`seattle`

### 创建前的验证

在创建书签之前，系统会执行以下检查：

### 用户批量保存多个链接时的处理方式

如果用户提供了多个链接，系统会分别处理每个链接。

### 更新现有书签

当用户请求“更新该书签”或“为我的书签添加标签”时，系统会更新相应的书签信息。

### 关键原则

- **始终获取元数据**：使用 `summarize` 功能获取准确的标题和描述。
- **使用现有标签**：在创建新标签前先检查标准标签列表。
- **选择性使用标签**：最多使用 2-5 个标签，并选择最具体的标签。
- **先进行验证**：创建前检查是否存在重复的书签。
- **提供上下文**：附上简短的描述，说明保存该链接的原因。

---

## 当前标准标签结构

经过合并后，Dave 的 Linkding 服务使用了 **263 个标准标签**，这些标签是从最初的 17,189 个重复标签中整理而来的。

**使用频率最高的标签（按数量排序）：**
- `pinboard`（4,987 个）
- `ifttt`（2,639 个）
- `webdev`（1,679 个）
- `design`（561 个）
- `content`（416 个）
- `cloud`（383 个）
- **business**（364 个）
- **ecommerce**（308 个）
- **smart-home**（295 个）
- **productivity**（291 个）

**黄金法则**：如果有疑问，优先使用现有的通用标签，而不是创建新的特定标签。