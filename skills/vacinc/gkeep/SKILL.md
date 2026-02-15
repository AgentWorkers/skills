---
name: gkeep
description: 通过 gkeepapi 在 Google Keep 中创建、搜索、管理和查看笔记。
homepage: https://github.com/kiwiz/gkeepapi
metadata: {"openclaw":{"emoji":"📝","requires":{"bins":["gkeep"]}}}
---

# gkeep

这是一个用于 Google Keep 的命令行工具（CLI），它通过使用 `gkeepapi`（一个非官方的 API）来实现与 Google Keep 的交互。

## 设置

使用您的 Google 账户登录：
```bash
gkeep login your.email@gmail.com
```

**重要提示：** 请使用 [应用密码](https://myaccount.google.com/apppasswords)，而非常规密码。同时，请确保启用了两步验证（2FA）。

## 命令

- 列出所有笔记：  
  ```bash
gkeep list
gkeep list --limit 10
```

- 搜索笔记：  
  ```bash
gkeep search "shopping"
```

- 获取特定笔记：  
  ```bash
gkeep get <note_id>
```

- 创建新笔记：  
  ```bash
gkeep create "Title" "Body text here"
```

- 将笔记归档：  
  ```bash
gkeep archive <note_id>
```

- 删除笔记：  
  ```bash
gkeep delete <note_id>
```

- 将笔记固定到首页：  
  ```bash
gkeep pin <note_id>
```

- 取消固定笔记：  
  ```bash
gkeep unpin <note_id>
```

## 注意事项：

- 该工具依赖于一个非官方的 API，该 API 是通过对 Google Keep 的内部接口进行逆向工程实现的。
- 如果 Google 更改其内部 API，该工具可能会无法正常使用。
- 用户令牌（Token）存储在 `~/.config/gkeep/token.json` 文件中。
- 首次运行时，会在 `skills/gkeep/.venv` 目录下生成一个本地虚拟环境（venv）。
- 该项目目前处于活跃开发状态，并持续更新（截至 2026 年 1 月）。