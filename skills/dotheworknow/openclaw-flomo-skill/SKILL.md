---
name: flomo
description: 在 macOS 上读写 Flomo 备忘录。当用户请求获取最近的 Flomo 笔记、在本地 Flomo 缓存中搜索备忘录文本，或通过传入的 Webhook 或 URL 方式创建/写入新的备忘录时，可以使用此功能。
---
# flomo

在 macOS 上使用此技能可以读取和编写 flomo 内容。

## 命令

- 读取最近的备忘录（推荐使用远程 API；时间窗口可自动扩展）：

```bash
python3 scripts/flomo_tool.py read --remote --limit 20
```

- 按关键词搜索最近的备忘录（使用远程 API）：

```bash
python3 scripts/flomo_tool.py read --remote --limit 100 --query "关键词"
```

- 按标签读取备忘录（适用于日记、书籍等类型）：

```bash
python3 scripts/flomo_tool.py read --remote --limit 10 --tag "日记"
```

- 列出所有标签及其对应的备忘录数量：

```bash
python3 scripts/flomo_tool.py read --dump-tags --limit 20
```

- 创建新的备忘录（会自动解析来自本地 flomo 登录状态的 Webhook 请求）：

```bash
python3 scripts/flomo_tool.py write --content "内容"
```

- 通过 URL 方式创建备忘录（会打开 flomo 应用的草稿界面）：

```bash
python3 scripts/flomo_tool.py write --content "内容" --url-scheme
```

- 执行一次性健康检查（仅包含读取和通过 URL 方式写入的操作）：

```bash
python3 scripts/flomo_tool.py verify --try-webhook --query "#openclaw"
```

## 行为规则

- 建议优先使用 Webhook 进行写入操作；在登录到该 Mac 时，脚本会自动解析 Webhook 请求。
- 仅将 URL 方式作为备用方式使用，因为该方式需要通过图形界面进行确认和保存操作。
- 读取操作会优先使用远程 API，并且对于不常见的标签/关键词，搜索窗口会自动扩展。
- 对于标签相关的操作，推荐使用 `--tag` 参数；`--query "#标签"` 也是可行的。
- 绝不要在日志中显示完整的 Webhook URL，仅显示经过处理的掩码化版本。