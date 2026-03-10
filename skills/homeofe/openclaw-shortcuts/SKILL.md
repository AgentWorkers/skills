---
name: openclaw-shortcuts
description: OpenClaw插件提供了一个基于配置的`/shortcuts`命令，该命令使用安全的默认占位符。当您需要一个能够列出本地命令和项目快捷方式的`/shortcuts`命令，同时又不想将私人信息泄露到公共仓库中时，可以使用这个插件。
---
# openclaw-shortcuts

该插件用于在您的 OpenClaw 代理中注册快捷方式。

## 功能说明

- 使用 `/shortcuts` 命令可以查看已配置的快捷方式（包括项目、命令、模型切换等相关设置）。
- 默认情况下，系统中使用的是通用占位符；真正的快捷方式会保存在本地配置文件中。
- 如果设置了 `requireAuth: false`，则授权逻辑将由 `gatewaycommands.allowFrom` 处理。

## 配置方法

通过 `openclaw.json` 文件来配置快捷方式：

```json5
{
  "plugins": {
    "entries": {
      "openclaw-shortcuts": {
        "enabled": true,
        "config": {
          "includeTips": false,
          "sections": [
            {
              "title": "📁 Projects",
              "lines": ["/myproject   - My project shortcut"]
            }
          ]
        }
      }
    }
  }
}
```

## 安全提示

切勿将个人使用的快捷方式提交到仓库中，所有快捷方式应仅保存在本地配置文件中。

**版本：** 0.1.0