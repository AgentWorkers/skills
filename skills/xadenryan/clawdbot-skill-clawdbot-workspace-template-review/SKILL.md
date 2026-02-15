---
name: clawdbot-workspace-template-review
description: 将 Clawdbot 的工作空间与通过 `npm` 或源代码安装的官方模板进行比较，列出需要添加的缺失部分，尤其是在升级之后。
---

# 工作区模板差异对比

当用户希望将自己的工作区 `.md` 文件（包括 AGENTS、SOUL、USER、IDENTITY、TOOLS、HEARTBEAT 等部分）与官方 Clawdbot 模板进行对比时，可以使用此技能，从而查看缺失的部分并决定需要添加哪些内容。

## 查找官方模板

找到已安装的 Clawdbot 源代码目录：

- 如果 Clawdbot 是通过 npm/pnpm 全局安装的：
  - 输入 `command -v clawdbot`，查看安装信息。
  - 如果安装路径显示为 `.../node_modules/.bin/`，则实际安装路径应为 `node_modules/clawdbot`。
  - 或者使用 `npm root -g` / `pnpm root -g` 命令，然后在输出目录中查找 `clawdbot` 文件夹。
- 如果 Clawdbot 是从源代码直接编译运行的，请使用该编译后的目录（该目录必须包含 `package.json` 文件）。

官方模板存储的位置如下：

```
<clawdbot-root>/docs/reference/templates/
```

如果无法找到源代码目录，请询问用户 Clawdbot 的安装位置。

## 对比流程

1. 确定工作区的根目录（即用户的“本地版本”目录）。
2. 遍历 `docs/reference/templates` 目录中的每个模板文件（排除 `*.dev.md` 文件）：
   - 打开官方模板和具有相同名称的工作区文件。
   - 忽略模板文件的开头部分（`---` 标签）以及任何“首次运行”或“引导”相关的内容。
   - 比较剩余的部分，并列出所有缺失的模块或内容。

**推荐使用的 CLI 工具（如 `diff`）**：

```
ls <clawdbot-root>/docs/reference/templates
sed -n '1,200p' <clawdbot-root>/docs/reference/templates/AGENTS.md
sed -n '1,200p' <workspace>/AGENTS.md
diff -u <clawdbot-root>/docs/reference/templates/AGENTS.md <workspace>/AGENTS.md
```

在报告差异时，请按照以下步骤操作：
- 逐条列出官方模板中缺失的内容。
- 简要说明这些内容的重要性，并询问用户是否需要将这些内容添加到工作区模板中。
- 逐个文件进行对比；对于仅在前端部分或引导内容上有差异的文件，可以跳过这些文件。

## 输出格式

使用我们之前约定的格式来显示差异结果：
- 文件路径
- 缺失的模块或内容
- 建议及后续操作建议