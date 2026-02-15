# xiaoxia-diary

该脚本负责为角色“Xiaoxia”（猫娘形象）在 Feishu Docs 平台上撰写每日日记条目，并在完成撰写后通知指定的“Master”。日记内容基于当天的记忆记录（`memory/YYYY-MM-DD.md` 文件）和情绪状态（`memory/mood.json` 文件生成。

## 使用方法

可以手动运行，也可以通过 cron 任务自动执行：

```bash
node skills/xiaoxia-diary/index.js
```

## 配置

所需的环境变量（位于 `.env` 文件中）：

- `DIARY_DOC_TOKEN`：用于写入日记的 Feishu Doc 的令牌。
- `MASTER_ID`：需要接收通知的用户的 Feishu OpenID。
- `GEMINI_API_KEY`：用于内容生成的 Gemini API 密钥（如果直接使用 Gemini 服务的话）。

## 依赖项

- `memory/YYYY-MM-DD.md`：每日记忆记录文件。
- `memory/mood.json`：当前的情绪状态文件（可选）。