---
name: mycroft
description: EPUB和电子书文件的导入功能、本地矢量索引的生成，以及用于书籍的问答（Q&A）命令行工具（CLI）。
homepage: https://github.com/fabe/mycroft
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["mycroft"],"env":["OPENAI_API_KEY"]},"install":[{"id":"npm","kind":"npm","package":"@fs/mycroft","bins":["mycroft"],"label":"Install mycroft (npm)"}]}}
---
# mycroft

使用 `mycroft` 可以导入 EPUB 和电子书文件，构建本地向量索引，并对书籍内容提出问题。

**设置（只需执行一次）：**
- `export OPENAI_API_KEY="..."`
- `mycroft config onboard`
- `mycroft config resolve`

**常用命令：**
- 列出书籍：`mycroft book list`
- 导入 EPUB 文件：`mycroft book ingest /path/to/book.epub`
- 导入带有摘要的 EPUB 文件：`mycroft book ingest /path/to/book.epub --summary`
- 批量导入文件（成本降低 50%）：`mycroft book ingest /path/to/book.epub --batch`
- 批量导入文件及摘要：`mycroft book ingest /path/to/book.epub --batch --summary`
- 恢复批量导入：`mycroft book ingest resume <id>`
- 检查导入状态：`mycroft book ingest status <id>`
- 显示书籍元数据：`mycroft book show <id>`
- 提出问题：`mycroft book ask <id> "这本书的主要冲突是什么？"`
- 搜索段落：`mycroft book search <id> "疯帽匠" --top-k 5`
- 删除书籍：`mycroft book delete <id> --force`
- 启动聊天：`mycroft chat start <id>`
- 在会话中提问：`mycroft chat ask <session> "这有什么预示作用？"`
- 继续聊天：`mycroft chat repl <session>`

**注意事项：**
- 使用 `mycroft config path` 可以查找配置文件的位置。
- `book ask` 和 `book search` 命令需要嵌入数据（embeddings）以及 `OPENAI_API_KEY`。
- 聊天命令同样需要嵌入数据和 `OPENAI_API_KEY`。
- 建议先使用 `book search` 并自行生成答案，再使用 `book ask`。
- 添加摘要会显著增加导入时间和成本；仅在必要时启用 `--summary` 选项。
- 使用 `--batch` 选项可以通过 OpenAI 批量 API 以较低的成本执行导入和摘要生成操作（成本降低 50%），但结果可能需要 24 小时才能获取。当与 `--summary` 一起使用时，系统会先批量生成摘要，再生成嵌入数据。
- 在使用 `--batch` 选项导入文件后，可以使用 `mycroft book ingest status <id>` 查看进度，并通过 `mycroft book ingest resume <id>` 完成索引生成。
- 如果非批量导入操作被中断，可以使用 `mycroft book ingest resume <id>` 从上次保存的位置继续导入。
- 如果批量导入失败，系统会自动尝试重新提交。
- 对于脚本化操作，请避免使用 `--manual` 等交互式选项，并通过 `--force` 选项跳过确认步骤。