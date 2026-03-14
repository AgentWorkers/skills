---
name: searxng-tool-for-openclaw
description: 安装一个 OpenClaw 插件，该插件可以在不使用付费搜索 API 的情况下提供基于 SearXNG 的网页搜索功能。
metadata:
  openclaw:
    emoji: "🔎"
    os:
      - linux
      - macos
      - windows
    requires:
      anyBins:
        - openclaw
      config:
        - ~/.openclaw/openclaw.json
    install:
      - kind: node
        package: openclaw
        bins:
          - openclaw
      - kind: node
        package: searxng-tool-for-openclaw
        bins:
          - searxng-tool-for-openclaw
    config:
      stateDirs:
        - ~/.openclaw
      example: |
        {
          "plugins": {
            "entries": {
              "searxng-tool": {
                "enabled": true,
                "config": {
                  "baseUrl": "http://127.0.0.1:8888",
                  "timeoutSeconds": 20,
                  "maxResults": 8,
                  "defaultLanguage": "auto",
                  "defaultCategories": "general",
                  "defaultSafeSearch": 0
                }
              }
            }
          }
        }
    cliHelp: |
      searxng-tool-for-openclaw install
      searxng-tool-for-openclaw print-path
    links:
      homepage: https://github.com/barrontang/searxng-tool-for-openclaw
      repository: https://github.com/barrontang/searxng-tool-for-openclaw
      documentation: https://github.com/barrontang/searxng-tool-for-openclaw#readme
---
# SearXNG 工具（适用于 OpenClaw）

本技能包将用户引导至用于安装 OpenClaw 插件的 npm 包。

## 安装内容

该 npm 包包含以下内容：
- 在 `openclawextensions` 文件中声明的 OpenClaw 插件条目
- 用于验证的 `openclaw.plugin.json` 配置文件
- 可执行的安装程序，使得 `npx searxng-tool-for-openclaw install` 命令能够正常使用

## 推荐的安装方式

**通过 OpenClaw 直接安装插件：**

```bash
openclaw plugins install searxng-tool-for-openclaw
```

**或使用该包的安装程序二进制文件：**

```bash
npx searxng-tool-for-openclaw install
```

## 所需运行环境**

- 确保您的机器上已安装并可以正常使用 OpenClaw
- 确保有一个可访问的 SearXNG 实例，并且该实例已启用 JSON 输出功能

## 最小配置要求**

将插件条目添加到您的 OpenClaw 配置文件中，并将其配置为指向您的 SearXNG 基本 URL。

```json
{
  "plugins": {
    "entries": {
      "searxng-tool": {
        "enabled": true,
        "config": {
          "baseUrl": "http://127.0.0.1:8888"
        }
      }
    }
  }
}
```

安装完成后或配置更改后，请重启 OpenClaw 服务器。