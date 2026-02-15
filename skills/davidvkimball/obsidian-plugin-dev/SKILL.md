---
name: obsidian-plugin
description: 从零开始创建和开发 Obsidian 插件。适用于构建新的 Obsidian 插件、使用 `sample-plugin-plus` 模板作为基础，或开发插件功能。内容涵盖项目设置、manifest 配置、TypeScript 开发、设置界面（UI）、命令、功能面板（ribbons）、弹出窗口（modals），以及 Obsidian API 的使用模式。
---

# Obsidian 插件开发

使用 [obsidian-sample-plugin-plus](https://github.com/davidvkimball/obsidian-sample-plugin-plus) 模板来构建可投入生产的 Obsidian 插件。

## 快速入门：创建新插件

### 1. 从模板开始创建

```bash
# Clone the template (or use GitHub's "Use this template" button)
gh repo create my-plugin --template davidvkimball/obsidian-sample-plugin-plus --public --clone
cd my-plugin

# Or clone directly
git clone https://github.com/davidvkimball/obsidian-sample-plugin-plus.git my-plugin
cd my-plugin
rm -rf .git && git init
```

### 2. 配置插件信息

使用您的插件信息更新以下文件：

**manifest.json:**
```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "0.0.1",
  "minAppVersion": "1.5.0",
  "description": "What your plugin does",
  "author": "Your Name",
  "authorUrl": "https://yoursite.com",
  "isDesktopOnly": false
}
```

**package.json:** 更新 `name`、`description`、`author`、`license`。

**README.md:** 将模板中的内容替换为您插件的文档。

### 3. 初始化开发环境

```bash
pnpm install
pnpm obsidian-dev-skills          # Initialize AI skills
./scripts/setup-ref-links.sh      # Unix
# or: scripts\setup-ref-links.bat  # Windows
```

### 4. 删除冗余代码

在 `src/main.ts` 文件中：
- 删除示例中的功能栏图标、状态栏、命令、模态框以及 DOM 事件处理代码
- 如果需要，保留设置选项卡；否则可以删除它
- 将 `MyPlugin` 类名更改为您的插件名称

如果您的插件不需要自定义样式，请删除 `styles.css` 文件。

## 开发工作流程

### 构建和测试

```bash
pnpm dev      # Watch mode — rebuilds on changes
pnpm build    # Production build
pnpm lint     # Check for issues
pnpm lint:fix # Auto-fix issues
pnpm test     # Run unit tests
```

### 在 Obsidian 中安装插件

将构建结果复制到您的 Obsidian 仓库中：
```bash
# Unix
cp main.js manifest.json styles.css ~/.obsidian/plugins/my-plugin/

# Or create a symlink for development
ln -s $(pwd) ~/.obsidian/plugins/my-plugin
```

在 Obsidian 的设置 → 社区插件中启用该插件。

使用 [Hot Reload](https://github.com/pjeby/hot-reload) 插件来实现开发过程中的自动刷新功能。

## 插件架构

### 入口点（`src/main.ts`）

```typescript
import { Plugin } from 'obsidian';

export default class MyPlugin extends Plugin {
  settings: MyPluginSettings;

  async onload() {
    await this.loadSettings();
    // Register commands, ribbons, events, views
  }

  onunload() {
    // Cleanup: remove event listeners, views, DOM elements
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }
}
```

### 设置界面模式

请参阅 [references/settings.md](references/settings.md) 以了解完整的设置界面实现方式。

### 常见设计模式

请参阅 [references/patterns.md](references/patterns.md)，了解以下内容：
- 命令（简单命令、编辑器相关命令、检查回调）
- 功能栏图标
- 模态框
- 事件与生命周期
- 文件操作
- 编辑器操作

## 开发约束

- **禁止自动执行 Git 操作**：未经明确批准，严禁执行 `git commit` 或 `git push` 操作
- **禁止使用 `eslint-disable`**：请正确修复代码中的 lint 问题，不要忽略它们
- **禁止使用 `any` 类型**：请使用正确的 TypeScript 类型声明
- **使用大小写规范**：UI 文本应遵循大小写规则（ESLint 可能会因此产生误报——如有误报，请忽略）

## 发布前检查清单

1. 在 `manifest.json` 和 `package.json` 中更新版本信息
2. 在 `versions.json` 中设置 `version` 为当前应用的最低版本号（`minAppVersion`）
3. 运行 `pnpm build`——确保没有错误
4. 运行 `pnpm lint`——确保没有代码问题
5. 在 GitHub 上创建与版本号匹配的发布版本（不要使用 `v` 前缀）
6. 上传文件：`main.js`、`manifest.json`、`styles.css`（如果使用了自定义样式）

## 参考资料

- [设置界面](references/settings.md) — 完整的设置界面实现指南
- [常见设计模式](references/patterns.md) — 命令、模态框、事件、文件操作的相关设计模式
- [Obsidian API 文档](https://docs.obsidian.md) — 官方文档