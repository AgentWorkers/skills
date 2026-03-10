---
name: openclaw-help
description: OpenClaw插件提供了一个基于配置的`/shortcuts`命令，该命令使用安全的默认占位符来保护用户隐私。当您需要一个能够列出本地命令和项目快捷方式的`/shortcuts`命令时，同时又不希望将私人信息泄露到公共仓库中，可以使用此插件。
---
# openclaw-help

用于在您的 OpenClaw 代理中注册快捷方式（shortcuts）。

## 功能说明

- `/shortcuts`：打印已配置的快捷方式信息（包括项目、命令、模型切换等）。
- 默认提供通用的占位符内容；实际的快捷方式应保存在本地配置文件中。
- `requireAuth: false`：授权逻辑由 `gatewaycommands.allowFrom` 处理。

## 配置方法

通过 `openclaw.json` 文件来配置快捷方式：

```json5
{
  "plugins": {
    "entries": {
      "openclaw-help": {
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

**版本：** 0.2.0