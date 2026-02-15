---
name: track17
description: 通过 17TRACK API 追踪包裹（使用本地的 SQLite 数据库，采用轮询方式；支持可选的 Webhook 数据同步功能）
user-invocable: true
metadata: {"clawdbot":{"emoji":"📦","requires":{"anyBins":["python3","python"],"env":["TRACK17_TOKEN"]},"primaryEnv":"TRACK17_TOKEN"}}
---

# track17（17TRACK包裹追踪功能）

该功能允许Clawdbot在本地维护您的包裹列表，通过**17TRACK追踪API v2.2**来追踪包裹的状态，并汇总相关变化信息。

所有数据都会存储在一个小型**SQLite数据库**中，该数据库位于您的**工作区**下（默认路径为：`<workspace>/packages/track17/track17.sqlite3`）。

`<workspace>`会自动检测为包含该功能的`skills/`目录的父目录。例如，如果您将其安装在`/clawd/skills/track17/`路径下，数据将存储在`/clawd/packages/track17/`目录中。

## 必需条件

- 必须设置`TRACK17_TOKEN`（17TRACK API令牌，用作`17token`请求头）。
- 推荐使用Python（优先版本为`python3`）。

可选配置：
- `TRACK17_WEBHOOK_SECRET`：用于验证Webhook签名。
- `TRACK17_DATA_DIR`：用于指定数据库或收件箱数据的存储路径。
- `TRACK17_WORKSPACE_DIR`：用于指定该工具识别的工作区目录。

## 快速入门

1) 初始化数据存储（可以多次运行该命令，不会造成问题）：

```bash
python3 {baseDir}/scripts/track17.py init
```

2) 添加包裹（将其注册到17TRACK系统并保存到本地）：

```bash
python3 {baseDir}/scripts/track17.py add "RR123456789CN" --label "AliExpress headphones"
```

如果自动识别运输公司失败，可以手动指定运输公司代码：

```bash
python3 {baseDir}/scripts/track17.py add "RR123456789CN" --carrier 3011 --label "..."
```

3) 查看已追踪的包裹列表：

```bash
python3 {baseDir}/scripts/track17.py list
```

4) 定期获取更新信息（如果您不使用Webhook功能，建议执行此操作）：

```bash
python3 {baseDir}/scripts/track17.py sync
```

5) 查看单个包裹的详细信息：

```bash
python3 {baseDir}/scripts/track17.py status 1
# or
python3 {baseDir}/scripts/track17.py status "RR123456789CN"
```

## Webhook功能（可选）

17TRACK支持将更新信息推送至Webhook地址。该功能支持两种Webhook接收方式：

### A) 运行内置的Webhook服务器

```bash
python3 {baseDir}/scripts/track17.py webhook-server --bind 127.0.0.1 --port 8789
```

然后将17TRACK的Webhook地址指向该服务器（建议通过反向代理或Tailscale Funnel进行转发）。

### B) 从标准输入/文件读取Webhook数据

```bash
cat payload.json | python3 {baseDir}/scripts/track17.py ingest-webhook
# or
python3 {baseDir}/scripts/track17.py ingest-webhook --file payload.json
```

如果您将Webhook响应数据保存到了收件箱目录中，可以执行以下操作来处理这些数据：

```bash
python3 {baseDir}/scripts/track17.py process-inbox
```

## 常用操作

- 停止包裹追踪：

```bash
python3 {baseDir}/scripts/track17.py stop 1
```

- 重新追踪已停止的包裹：

```bash
python3 {baseDir}/scripts/track17.py retrack 1
```

- 从本地数据库中删除包裹（除非同时调用`delete-remote`命令，否则不会从17TRACK系统中删除该包裹）：

```bash
python3 {baseDir}/scripts/track17.py remove 1
```

- 查看API使用量：

```bash
python3 {baseDir}/scripts/track17.py quota
```

## 对代理程序的操作指南

- 为简化操作，建议优先使用**同步方式（定期请求更新信息）**，除非用户明确要求使用Webhook功能。
- 添加包裹后，运行`status`命令一次以确认系统返回了正确的运输公司和包裹状态。
- 在汇总数据时，优先显示以下状态：
  - 已送达/正在运输中
  - 交付失败
  - 被海关扣留
  - 由其他运输公司接手处理
- 严禁泄露`TRACK17_TOKEN`或`TRACK17_WEBHOOK_SECRET`。