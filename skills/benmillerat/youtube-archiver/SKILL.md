---
name: youtube-archiver
description: 将 YouTube 播放列表转换为包含元数据、字幕、AI 摘要和标签的 Markdown 笔记。适用于用户需要导入/同步 YouTube 播放列表、归档“稍后观看”或“已收藏”的视频、丰富 YouTube 笔记、批量处理视频笔记，或使用 Cron 任务自动化重复的 YouTube 到 Markdown 的同步操作的场景。
---
# YouTube 归档器

使用此技能可将 YouTube 播放列表导入 Markdown 文件，并可选择性地添加字幕、摘要和标签等丰富信息。

## 系统要求

- Python 3.7 或更高版本
- `yt-dlp`（通过 `pip install yt-dlp` 或 `brew install yt-dlp` 安装）
- 已登录 YouTube 的浏览器（用于访问私密播放列表，如“喜欢”或“稍后观看”）
- **macOS**：终端需要具有完整磁盘访问权限以读取浏览器cookie
- **Windows**：浏览器cookie的提取可能不稳定；建议使用 `cookies_file` 文件进行存储
- **Linux**：适用于桌面环境；无头服务器需要使用 `cookies_file`

## 首次运行时的设置流程（交互式）

如果 `<output>/.config.json` 文件不存在，请在运行脚本前回答以下问题：

### 必需回答的问题

1. 归档后的笔记应存储在何处？
   - 默认路径：`./YouTube-Archive`
2. 应归档哪些播放列表？
   - 可输入播放列表的 ID 或 URL
   - 默认值：`LL`（“喜欢”的视频）、`WL`（“稍后观看”的视频）
3. 使用哪个浏览器登录 YouTube 以获取 cookie？
   - 默认值：`chrome`

### 可选设置问题（仅当用户需要摘要或标签时回答）

1. 是否生成 AI 摘要？（是/否）
2. 摘要服务提供商：`openai`、`gemini`、`anthropic`、`openrouter`、`ollama` 或 `none`
3. 摘要模型的名称？
4. API 密钥的环境变量名称？
5. 是否启用自动标签生成？（是/否）
6. 标签服务提供商/模型及环境变量？
7. 保持默认标签还是自定义标签词汇？

## 首次运行的执行顺序

1. 运行初始化脚本：
   - `python3 <skill>/scripts/yt-import.py --output <output-dir> --init`
2. 根据用户的回答编辑 `<output-dir>/.config.json` 文件
3. 通过 dry run 验证登录信息：
   - `python3 <skill>/scripts/yt-import.py --output <output-dir> --dry-run`
4. 运行实际的导入操作
5. 运行丰富化处理（可选）：
   - `python3 <skill>/scripts/yt-enrich.py --output <output-dir> --limit 10`

## 快速入门方法

若需立即手动同步数据，可以使用以下命令：

```bash
python3 <skill>/scripts/yt-import.py --output <output-dir>
python3 <skill>/scripts/yt-enrich.py --output <output-dir> --limit 10
```

**有用的导入参数：**
- `--dry-run`：仅执行导入操作，不生成摘要或标签
- `--playlist <ID>`：指定要导入的播放列表 ID
- `--no-summary`：不生成摘要
- `--no-tags`：不添加标签
- `--cookies <path/to/cookies.txt>`：指定 cookie 文件的路径
- `--browser <name>`：指定使用的浏览器

**有用的丰富化参数：**
- `--dry-run`：仅执行丰富化处理，不导入视频
- `--limit <N>`：限制导入的视频数量
- `--strict-config`：严格检查配置文件内容

## 重试机制与安全性

- 系统会跳过已归档的视频（通过 `video_id` 进行判断）
- 文件名格式为：`Title [video_id].md`
- 如果笔记的前言部分包含 `enriched: true`，则不会对其进行丰富化处理
- 使用 `<output-dir>/.yt-archiver.lock` 文件来防止脚本同时运行

## 使用 Cron 任务自动化（默认配置为单代理）

仅在首次手动操作成功后，才能使用 Cron 任务进行自动化处理。

**示例调度安排（每天 11:00）：**
1. 导入新视频
2. 对指定数量的视频进行丰富化处理

**示例任务命令：**
- 先运行 `yt-import.py` 对 `<output-dir>` 目录进行导入，然后运行 `yt-enrich.py --limit 10` 对导入的视频进行丰富化处理。

**默认设置为单代理模式**，请勿尝试多代理部署。

## 故障排除与服务提供商信息**

如需了解更多信息，请参考以下文档：
- 服务提供商设置、模型推荐及费用：`references/providers.md`
- 常见问题及解决方法：`references/troubleshooting.md`
- 默认摘要生成模板：`references/default-summary-prompt.md`