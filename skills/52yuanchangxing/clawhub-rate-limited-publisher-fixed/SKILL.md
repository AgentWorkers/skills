---
name: clawhub-rate-limited-publisher
description: 使用本地的 `clawhub CLI` 和主机调度器，将本地技能添加到 `ClawHub` 并发布，同时严格遵守每小时最多添加 5 项技能的限制。
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🦀","os":["darwin","linux"],"requires":{"bins":["python3","clawhub"]},"homepage":"https://github.com/openclaw/clawhub"}}
---
# ClawHub限速发布工具

当用户希望向ClawHub发布一个或多个本地技能时，可以使用此工具，以确保不会超出平台的发布限制。

## 该工具的功能

该工具并不会自动授予用户shell权限。它为用户自己的`clawhub` CLI提供了一套安全的本地队列处理和调度流程。

请按照以下步骤操作：

1. 确认技能文件夹存在，并且其中包含`SKILL.md`文件。
2. 生成或更新队列JSON文件。
3. 要求主机运行`{baseDir}/scripts/clawhub_rate_limited_uploader.py`辅助脚本。
4. 建议使用cron或systemd定时器等调度工具，以便每12分钟自动执行一次上传操作。
5. 在任何连续的3600秒时间内，上传尝试次数不得超过5次。
6. 记录每次尝试的stdout/stderr输出，并将队列中的项目标记为“已发布”或“失败”。

## 运行环境要求

- 主机上必须已安装并配置好`clawhub`。
- 主机必须允许执行命令。在OpenClaw环境中，通常需要启用`bash`/`exec`等运行时工具，或者直接在聊天界面之外运行Python脚本。
- 更改技能配置后可能需要重新创建会话，因为符合条件的技能信息是按会话进行快照处理的。

## 推荐的使用方式

### 一次性手动运行

执行命令：

`python3 "{baseDir}/scripts/clawhub_rate_limited_uploader.py" --queue "/absolute/path/to/queue.json" --execute`

### 干运行（不执行实际上传）

执行命令：

`python3 "{baseDir}/scripts/clawhub_rate_limited_uploader.py" --queue "/absolute/path/to/queue.json" --dry-run`

### 使用Cron定时器

根据`{baseDir}/resources/cron.example`中的示例，设置每12分钟执行一次上传任务。

## 队列文件格式

参考`{baseDir}/examples/queue.sample.json`文件。

每个队列项可以包含以下信息：

- `path`：技能目录的绝对路径
- `command`：可选的命令模板，默认为`clawhub publish "{path}"`

## 安全注意事项

- 使用绝对路径进行文件操作。
- 禁止使用`curl|bash`、base64编码或隐藏的远程安装方式。
- 除非用户明确审核并同意，否则`command`应限制为`clawhub publish "{path}"`这一基本命令。
- 失败的上传尝试会计入每小时的最大上传次数限制中，以避免在认证或验证出现问题时对ClawHub造成过大的负担。