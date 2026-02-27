---
name: xqueue
description: 基于文件的X/Twitter帖子调度工具：将推文保存到指定的日期/时间文件夹中，推文会自动发布。无需前端界面或应用程序，你的文件系统本身就是用户界面。
metadata: {"openclaw":{"requires":{"env":["X_CONSUMER_KEY","X_CONSUMER_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET"],"bins":["python3"]},"permissions":{"filesystem":"read/write within xqueue/ directory","network":"api.twitter.com, upload.twitter.com","keychain":"optional macOS Keychain if XQUEUE_KEYCHAIN_ACCOUNT is set"}}}
---
# XQueue

这是一个基于文件的X（Twitter）推文调度工具。你的文件系统本身就是用户界面。

## 工作原理

1. 创建一个包含不同日期和时间的文件夹结构。
2. 将推文文件放入相应的时间槽中。
3. 每15分钟运行一次Cron作业：如果当前日期和时间符合要求且文件存在，就会执行推文发布并清理相应的文件。

```
xqueue/
  config.json
  backlog/
    ebook-launch-thread.md
    ai-tools-roundup.md
  Sunday/
    10am/
      my-tweet.md
      photo.jpg
  Monday/
    9am/
      thread-about-shipping.md
    12pm/
    5pm/
  Tuesday/
    ...
```

该调度系统每周循环执行一次。例如，周一上午9点的推文会在每周一上午9点自动发布。如果某个时间槽为空，系统会从`backlog/`文件夹中（按字母顺序）选取最旧的文件进行发布；如果时间槽中有内容，则直接发布该文件，其余文件会被放入`backlog/`文件夹中等待下一次发布。

你可以为最多一周的内容制定发布计划，其余未发布的文件会自动放入`backlog/`文件夹中。

发布完成后，文件会被删除（默认设置），以避免重复推送。

## 设置

运行设置命令来配置XQueue：

```bash
python3 xqueue-setup.py
```

设置过程中需要回答以下问题：
- 每天希望发布多少次推文？
- 发布的具体时间是什么？（也可以让系统自动选择最佳时间）
- 使用哪个时区？
- 需要发布到哪些X社区？
- 推文之间的分隔符是什么？（默认值：`---`）
- 发布后是否删除文件？（建议设置为“是”——否则可能会重复推送）

设置完成后，系统会创建完整的文件夹结构及`config.json`配置文件。

## 推文格式

### 简单推文
只需将推文内容写入`.md`或`.txt`文件中即可：

```
This is my tweet. It can be up to 280 characters.
```

### 发布到特定社区的推文
在文件的第一行输入`Post to [社区名称]:`：

```
Post to Build in Public: Just shipped my first ClawHub skill. File-based tweet scheduler, no frontend needed.
```

### 多条推文的推文串
将多条推文放入同一个文件中，并使用你配置的分隔符（默认为`---`）进行分隔：

```
I built a file-based tweet scheduler with no frontend. Your filesystem is the UI.
---
Drop a .md file into Monday/9am/ and a cron job posts it. Empty slot? It pulls from a backlog/ folder automatically.
---
No database, no app, no dashboard. Just folders and text files. Sometimes the simplest architecture wins.
```

### 带有图片/视频的推文
将图片/视频文件放在与推文相同的文件夹中。支持的文件格式为JPG、PNG、GIF（图片文件大小不超过5MB，GIF文件不超过15MB）。

### 多个媒体文件的处理
如果有多个媒体文件，它们会按字母顺序被添加到推文中（每条推文最多支持4个媒体文件）。

## 配置文件（`xqueue/config.json`）

```json
{
  "timezone": "America/Chicago",
  "separator": "---",
  "deleteAfterPost": true,
  "communities": {
    "Build in Public": "community_id",
    "Indie Hackers": "community_id"
  },
  "logFile": "xqueue/posted.log",
  "dryRun": false
}
```

在设置时，需要提供社区的URL（例如`x.com/i/communities/123456`）或社区的ID。脚本会自动提取ID并询问社区的显示名称。没有ID的纯文本推文会被拒绝；所有必要的信息都会在设置时被收集完毕。

## 待发布文件（Backlog）

`xqueue/backlog/`文件夹用于存储尚未安排发布的推文。当Cron作业运行且某个时间槽为空时，系统会从`backlog/`文件夹中选取最旧的推文进行发布（文件名前会加上数字前缀，如`01-`、`02-`等，以确定发布顺序）。

这种方式允许你批量处理内容，无需担心文件是否能够完美地分配到每周的各个时间槽中。对于需要及时发布的推文，可以直接安排；其余内容则可以放入`backlog/`文件夹中等待。

## Cron作业集成

XQueue包含一个每15分钟运行一次的Cron作业，其功能包括：
- 检查当前日期和时间是否与文件夹结构匹配；
- 如果时间槽中有内容，则执行推文发布；
- 如果时间槽为空，则从`backlog/`文件夹中选取最旧的文件进行发布；
- 如果两者都为空，则跳过当前时间槽；
- 将执行结果记录到`posted.log`文件中；
- 如果启用了`deleteAfterPost`选项，发布后的文件会被删除。

## 各项操作的对应操作方式

| 操作需求                          | 所需操作                                      |
| ----------------------------------------- | -------------------------------------------- |
| 为周二上午9点安排推文                | 将推文文件放入`xqueue/Tuesday/9am/`文件夹                |
| 发布多条推文                         | 将推文文件放入同一个文件夹，并使用`---`分隔                   |
| 附加图片                        | 将图片文件放在与推文相同的文件夹中                         |
| 发布到特定社区                     | 在文件开头添加`Post to [社区名称]:`                         |
| 重新排列推文顺序                     | 在不同的时间文件夹之间移动文件                         |
| 跳过某个时间槽                    | 保持该时间槽的文件夹为空                         |
| 查看待发布的推文                   | 浏览`xqueue`文件夹                             |
| 查看已发布的推文                   | 查看`xqueue/posted.log`文件                         |
| 为未指定时间的推文创建队列                | 将文件放入`xqueue/backlog/`文件夹                         |
| 控制待发布文件的顺序                 | 为文件添加前缀（如`01-first.md`、`02-second.md`）           |

## 重要说明

- **deleteAfterPost: true**（默认值）表示每个文件只会发布一次，之后会被删除。如果关闭此选项，相同内容会在下周再次发布。
- 超过280个字符的推文会被拒绝（仅记录错误日志，不会实际发布）。
- 每条包含多条推文的推文都会单独检查字符长度是否超过280个字符。
- 空文件夹会被自动跳过。
- Cron作业每15分钟执行一次，因此推文会在预定时间前0到15分钟内发布。