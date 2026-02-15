---
name: project-tree
description: 生成 `~/projects` 文件夹的可视化目录树，并将结果更新到 `MEMORY.md` 文件中。当用户需要查看、更新项目结构，或者询问“项目树”、“树状视图”、“文件夹结构”或“显示我的项目”时，可以使用此功能。
---

# 项目结构树

## 概述

该工具会生成 `~/projects` 目录的可视化树状结构，并自动将生成的树状结构更新到 `MEMORY.md` 文件中，以反映当前的项目组织结构。该树状结构仅显示文件夹和 `.md` 文件，并会对连续编号的文件进行智能分组。

## 使用方法

运行树状结构生成脚本：

```bash
node ~/clawd/skills/project-tree/scripts/project-tree.js
```

或者使用便捷的封装脚本：

```bash
~/clawd/scripts/update-tree
```

## 主要特性

- **仅显示文件夹和 `.md` 文件**：仅显示目录和 markdown 文件，隐藏代码文件及依赖项。
- **智能分组**：能够识别连续编号的文件（例如 `script1-video`、`script2-video` 等），并将它们合并为 `script[1-28]-video/` 的形式（共 28 个文件）。
- **自动更新 `MEMORY.md`**：生成的树状结构会自动插入到 `MEMORY.md` 文件的 `PROJECT_TREE` 部分。
- **可配置的深度**：默认深度为 3 层（可通过脚本进行调整）。

## 配置

在 `scripts/project-tree.js` 文件中修改以下配置参数：

- `MAX_DEPTH`：显示的目录层级数（默认值：3）
- `EXCLUDE_DIRS`：需要跳过的目录（例如 `node_modules`、`.git` 等）
- `ROOT_DIR`：扫描的根目录（默认值：`~/projects`）

## 自动化（钩子）

你可以通过以下步骤实现项目结构树的自动更新：

### 1. 启用内部钩子

在 `clawdbot.json` 文件中添加相应的配置：

```json
{
  "hooks": {
    "internal": {
      "enabled": true
    }
  }
}
```

### 2. 创建钩子

创建 `~/.clawdbot/hooks/reset-project-tree/HOOK.md` 文件：

```markdown
---
name: reset-project-tree
description: "Generate project tree on session reset"
metadata: {"clawdbot":{"emoji":"🌳","events":["command:reset"],"requires":{"bins":["node"]}}}
---

Generates project tree when /reset is issued.
```

创建 `~/.clawdbot/hooks/reset-project-tree/handler.ts` 文件：

```typescript
import { execSync } from 'child_process';
import type { HookHandler } from '../../../src/hooks/hooks.js';

const handler: HookHandler = async (event) => {
  if (event.type !== 'command' || event.action !== 'reset') return;

  try {
    const scriptPath = `${event.context.workspaceDir}/skills/project-tree/scripts/project-tree.js`;
    execSync(`node ${scriptPath}`, { cwd: event.context.workspaceDir, stdio: 'pipe' });
    console.log('[reset-project-tree] Updated');
  } catch (err) {
    console.error('[reset-project-tree] Failed:', err instanceof Error ? err.message : String(err));
  }
};

export default handler;
```

### 3. 启用并重启 ClawDBot

完成上述配置后，需要重启 ClawDBot 以应用更改。

## 相关资源

### scripts/

- `project-tree.js`：主要的树状结构生成脚本，包含智能分组逻辑