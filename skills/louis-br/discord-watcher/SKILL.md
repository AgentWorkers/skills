---
name: discord-watcher
description: 使用此技能可以通过获取最近的消息来实时关注特定的 Discord 频道。需要 DISCORD_TOKEN。
---

# Discord 监控工具

该工具使用 `DiscordChatExporter` 从所有可访问的 Discord 频道中获取最新消息。

## 先决条件

- **DISCORD_TOKEN**：必须在环境中设置或传递给脚本。
- **DiscordChatExporter (CLI)**：必须安装在 `dce` 子目录中。

## 安装

1. 从 GitHub 下载 DiscordChatExporter 的 **CLI 版本**：
   [https://github.com/Tyrrrz/DiscordChatExporter/releases](https://github.com/Tyrrrz/DiscordChatExporter/releases)
   （请下载 `DiscordChatExporter.Cli.linux-x64.zip` 或适用于您操作系统的版本）

2. 将其解压到该工具目录下的 `dce` 文件夹中：
   ```bash
   mkdir -p skills/discord-watcher/dce
   unzip DiscordChatExporter.Cli.linux-x64.zip -d skills/discord-watcher/dce
   chmod +x skills/discord-watcher/dce/DiscordChatExporter.Cli
   ```

## 使用方法

运行更新脚本，以获取过去 24 小时内所有频道的消息：

```bash
./skills/discord-watcher/update.sh [TOKEN]
```

该脚本可以从任何目录运行（它会自动检测自身的位置）。

执行此操作后：
1. 会在 `exports/updates/` 目录下创建一个带有时间戳的文件夹。
2. 从所有可访问的频道中导出过去 24 小时内的所有新消息。
3. 将这些消息按服务器和类别分类保存为纯文本文件。

## 获取 DISCORD_TOKEN（浏览器方法）

如果您需要帮助从已登录的浏览器会话中获取 DISCORD_TOKEN，可以使用以下页面内技术（在允许脚本执行的页面环境中运行）通过注入的 iframe 从 `localStorage` 中可靠地提取该令牌。获取令牌后，请将其视为机密信息。

JavaScript 代码片段（通过能够执行页面脚本的自动化工具在页面环境中运行）：

```js
// Inject a hidden iframe and read its localStorage 'token' key
(() => {
  try {
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    document.documentElement.appendChild(iframe);
    const token = iframe.contentWindow.localStorage.getItem('token');
    iframe.remove();
    return {ok: !!token, method: 'iframe', token};
  } catch (e) {
    return {ok: false, error: e.toString()};
  }
})();
```

**注意事项与替代方案**：
- 某些自动化环境无法直接访问页面的 `localStorage`；使用 iframe 技巧通常可以绕过这一限制。
- 另一种方法是使用 “webpack chunk” 方法来获取 Discord 的内部令牌获取器，但请谨慎使用。
- **切勿将令牌提交到源代码控制系统中**，应将其存储在 `.env` 文件或环境变量中。

## 自动更新

要实现自动更新，您可以添加一个 `HEARTBEAT.md` 文件：

```markdown
- [ ] Every 6 hours: Run `skills/discord-watcher/update.sh` and summarize any new important discussions in `memory/discord-news.md`.
```

## 搜索与索引（推荐）

导出的文本文件非常适合使用 `qmd` 进行索引：

1. **创建索引集合：**
   ```bash
   qmd collection add exports/updates --name discord-logs --mask "**/*.txt"
   ```
   *注意：请使用 `--mask "**/*.txt"` 标志，因为导出器会保存纯文本文件。*
2. **更新索引：**
   ```bash
   qmd update
   ```
3. **搜索：**
   ```bash
   qmd search "query"
   ```