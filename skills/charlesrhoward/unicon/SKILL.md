---
name: unicon
description: 帮助用户使用 Unicon 图标库为他们的项目添加图标。Unicon 提供了来自 Lucide、Phosphor、Hugeicons、Heroicons、Tabler、Feather、Remix、Simple Icons（品牌标志）和 Iconoir 等来源的 19,000 多个图标。您可以使用以下方法来使用 Unicon：  
- 在 React、Vue、Svelte 或 Web 项目中添加图标；  
- 使用 unicon CLI 进行图标搜索、下载或打包；  
- 配置 `.uniconrc.json` 文件；  
- 生成可被 Tree-Shake 工具处理的图标组件；  
- 使用 Unicon API；  
- 在不同图标格式之间进行转换。
license: MIT
metadata:
  author: webrenew
  version: "0.2.0"
  website: https://unicon.sh
  repository: https://github.com/WebRenew/unicon
  openclaw:
    emoji: "🦄"
    requires:
      bins: ["node"]
    install:
      - type: node
        package: "@webrenew/unicon"
        global: true
---

# Unicon

Unicon 是一个统一的图标库，提供了来自 9 个流行图库的 19,000 多个图标。与传统的 npm 包不同，Unicon 只会生成您实际需要的图标，而不会下载数千个不必要的图标。

## 快速入门

```bash
# Install CLI globally
npm install -g @webrenew/unicon

# Or use directly with npx
npx @webrenew/unicon search "dashboard"
```

## 核心命令

| 命令 | 描述 |
|---------|-------------|
| `unicon search <查询>` | 基于 AI 的语义搜索（支持 `--pick` 选项进行交互式选择） |
| `unicon get <名称>` | 将单个图标输出到标准输出、文件或剪贴板（支持 `--copy` 选项） |
| `unicon info <名称>` | 显示图标的详细信息 |
| `unicon preview <名称>` | 在终端中预览图标的 ASCII 艺术效果 |
| `unicon bundle` | 将多个图标打包成一个文件包（支持 `--stars` 选项将图标添加到收藏夹） |
| `unicon init` | 创建 `.uniconrc.json` 配置文件（支持 `--interactive` 选项进行向导式设置） |
| `unicon sync` | 重新生成图标包（支持 `--watch` 选项实现自动同步） |
| `unicon add <名称>` | 将图标添加到配置文件中 |
| `unicon star <名称>` | 将图标添加到收藏夹 |
| `unicon audit` | 检查项目中未使用或缺失的图标 |
| `unicon sources` | 列出可用的图标库 |
| `unicon categories` | 列出图标分类 |
| `unicon cache` | 管理本地缓存 |
| `unicon skill` | 安装 AI 助手相关技能 |

## 输出格式

| 格式 | 扩展名 | 适用场景 |
|--------|-----------|----------|
| `react` | `.tsx` | React/Next.js 项目（自动识别） |
| `vue` | `.vue` | Vue 3 组件（自动识别） |
| `svelte` | `.svelte` | Svelte 组件（自动识别） |
| `svg` | `.svg` | 原始 SVG 标记 |
| `json` | `.json` | 数据处理或编程用途 |

**注意：** CLI 会根据 `package.json` 自动识别您的开发框架，并使用相应的输出格式。

## 图标来源

| 图标库 | 图标数量 | 图标特点 |
|--------|-------|-------------|
| `lucide` | 1,900 多个 | 美观且风格统一 |
| `phosphor` | 1,500 多个 | 提供多种粗细级别的图标 |
| `hugeicons` | 1,800 多个 | 现代风格的轮廓图标 |
| `heroicons` | 292 个 | 来自 Tailwind Labs 的图标 |
| `tabler` | 4,600 多个 | 精细的线条风格图标 |
| `feather` | 287 个 | 简洁明了的图标设计 |
| `remix` | 2,800 多个 | 多样化的图标分类 |
| `simple-icons` | 3,300 多个 | 品牌标识符图标 |
| `iconoir` | 1,600 多个 | 现代风格的轮廓图标 |

## 常见使用流程

