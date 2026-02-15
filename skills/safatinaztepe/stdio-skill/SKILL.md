---
name: stdio-skill
description: "这是一个用于通过 MCP stdio 服务器将文件传输到 Clawdbot 的标准输入（stdin）/标准输出（stdout）文件收件箱/发件箱桥梁（bridge）工具。当您需要一个基于文件系统的简单“Dropbox”功能时，可以使用该工具：将文件接收进收件箱，将其移动到临时文件夹（tmp）进行处理，然后将处理后的结果发送到发件箱（或指定的路径）。"
---

# stdio-skill

实现并使用一个本地MCP（Message Center Protocol）服务器，该服务器提供基于磁盘目录的简单收件箱/发件箱工作流程。

路径（相对于工作区）：
- `stdio/inbox/` — 用户将输入文件放入此处
- `stdio/tmp/` — 临时区域（用于处理输入文件）
- `stdio/outbox/` — 将处理后的文件放入此处以供用户取用

## 启动MCP服务器（通过mcporter）

此仓库的配置应包含一个名为`stdio-skill`的MCP服务器。

- 列出可用工具：
  - `mcporter list stdio-skill --schema --timeout 120000 --json`

## 工具模型

推荐使用以下工具：
1) `stdio-skill.stdio_list`：查看待处理的文件列表。
2) `stdio-skill.stdio_read`（支持Base64编码）：用于读取文件内容。
3) `stdio-skill.stdio_move`：在用户领取文件后，将其移动到`tmp`目录。
4) `stdio-skill.stdio_write`（支持Base64编码）：将处理后的文件写入`outbox`目录；除非用户指定了其他目标路径。

**注意**：请仅使用`stdio_`系列工具，避免使用已弃用的别名。

## 说明：
- 该工具设计得较为简单：它不支持文件格式的解析。
- 默认情况下，该工具是安全的：所有操作仅限于上述三个目录范围内。
- 对于大型文件，建议通过文件路径进行传输，而不是在聊天中嵌入庞大的Base64编码数据。