---
name: snapbyte-digest-api
description: 通过 API 密钥认证，从 Snapbyte 外部 API 获取个性化的开发者新闻摘要。适用于 Hacker News、Reddit、Lobsters 和 DEV.to 的新闻摘要生成工作流程。
homepage: https://api.snapbyte.dev/docs
metadata: {"openclaw":{"emoji":"📰","requires":{"bins":["python3","curl"],"env":["SNAPBYTE_API_KEY"]},"primaryEnv":"SNAPBYTE_API_KEY"}}
---
# Snapbyte Digest API

使用此技能可以从 Snapbyte 获取用户范围内的摘要内容，并以格式化良好的 Markdown 格式呈现给用户。

## 使用场景

- 用户请求查看他们的最新摘要。
- 用户请求查看摘要的历史记录。
- 用户请求从 Snapbyte API 获取摘要的具体内容或摘要的概要。
- 用户请求在 OpenClaw 中使用开发者新闻摘要 API 的工作流程。

## 认证

- 需要 `SNAPBYTE_API_KEY`。
- 向 Snapbyte API 发送 `Authorization: Bearer <SNAPBYTE_API_KEY>` 请求头。

## 基本 URL

- `https://api.snapbyte.dev`

## 命令模式

从该技能文件夹中运行辅助脚本：

```bash
python3 scripts/snapbyte_digest.py configurations
python3 scripts/snapbyte_digest.py latest
python3 scripts/snapbyte_digest.py latest --configuration-id 12
python3 scripts/snapbyte_digest.py history --configuration-id 12 --page 1 --limit 10
python3 scripts/snapbyte_digest.py digest --id dst_abc123
python3 scripts/snapbyte_digest.py items --digest-id dst_abc123 --page 1 --limit 10
```

## 输出规则

- 默认情况下，脚本会输出格式化的 Markdown 内容。
- 如果用户请求原始数据（raw payload），请使用 `--raw` 选项。
- 请保留 API 返回的所有链接，不要自行添加任何未在 API 中定义的字段。

## 错误处理

- `401`：提示用户提供的 API 密钥缺失、无效、已被吊销或过期，请用户更新 `SNAPBYTE_API_KEY`。
- `404`：提示用户未找到相应的摘要或配置信息。
- 验证错误：显示错误信息并提示用户使用正确的参数重新运行脚本。

## 参考资料

- 有关设置和示例，请参阅 `references/quickstart.md`。