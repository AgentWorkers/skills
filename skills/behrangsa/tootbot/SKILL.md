---
name: mastodon-publisher
description: 将内容发布到 Mastodon。当您需要发布 Mastodon 状态更新时，请使用此功能。
author: Behrang Saeedzadeh
version: 0.5.0
triggers:
  - "post to mastodon"
  - "publish status to mastodon"
metadata: { "clawdbot": { "emoji": "🐘" }, "requires": { "bins": ["bun"] } }
---

# Mastodon 发布器

用于将内容发布到 Mastodon。当你需要分享更新、帖子或媒体文件时，可以使用该工具。

## 使用方法

### 向 Mastodon 发布一个或多个状态更新

使用 `bun` 命令向 Mastodon 发布一个新的状态更新：

```bash
bun {baseDir}/scripts/tootbot.js '{"status": "Hello, Mastodon!"}' '{"status": "Goodby, Mastodon!"}'
```

**JSON 参数说明：**

| 参数名                | 描述                                      | 类型                                      | 示例                                                    | 是否必填 | 默认值       |
|-------------------|----------------------------------------|-----------------------------------|-----------------------------------------------------|-----------|------------|
| `status`              | 状态更新的文本内容                          | 字符串                                      | "Hello, World"                                        | 是        |            |
| `visibility`          | 设置状态更新的可见性（public、private、unlisted 或 direct） | string                                      | "private"                                             | 否        | "public"     |
| `language`            | 该状态更新的 ISO 639-1 语言代码                    | string                                      | "en"                                                  | 否        |            |
| `scheduledAt`         | 状态更新的计划发布时间（RFC3339 格式）                    | string                                      | "2029-02-03T15:30:45.000Z"                            | 否        |            |
| `quoteApprovalPolicy`     | 允许谁引用该状态更新（public、followrs 或 nobody）      | string                                      | "nobody"                                              | 否        | "public"     |
| `media`               | 附加到状态更新中的媒体文件（数组格式）                    | 数组                                        | `{"file": "/path/to/foo.png", "description": "Foo"}`         | 否        |            |

- ^1 如果提供了 `--media-path` 参数，则可以省略 `status` 参数。
- ^2 如果省略了 `status` 参数，则必须提供至少一个 `media` 对象。
- ^2 `media.description` 是可选的。

**环境变量：**

| 变量名                | 描述                                      | 示例                                      |
|-------------------|----------------------------------------|-----------------------------------------|
| `MASTODON_URL`          | 你的 Mastodon 实例 URL                          | `https://mastodon.social`                          |            |            |
| `MASTODON_ACCESS_TOKEN` | 你的 Mastodon 访问令牌                          | `xAyBzC`                                      |            |

## 示例：

- **发布一个新的状态更新：**

  ```bash
  bun {baseDir}/scripts/tootbot.js '{"status": "Hello, Mastodon"}'
  ```

  请阅读输出结果，并为用户总结其内容。

- **发布一个计划好的状态更新：**

  ```bash
  bun {baseDir}/scripts/tootbot.js '{"status": "Hello, future!", "scheduledAt" : "2030-02-05T13:21:34.000Z"}'
  ```

  请阅读输出结果，并为用户总结其内容。

- **发布一个计划好的状态更新，同时设置可见性、语言、引用权限以及一个媒体附件：**

  ```bash
  bun {baseDir}/scripts/tootbot.js <<EOF
  {
    "status" : "Dorood",
    "visibility" : "public",
    "language" : "fa",
    "scheduledAt" : "2029-02-03T15:30:45.123456789+03:30",
    "quoteApprovalPolicy" : "followers",
    "media" : [
      {
        "file" : "/path/to/media.png",
        "description" : "Nowrooz Pirooz"
      }
    ]
  }
  EOF
  ```

  请阅读输出结果，并为用户总结其内容。

- **发布一个包含多个媒体附件的状态更新：**

  ```bash
  bun {baseDir}/scripts/tootbot.js <<EOF
  {
    "status" : "Edsger W Dijkstra",
    "visibility" : "public",
    "language" : "fa",
    "scheduledAt" : "2029-02-03T15:30:45.123456789+03:30",
    "quoteApprovalPolicy" : "followers",
    "media" : [
      {
        "file" : "/path/to/dijkstra.png",
        "description" : "Portrait"
      },
      {
        "file" : "/path/to/signature.png",
        "description" : "Signature"
      }
    ]
  }
  EOF
  ```

- **发布一个包含媒体附件但无状态文本的状态更新：**

  ```bash
  bun {baseDir}/scripts/tootbot.js <<EOF
  {
    "media" : [
      {
        "file" : "/path/to/flower-1.png",
        "description" : "White Rose"
      },
      {
        "file" : "/path/to/flower-2.png",
        "description" : "Red Rose"
      }
    ]
  }
  EOF
  ```

## 注意事项：

- 使用该工具前，请确保已安装 `bun` 并将其添加到系统的 PATH 环境变量中。