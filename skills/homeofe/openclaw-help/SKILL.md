---
name: openclaw-help
description: OpenClaw插件提供了一个由配置文件驱动的 `/help` 命令（默认情况下仅使用安全的占位符）。
---
# openclaw-help

该插件为您的 OpenClaw 代理添加了一个 `/help` 命令。

**核心设计目标** 是确保 **公共仓库的安全性**：该插件默认提供的是通用的占位符帮助文本，您需要通过配置文件（例如 `~/.openclaw/openclaw.json`）来设置自定义的快捷命令。

## 功能介绍

- 注册 `/help` 命令；
- 显示以下内容：
  - 通用的默认信息（快捷命令、内存管理、待办事项等）；
  - 可选的使用提示；
  - 从配置文件中加载的自定义信息。

## 设计初衷

用户常常会将个人命令、电话号码、团队 ID 以及内部工作流程的备注硬编码到项目的 `README` 文件中。如果将这些信息发布到 GitHub 或 ClawHub 上，就可能导致隐私泄露。

该插件通过以下方式避免此类问题：

- 仅将仓库内容设置为占位符；
- 将实际的自定义命令映射信息存储在本地配置文件中。

## 安装方法

通过 ClawHub 安装：

```bash
clawhub install openclaw-help
```

**本地开发环境下的安装方法：**

```bash
openclaw plugins install -l ~/.openclaw/workspace/openclaw-help
openclaw gateway restart
```

## 配置方法

以下是一个安全的、通用的配置示例：

```json
{
  "plugins": {
    "entries": {
      "openclaw-help": {
        "enabled": true,
        "config": {
          "includeTips": true,
          "sections": [
            {
              "title": "Public example projects",
              "lines": [
                "- AAHP - protocol + handoff structure example",
                "- BMAS - research project example"
              ]
            },
            {
              "title": "Your shortcuts (fill in locally)",
              "lines": [
                "- /<project> - your project shortcut",
                "- /<command> - your custom command"
              ]
            }
          ]
        }
      }
    }
  }
}
```

## 安全使用规则：

- **严禁** 将任何私人命令、电话号码、团队 ID、访问令牌、域名或内部工作流程信息放入该仓库中；
- **所有此类信息必须仅保存在本地配置文件中**。