---
name: iserv
description: 这是一个用于 IServ 学校平台的 HTTP 客户端。用户可以通过该客户端登录到 IServ 实例（例如：https://grabbe-dt.de），并通过 HTTP 端点获取学生的常用信息，如未读邮件数量、日历事件、文件/文件夹、任务/练习、公告/新闻等。该客户端支持基本的文件操作功能以及练习的提交功能。
---

# IServ（学校平台）

该技能使用HTTP客户端（不依赖浏览器自动化）来登录并调用IServ的各个接口。

## 凭据/安全性

- **切勿将凭据硬编码**，应通过环境变量来传递。
- 单一用户配置：
  - `ISERV_BASE_URL`（例如：`https://grabbe-dt.de`）
  - `ISERV_USER`
  - `ISERV_PASS`
- 多个用户配置（同时使用）：
  - 设置 `ISERV_PROFILE=<名称>` 或通过命令行参数 `--profile <名称>`
  - 提供 `ISERV_<PROFILE>_BASE_URL`、`ISERV_<PROFILE>_USER`、`ISERV_<PROFILE>_PASS`

## 命令

```bash
cd skills/iserv/scripts

# unread inbox count
./iserv.py mail-unread

# last 3 mails (IMAP)
./iserv.py mail-last --n 3

# upcoming calendar events (JSON)
./iserv.py calendar-upcoming

# list files (JSON)
./iserv.py files-list --path "/"        # root
./iserv.py files-list --path "/Files"   # typical user file area

# search files/folders recursively by substring
./iserv.py files-search --query "bio" --start-dir "/Files" --max-depth 6

# download a file (best-effort across IServ versions)
./iserv.py files-download --path "/Files/foo.pdf" --out-dir ./downloads

# upload a file (prefers FS Dropzone-style chunked upload; falls back to legacy form upload)
./iserv.py files-upload --file ./foo.pdf --dest-dir "/Files"
# optionally tune chunk size (bytes)
./iserv.py files-upload --file ./foo.pdf --dest-dir "/Files" --chunk-size 8388608

# create folder (best-effort; depends on IServ version)
./iserv.py files-mkdir --path "/Dokumente/Neu"

# rename/move (best-effort)
./iserv.py files-rename --src "/Dokumente/Alt.txt" --dest "/Dokumente/Neu.txt"

# delete (best-effort; USE WITH CARE)
./iserv.py files-delete --path "/Dokumente/Neu.txt"

# messenger: list chats / conversations
./iserv.py messenger-chats

# messenger: fetch messages for a chat
./iserv.py messenger-messages --chat-id <ID>

# messenger: send message
./iserv.py messenger-send --chat-id <ID> --text "Hello"

# list exercises (best-effort HTML scrape)
./iserv.py exercise-list --limit 50

# view one exercise + list attachments (optionally download them)
./iserv.py exercise-detail --id 123
./iserv.py exercise-detail --id 123 --download-dir ./downloads

# attempt to submit an exercise file (best-effort; depends on IServ version)
./iserv.py exercise-submit --id 123 --file ./solution.pdf --comment "Abgabe"
```

## 注意事项/后续步骤

- **练习功能**：练习的列表、详情查看和提交操作是通过HTML抓取实现的。
  - 提交功能现在采用表单驱动的方式（解析练习页面上的实际表单数据并通过multipart方式发送数据），这种方式比猜测内部上传API更为可靠。
  - 如果在某个特定的IServ实例上仍然出现错误，请记录以下信息：
    - 登录后的练习详情页面的HTML内容
    - 响应状态码及重定向URL
- **文件操作**：文件列表、下载、上传、创建目录、重命名和删除等功能在不同版本的ISServ中均按“最佳实践”进行实现。
  - 部分IServ实例的接口可能略有不同；客户端会尝试检测是否存在Symfony FOS路由（如果可用），并在无法使用时切换到通用的API路径。

**进一步扩展的思路**：
- **增强练习信息的解析功能**：添加截止日期、教师信息、练习描述等字段
- **添加公告/新闻功能**
- **实现消息通知系统**（目前仍处于实验阶段）
- **提供强大的文件搜索、移动/复制以及递归文件夹下载功能**

**参考资料**：IServ的接口路径可以通过随软件提供的FOS路由JavaScript文件（通常位于 `/iserv/js/fos_js_routes.js`）来获取；部分实例也可能使用 `/iserv/js/assets/fos_js_routes*.js` 文件。