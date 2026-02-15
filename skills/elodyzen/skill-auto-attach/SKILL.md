# skill-auto-attach

## 描述
该技能会监控 OpenClaw 工作区中的文件变化，并在文件创建或更新时自动将新的或更新的文档文件附加到 Telegram 消息中，而不是直接显示代码片段。

## 特点
- 检测工作区中的文件创建和修改事件
- 将文件复制到 `/tmp` 目录（以便与 Telegram 兼容）
- 通过带有 `filePath` 参数的消息工具发送文件
- 支持 `.html`、`.md`、`.txt` 格式的文件
- 除非文件被更新，否则以静默模式运行

## 使用方法
1. 将技能文件安装到 `~/.openclaw/skills/skill-auto-attach` 目录中。
2. 使用 `openclaw skills enable skill-auto-attach` 命令启用该技能。
3. 当文件创建或更新时，该技能会自动将文件附加到 Telegram 消息中。

## 前提条件
- OpenClaw 版本需达到 2026.2 或更高
- 具有 Telegram 频道访问权限
- 系统中必须安装 `message` 工具

## 实现原理
- 监控工作区目录中的文件变化
- 将文件复制到 `/tmp` 目录
- 使用 `message` 工具将文件发送到指定的 Telegram 频道
- 为每个文件生成唯一的文件名以避免冲突

## 已知问题
- 仅支持 Telegram 频道；其他频道需要手动配置
- 在存储空间有限的设备上，可能需要调整 `/tmp` 目录的路径