### 将图标添加到 React 项目中

```bash
# 1. Initialize config (interactive wizard)
unicon init --interactive

# 2. Search for icons interactively
unicon search "navigation arrows" --pick

# 3. Add bundle to config
unicon add nav --query "arrow chevron menu"

# 4. Generate components
unicon sync

# 5. Import and use
# import { ArrowRight, Menu } from "./src/icons/nav"
```

### 快速获取单个图标

```bash
# Output to stdout (auto-detects framework)
unicon get home

# Copy to clipboard directly
unicon get home --copy

# Save to file
unicon get settings --format react -o ./Settings.tsx

# Different framework
unicon get home --format vue -o ./Home.vue
```

### 交互式搜索并选择图标

```bash
# Search and pick icons interactively
unicon search "dashboard" --pick

# Then choose action: copy, save, star, or create bundle
```

### 按类别打包图标

```bash
# Bundle all dashboard icons (tree-shakeable by default)
unicon bundle --category Dashboards -o ./src/icons

# Bundle specific icons by search
unicon bundle --query "social media" --format svg -o ./public/icons

# Bundle all favorited icons
unicon bundle --stars -o ./src/icons/favorites

# Single file mode (not tree-shakeable)
unicon bundle --query "ui" --single-file -o ./icons.tsx
```

### 收藏夹功能

```bash
# Star icons for later
unicon star home
unicon star settings
unicon star user

# Bundle all starred icons
unicon bundle --stars -o ./src/icons/favorites

# View favorites
unicon favorites
```

### 开发模式下的自动同步

```bash
# Auto-regenerate when config changes
unicon sync --watch
```

### 检查项目中的图标使用情况

```bash
# Find unused bundled icons and missing imports
unicon audit
```

### 在终端中预览图标

```bash
# ASCII art preview
unicon preview home

# Custom size
unicon preview star --width 24
```

## 与 `npm` 的区别

与 `npm install lucide-react`（该命令会下载数千个图标）相比，Unicon 有以下优势：

- **仅生成您需要的图标**，并以单独的文件形式提供 |
- **无需依赖任何外部库** |
- 采用“树摇动”（tree-shaking）技术，每个文件只包含实际使用的组件 |
- 可以按需导入：`import { Home } from "./icons";`

## Web 界面

您可以在 [https://unicon.sh](https://unicon.sh) 上浏览和复制图标：

- 支持基于 AI 的可视化搜索 |
- 一键复制图标（支持 SVG、React、Vue、Svelte 格式） |
- 可按图库和类别进行筛选 |
- 提供多图标打包功能 |

## 参考资料

- [CLI 命令](references/cli-commands.md) - 所有命令及其选项 |
- [配置文件](references/config-file.md) - `.uniconrc.json` 文件的格式规范 |
- [API 参考](references/api-reference.md) - REST API 接口说明 |

## AI 助手集成

您可以为 AI 编码助手安装 Unicon 相关技能：

```bash
# List supported assistants
unicon skill --list

# Install for specific assistant
unicon skill --ide claude      # Claude Code
unicon skill --ide cursor      # Cursor
unicon skill --ide windsurf    # Windsurf

# Install for all supported assistants
unicon skill --all
```

### 支持的 AI 助手

| 开发环境 | 技能文件路径 |
|-----|-----------|
| Claude Code | `.claude/skills/unicon/SKILL.md` |
| Cursor | `.cursor/rules/unicon.mdc` |
| Windsurf | `.windsurf/rules/unicon.md` |
| Agent | `.agent/rules/unicon.md` |
| Antigravity | `.antigravity/rules/unicon.md` |
| OpenCode | `.opencode/rules/unicon.md` |
| Codex | `.codex/unicon.md` |
| Aider | `.aider/rules/unicon.md` |

安装完成后，您可以通过 AI 助手执行如下命令：“在我的项目中添加一个首页图标”。

## 缓存机制

图标会缓存到本地 `~/.unicon/cache` 文件夹中，缓存有效期为 24 小时：

```bash
unicon cache --stats   # Show cache info
unicon cache --clear   # Clear cache
```