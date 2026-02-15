---
name: ghost-cms-skill
description: 全面的 Ghost CMS 集成功能，支持博客内容的创建、发布、调度及管理，同时涵盖新闻通讯、会员信息以及数据分析。适用于需要使用 Ghost 系统进行内容创作（草稿、发布、调度）、会员/订阅者管理（层级划分、新闻通讯发送）、评论审核，以及数据分析（热门文章、订阅者增长）的场景。该集成方案支持 Ghost Admin API 的所有操作。
author: Chris Giddings
homepage: https://github.com/chrisagiddings/moltbot-ghost-skill
repository: https://github.com/chrisagiddings/moltbot-ghost-skill
metadata: {"openclaw":{"disable-model-invocation":true,"capabilities":["content-management","member-management","subscription-management","comment-management","user-management","media-management","destructive-operations","public-publishing"],"requires":{"env":["GHOST_ADMIN_KEY","GHOST_API_URL"],"bins":["node","npm"]},"primaryEnv":"GHOST_ADMIN_KEY","install":{"type":"npm","directory":"scripts","command":"npm install","dependencies":["form-data@^4.0.5","jsonwebtoken@^9.0.3"]},"credentials":{"types":[{"type":"file","locations":["~/.config/ghost/api_key","~/.config/ghost/api_url"],"description":"Ghost Admin API credentials"},{"type":"env","variables":[{"name":"GHOST_ADMIN_KEY","description":"Ghost Admin API key (JWT)","required":true},{"name":"GHOST_API_URL","description":"Ghost site URL (Ghost Pro OR self-hosted, include :PORT if needed)","required":true}]}]}}}
---

# Ghost CMS

通过 Ghost Admin API，您可以管理 Ghost 博客的内容、会员信息、分析数据以及新闻通讯。

## ⚠️ 安全警告

**Ghost Admin API 密钥可提供对您 Ghost 网站的完全访问权限：**

- **内容管理：** 创建、更新、删除、发布文章和页面
- **会员管理：** 添加、修改、删除会员和订阅信息
- **订阅管理：** 创建、修改、删除订阅层级
- **评论管理：** 回复、批准、删除评论
- **用户管理：** 邀请、修改、删除用户
- **媒体管理：** 上传图片和文件（会影响存储空间）
- **站点配置：** 修改新闻通讯和设置

**已发布的内容会立即公开**——请在发布操作时格外小心。

**安全最佳实践：**
- **安全存储 API 密钥**——使用 1Password CLI 或安全的环境变量
- **发布前审核内容**——在公开内容前务必进行检查
- **切勿将密钥提交到版本控制系统中**——避免将凭据泄露
- **定期轮换密钥**——每 90 天创建新的密钥
- **为不同用途使用不同的密钥**——为不同的集成场景分配不同的密钥
- **先在测试环境中进行测试**——如果可能的话，请在测试 Ghost 网站上进行操作

**Admin API 密钥的权限范围：**
Ghost Admin API 密钥没有权限限制选项——它们提供了对所有功能的完全访问权限。因此不存在只读密钥。

**操作类型：**

**只读操作**（✅ 安全）：
- 列出文章、页面、标签、会员、订阅层级、新闻通讯、评论
- 获取分析和会员统计数据
- 所有的 GET 请求

**破坏性操作**（⚠️ 可能修改或删除数据，内容可能会立即公开）：
- 创建/更新/删除文章、页面、标签（POST、PUT、DELETE）
- 发布/取消发布/安排文章发布（**使内容立即公开**）
- 创建/更新/删除会员、订阅层级、新闻通讯
- 创建回复、批准/删除评论
- 上传图片（会占用存储空间）
- 所有的 POST、PUT、DELETE 请求

有关详细操作说明，请参阅 [api-reference.md](references/api-reference.md)。

## 快速设置

1. **获取您的 Ghost Admin API 凭据：**
   - 登录 Ghost 控制面板 → 设置 → 集成
   - 创建一个新的“自定义集成”
   - 复制 **Admin API 密钥** 和 **API URL**

