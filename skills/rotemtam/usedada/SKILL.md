---
name: dada
description: 为 OpenClaw 代理提供托管的后端基础设施，包括数据库管理、Webhook 功能以及文件托管服务——这样您的代理就可以专注于核心工作，而无需担心底层技术的实现细节。
homepage: https://usedada.dev
metadata: { "openclaw": { "emoji": "🗄️" } }
---
# dada

`dada` 是一个用于持久化结构化数据存储、Webhook 配置和文件托管的工具。每个项目都会拥有自己独立的数据库，并且数据库中的表结构都是类型化的（即字段类型是预先定义好的）。所有的操作都通过命令行界面（CLI）来完成。

## 安装

使用 `npx`（需要 Node.js）进行安装：
```
npx @usedada/cli
```

或者从 GitHub 的 Releases 下载预编译的二进制文件：https://github.com/honeybadge-labs/dada/releases

如果你直接下载了二进制文件，那么下面的所有命令都可以直接使用 `dada` 而不需要加上 `npx @usedada/cli`。

## 首次设置

首次登录时，系统会为你生成一个身份标识（Ed25519 密钥对，并将其保存在本地）：
```
dada login --nickname myagent --email me@example.com
```

之后的登录只需重新连接即可（密钥对会保留在磁盘上）：
```
dada login
```

验证连接是否成功：
```
dada login  # prints identity info on success
```

## 常用命令

### 项目管理
- `dada project create <name>`：创建一个新的项目
- `dada project list`：列出所有项目
- `dada project use <name>`：设置当前项目为活动项目

### 表管理
- `dada table create <name> <field:type ...>`：创建一个包含类型化字段的表
- `dada table list`：列出当前项目中的所有表
- `dada table describe <name>`：显示表的详细结构（即字段和类型）

### 记录管理
- `dada insert <table> '<json>'`：插入一条记录
- `dada bulk-insert <table> '[<json>, ...]'`：一次性插入多条记录（适用于批量操作）
- `dada query <table> [-w filter]`：查询记录（可选过滤条件）
- `dada update <table> '<json>' -w filter`：更新符合条件的记录
- `dada delete <table> -w filter`：删除符合条件的记录

### Webhook 管理
- `dada webhook create <name>`：创建一个入站 Webhook（返回 Webhook 的 URL）
- `dada webhook list`：列出当前项目中的所有 Webhook
- `dada webhook delete <name>`：删除一个 Webhook
- `dada webhook watch <name>`：通过 SSE 协议实时接收 Webhook 事件（按 Ctrl+C 可停止接收）
- `dada webhook dequeue <name> [--limit N]`：从队列中取出指定数量的事件（默认限制为 100 条）

### 协作管理
- `dada invite <email> [project] [-r ROLE]`：邀请协作者（角色包括 OWNER、ADMIN、USER）

### 数据发现
- `dada schema`：以 JSON 格式输出命令行接口的完整结构（供代理工具使用）

## 字段类型
- `string`：文本字符串
- `int`：整数
- `float`：浮点数
- `bool`：布尔值（0/1）
- `datetime`：ISO 8601 格式的日期时间戳

每个表都会自动包含一个名为 `id` 的主键字段。

## 过滤条件

使用 `-w` 标志进行过滤：
- `field>value`：字段值大于指定值
- `field>=value`：字段值大于或等于指定值
- `field=value`：字段值等于指定值
- `field<value`：字段值小于指定值

示例：`score>50`、`done=1`、`name=Alice`

## 代理工具使用指南
- 对于批量操作，建议使用 `bulk-insert` 而不是多次 `insert` 命令。
- 在检查记录是否存在时，使用 `--fail-empty` 选项；如果结果为空，则程序会退出（退出代码为 3）。
- 使用 `-j` 选项生成 JSON 格式的输出，以便机器能够正确解析数据。
- 使用 `--select field1,field2` 仅输出所需的字段。
- 创建 Webhook 时，请保存返回的 URL，因为后续可能需要用它来配置外部服务。
- `webhook watch` 会持续接收 Webhook 事件（通过 SSE 协议），可以使用 `webhook dequeue` 来获取指定的事件数量。
- 在向用户报告结果时，尽量使用自然语言进行总结；如果需要的话，可以包含记录 ID 和命令详情以帮助调试或提高透明度。

## 输出格式选项
- `-j`：输出 JSON 格式的数据
- `-p`：以制表符分隔的纯文本格式输出
- `--select FIELDS`：指定需要输出的字段（用逗号分隔）
- `--fail-empty`：如果结果集为空，则程序退出（退出代码为 3）
- `--non-interactive`：禁用交互式提示（适用于 `webhook watch` 模式）