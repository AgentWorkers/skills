# Wiki.js Skill v1.4

这是一个用于通过GraphQL API管理Wiki.js的完整命令行工具（CLI）。

## 快速入门

```bash
# Install
npm install && npm link

# Configure
cp config/wikijs.example.json ~/.config/wikijs.json
# Edit with your Wiki.js URL and API token

# Test connection
wikijs health
```

## 命令参考

### 读取操作

| 命令 | 描述 |
|---------|-------------|
| `wikijs list` | 列出所有页面 |
| `wikijs search "查询"` | 搜索页面 |
| `wikijs get <id或路径>` | 读取页面内容 |
| `wikijs info <id或路径>` | 显示页面元数据 |
| `wikijs grep "模式"` | 在页面内容中搜索 |
| `wikijs tree` | 显示页面层次结构 |

### 编写操作

| 命令 | 描述 |
|---------|-------------|
| `wikijs create <路径> <标题>` | 创建新页面 |
| `wikijs create ... --template doc` | 使用模板创建页面 |
| `wikijs update <id>` | 更新页面 |
| `wikijs move <id> <新路径>` | 移动页面 |
| `wikijs delete <id>` | 删除页面 |

### 标签操作

| 命令 | 描述 |
|---------|-------------|
| `wikijs tags` | 列出所有标签 |
| `wikijs tag <id> add <标签>` | 为页面添加标签 |
| `wikijs tag <id> remove <标签>` | 从页面移除标签 |

### 备份与恢复

| 命令 | 描述 |
|---------|-------------|
| `wikijs backup` | 创建备份 |
| `wikijs restore-backup <文件>` | 从备份中恢复 |
| `wikijs export <目录>` | 将页面内容导出为文件 |

### 版本管理

| 命令 | 描述 |
|---------|-------------|
| `wikijs versions <id>` | 查看页面版本历史 |
| `wikijs revert <id> <版本>` | 恢复到指定版本 |
| `wikijs diff <id>` | 比较两个版本的内容 |

### 资产管理

| 命令 | 描述 |
|---------|-------------|
| `wikijs images` | 列出所有图片资源 |
| `wikijs upload <文件>` | 上传图片文件 |
| `wikijs delete-image <id>` | 删除图片资源 |

### 批量操作

| 命令 | 描述 |
|---------|-------------|
| `wikijs bulk-create <文件夹>` | 从文件创建多个页面 |
| `wikijs bulk-update <文件夹>` | 批量更新多个页面 |
| `wikijs sync` | 将页面内容同步到本地 |
| `wikijs sync --watch` | 监控页面变化 |

### 分析操作

| 命令 | 描述 |
|---------|-------------|
| `wikijs tree` | 显示页面层次结构 |
| `wikijs check-links` | 检查页面中的链接是否有效 |
| `wikijs stats` | 显示页面统计信息 |
| `wikijs lint <文件>` | 代码格式检查（针对Markdown文件） |
| `wikijs lint --id <id>` | 代码格式检查（针对特定页面） |
| `wikijs orphans` | 查找没有外部链接的页面 |
| `wikijs duplicates` | 查找重复内容 |
| `wikijs toc <id>` | 生成页面目录 |
| `wikijs validate <id>` | 验证页面内容 |
| `wikijs validate --all` | 验证所有页面内容 |
| `wikijs spellcheck <id>` | 检查页面拼写错误 |

### 内容操作

| 命令 | 描述 |
|---------|-------------|
| `wikijs clone <id> <路径>` | 复制页面内容 |
| `wikijs replace "旧内容" "新内容"` | 在多个页面中替换指定内容 |
| `wikijs sitemap` | 生成XML站点地图 |

### 交互式操作

| 命令 | 描述 |
|---------|-------------|
| `wikijs shell` | 进入交互式shell模式 |
| `wikijs watch <id>` | 监控指定页面的变更 |

### 模板操作

| 命令 | 描述 |
|---------|-------------|
| `wikijs template list` | 列出所有模板 |
| `wikijs template show <名称>` | 查看模板内容 |
| `wikijs template create <名称>` | 创建新模板 |
| `wikijs template delete <名称>` | 删除模板 |

### 系统管理

| 命令 | 描述 |
|---------|-------------|
| `wikijs health` | 检查系统连接状态 |
| `wikijs cache clear` | 清除缓存 |
| `wikijs completion bash` | 提供bash命令补全功能 |

## 全局选项

| 选项 | 描述 |
|--------|-------------|
| `-v, --verbose` | 详细输出 |
| `-d, --debug` | 调试模式 |
| `--no-color` | 禁用颜色显示 |
| `--rate-limit <毫秒>` | 设置API请求速率限制 |

## 常用选项

| 选项 | 描述 |
|--------|-------------|
| `--format json` | 输出格式（JSON或表格） |
| `--limit <数量>` | 限制返回结果的数量 |
| `--force` | 强制执行操作，无需确认 |
| `--locale <语言>` | 设置显示语言 |
| `--dry-run` | 预览操作结果 |

## 示例

```bash
# Create page with template
wikijs template create doc --content "# {{title}}\n\n{{date}}"
wikijs create "/docs/api" "API Docs" --template doc

# Find broken links in docs section
wikijs check-links --path "/docs"

# Bulk import with rate limiting
wikijs --rate-limit 500 bulk-create ./pages --path-prefix "/imported"

# Watch mode for continuous sync
wikijs sync --output ~/wiki-mirror --watch --interval 60

# Debug API issues
wikijs --debug list

# Clone a page
wikijs clone 42 "/docs/new-page" --with-tags

# Find orphan pages (no incoming links)
wikijs orphans

# Search and replace across wiki
wikijs replace "oldterm" "newterm" --path "/docs" --dry-run

# Generate table of contents
wikijs toc 42 --format markdown

# Find duplicate content
wikijs duplicates --threshold 80

# Generate sitemap for SEO
wikijs sitemap --output sitemap.xml

# Interactive shell mode
wikijs shell

# Watch a page for changes
wikijs watch "/docs/api" --interval 60

# Spell check a page
wikijs spellcheck 42 --lang en --ignore "API,CLI,GraphQL"

# Validate all pages
wikijs validate --all --format json
```

## 集成说明

- 所有命令在成功执行时返回0，失败时返回1。
- 使用`--format json`选项可获取机器可读的输出格式。
- 删除操作默认需要用户确认，除非使用了`--force`选项。
- 在`--content`参数中，`\n`和`\t`等转义字符会被正确解析。
- 模板支持以下占位符：`{{title}}`、`{{path}}`、`{{date}}`。