2. **安全存储凭据：**

   **选项 A：环境变量（推荐）**
   ```bash
   # Add to your shell profile (~/.zshrc, ~/.bashrc)
   export GHOST_ADMIN_KEY="YOUR_ADMIN_API_KEY"
   export GHOST_API_URL="YOUR_GHOST_URL"
   ```

   **API URL 示例（适用于所有托管类型）：**
   ```bash
   # Ghost(Pro) hosted
   export GHOST_API_URL="https://yourblog.ghost.io"
   
   # Self-hosted with reverse proxy (production)
   export GHOST_API_URL="https://blog.yourdomain.com"
   
   # Self-hosted development (Ghost default port 2368)
   export GHOST_API_URL="http://localhost:2368"
   
   # Self-hosted with custom port
   export GHOST_API_URL="https://ghost.example.com:8080"
   ```

   **重要提示：**
   - 必须包含协议（`http://` 或 `https://`）
   - 如果 Ghost 运行在非标准端口上，请包含 `:PORT`
   - 不要包含尾随的斜杠 `/ghost/api/admin`（该路径会自动添加）

   **选项 B：配置文件**
   ```bash
   mkdir -p ~/.config/ghost
   echo "YOUR_ADMIN_API_KEY" > ~/.config/ghost/api_key
   echo "YOUR_GHOST_URL" > ~/.config/ghost/api_url
   
   # Secure the files (owner read-only)
   chmod 600 ~/.config/ghost/api_key
   chmod 600 ~/.config/ghost/api_url
   ```

   **选项 C：1Password CLI（最安全的方式）**
   ```bash
   # Store key in 1Password
   op item create --category=API_CREDENTIAL \
     --title="Ghost Admin API" \
     admin_key[password]="YOUR_ADMIN_API_KEY" \
     api_url[text]="YOUR_GHOST_URL"

   # Use in commands
   export GHOST_ADMIN_KEY=$(op read "op://Private/Ghost Admin API/admin_key")
   export GHOST_API_URL=$(op read "op://Private/Ghost Admin API/api_url")
   ```

   **安全注意事项：**
   - 密钥具有对整个网站的完全访问权限——请像保护密码一样保护它们
   - 每 90 天轮换一次密钥（创建新密钥并撤销旧密钥）
   **切勿将密钥提交到 Git 或公开分享**
   **为生产环境和测试环境使用不同的密钥**
   **建议使用 HTTPS**：在生产环境中使用 HTTPS（仅限本地测试时使用 HTTP）

3. **安装依赖项：**
   ```bash
   cd ghost-cms-skill/scripts
   npm install
   ```

   **已安装的依赖项：**
   - `form-data` (^4.0.5) - 用于处理多部分文件上传（如主题 ZIP 文件）
   - `jsonwebtoken` (^9.0.3) - 用于 Ghost Admin API 认证的身份验证

   **可选依赖项**（如需可手动安装）：
   - `gscan` (^5.2.4) - 官方的 Ghost 主题验证工具（来自 TryGhost）
     - 仅用于主题验证功能
     - 安装方式：`cd scripts && npm install gscan`

   **所有依赖项均来自公共 npm 仓库，无需自定义下载。**

4. **测试连接：**
   有关详细的认证和故障排除信息，请参阅 [setup.md](references/setup.md)。

## 工具与实用程序

### Snippet Extractor（片段提取器）

**用途：** 将现有的 Ghost 片段迁移到本地库以便程序化使用。

**为什么需要这个工具？**  
Ghost Admin API 限制了通过集成令牌访问片段的功能（返回 403 Forbidden 错误）。此工具可以绕过这一限制。

**使用方法：**
```bash
# Extract snippets from a specially-formatted draft post
node scripts/snippet-extractor.js my-snippets-post

# Validate format before extracting
node scripts/snippet-extractor.js my-snippets-post --validate

# Preview without saving
node scripts/snippet-extractor.js my-snippets-post --dry-run

# Custom marker prefix
node scripts/snippet-extractor.js my-snippets-post --marker "This is:"

# Full help
node scripts/snippet-extractor.js --help
```

**工作流程：**
1. 在 Ghost 中创建草稿文章。
2. 为每个片段添加标记（例如：“SNIPPET: 名称”或“This is: 名称”）。
3. 将片段内容插入到相应的标记下方。
4. 运行提取器工具，所有片段将被保存到 `snippets/library/` 目录中。

**功能：**
- ✅ 提取所有类型的片段（书签、引用、图片、Markdown 等）
- ✅ 保持原始的词汇结构
- ✅ 自动从 `~/.config/ghost/` 或环境变量中获取认证信息
- ✅ 支持自定义标记格式
- ✅ 提供调试模式和预览功能
- ✅ 提供详细的输出信息

