---
name: chats-share
description: "**使用场景：** 当用户希望将 OpenClaw 通道中的对话内容分享给外部用户时"
metadata: {"openclaw":{"emoji":"💬","homepage":"https://github.com/imyelo/openclaw-chats-share"}}
---
# chats-share

将 OpenClaw 的对话内容共享为公共网页。

## 使用场景

- 用户希望将对话内容分享给外部用户
- 用户需要导出对话记录以用于文档编写

## 配置参数

**项目目录**：`create-openclaw-chats-share` 命令的执行路径

- **OpenClaw**：配置信息从 `~/.openclaw/workspace/TOOLS.md` 文件中读取
- **其他代理（agents）**：作为参数传递

**站点（site）**：从 `{projectDir}/chats-share.toml` 文件中读取站点 URL

**输出目录（outputDir）**：`{projectDir}/chats/`（默认值，非配置项）

## 步骤

1. **预检查**：检查 `TOOLS.md` 文件中是否配置了 `chats-share` 项目
   - 读取 `~/.openclaw/workspace/TOOLS.md`
   - 如果未找到项目目录 → 运行首次设置（参见下面的“首次设置”部分）

2. 加载项目目录（来自 `TOOLS.md` 或命令参数）

3. 从 `{projectDir}/chats-share.toml` 文件中读取站点 URL（作为输出 URL 的基础）

4. 查找对话会话：
   - 列出所有会话：`ls -t ~/.openclaw/agents/main/sessions/*.jsonl`
   - 根据以下条件进行筛选：
     - `sessionId=xxx` → 通过 ID 进行精确匹配
     - `topic=xxx` → 在会话内容中搜索指定主题
     - `current` → 选择最新的会话（`ls -t` 命令的输出结果中的第一条记录）
   - 将符合条件的会话列表显示给用户进行确认

5. 将会话内容解析为临时文件：`openclaw-chats-share parse {session} -o {projectDir}/chats/.tmp/{timestamp}.md`

6. 从解析后的文件中提取摘要，并根据内容建议一个合适的主题名称（例如：“如何使用 OpenClaw 与 Python”）

7. 确认参与者信息：读取临时文件中自动生成的参与者列表
   - 显示当前的参与者名单，并询问用户是否需要修改他们的显示名称（例如，将“user”更改为用户的真实姓名，或将“assistant”更改为代理的显示名称）
   - 如果用户提供了新的名称，请直接更新临时文件中的参与者信息；其他字段（如 `role`、`model`）保持不变

8. 与用户确认：展示预览内容，并询问用户是否需要修改主题名称

9. 重命名文件：`mv {temp} {projectDir}/chats/{YYYYMMDD}-{topic}.md`

10. 遮盖敏感信息（例如：API 密钥、令牌、路径、电子邮件地址、IP 地址）（参见下面的“遮盖敏感信息”部分）

11. 在提交之前再次与用户确认：`git add {projectDir}/chats/{topic}.md && git commit -m "docs: add {topic}"`
12. 在推送之前再次与用户确认：`git push`

## 首次设置

运行一次该脚本以初始化项目：
```bash
create-openclaw-chats-share
```
此操作会设置项目的基本结构。

设置完成后，需要在 `TOOLS.md` 文件中注册该项目：
```bash
# Append to ~/.openclaw/workspace/TOOLS.md
echo -e "\n## chats-share\n\n- Project: {projectDir}\n" >> ~/.openclaw/workspace/TOOLS.md
```

## 遮盖敏感信息

在公开分享时，需要审查并删除以下敏感内容：
- API 密钥、令牌、密码
- 包含用户名的文件路径（例如：`/Users/xxx` → 更改为 `~`）
- 电子邮件地址、电话号码
- 内部 URL 和私有 IP 地址

## 输出结果

- 输出文件：`{projectDir}/chats/{YYYYMMDD}-{topic}.md`
- 公共访问 URL：`{site}/share/{slug}`

## 开发环境（Dev）

运行本地开发服务器：
```bash
openclaw-chats-share-web dev
```