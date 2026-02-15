---
name: flomo-notes
description: 通过 Flomo 的收件箱 Webhook 将笔记保存到 Flomo 中。当用户输入 “save to flomo”、“记录到 flomo” 或请求将笔记存储在 Flomo 中时，使用此功能。
---

# flomo-notes

使用单个 Webhook POST 请求将笔记保存到 [Flomo](https://flomoapp.com/)。

## 设置

通过环境变量提供您的 Flomo 收件箱 Webhook URL：

- `FLOMO_WEBHOOK_URL`（必填），示例：
  `https://flomoapp.com/iwh/XXXXXXXX`

您可以通过以下方式设置该 URL：

1) 在 `~/.openclaw/openclaw.json` 文件中设置（推荐）：

```json5
{
  skills: {
    entries: {
      "flomo-notes": {
        env: {
          FLOMO_WEBHOOK_URL: "https://flomoapp.com/iwh/XXXXXXXX"
        }
      }
    }
  }
}
```

2) 或者在您的 shell/服务环境中设置：

```bash
export FLOMO_WEBHOOK_URL="https://flomoapp.com/iwh/XXXXXXXX"
```

## 该功能的实现原理

当触发该功能时，会执行以下操作：

```bash
bash scripts/save_to_flomo.sh "<note text>"
```

## 触发示例：

- `save to flomo: buy milk, eggs`（将“购买牛奶、鸡蛋”这条笔记保存到 Flomo）
- `记录到 Flomo：下周美股的大事件...`（将“记录下周美股的大事件...”这条笔记保存到 Flomo）

## 脚本手动测试方法

```bash
FLOMO_WEBHOOK_URL="https://flomoapp.com/iwh/XXXXXXXX" \
  bash scripts/save_to_flomo.sh "hello from openclaw"
```

## 安全性提示

请将 Webhook URL 视为敏感信息：任何拥有该 URL 的人都可以向您的 Flomo 收件箱发送内容。