**示例：**
```bash
# User has 12 snippets in Ghost
# Creates "My Snippets" draft with markers
# Runs: node scripts/snippet-extractor.js my-snippets --marker "This is:"
# Result: All 12 snippets in library/ ready for use
```

有关完整文档，请参阅 `snippets/README.md`。

### Theme Manager（主题管理器）

**用途：** 程序化地上传、激活、切换和管理 Ghost 主题。

**为什么需要这个工具？**  
它可以帮助自动化主题的部署、切换以及管理主题版本。

**使用方法：**
```bash
cd scripts

# List all installed themes
node theme-manager.js list

# Upload theme ZIP
node theme-manager.js upload /path/to/theme.zip

# Upload and activate immediately
node theme-manager.js upload /path/to/theme.zip --activate

# Activate existing theme
node theme-manager.js activate theme-name

# Download theme backup
node theme-manager.js download theme-name backup.zip

# Delete theme (cannot delete active theme)
node theme-manager.js delete old-theme

# Show current active theme
node theme-manager.js active
```

**功能：**
- ✅ 从 ZIP 文件中上传自定义主题
- ✅ 在已安装的主题之间切换
- ✅ 下载主题备份
- ✅ 删除未使用的主题
- ✅ 提供验证和错误处理功能
- ✅ 主题更改会立即生效并公开

**⚠️ 重要提示：**
- 主题激活后会立即生效并公开——网站外观会立即发生变化
- 无法删除当前激活的主题（请先切换到其他主题）
- 确保使用的主题是有效的 Ghost 主题 ZIP 文件

**工作流程：**
```bash
# Safe theme switching with rollback
node theme-manager.js active              # Note current theme
node theme-manager.js activate new-theme  # Switch to new theme
# Test site in browser
node theme-manager.js activate old-theme  # Rollback if needed
```

有关完整的主题管理文档和最佳实践，请参阅 `references/themes.md`。

### Theme Validator（主题验证器）

**用途：** 在上传主题之前使用官方的 gscan 工具进行验证。

**⚠️ 可选功能：** 需要安装 `gscan` 包。安装方法：```bash
cd scripts
npm install gscan
```

**为什么需要这个工具？**  
它可以提前发现错误，例如文件缺失、语法错误或过时的辅助函数。

**使用方法：**
```bash
cd scripts

# Validate theme directory
node theme-validator.js ~/themes/my-theme/

# Validate ZIP file  
node theme-validator.js theme.zip

# Target specific Ghost version
node theme-validator.js theme.zip --version v6

# JSON output for CI/CD
node theme-validator.js theme.zip --json

# Show only errors (hide warnings)
node theme-validator.js theme.zip --errors-only
```

**功能：**
- ✅ 官方的 Ghost 验证工具（来自 TryGhost）
- ✅ 与 Ghost Admin 的验证规则相同
- ✅ 验证目录或 ZIP 文件
- ✅ 检查 Ghost v5/v6 的兼容性
- ✅ 发现过时的辅助函数和语法错误
- ✅ 支持持续集成/持续部署（CI/CD）流程
- ✅ 提供分类的错误信息（错误、警告、建议）

**验证级别：**
- **错误**：必须在上传前修复（否则主题会被拒绝）
- **警告**：建议修复以获得最佳兼容性
- **建议**：提供有用的修复建议

**安全的部署流程：**
```bash
# 1. Validate before upload
node theme-validator.js my-theme.zip

# 2. Fix any errors

# 3. Re-validate
node theme-validator.js my-theme.zip

# 4. Upload when clean
node theme-manager.js upload my-theme.zip
```

**CI/CD 集成：**
```bash
node theme-validator.js theme.zip --json
if [ $? -eq 0 ]; then
  node theme-manager.js upload theme.zip --activate
fi
```

**返回代码：** 0 = 主题有效；1 = 发现错误；2 = 参数无效

有关完整的验证文档和常见错误修复方法，请参阅 `references/themes.md`。

---

## 核心操作

本技能涵盖了 Ghost 的所有主要操作。如需详细指导，请参阅相应的参考文档：

### 内容管理
**使用场景：** 创建草稿、发布文章、安排内容发布时间、管理页面

