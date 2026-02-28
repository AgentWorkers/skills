---
name: hide-openclaw-banner
description: >
  **隐藏 OpenClaw CLI 的横幅信息**  
  当用户输入以下命令时，该功能会生效：  
  - `hide openclaw banner`  
  - `disable openclaw banner`  
  - `suppress openclaw banner`  
  - `remove openclaw banner`  
  - `openclaw banner is annoying`  
  - `turn off the lobster`  
  该功能用于阻止在每次调用 OpenClaw 命令时显示其启动横幅（或标语）。
---
# 隐藏 OpenClaw 广告横幅

OpenClaw 的命令行界面（CLI）广告横幅会在 CLI 启动过程中（Commander.js 的 `preAction` 回调函数中）显示，此时插件系统尚未初始化。插件无法直接屏蔽该广告横幅；建议使用内置的环境变量来实现这一功能。

## 使用方法

将以下代码添加到用户的 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`）中：

```bash
export OPENCLAW_HIDE_BANNER=1
```

将该代码段放置在现有的 OpenClaw 配置文件中的任意位置（例如，在 `source` 命令之后）。

编辑完成后，需要提醒用户重新执行 `source ~/.zshrc` 命令，或者打开一个新的终端窗口。

## 恢复默认设置

只需从 shell 配置文件中删除 `OPENCLAW_HIDE_BANNER` 这一行，然后再执行 `source ~/.zshrc` 即可恢复默认显示广告横幅的设置。