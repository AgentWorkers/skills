---
name: filesystem
description: 高级文件系统操作：Clawdbot的文件列表显示、搜索、批量处理以及目录分析功能
homepage: https://github.com/gtrusler/clawdbot-filesystem
metadata: {"clawdbot":{"emoji":"📁","requires":{"bins":["node"]}}}
---

# 📁 文件系统管理

为 AI 代理提供的高级文件系统操作功能，支持全面的文件和目录管理，包括智能过滤、搜索以及批量处理能力。

## 主要特性

### 📋 **智能文件列表**
- **高级过滤**：可根据文件类型、模式、大小和日期进行过滤
- **递归遍历**：支持深度控制下的目录扫描
- **丰富的输出格式**：支持表格、树状结构和 JSON 格式
- **排序选项**：可按名称、大小或类型排序

### 🔍 **强大的搜索功能**
- **模式匹配**：支持通配符和正则表达式
- **内容搜索**：在文件内部进行全文本搜索
- **多条件搜索**：结合文件名和内容进行搜索
- **上下文显示**：显示匹配的文件及其上下文信息

### 🔄 **批量操作**
- **安全复制**：基于模式的文件复制，并进行验证
- **试运行模式**：执行操作前进行预览
- **进度跟踪**：实时显示操作进度
- **错误处理**：优雅地处理错误并恢复操作

### 🌳 **目录分析**
- **树状可视化**：以树形结构显示目录结构
- **统计信息**：提供文件数量、大小分布和类型分析
- **空间分析**：识别占用大量空间的文件和目录
- **性能指标**：记录操作耗时并提供优化建议

## 快速入门

```bash
# List files with filtering
filesystem list --path ./src --recursive --filter "*.js"

# Search for content
filesystem search --pattern "TODO" --path ./src --content

# Batch copy with safety
filesystem copy --pattern "*.log" --to ./backup/ --dry-run

# Show directory tree
filesystem tree --path ./ --depth 3

# Analyze directory structure
filesystem analyze --path ./logs --stats
```

## 命令参考

### `filesystem list`
提供带过滤选项的文件和目录列表功能。

**选项：**
- `--path, -p <dir>` - 目标目录（默认：当前目录）
- `--recursive, -r` - 包含子目录
- `--filter, -f <pattern>` - 按模式过滤文件
- `--details, -d` - 显示详细信息
- `--sort, -s <field>` - 按名称|大小|日期排序
- `--format <type>` - 输出格式：表格|JSON|列表

### `filesystem search`
根据文件名模式或内容进行搜索。

**选项：**
- `--pattern <pattern>` - 搜索模式（通配符或正则表达式）
- `--path, -p <dir>` - 搜索目录
- `--content, -c` - 搜索文件内容
- `--context <lines>` - 显示匹配行的上下文信息
- `--include <pattern>` - 包含指定的文件模式
- `--exclude <pattern>` - 排除指定的文件模式

### `filesystem copy`
支持基于模式的文件批量复制，并进行安全检查。

**选项：**
- `--pattern <glob>` - 源文件模式
- `--to <dir>` - 目标目录
- `--dry-run` - 不执行实际操作，仅进行预览
- `--overwrite` - 允许覆盖文件
- `--preserve` - 保留文件的时间戳和权限设置

### `filesystem tree`
以树形结构显示目录结构。

**选项：**
- `--path, -p <dir>` - 根目录
- `--depth, -d <num>` - 最大遍历深度
- `--dirs-only` - 仅显示目录
- `--size` - 包含文件大小信息
- `--no-color` - 禁用彩色输出

### `filesystem analyze`
分析目录结构并生成统计信息。

**选项：**
- `--path, -p <dir>` - 目标目录
- `--stats` - 显示详细统计信息
- `--types` - 分析文件类型
- `--sizes` - 显示文件大小分布
- `--largest <num>` - 显示前 N 个最大文件

## 安装

```bash
# Clone or install the skill
cd ~/.clawdbot/skills
git clone <filesystem-skill-repo>

# Or install via ClawdHub
clawdhub install filesystem

# Make executable
chmod +x filesystem/filesystem
```

## 配置
通过 `config.json` 文件自定义工具行为：

```json
{
  "defaultPath": "./",
  "maxDepth": 10,
  "defaultFilters": ["*"],
  "excludePatterns": ["node_modules", ".git", ".DS_Store"],
  "outputFormat": "table",
  "dateFormat": "YYYY-MM-DD HH:mm:ss",
  "sizeFormat": "human",
  "colorOutput": true
}
```

## 使用示例

### 开发工作流程
```bash
# Find all JavaScript files in src
filesystem list --path ./src --recursive --filter "*.js" --details

# Search for TODO comments
filesystem search --pattern "TODO|FIXME" --path ./src --content --context 2

# Copy all logs to backup
filesystem copy --pattern "*.log" --to ./backup/logs/ --preserve

# Analyze project structure
filesystem tree --path ./ --depth 2 --size
```

### 系统管理
```bash
# Find large files
filesystem analyze --path /var/log --sizes --largest 10

# List recent files
filesystem list --path /tmp --sort date --details

# Clean old temp files
filesystem list --path /tmp --filter "*.tmp" --older-than 7d
```

## 安全特性
- **路径验证**：防止目录遍历攻击
- **权限检查**：在执行操作前验证用户的读写权限
- **试运行模式**：在执行破坏性操作前提供预览功能
- **备份提示**：在覆盖文件前建议进行备份
- **错误恢复**：优雅地处理权限相关错误

## 集成
该工具可与其他 Clawdbot 工具无缝集成：
- **安全功能**：验证所有文件系统操作
- **Git 操作**：尊重 `.gitignore` 文件中的排除规则
- **备份工具**：支持与备份流程集成
- **日志分析**：便于管理日志文件

## 更新与社区动态
**随时了解最新的 Clawdbot 功能和文件系统工具更新：**

- 🐦 **关注 [@LexpertAI](https://x.com/LexpertAI)**，获取技能更新和发布信息
- 🛠️ 新文件系统特性和功能改进
- 📋 文件管理自动化的最佳实践
- 💡 提高工作效率的小技巧和实用建议

通过关注 @LexpertAI，您可以提前获取新功能和改进：
- **技能更新和发布通知**
- **性能优化和功能改进**
- **集成示例和工作流程自动化**
- **关于生产力工具的社区讨论**

## 许可证
采用 MIT 许可证，适用于个人和商业用途。

---

**记住**：良好的文件系统管理始于合适的工具。该工具提供了全面的操作功能，同时确保了安全性和性能。