请参阅 **[content.md](references/content.md)**，了解以下内容：
- 创建新文章（草稿）
- 发布和安排文章发布时间
- 更新现有内容
- 管理标签、特色图片、元数据
- 区分文章和页面的用法

请参阅 **[lexical-cards.md](references/lexical-cards.md)**，了解：
- **完整的 Ghost 词汇卡片类型参考**（共 23 种类型）
- 最全面的 Ghost 词汇文档
- 包含字段引用的 JSON 结构
- 支持视频、音频、文件上传、按钮、切换开关、嵌入元素
- 产品卡片、页眉、号召行动按钮、付费墙设置
- 会员可见性和内容个性化设置

**⚠️ Ghost 片段的限制：**
Ghost 的原生片段功能（保存在编辑器中的可重用内容块）**无法通过 Admin API 访问**（会返回 403 Forbidden 错误）。这意味着：
- ❌ 无法列出可用的片段
- ❌ 无法获取片段内容
- ❌ 无法程序化地使用作者已有的片段

**解决方案：** 使用 **自动片段提取工具**

该技能提供了一个 **片段提取器**，可以将 Ghost 片段迁移到本地文件：
1. 在 Ghost 中创建一个包含所有片段的草稿文章（只需设置一次）。
2. 运行提取器工具：`node scripts/snippet-extractor.js post-slug`。
3. 完成！所有片段将被保存到 `snippets/library/` 目录中，可供程序化使用。

**相关命令：**
```bash
# Extract snippets (auto-detects credentials from ~/.config/ghost/)
node scripts/snippet-extractor.js my-snippets-post

# Validate format before extracting
node scripts/snippet-extractor.js my-snippets-post --validate

# Preview without saving
node scripts/snippet-extractor.js my-snippets-post --dry-run

# Custom marker format
node scripts/snippet-extractor.js my-snippets-post --marker "This is:"

# Full help
node scripts/snippet-extractor.js --help
```

**优势：**
- ✅ 在几秒钟内迁移所有现有的 Ghost 片段
- ✅ 保持原始的词汇结构（书签、引用、图片等）
- 可通过 Git 进行版本控制
- 可在自动化文章中程序化使用这些片段
- 支持所有类型的片段

有关提取流程和本地片段使用的完整文档，请参阅 `snippets/README.md`。

### 分析与洞察
**使用场景：** 查看订阅者数量、热门内容、流量趋势

请参阅 **[analytics.md](references/analytics.md)**，了解以下内容：
- 订阅者增长和数量
- 最受欢迎的文章（浏览量和互动情况）
- 标签/主题的长期表现
- 会员订阅层级的分布情况

### 评论与互动
**使用场景：** 回复评论、管理讨论

请参阅 **[comments.md](references/comments.md)**，了解以下内容：
- 查看待处理或未回复的评论
- 回复评论
- 评论管理功能

### 会员与订阅
**使用场景：** 管理订阅层级、会员权限、高级内容

请参阅 **[members.md](references/members.md)**，了解以下内容：
- 订阅层级管理
- 仅限会员的内容设置
- 最近的会员活动
- 订阅状态

### 新闻通讯
**使用场景：** 管理新闻通讯的设置和发送邮件

请参阅 **[newsletters.md](references/newsletters.md)**，了解以下内容：
- 新闻通讯的配置
- 发送新闻通讯
- 订阅者的电子邮件设置

## API 参考

有关高级操作或端点详情，请参阅 **[api-reference.md](references/api-reference.md)**。

## 常见工作流程

**Notion → Ghost：**
1. 在 Notion 中协作编写内容草稿。
2. 完成内容后，使用本技能将其复制到 Ghost 作为草稿。
3. 在 Ghost 管理界面中审核内容。
4. 安排发布时间或直接发布。

**每周内容系列：**
1. “Navi，根据本周的讨论内容撰写并发布一篇独特的每周文章。”
2. 使用本技能创建文章，设置作者为 “Navi”，然后自动发布。

**评论管理：**
1. “是否有待处理的评论？”
2. 查看带有文章标题的评论列表。
3. “回复评论 #123，内容为 [回复内容]。”

**分析检查：**
1. “过去 6 个月里哪些标签最受欢迎？”
2. “这个月新增了多少订阅者？”
3. “我的上一篇仅限会员阅读的文章是什么时候发布的？”